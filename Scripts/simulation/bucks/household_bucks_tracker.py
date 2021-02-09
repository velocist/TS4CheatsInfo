# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\bucks\household_bucks_tracker.py
# Compiled at: 2020-05-15 01:56:16
# Size of source mod 2**32: 1579 bytes
from bucks.bucks_tracker import BucksTrackerBase
from distributor.ops import SetBuckFunds
from distributor.system import Distributor
from households.household_tracker import HouseholdTracker
import services

class HouseholdBucksTracker(BucksTrackerBase, HouseholdTracker):

    def on_all_households_and_sim_infos_loaded(self):
        if not self._owner.id == services.active_household_id():
            return
        super().on_all_households_and_sim_infos_loaded()

    def on_zone_load(self):
        if not self._owner.id == services.active_household_id():
            return
        super().on_zone_load()

    def _owner_sim_info_gen(self):
        yield from self._owner
        if False:
            yield None

    def household_lod_cleanup(self):
        self.clear_bucks_tracker()

    def distribute_bucks(self, bucks_type):
        op = SetBuckFunds(bucks_type, self._bucks[bucks_type])
        Distributor.instance().add_op_with_no_owner(op)

    def is_distributable_tracker(self):
        return self._owner.id == services.active_household_id()