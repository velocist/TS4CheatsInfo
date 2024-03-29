# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\components\proximity_component.py
# Compiled at: 2020-07-23 22:49:23
# Size of source mod 2**32: 14091 bytes
import random, alarms, clock, event_testing, interactions.constraints, objects.components, placement, services, sims4.tuning.tunable
from collections import defaultdict
from sims4.callback_utils import CallableList
from sims4.tuning.tunable import TunableList, TunableReference
logger = sims4.log.Logger('ProximityComponent')

class ProximityComponent(objects.components.Component, sims4.tuning.tunable.HasTunableFactory, component_name=objects.components.types.PROXIMITY_COMPONENT, allow_dynamic=True):
    FACTORY_TUNABLES = {'buffs':sims4.tuning.tunable.TunableList(sims4.tuning.tunable.TunableReference(description='\n                    A list of buffs to apply to Sims that are near the\n                    component owner.\n                    ',
       manager=(services.get_instance_manager(sims4.resources.Types.BUFF)),
       pack_safe=True)), 
     'update_frequency':sims4.tuning.tunable.TunableRealSecond(description='\n                Number of seconds between proximity updates.\n                ',
       default=18.0,
       tuning_filter=sims4.tuning.tunable_base.FilterTag.EXPERT_MODE), 
     'update_distance':sims4.tuning.tunable.Tunable(int, 10, description='\n                Max distance Sims away from component owner and still be\n                considered in proximity.\n                ',
       tuning_filter=sims4.tuning.tunable_base.FilterTag.EXPERT_MODE), 
     'disabling_state_values':TunableList(description='\n            If tuned, states which will, if active, cause this component to \n            disable.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.OBJECT_STATE)),
       class_restrictions=('ObjectStateValue', )))}

    def __init__(self, owner, buffs=(), update_frequency=6, update_distance=10, disabling_state_values=None, **kwargs):
        (super().__init__)(owner, **kwargs)
        self.buff_types = buffs
        self.update_frequency = update_frequency
        self.update_distance = update_distance
        self.active_buff_handles = {}
        self._alarm = None
        self._disabling_state_values = disabling_state_values
        self._proximity_callbacks = defaultdict(CallableList)

    def has_proximity_callback(self, sim_id, callback):
        if sim_id not in self._proximity_callbacks:
            return False
        return callback in self._proximity_callbacks[sim_id]

    def register_proximity_callback(self, sim_id, callback):
        self._proximity_callbacks[sim_id].register(callback)

    def unregister_proximity_callback(self, sim_id, callback):
        self._proximity_callbacks[sim_id].unregister(callback)

    def on_state_changed(self, state, old_value, new_value, from_init):
        if new_value in self._disabling_state_values:
            self._stop()
        else:
            if old_value in self._disabling_state_values:
                if not any((self.owner.state_value_active(state_value) for state_value in self._disabling_state_values)):
                    self._start()

    def on_add(self):
        self._start()

    def on_remove(self):
        self._stop()

    def on_added_to_inventory(self):
        self._stop()

    def on_removed_from_inventory(self):
        self._start()

    def component_reset(self, reset_reason):
        self._stop()
        self._start()

    def _start(self):
        if self._alarm is None:
            time_span = clock.interval_in_real_seconds(self.update_frequency)
            time_span *= random.random()
            self._alarm = alarms.add_alarm_real_time((self.owner),
              time_span,
              (self._initial_update_callback),
              repeating=False,
              use_sleep_time=False)

    def _stop(self):
        self._remove_buffs_from_sims()
        if self._alarm is not None:
            alarms.cancel_alarm(self._alarm)
            self._alarm = None

    def _initial_update_callback(self, alarm_handle):
        self._pulse()
        time_span = clock.interval_in_real_seconds(self.update_frequency)
        self._alarm = alarms.add_alarm_real_time((self.owner),
          time_span,
          (self._update_callback),
          repeating=True,
          use_sleep_time=False)

    def _update_callback(self, alarm_handle):
        self._pulse()

    def _pulse(self):
        nearby_sims = self._get_nearby_sims()
        if self._proximity_callbacks:
            for sim in nearby_sims:
                sim_id = sim.id
                callback_list = self._proximity_callbacks.get(sim_id, None)
                if callback_list is not None:
                    callback_list(sim_id)

        self._remove_buffs_from_sims(sim_exceptions=nearby_sims)
        for sim in nearby_sims:
            self._add_and_remove_buffs_for_sim(sim)

    def _get_nearby_sims(self):
        sims = set()
        if self.owner.is_hidden():
            return sims
        exclude = (self.owner,) if self.owner.is_sim else None
        nearby_sims = placement.get_nearby_sims_gen(position=(self.owner.position),
          surface_id=(self.owner.routing_surface),
          radius=(self.update_distance),
          exclude=exclude,
          stop_at_first_result=False,
          only_sim_position=True,
          check_all_surfaces_on_level=True)
        object_constraint = interactions.constraints.Transform((self.owner.transform),
          routing_surface=(self.owner.routing_surface))
        for sim in nearby_sims:
            if sim.is_hidden():
                continue
            los_constraint = sim.lineofsight_component.constraint
            test_constraint = los_constraint.intersect(object_constraint)
            if test_constraint.valid:
                sims.add(sim)

        return sims

    def _remove_buffs_from_sims(self, sim_exceptions=None, **kwargs):
        sim_info_manager = services.sim_info_manager()
        if sim_info_manager is None:
            return
        sim_ids = set(iter(self.active_buff_handles))
        if sim_exceptions:
            nearby_sim_ids = {sim.id for sim in sim_exceptions}
            sim_ids -= nearby_sim_ids
        for sim_id in sim_ids:
            active_buff_handles = self.active_buff_handles.pop(sim_id)
            sim_info = sim_info_manager.get(sim_id)
            if sim_info:
                buff_component = sim_info.Buffs
                if buff_component is not None:
                    (self._remove_buffs_from_sim)(buff_component, active_buff_handles, **kwargs)

    def _add_and_remove_buffs_for_sim(self, sim):
        buffs_to_add = set()
        if self.owner.is_sim or hasattr(self.owner, 'sim_info'):
            resolver = event_testing.resolver.DoubleSimResolver(sim.sim_info, self.owner.sim_info)
        else:
            resolver = event_testing.resolver.SingleActorAndObjectResolver(sim.sim_info, self.owner, self)
        for buff in self._proximity_buffs_gen(sim.sim_info):
            if buff.proximity_detection_tests:
                if not buff.proximity_detection_tests.run_tests(resolver):
                    continue
            buffs_to_add.add(buff)

        buffs_component = sim.Buffs
        active_buff_handles = self.active_buff_handles.get(sim.id)
        if active_buff_handles:
            stale_buff_handles = set()
            for handle in active_buff_handles:
                buff_type = buffs_component.get_buff_type(handle)
                if buff_type is None or buff_type not in buffs_to_add:
                    stale_buff_handles.add(handle)
                else:
                    buffs_to_add.remove(buff_type)

            if stale_buff_handles:
                self._remove_buffs_from_sim(buffs_component, stale_buff_handles)
                active_buff_handles -= stale_buff_handles
        elif buffs_to_add:
            new_handles = self._add_buffs_to_sim(buffs_component, buffs_to_add)
            if active_buff_handles is None:
                active_buff_handles = new_handles
                self.active_buff_handles[sim.id] = new_handles
            else:
                active_buff_handles |= new_handles
        if not active_buff_handles:
            self.active_buff_handles.pop(sim.id, None)

    def _add_buffs_to_sim(self, buffs_component, buffs):
        handles = set()
        for buff in buffs:
            handle = buffs_component.add_buff(buff, buff_reason=(buff.proximity_buff_added_reason))
            if handle:
                handles.add(handle)

        return handles

    def _remove_buffs_from_sim(self, buffs_component, handles, on_destroy=False):
        for handle in handles:
            buffs_component.remove_buff(handle, on_destroy=on_destroy)

    def _proximity_buffs_gen(self, buff_recipient):
        for buff_type in self.buff_types:
            yield buff_type

        if self.owner.is_sim:
            for trait in buff_recipient.trait_tracker:
                for buff_type in trait.buffs_proximity:
                    yield buff_type