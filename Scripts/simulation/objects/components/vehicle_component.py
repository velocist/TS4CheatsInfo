# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\components\vehicle_component.py
# Compiled at: 2020-08-13 21:06:46
# Size of source mod 2**32: 21239 bytes
from _math import Vector3
import weakref
from animation.posture_manifest import PostureManifest, AnimationParticipant, SlotManifest, MATCH_ANY, PostureManifestEntry, MATCH_NONE
from event_testing.results import ExecuteResult
from interactions.aop import AffordanceObjectPair
from interactions.constraints import Circle, Constraint
from interactions.context import InteractionContext, QueueInsertStrategy
from interactions.priority import Priority
from objects.components import Component, types
from objects.components.utils.footprint_toggle_mixin import FootprintToggleMixin
from postures.posture_specs import PostureSpecVariable
from postures.posture_state_spec import PostureStateSpec
from routing import SurfaceType
from sims4.tuning.tunable import AutoFactoryInit, HasTunableFactory, Tunable, TunableEnumSet, TunableReference, TunableTuple, OptionalTunable, TunableRange, TunedInterval
from singletons import DEFAULT
from terrain import is_terrain_tag_at_position
from world.ocean_tuning import OceanTuning
from world.terrain_enums import TerrainTag
import interactions.utils, services, sims4.log
logger = sims4.log.Logger('Vehicles', default_owner='rmccord')

