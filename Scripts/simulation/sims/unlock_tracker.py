# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\unlock_tracker.py
# Compiled at: 2020-09-10 00:06:47
# Size of source mod 2**32: 8232 bytes
from event_testing import test_events
from protocolbuffers import SimObjectAttributes_pb2 as protocols
import services, sims4.log, sims4.resources
from collections import namedtuple
from distributor.rollback import ProtocolBufferRollback
from objects.mixins import ProvidedAffordanceData, AffordanceCacheMixin
from sims.sim_info_lod import SimInfoLODLevel
from sims.sim_info_tracker import SimInfoTracker
from sims4.tuning.tunable import TunableVariant, TunablePackSafeReference
from sims4.utils import classproperty
Unlock = namedtuple('Unlock', ('tuning_class', 'name'))
logger = sims4.log.Logger('UnlockTracker')

class TunableUnlockVariant(TunableVariant):

    def __init__(self, **kwargs):
        (super().__init__)(unlock_recipe=TunablePackSafeReference(manager=(services.get_instance_manager(sims4.resources.Types.RECIPE))), 
         unlock_spell=TunablePackSafeReference(manager=(services.get_instance_manager(sims4.resources.Types.SPELL))), 
         default='unlock_recipe', **kwargs)


class UnlockTracker(AffordanceCacheMixin, SimInfoTracker):

    def __init__(self, sim_info):
        super().__init__()
        self._sim_info = sim_info
        self._unlocks = []
        self._marked_new_unlocks = set()

    def add_unlock(self, tuning_class, name, mark_as_new=False):
        if tuning_class is not None:
            self._unlocks.append(Unlock(tuning_class, name))
            if mark_as_new:
                self._marked_new_unlocks.add(tuning_class)
            provided_super_affordances, provided_target_affordances = self._get_provided_super_affordances_from_unlock(tuning_class)
            self.add_to_affordance_caches(provided_super_affordances, provided_target_affordances)
            services.get_event_manager().process_event((test_events.TestEvent.UnlockTrackerItemUnlocked), sim_info=(self._sim_info))

    def is_marked_as_new(self, tuning_class):
        return tuning_class in self._marked_new_unlocks

    def unmark_as_new(self, tuning_class):
        if tuning_class in self._marked_new_unlocks:
            self._marked_new_unlocks.remove(tuning_class)

    def _get_provided_super_affordances_from_unlock(self, tuning_class):
        target_super_affordances = getattr(tuning_class, 'target_super_affordances', ())
        provided_target_affordances = []
        for provided_affordance in target_super_affordances:
            provided_affordance_data = ProvidedAffordanceData(provided_affordance.affordance, provided_affordance.object_filter, provided_affordance.allow_self)
            provided_target_affordances.append(provided_affordance_data)

        provided_super_affordances = getattr(tuning_class, 'super_affordances', ())
        return (provided_super_affordances, provided_target_affordances)

    def get_provided_super_affordances(self):
        affordances, target_affordances = set(), list()
        for tuning_class, _, _ in self._unlocks:
            provided_super_affordances, provided_target_affordances = self._get_provided_super_affordances_from_unlock(tuning_class)
            affordances.update(provided_super_affordances)
            target_affordances.append(provided_target_affordances)

        return (affordances, target_affordances)

    def get_sim_info_from_provider(self):
        return self._sim_info

    def get_unlocks(self, tuning_class):
        if tuning_class is None:
            return []
        return [unlock for unlock in self._unlocks if issubclass(unlock.tuning_class, tuning_class)]

    def is_unlocked(self, tuning_class):
        return any((unlock.tuning_class is tuning_class for unlock in self._unlocks))

    def get_number_unlocked(self, tag):
        return sum((1 for unlock in self._unlocks if unlock.tuning_class is not None if hasattr(unlock.tuning_class, 'tuning_tags') if tag in unlock.tuning_class.tuning_tags))

    def save_unlock(self):
        unlock_tracker_data = protocols.PersistableUnlockTracker()
        for unlock in self._unlocks:
            with ProtocolBufferRollback(unlock_tracker_data.unlock_data_list) as (unlock_data):
                unlock_data.unlock_instance_id = unlock.tuning_class.guid64
                unlock_data.unlock_instance_type = unlock.tuning_class.tuning_manager.TYPE
                if unlock.name is not None:
                    unlock_data.custom_name = unlock.name
                if unlock in self._marked_new_unlocks:
                    unlock_data.marked_as_new = True

        return unlock_tracker_data

    def load_unlock(self, unlock_proto_msg, skip_load=False):
        for unlock_data in unlock_proto_msg.unlock_data_list:
            if skip_load:
                if unlock_data.custom_name:
                    continue
            instance_id = unlock_data.unlock_instance_id
            instance_type = sims4.resources.Types(unlock_data.unlock_instance_type)
            manager = services.get_instance_manager(instance_type)
            if manager is None:
                logger.error('Loading: Sim {} failed to get instance manager for unlock item {}, {}', (self._sim_info), instance_id, instance_type, owner='jdimailig')
                continue
            tuning_class = manager.get(instance_id)
            if tuning_class is None:
                logger.info('Trying to load unavailable {} resource: {}', instance_type, instance_id)
                continue
            self._unlocks.append(Unlock(tuning_class, unlock_data.custom_name))
            if unlock_data.marked_as_new:
                self._marked_new_unlocks.add(tuning_class)
            (self.add_to_affordance_caches)(*self._get_provided_super_affordances_from_unlock(tuning_class))

    @classproperty
    def _tracker_lod_threshold(cls):
        return SimInfoLODLevel.FULL

    def on_lod_update(self, old_lod, new_lod):
        if new_lod < self._tracker_lod_threshold:
            self._unlocks.clear()
        else:
            if old_lod < self._tracker_lod_threshold:
                sim_msg = services.get_persistence_service().get_sim_proto_buff(self._sim_info.id)
                if sim_msg is not None:
                    self.load_unlock(sim_msg.attributes.unlock_tracker)