# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\global_gender_preference_tuning.py
# Compiled at: 2016-03-03 03:01:44
# Size of source mod 2**32: 5483 bytes
from sims4.tuning.tunable import TunableMapping, TunableEnumEntry, TunableReference, TunableList, TunableTuple, Tunable, TunableSet
import enum, services, sims.sim_info_types, sims4

class GenderPreference(enum.Int):
    LIKES_NEITHER = 0
    HETEROSEXUAL = 1
    HOMOSEXUAL = 2
    BISEXUAL = 3


class GlobalGenderPreferenceTuning:
    GENDER_PREFERENCE = TunableMapping(key_type=TunableEnumEntry((sims.sim_info_types.Gender), (sims.sim_info_types.Gender.MALE),
      description='The gender to index the gender preference to.'),
      value_type=TunableReference((services.get_instance_manager(sims4.resources.Types.STATISTIC)), description='The statistic that represents the matching gender preference'),
      description='A mapping between gender and the gender preference statistic for easy lookup.')
    GENDER_PREFERENCE_WEIGHTS = TunableList(description='A weightings list for the weighted random choice of sexual preference.', tunable=TunableTuple(gender_preference=TunableEnumEntry(GenderPreference, (GenderPreference.LIKES_NEITHER),
      description='The gender to index the gender preference to.'),
      weight=Tunable(int, 0, description='The minimum possible skill.'),
      description='A mapping between gender and the gender preference statistic for easy lookup.'))
    GENDER_PREFERENCE_MAPPING = TunableMapping(key_type=TunableEnumEntry(GenderPreference, (GenderPreference.LIKES_NEITHER),
      description='The gender to index the gender preference to.'),
      value_type=TunableMapping(key_type=TunableEnumEntry((sims.sim_info_types.Gender), (sims.sim_info_types.Gender.MALE),
      description='The gender to index the gender preference to.'),
      value_type=(TunableSet(TunableReference((services.get_instance_manager(sims4.resources.Types.STATISTIC)), description='The statistic that represents the matching gender preference'))),
      description='A mapping between gender and the gender preference statistic for easy lookup.'),
      description='A mapping between gender and the gender preference statistic for easy lookup.')
    enable_autogeneration_same_sex_preference = False
    ENABLE_AUTOGENERATION_SAME_SEX_PREFERENCE_THRESHOLD = Tunable(description="\n        A value that, once crossed, indicates the player's allowance of same-\n        sex relationships with townie auto-generation.\n        ",
      tunable_type=float,
      default=1.0)
    ENABLED_AUTOGENERATION_SAME_SEX_PREFERENCE_WEIGHTS = TunableList(description='\n        An alternative weightings list for the weighted random choice of sexual\n        preference after a romantic same-sex relationship has been kindled.\n        ',
      tunable=TunableTuple(gender_preference=TunableEnumEntry(GenderPreference, (GenderPreference.LIKES_NEITHER),
      description='The gender to index the gender preference to.'),
      weight=Tunable(int, 0, description='The minimum possible skill.'),
      description='A mapping between gender and the gender preference statistic for easy lookup.'))
    MALE_CLOTHING_PREFERENCE_TRAIT = TunableReference(description='\n        The trait that signifies that this sim prefers to wear male clothing.\n        ',
      manager=(services.trait_manager()))
    FEMALE_CLOTHING_PREFERENCE_TRAIT = TunableReference(description='\n        The trait that signifies that this sim prefers to wear female clothing.\n        ',
      manager=(services.trait_manager()))