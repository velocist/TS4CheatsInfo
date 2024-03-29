# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\components\line_of_sight_component.py
# Compiled at: 2017-02-17 00:31:14
# Size of source mod 2**32: 19195 bytes
from math import cos, sin
import _line_of_sight
from debugvis import Context
from interactions.constraints import Constraint, Nowhere
from interactions.interaction_finisher import FinishingType
from objects.components import Component, types
from sims4.tuning.tunable import TunableFactory, Tunable
from sims4.tuning.tunable_base import FilterTag
from singletons import DEFAULT
import build_buy, routing, services, sims4.color, sims4.log, sims4.math, sims4.reload, zone_types
with sims4.reload.protected(globals()):
    enable_visualization = False
logger = sims4.log.Logger('LineOfSightComponent')

class LineOfSight(_line_of_sight._LineOfSight):
    FACTORY_TUNABLES = {'max_line_of_sight_radius':Tunable(description='\n                The maximum possible distance from this object than an\n                interaction can reach.\n                ',
       tunable_type=float,
       default=10), 
     'map_divisions':Tunable(description='"\n                The number of points around the object to check collision from.\n                More points means higher accuracy.\n                ',
       tunable_type=int,
       default=30), 
     'simplification_ratio':Tunable(description='\n                A factor determining how much to combine edges in the line of\n                sight polygon.\n                ',
       tunable_type=float,
       default=0.35,
       tuning_filter=FilterTag.EXPERT_MODE), 
     'boundary_epsilon':Tunable(description='\n                The LOS origin is allowed to be outside of the boundary by this\n                amount.\n                ',
       tunable_type=float,
       default=0.01,
       tuning_filter=FilterTag.EXPERT_MODE)}

    def __init__(self, max_line_of_sight_radius, map_divisions, simplification_ratio, boundary_epsilon, build_convex=False, multi_surface=False, debug_str_data=None):
        super().__init__(max_line_of_sight_radius, map_divisions, simplification_ratio, boundary_epsilon, build_convex)
        self._constraint = None
        self._constraint_multi_surface = None
        self._constraint_convex = None
        self._constraint_convex_multi_surface = None
        self._routing_surface = None
        self._multi_surface = multi_surface
        self._enables_height_scoring = False
        self._los_debug_str = None

    def __repr__(self):
        return 'LineOfSight: {}'.format(id(self))

    @property
    def max_line_of_sight_radius(self):
        return self._max_line_of_sight_radius

    @property
    def constraint(self):
        return self._constraint

    @property
    def constraint_multi_surface(self):
        if self._constraint_multi_surface is None:
            if self._constraint is not None:
                self._constraint_multi_surface = self._constraint.get_multi_surface_version()
        return self._constraint_multi_surface

    @property
    def constraint_convex(self):
        return self._constraint_convex

    @property
    def constraint_convex_multi_surface(self):
        if self._constraint_convex_multi_surface is None:
            if self._constraint_convex is not None:
                self._constraint_convex_multi_surface = self._constraint_convex.get_multi_surface_version()
        return self._constraint_convex_multi_surface

    @property
    def multi_surface(self):
        return self._multi_surface

    @property
    def enables_height_scoring(self):
        return self._enables_height_scoring

    def generate(self, position, routing_surface, build_convex=DEFAULT, allow_object_routing_surface=False):
        self._position = position
        self._routing_surface = routing_surface
        self._constraint_multi_surface = None
        self._constraint_convex_multi_surface = None
        if not allow_object_routing_surface:
            if routing_surface is not None:
                if routing_surface.type in routing.object_routing_surfaces:
                    zone_id = services.current_zone_id()
                    routing_surface = routing.SurfaceIdentifier(zone_id or 0, routing_surface.secondary_id, routing.SurfaceType.SURFACETYPE_WORLD)
        self._contours = build_buy.get_wall_contours(self._position.x, self._position.z, routing_surface, True)
        self.generate_constraint(build_convex=build_convex)

    def generate_constraint(self, build_convex=DEFAULT):
        self._distance_map = [
         None] * self._map_divisions
        self._connection_map = [None] * self._map_divisions
        self._connection_index = 0
        self._collect_segments()
        vertices = self._render_vertices()
        segments = self._simplify_geometry(vertices)
        if build_convex is DEFAULT:
            build_convex = self.build_convex
        elif build_convex:
            try:
                convex_segments = list(self.maximal_convex(vertices))
            except RuntimeError as ex:
                try:
                    logger.error('LOS Constraint: {}, {}: {}', self, ex, ','.join((str(v) for v in vertices)))
                    self._constraint_convex = Nowhere('Exception while trying to generate convex_segments for line of sight.')
                    return
                finally:
                    ex = None
                    del ex

            simple_convex = self._simplify_geometry(convex_segments)
            maximal_convex_polygon = self._make_compound_polygon([simple_convex])
            self._constraint_convex = Constraint(debug_name='LineOfSightConvex', routing_surface=(self._routing_surface),
              geometry=(sims4.geometry.RestrictedPolygon(maximal_convex_polygon, [])),
              multi_surface=(self._multi_surface))
        else:
            maximal_convex_polygon = None
            self._constraint_convex = Nowhere('LineOfSight.generate_constraint, not build_convex')
        convex_polygons = self._concave_to_convex(segments)
        cp = self._make_compound_polygon(convex_polygons)
        self._constraint = Constraint(debug_name='LineOfSight', routing_surface=(self._routing_surface),
          geometry=(sims4.geometry.RestrictedPolygon(cp, [])),
          multi_surface=(self._multi_surface))
        if self._multi_surface:
            self._constraint_multi_surface = self._constraint
            self._constraint_convex_multi_surface = self._constraint_convex

    def _map_location_to_point(self, pos):
        dist = self._distance_map[pos]
        if dist is None:
            dist = self._max_line_of_sight_radius
        angle = pos / self._interval
        x = dist * cos(angle) + self._position.x
        z = dist * sin(angle) + self._position.z
        return sims4.math.Vector3(x, 0, z)

    def _visualize_constraint(self, segments, convex_polygons, maximal_convex_polygon):
        self._visualize_contours('los_contours', (self._contours), (sims4.color.from_rgba(0.0, 1.0, 1.0)), make_closed=False)
        self._visualize_rays('los_rays', color=(sims4.color.from_rgba(0.0, 0.0, 0.8)))
        self._visualize_contours('los_map', [segments], sims4.color.from_rgba(1.0, 0.5, 0.0))
        self._visualize_contours('los_final', convex_polygons, sims4.color.from_rgba(1.0, 0.5, 0.0))
        if maximal_convex_polygon:
            self._visualize_contours('los_convex', [[point for point in maximal_convex_polygon[0]]], sims4.color.from_rgba(1.0, 1.0, 1.0))
        else:
            if self.build_convex:
                logger.error('Failed to generate maximal convex polygon for object!')

    def _visualize_contours(self, layer, contours, color, make_closed=True):
        with Context(layer, routing_surface=(self._routing_surface)) as (context):
            for contour in contours:
                length = len(contour)
                if length != 0:
                    for i in range(length - 1):
                        context.add_segment((contour[i]), (contour[(i + 1)]), color=color)

                    if make_closed:
                        context.add_segment((contour[(length - 1)]), (contour[0]), color=color)

    def _visualize_rays(self, layer, color):
        with Context(layer, routing_surface=(self._routing_surface)) as (context):
            for i in range(len(self._distance_map)):
                context.add_segment((self._position), (self._map_location_to_point(i)), color=color)


