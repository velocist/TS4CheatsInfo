# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\buffs\appearance_modifier\appearance_modifier_type.py
# Compiled at: 2019-10-11 21:38:06
# Size of source mod 2**32: 339 bytes
import enum

class AppearanceModifierType(enum.Int):
    SET_CAS_PART = 0
    RANDOMIZE_BODY_TYPE_COLOR = 1
    RANDOMIZE_SKINTONE_FROM_TAGS = 2
    GENERATE_OUTFIT = 3
    RANDOMIZE_CAS_PART = 4