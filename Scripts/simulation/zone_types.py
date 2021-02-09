# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\zone_types.py
# Compiled at: 2014-06-12 00:38:33
# Size of source mod 2**32: 888 bytes
import enum

class ZoneState(enum.Int, export=False):
    ZONE_INIT = 0
    OBJECTS_LOADED = 1
    CLIENT_CONNECTED = 2
    HOUSEHOLDS_AND_SIM_INFOS_LOADED = 3
    HITTING_THEIR_MARKS = 4
    RUNNING = 5
    SHUTDOWN_STARTED = 6