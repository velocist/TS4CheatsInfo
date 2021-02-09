# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\favorites\favorites_tuning.py
# Compiled at: 2019-07-12 00:55:05
# Size of source mod 2**32: 1688 bytes
import services
from animation.tunable_animation_overrides import TunableAnimationOverrides
from sims4.tuning.tunable import TunableReference, TunableList, TunableSet, TunableTuple

class FavoritesTuning:
    FAVORITES_ANIMATION_OVERRIDES = TunableList(description='\n        A list of favorite object definitions and animation overrides. These will\n        be applied any time one of these favorites is used (currently only with \n        prop overrides).\n        ',
      tunable=TunableTuple(description='\n            A set of favorite object definitions and animation overrides to apply\n            when one of those definitions is used as a favorite.\n            ',
      favorite_definitions=TunableSet(description='\n                A set of object definitions. If any object in this set is used as a \n                favorite, the corresponding Animation Overrides will be applied.\n                ',
      tunable=TunableReference(description='\n                    The definition of the favorite.\n                    ',
      manager=(services.definition_manager()),
      pack_safe=True)),
      animation_overrides=TunableAnimationOverrides(description='\n                Any animation overrides to use when one of the listed favorite \n                objects is used. Currently, this only applies to prop overrides.\n                ')))