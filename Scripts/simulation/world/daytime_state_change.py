# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\world\daytime_state_change.py
# Compiled at: 2019-01-17 23:28:39
# Size of source mod 2**32: 213 bytes
import enum

class DaytimeStateChange(enum.Int):
    Sunrise = 1
    Sunset = 2