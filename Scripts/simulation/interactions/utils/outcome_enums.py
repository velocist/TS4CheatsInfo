# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\utils\outcome_enums.py
# Compiled at: 2013-10-22 19:19:24
# Size of source mod 2**32: 262 bytes
from sims4.tuning.dynamic_enum import DynamicEnum

class OutcomeResult(DynamicEnum):
    NONE = 0
    SUCCESS = 1
    FAILURE = 2