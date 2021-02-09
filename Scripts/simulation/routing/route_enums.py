# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\route_enums.py
# Compiled at: 2020-08-20 22:00:38
# Size of source mod 2**32: 1696 bytes
from sims4.tuning.dynamic_enum import DynamicEnum
import enum

class RouteEventType(enum.Int, export=False):
    LOW_REPEAT = 1
    LOW_SINGLE = 2
    HIGH_SINGLE = 3
    BROADCASTER = 4
    INTERACTION_PRE = 5
    INTERACTION_POST = 6
    FIRST_OUTDOOR = 7
    LAST_OUTDOOR = 8
    FIRST_INDOOR = 9
    LAST_INDOOR = 10


class RouteEventPriority(DynamicEnum):
    DEFAULT = 0


class RoutingStageEvent(enum.Int, export=False):
    ROUTE_START = 0
    ROUTE_END = 1