class VehicleComponent(FootprintToggleMixin, Component, HasTunableFactory, AutoFactoryInit, component_name=types.VEHICLE_COMPONENT):
    FACTORY_TUNABLES = {'minimum_route_distance':Tunable(description="\n            The minimum distance we require for this vehicle to route. This is\n            also the distance threshold for when the vehicle delays it's\n            dismount. If the Sim attempts to get off of the vehicle to go\n            somewhere, they will defer that dismount and get closer to their\n            destination first.\n            ",
       tunable_type=float,
       default=3.0), 
     'object_radius_dismount_multiplier':TunableRange(description="\n            The multiplier of the object's agent radius when used to defer\n            dismount near a destination. We use the agent radius because we\n            want to fit the vehicle near the destination. But we don't want to\n            make it so large that it trumps the minimum route distance.\n            ",
       tunable_type=float,
       default=1.25,
       minimum=1.0), 
     'ideal_route_radius':Tunable(description='\n            This is the tuning for the ideal radius used when trying to get\n            close to the destination if the destination is farther away than\n            the minimum_route_distance.\n            ',
       tunable_type=float,
       default=3.0), 
     'allowed_surfaces':TunableEnumSet(description='\n            The allowed surfaces for this vehicle. This is how we determine we\n            should use a vehicle in our inventory to get somewhere faster and\n            when we can do it.\n            \n            Also helps us dismount vehicles before we transition through\n            portals.\n            ',
       enum_type=SurfaceType,
       enum_default=SurfaceType.SURFACETYPE_WORLD,
       invalid_enums=(
      SurfaceType.SURFACETYPE_UNKNOWN,)), 
     'deploy_tuning':OptionalTunable(description=',\n            If enabled, a Sim may deploy this vehicle from their inventory.\n            ',
       tunable=TunableTuple(description='\n                Tuning for deploying this vehicle.\n                ',
       deploy_affordance=OptionalTunable(description='\n                    If enabled, we will override the deployment affordance to\n                    use something specific when deploying vehicles for speed.\n                    Otherwise we simply refer to the inventory item component\n                    affordances.\n                    ',
       tunable=TunableReference(description='\n                        The affordance a Sim will use to deploy the vehicle from\n                        inventory and drive it.\n                        ',
       manager=(services.affordance_manager())),
       disabled_name='use_inventory_item_component_affordance',
       enabled_name='override'),
       auto_deploy_here_affordance=OptionalTunable(description="\n                    If enabled, this affordance will be used to deploy the\n                    vehicle further in a route, such as on the other side of\n                    some nearby stairs or portals that the vehicle can't\n                    traverse.\n                    ",
       tunable=TunableReference(description='\n                        The affordance a Sim will use to deploy the vehicle at\n                        a specific location. Likely needs a vehicle liability.\n                        ',
       manager=(services.affordance_manager()))))), 
     'drive_affordance':TunableReference(description='\n            The affordance a Sim will use to drive this vehicle.\n            ',
       manager=services.affordance_manager()), 
     'retrieve_tuning':OptionalTunable(description='\n            If enabled, the Sim may attempt to retrieve this vehicle for their\n            inventory.\n            ',
       tunable=TunableTuple(description='\n                Tuning for retrieving this vehicle.\n                ',
       retrieve_affordance=OptionalTunable(description='\n                    If enabled, we will override the retrieval affordance to\n                    use something specific when retrieving vehicles after\n                    dismount. Otherwise, we simply refer to the inventory item\n                    component affordances.\n                    ',
       tunable=TunableReference(description='\n                        The affordance a Sim will use to deploy the vehicle from\n                        inventory and drive it.\n                        ',
       manager=(services.affordance_manager())),
       disabled_name='use_inventory_item_component_affordance',
       enabled_name='override'))), 
     'prohibited_terrain_transitions':TunableEnumSet(description='\n            Terrain tags that this vehicle cannot transition across.\n            ',
       enum_type=TerrainTag,
       enum_default=TerrainTag.DEEPSNOW,
       invalid_enums=(
      TerrainTag.INVALID,))}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            return
        return self._driver()

    def on_add(self):
        self.register_routing_event_callbacks()
        self.owner.routing_component.pathplan_context.disable_fake_portals = True

    def on_remove(self):
        self.unregister_routing_event_callbacks()

    def _check_update_driver(self, child):
        self._driver = weakref.ref(child)

    def on_child_added(self, child, _):
        return self.driver is not None or child.is_sim or None
        self._check_update_driver(child)

    def on_child_removed(self, child, new_parent=None):
        if child is self.driver:
            self._driver = None
        if new_parent is not None:
            self._check_update_driver(child)

    def on_added_to_inventory(self):
        owner_inventory = self.owner.get_inventory()
        if owner_inventory.owner.is_sim:
            owner_inventory.add_vehicle_object(self.owner)

    def on_removed_from_inventory(self):
        owner = self.owner.inventoryitem_component.last_inventory_owner
        if owner.is_sim:
            owner.inventory_component.remove_vehicle_object(self.owner)

    def push_drive_affordance(self, sim, depend_on_si=None, priority=Priority.High):
        return self._push_affordance(sim, (self.drive_affordance), (self.owner), depend_on_si=depend_on_si,
          priority=priority)

    def _create_drive_posture_constraint(self, posture_type):
        posture_manifest = PostureManifest()
        entry = PostureManifestEntry(AnimationParticipant.ACTOR, posture_type.name, posture_type.family_name, MATCH_ANY, MATCH_NONE, MATCH_NONE, MATCH_ANY, None)
        posture_manifest.add(entry)
        posture_manifest = posture_manifest.intern()
        posture_state_spec = PostureStateSpec(posture_manifest, SlotManifest(), PostureSpecVariable.ANYTHING)
        return Constraint(posture_state_spec=posture_state_spec, debug_name='VehiclePostureConstraint')

    def push_dismount_affordance(self, sim, final_location, depend_on_si=None):
        if sim.posture.is_vehicle:
            constraint = sim.posture_state.posture_constraint
        else:
            constraint = self._create_drive_posture_constraint(self.drive_affordance.provided_posture_type)
        radius = max(self.owner.routing_component.object_radius * self.object_radius_dismount_multiplier, self.ideal_route_radius)
        circle_constraint = None
        wading_interval = TunedInterval(0.1, 0.1)
        min_water_depth, max_water_depth = OceanTuning.make_depth_bounds_safe_for_surface(sim.routing_surface, wading_interval)
        if min_water_depth is None:
            water_constraint = max_water_depth is None or Constraint(min_water_depth=min_water_depth, max_water_depth=max_water_depth)
            if water_constraint.is_location_water_depth_valid(final_location):
                constraint = constraint.intersect(water_constraint)
        else:
            large_radius = max(self.minimum_route_distance, radius)
            circle_constraint = Circle((final_location.transform.translation), large_radius, (sim.routing_surface), ideal_radius=(self.ideal_route_radius), los_reference_point=DEFAULT)
            water_constraint = water_constraint.intersect(circle_constraint)
            if water_constraint.is_any_geometry_water_depth_valid():
                constraint = constraint.intersect(water_constraint)
            else:
                constraint = constraint.intersect(circle_constraint)
                circle_constraint = None
        if circle_constraint is None:
            circle_constraint = Circle((final_location.transform.translation), radius, (sim.routing_surface), ideal_radius=(self.ideal_route_radius), los_reference_point=DEFAULT)
            constraint = constraint.intersect(circle_constraint)
        proxy_obj = services.terrain_service.TerrainService.create_surface_proxy_from_location(final_location)
        constraint = constraint.intersect(circle_constraint)
        return self._push_affordance(sim, (interactions.utils.satisfy_constraint_interaction.SatisfyConstraintSuperInteraction), proxy_obj,
          depend_on_si=depend_on_si, constraint_to_satisfy=constraint,
          name_override='DismountVehicle')

    def push_retrieve_vehicle_affordance(self, sim, depend_on_si=None):
        affordance = self.retrieve_tuning.retrieve_affordance or next(self.owner.inventoryitem_component.place_in_inventory_affordances_gen(), None)
        if affordance is None:
            return affordance
        return self._push_affordance(sim, affordance, (self.owner), depend_on_si=depend_on_si, must_run_next=False)

    def push_deploy_vehicle_affordance(self, sim, depend_on_si=None):
        affordance = self.deploy_tuning is not None and self.deploy_tuning.deploy_affordance or next(self.owner.inventoryitem_component.place_in_world_affordances_gen(), None)
        if affordance is None:
            return
        return self._push_affordance(sim, affordance, (self.owner), depend_on_si=depend_on_si, must_run_next=False)

    def push_auto_deploy_affordance(self, sim, deploy_location, depend_on_si=None):
        affordance = self.deploy_tuning.auto_deploy_here_affordance if self.deploy_tuning is not None else None
        if affordance is None:
            return
        picked_item_ids = frozenset((self.owner.id,))
        target = services.get_terrain_service().create_surface_proxy_from_location(deploy_location)
        if target is None:
            return ExecuteResult(False, None, 'Failed to get surface proxy object')
        return self._push_affordance(sim, affordance, target, depend_on_si=depend_on_si, must_run_next=False, picked_item_ids=picked_item_ids)

    def _push_affordance(self, sim, affordance, target, depend_on_si, priority=Priority.High, must_run_next=True, **kwargs):
        aop = AffordanceObjectPair(affordance, target, affordance, None, route_fail_on_transition_fail=False, 
         allow_posture_changes=True, 
         depend_on_si=depend_on_si, **kwargs)
        context = InteractionContext(sim, (InteractionContext.SOURCE_SCRIPT), priority,
          insert_strategy=(QueueInsertStrategy.FIRST),
          must_run_next=must_run_next,
          group_id=(depend_on_si.group_id if depend_on_si is not None else None))
        return aop.test_and_execute(context)

    def can_transition_through_portal(self, portal_obj, portal_id):
        if portal_id:
            if portal_obj:
                portal = portal_obj.get_portal_by_id(portal_id)
                entry_loc, exit_loc = portal.get_portal_locations(portal_id)
                flags = portal.portal_template.required_flags or 0
                flags |= portal.traversal_type.get_additional_required_portal_flags(entry_loc, exit_loc)
                if ~self.owner.routing_component.pathplan_context.get_portal_key_mask() & flags:
                    return False
        return True

    def can_transition_over_node(self, curr_node, prev_node):
        if curr_node is None or prev_node is None:
            return True
        current_node_terrain_tags = curr_node.tracked_terrain_tags
        if current_node_terrain_tags is None:
            return True
        for tag in self.prohibited_terrain_transitions:
            if any((int(tag) in x for x in current_node_terrain_tags)):
                return is_terrain_tag_at_position(prev_node.position[0], prev_node.position[2], (tag,)) or False

        return True

    def should_deploy_for_path--- This code section failed: ---

 L. 395         0  LOAD_FAST                'self'
                2  LOAD_ATTR                deploy_tuning
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_TRUE     36  'to 36'

 L. 396        10  LOAD_FAST                'routing_surface'
               12  LOAD_ATTR                type
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                allowed_surfaces
               18  COMPARE_OP               not-in
               20  POP_JUMP_IF_TRUE     36  'to 36'

 L. 397        22  LOAD_FAST                'path'
               24  LOAD_METHOD              length
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                minimum_route_distance
               32  COMPARE_OP               <=
               34  POP_JUMP_IF_FALSE    40  'to 40'
             36_0  COME_FROM            20  '20'
             36_1  COME_FROM             8  '8'

 L. 398        36  LOAD_CONST               False
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 400        40  LOAD_CONST               0.0
               42  STORE_FAST               'total_dist'

 L. 401        44  LOAD_GLOBAL              any
               46  LOAD_GENEXPR             '<code_object <genexpr>>'
               48  LOAD_STR                 'VehicleComponent.should_deploy_for_path.<locals>.<genexpr>'
               50  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               52  LOAD_FAST                'path'
               54  LOAD_ATTR                nodes
               56  GET_ITER         
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  POP_JUMP_IF_TRUE     84  'to 84'
               64  LOAD_GLOBAL              any
               66  LOAD_GENEXPR             '<code_object <genexpr>>'
               68  LOAD_STR                 'VehicleComponent.should_deploy_for_path.<locals>.<genexpr>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               72  LOAD_FAST                'path'
               74  LOAD_ATTR                nodes
               76  GET_ITER         
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  POP_JUMP_IF_FALSE   254  'to 254'
             84_0  COME_FROM            62  '62'

 L. 405        84  LOAD_GLOBAL              len
               86  LOAD_FAST                'path'
               88  LOAD_ATTR                nodes
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  LOAD_CONST               1
               94  COMPARE_OP               >
               96  POP_JUMP_IF_FALSE   252  'to 252'

 L. 406        98  LOAD_FAST                'path'
              100  LOAD_ATTR                nodes
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  STORE_FAST               'prev_node'

 L. 407       108  LOAD_GLOBAL              services
              110  LOAD_METHOD              object_manager
              112  CALL_METHOD_0         0  '0 positional arguments'
              114  STORE_FAST               'object_manager'

 L. 408       116  LOAD_GLOBAL              list
              118  LOAD_FAST                'path'
              120  LOAD_ATTR                nodes
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  STORE_FAST               'nodes'

 L. 409       126  SETUP_LOOP          262  'to 262'
              128  LOAD_FAST                'nodes'
              130  LOAD_CONST               1
              132  LOAD_CONST               None
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  GET_ITER         
            140_0  COME_FROM           244  '244'
              140  FOR_ITER            250  'to 250'
              142  STORE_FAST               'next_node'

 L. 410       144  LOAD_GLOBAL              Vector3
              146  LOAD_FAST                'next_node'
              148  LOAD_ATTR                position
              150  CALL_FUNCTION_EX      0  'positional arguments only'
              152  LOAD_GLOBAL              Vector3
              154  LOAD_FAST                'prev_node'
              156  LOAD_ATTR                position
              158  CALL_FUNCTION_EX      0  'positional arguments only'
              160  BINARY_SUBTRACT  
              162  LOAD_METHOD              magnitude
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  STORE_FAST               'node_dist'

 L. 411       168  LOAD_FAST                'total_dist'
              170  LOAD_FAST                'node_dist'
              172  INPLACE_ADD      
              174  STORE_FAST               'total_dist'

 L. 412       176  LOAD_FAST                'next_node'
              178  STORE_FAST               'prev_node'

 L. 414       180  LOAD_FAST                'next_node'
              182  LOAD_ATTR                portal_object_id
              184  STORE_FAST               'portal_obj_id'

 L. 415       186  LOAD_FAST                'portal_obj_id'
              188  POP_JUMP_IF_FALSE   200  'to 200'
              190  LOAD_FAST                'object_manager'
              192  LOAD_METHOD              get
              194  LOAD_FAST                'portal_obj_id'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  JUMP_FORWARD        202  'to 202'
            200_0  COME_FROM           188  '188'
              200  LOAD_CONST               None
            202_0  COME_FROM           198  '198'
              202  STORE_FAST               'portal_obj'

 L. 416       204  LOAD_FAST                'portal_obj'
              206  POP_JUMP_IF_FALSE   226  'to 226'

 L. 417       208  LOAD_FAST                'self'
              210  LOAD_METHOD              can_transition_through_portal
              212  LOAD_FAST                'portal_obj'
              214  LOAD_FAST                'next_node'
              216  LOAD_ATTR                portal_id
              218  CALL_METHOD_2         2  '2 positional arguments'
              220  POP_JUMP_IF_TRUE    248  'to 248'

 L. 419       222  BREAK_LOOP       
              224  JUMP_BACK           140  'to 140'
            226_0  COME_FROM           206  '206'

 L. 420       226  LOAD_FAST                'portal_obj_id'
              228  POP_JUMP_IF_FALSE   234  'to 234'

 L. 423       230  BREAK_LOOP       
              232  JUMP_BACK           140  'to 140'
            234_0  COME_FROM           228  '228'

 L. 424       234  LOAD_FAST                'self'
              236  LOAD_METHOD              can_transition_over_node
              238  LOAD_FAST                'next_node'
              240  LOAD_FAST                'prev_node'
              242  CALL_METHOD_2         2  '2 positional arguments'
              244  POP_JUMP_IF_TRUE    140  'to 140'

 L. 426       246  BREAK_LOOP       
            248_0  COME_FROM           220  '220'
              248  JUMP_BACK           140  'to 140'
              250  POP_BLOCK        
            252_0  COME_FROM            96  '96'
              252  JUMP_FORWARD        262  'to 262'
            254_0  COME_FROM            82  '82'

 L. 428       254  LOAD_FAST                'path'
              256  LOAD_METHOD              length
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  STORE_FAST               'total_dist'
            262_0  COME_FROM           252  '252'
            262_1  COME_FROM_LOOP      126  '126'

 L. 430       262  LOAD_FAST                'total_dist'
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                minimum_route_distance
              268  COMPARE_OP               >
              270  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 248_0