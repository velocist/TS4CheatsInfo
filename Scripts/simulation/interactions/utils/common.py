# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\utils\common.py
# Compiled at: 2015-06-18 22:36:38
# Size of source mod 2**32: 1459 bytes
from element_utils import build_critical_section_with_finally

class InteractionRetargetHandler:

    def __init__(self, interaction, target):
        self._target = target
        self._old_target = interaction.target
        self._interaction = interaction

    def begin(self, _):
        self._interaction.set_target(self._target)

    def end(self, _):
        self._interaction.set_target(self._old_target)


def retarget_interaction(interaction, target, *args):
    if interaction is not None:
        interaction_retarget_handler = InteractionRetargetHandler(interaction, target)
        return build_critical_section_with_finally(interaction_retarget_handler.begin, args, interaction_retarget_handler.end)
    return args