# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\path_planner\path_plan_enums.py
# Compiled at: 2016-09-02 22:06:49
# Size of source mod 2**32: 618 bytes
import enum, routing

class FootprintKeyMaskBits(enum.IntFlags):
    SMALL_HEIGHT = routing.FOOTPRINT_KEY_REQUIRE_SMALL_HEIGHT
    TINY_HEIGHT = routing.FOOTPRINT_KEY_REQUIRE_TINY_HEIGHT
    FLOATING = routing.FOOTPRINT_KEY_REQUIRE_FLOATING
    LARGE_HEIGHT = routing.FOOTPRINT_KEY_REQUIRE_LARGE_HEIGHT