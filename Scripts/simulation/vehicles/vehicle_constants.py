# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\vehicles\vehicle_constants.py
# Compiled at: 2019-11-05 23:10:23
# Size of source mod 2**32: 345 bytes
import enum

class VehicleTransitionState(enum.Int):
    NO_STATE = 1
    DEPLOYING = ...
    MOUNTING = ...