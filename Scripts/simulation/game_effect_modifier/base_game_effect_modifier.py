# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\game_effect_modifier\base_game_effect_modifier.py
# Compiled at: 2018-11-17 02:59:40
# Size of source mod 2**32: 799 bytes


class BaseGameEffectModifier:

    def __init__(self, modifier_type):
        self.modifier_type = modifier_type

    def apply_modifier(self, sim_info):
        pass

    def remove_modifier(self, sim_info, handle):
        pass