TunableLineOfSightFactory = TunableFactory.create_auto_factory(LineOfSight)

class LineOfSightComponent(Component, component_name=types.LINE_OF_SIGHT_COMPONENT, allow_dynamic=True):
    FACTORY_TUNABLES = {'description':'\n            This component will generate a line_of_sight region around its owner. A\n            line_of_sight region represents an area viewable from a point, so it\n            adapts itself to respect the wall graph.  If an interaction on the\n            owner of this component is tuned to require line_of_sight, Sims will\n            need to be within this region in order to run that interaction.\n            \n            Tunable Dependencies: In order to have an interaction utilize this,\n            you\'ll need to add a "line_of_sight" constraint under that\n            interaction\'s "Constraints" list.\n            \n            Example: The television has a line_of_sight component tuned on it. When\n            Sims try to use the television, they will try to route to within the\n            line_of_sight constraint to watch it.  This ensures that Sims cannot\n            watch the television from too far away or through walls.\n            ', 
     'line_of_sight':TunableLineOfSightFactory(description='\n                The Line of Sight constraint.\n                '), 
     'facing_offset':Tunable(description='\n                The LOS origin is offset from the object origin by this amount\n                (mainly to avoid intersecting walls).\n                ',
       tunable_type=float,
       default=0.1,
       tuning_filter=FilterTag.EXPERT_MODE)}

    def __init__(self, owner, facing_offset, line_of_sight, add_wall_countour_callbacks=True):
        super().__init__(owner)
        self._facing_offset = facing_offset
        self._los = line_of_sight(debug_str_data=('LOS Component: {}', self.owner))
        self._dirty = True
        self._locked = False
        self._build_convex = False
        zone = services.current_zone()
        if add_wall_countour_callbacks:
            self.add_wall_contours_updated_callback()
        if zone.is_zone_loading:
            zone.register_callback(zone_types.ZoneState.OBJECTS_LOADED, self._on_lot_loaded)

    def __repr__(self):
        return 'LOS_Component: {}'.format(self._los)

    @property
    def position(self):
        return self._los._position

    @property
    def routing_surface(self):
        return self._los._routing_surface

    @property
    def constraint(self):
        if self._dirty:
            if not self._locked:
                self._generate_los()
        return self._los.constraint

    @property
    def multi_surface_constraint(self):
        if self._dirty:
            if not self._locked:
                self._generate_los()
        return self._los.constraint_multi_surface

    def _prepare_constraint_convex(self):
        if not self._build_convex:
            self._build_convex = True
            self._los.build_convex = True
            self._dirty = True
        if self._dirty:
            if not self._locked:
                self._generate_los()

    @property
    def constraint_convex(self):
        self._prepare_constraint_convex()
        return self._los.constraint_convex

    @property
    def multi_surface_constraint_convex(self):
        self._prepare_constraint_convex()
        return self._los.constraint_convex_multi_surface

    @property
    def max_line_of_sight_radius(self):
        return self._los.max_line_of_sight_radius

    def _on_lot_loaded(self):
        self._generate_los()

    def add_wall_contours_updated_callback(self):
        zone = services.current_zone()
        if self._on_wall_contours_updated not in zone.wall_contour_update_callbacks:
            zone.wall_contour_update_callbacks.append(self._on_wall_contours_updated)

    def _on_wall_contours_updated(self):
        self._dirty = True
        users = self.owner.get_users(sims_only=True)
        if not users:
            return
        self._generate_los()
        social_groups = set()
        cancel_reason_msg = 'LOS Constraint no longer valid.'
        for user in users:
            user.evaluate_si_state_and_cancel_incompatible(FinishingType.INTERACTION_INCOMPATIBILITY, cancel_reason_msg)
            for social_group in user.get_groups_for_sim_gen():
                if social_group is not None:
                    social_groups.add(social_group)

        if social_groups:
            for social_group in social_groups:
                social_group.regenerate_constraint_and_validate_members()

    def on_remove(self):
        zone = services.current_zone()
        if self._on_wall_contours_updated in zone.wall_contour_update_callbacks:
            zone.wall_contour_update_callbacks.remove(self._on_wall_contours_updated)
        if zone.is_zone_loading:
            zone.unregister_callback(zone_types.ZoneState.OBJECTS_LOADED, self._on_lot_loaded)

    def on_added_to_inventory(self):
        services.current_zone().wall_contour_update_callbacks.remove(self._on_wall_contours_updated)

    def on_removed_from_inventory(self):
        services.current_zone().wall_contour_update_callbacks.append(self._on_wall_contours_updated)

    def on_location_changed(self, old_location):
        self._dirty = True

    @property
    def facing_offset(self):
        return self._facing_offset

    @property
    def default_position(self):
        return self.owner.intended_position + self.owner.intended_forward * self._facing_offset

    def _generate_los(self):
        self._dirty = False
        position = self.default_position
        self._los.generate(position, self.owner.intended_routing_surface)

    def generate(self, position=None, routing_surface=None, lock=False, **kwargs):
        if position is None:
            position = self.default_position
        if routing_surface is None:
            routing_surface = self.owner.intended_routing_surface
        self._locked = lock
        (self._los.generate)(position, routing_surface, **kwargs)


TunableLineOfSightComponent = TunableFactory.create_auto_factory(LineOfSightComponent)