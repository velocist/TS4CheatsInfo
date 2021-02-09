# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\event_testing\__init__.py
# Compiled at: 2018-11-10 01:40:16
# Size of source mod 2**32: 357 bytes
import enum

class TargetIdTypes(enum.Int):
    DEFAULT = 0
    INSTANCE = 1
    DEFINITION = 2
    HOUSEHOLD = 3
    PICKED_ITEM_ID = 4