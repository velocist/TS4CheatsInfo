# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\game_effect_modifier\game_effect_type.py
# Compiled at: 2020-08-04 00:24:14
# Size of source mod 2**32: 545 bytes
import enum

class GameEffectType(enum.Int, export=False):
    AFFORDANCE_MODIFIER = 0
    EFFECTIVE_SKILL_MODIFIER = 1
    CONTINUOUS_STATISTIC_MODIFIER = 3
    RELATIONSHIP_TRACK_DECAY_LOCKER = 4
    MOOD_EFFECT_MODIFIER = 5
    STATISTIC_STATIC_MODIFIER = 6
    AUTONOMY_MODIFIER = 7
    WHIM_MODIFIER = 8
    PIE_MENU_MODIFIER = 9
    AFFORDANCE_FILTER_MODIFIER = 10
    RELATIONSHIP_TRACK_DECAY_MODIFIER = 11