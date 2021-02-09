# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\picker\lock_picker_interaction.py
# Compiled at: 2018-08-20 20:33:09
# Size of source mod 2**32: 3434 bytes
from interactions.base.picker_interaction import SimPickerInteraction
from objects.components.portal_lock_data import IndividualSimDoorLockData
from objects.components.portal_locking_enums import LockPriority, LockSide, ClearLock
from sims4.tuning.tunable import TunableEnumEntry
from sims4.tuning.tunable_base import GroupNames
from sims4.utils import flexmethod
import enum, services

class LockOperationType(enum.Int):
    LOCK = 0
    UNLOCK = 1


class LockHouseholdSimsPickerInteraction(SimPickerInteraction):
    INSTANCE_TUNABLES = {'lock_operation': TunableEnumEntry(description='\n            Define the type of lock operation that should be made on this\n            portal.\n            ',
                         tunable_type=LockOperationType,
                         default=(LockOperationType.LOCK),
                         tuning_group=(GroupNames.PICKERTUNING))}

    @flexmethod
    def _get_valid_sim_choices_gen(cls, inst, target, context, **kwargs):
        if context.sim is None:
            return
        for filter_result in (super()._get_valid_sim_choices_gen)(target, context, **kwargs):
            sim_locked = target.test_lock(filter_result.sim_info)
            if cls.lock_operation == LockOperationType.LOCK:
                if sim_locked:
                    continue
            elif not sim_locked:
                continue
            yield filter_result

    def _on_successful_picker_selection(self, results=()):
        sim_info_manager = services.sim_info_manager()
        for sim_id in results:
            sim_info = sim_info_manager.get(sim_id)
            if sim_info is None:
                continue
            if self.lock_operation == LockOperationType.LOCK:
                lock_data = IndividualSimDoorLockData(lock_sim=sim_info, lock_priority=(LockPriority.PLAYER_LOCK),
                  lock_sides=(LockSide.LOCK_BOTH),
                  should_persist=True)
                self.target.add_lock_data(lock_data, replace_same_lock_type=False, clear_existing_locks=(ClearLock.CLEAR_OTHER_LOCK_TYPES))
            else:
                lock_data = IndividualSimDoorLockData(unlock_sim=sim_info, lock_priority=(LockPriority.PLAYER_LOCK),
                  lock_sides=(LockSide.LOCK_BOTH),
                  should_persist=True)
                self.target.add_lock_data(lock_data, replace_same_lock_type=False, clear_existing_locks=(ClearLock.CLEAR_NONE))