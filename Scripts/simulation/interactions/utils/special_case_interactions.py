# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\utils\special_case_interactions.py
# Compiled at: 2020-07-01 20:21:10
# Size of source mod 2**32: 663 bytes
from interactions.base.super_interaction import SuperInteraction

class MultiSimPostureSpecialExitSuperInteraction(SuperInteraction):

    def should_push_posture_primitive_for_multi_exit(self):
        return False