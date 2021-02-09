# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\situations\visiting\visiting_tuning.py
# Compiled at: 2016-08-10 00:03:20
# Size of source mod 2**32: 905 bytes
from sims4.tuning.tunable import TunableList, TunableReference
import services

class VisitingTuning:
    ALWAYS_WELCOME_TRAITS = TunableList(description='\n        Traits that will guarantee that after the Sim is welcomed into a \n        household, it will always be automatically welcomed if he/she comes\n        back.\n        i.e. Vampires are always welcomed after being welcomed once.\n        ',
      tunable=TunableReference(description='\n            Trait reference to make the Sim always be welcomed after they \n            are welcomed once.\n            ',
      manager=(services.trait_manager()),
      pack_safe=True))