# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\visibility\visibility_enums.py
# Compiled at: 2016-08-30 02:46:43
# Size of source mod 2**32: 591 bytes
import enum

class VisibilityFlags(enum.IntFlags):
    MIRRORS = 1
    LOT_WATER_REFLECTION = 2
    WORLD_WATER_REFLECTION = 4