# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\sim_info_lod.py
# Compiled at: 2019-07-08 18:13:46
# Size of source mod 2**32: 1264 bytes
import enum

class SimInfoLODLevel(enum.Int):
    MINIMUM = 1
    BACKGROUND = 10
    BASE = 25
    INTERACTED = 50
    FULL = 100
    ACTIVE = 125
    _prev_lod = {BACKGROUND: MINIMUM, BASE: BACKGROUND, INTERACTED: BASE, FULL: INTERACTED, ACTIVE: FULL}
    _next_lod = {MINIMUM: BACKGROUND, BACKGROUND: BASE, BASE: INTERACTED, INTERACTED: FULL}

    @staticmethod
    def get_previous_lod(from_lod):
        if from_lod in SimInfoLODLevel._prev_lod:
            return SimInfoLODLevel._prev_lod[from_lod]

    @staticmethod
    def get_next_lod(from_lod):
        if from_lod in SimInfoLODLevel._next_lod:
            return SimInfoLODLevel._next_lod[from_lod]