# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\doors\door_enums.py
# Compiled at: 2019-08-06 23:30:11
# Size of source mod 2**32: 285 bytes
import enum

class VenueFrontdoorRequirement(enum.Int):
    NEVER = 0
    ALWAYS = 1
    OWNED_OR_RENTED = 2