# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\sickness_tuning.py
# Compiled at: 2015-02-09 21:17:37
# Size of source mod 2**32: 1642 bytes
from interactions.utils.loot import LootActions
from sims4.tuning.tunable import TunableList, TunableReference
import services

class SicknessTuning:
    SICKNESS_BUFFS_PLAYER_FACED = TunableList(description="\n        List of buffs that define if a sim is sick from what the player can \n        see.  The way sickness work, a sim might be sick but it may not be \n        visible to the player, so on this list we should only tune the buff's\n        that would make the sim sick on the players perspective.\n        i.e. buffs that would make a child sim take a day of school.\n        ",
      tunable=TunableReference(manager=(services.buff_manager()),
      pack_safe=True))
    LOOT_ACTIONS_ON_CHILD_CAREER_AUTO_SICK = TunableList(description='\n        Loot actions to test and apply on the event its time to go to work \n        and the child sim is sick.\n        i.e. notification...  \n        ',
      tunable=LootActions.TunableReference(pack_safe=True))

    @classmethod
    def is_child_sim_sick(cls, sim_info):
        if not sim_info.is_child:
            return False
        return any((sim_info.has_buff(buff_type) for buff_type in SicknessTuning.SICKNESS_BUFFS_PLAYER_FACED))