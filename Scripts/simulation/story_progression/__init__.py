# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\story_progression\__init__.py
# Compiled at: 2015-02-27 04:40:32
# Size of source mod 2**32: 584 bytes
import enum

class StoryProgressionFlags(enum.IntFlags, export=False):
    DISABLED = 0
    ALLOW_POPULATION_ACTION = 1
    ALLOW_INITIAL_POPULATION = 2
    SIM_INFO_FIREMETER = 4