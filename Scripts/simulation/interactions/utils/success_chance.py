# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\utils\success_chance.py
# Compiled at: 2017-07-11 23:17:19
# Size of source mod 2**32: 2355 bytes
from event_testing.tests import TunableTestSet
from sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, TunablePercent, TunableList, TunableTuple, TunableRange

class SuccessChance(HasTunableSingletonFactory, AutoFactoryInit):
    ONE = None
    FACTORY_TUNABLES = {'base_chance':TunablePercent(description='\n            The basic chance of success.\n            ',
       default=100), 
     'multipliers':TunableList(description='\n            A list of multipliers to apply to base_chance.\n            ',
       tunable=TunableTuple(multiplier=TunableRange(description='\n                    The multiplier to apply to base_chance if the associated\n                    tests pass.\n                    ',
       tunable_type=float,
       default=1,
       minimum=0),
       tests=TunableTestSet(description='\n                    A series of tests that must pass in order for multiplier to\n                    be applied.\n                    ')))}

    def get_chance(self, participant_resolver):
        chance = self.base_chance
        for multiplier_data in self.multipliers:
            if multiplier_data.tests.run_tests(participant_resolver):
                chance *= multiplier_data.multiplier

        return min(chance, 1)

    def __hash__(self):
        return hash(self.base_chance) ^ hash(self.multipliers)

    def __eq__(self, other_chance):
        if type(self) is not type(other_chance):
            return False
        return self.base_chance == other_chance.base_chance and self.multipliers == other_chance.multipliers

    def __ne__(self, other_chance):
        return not self.__eq__(other_chance)


SuccessChance.ONE = SuccessChance(base_chance=1, multipliers=())