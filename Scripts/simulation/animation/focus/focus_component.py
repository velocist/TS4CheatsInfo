# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\animation\focus\focus_component.py
# Compiled at: 2016-07-25 21:29:27
# Size of source mod 2**32: 2177 bytes
from animation.focus.focus_ops import SetFocusScore
from animation.focus.focus_score import TunableFocusScoreVariant
from objects.components import Component, types, componentmethod
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit
from sims4.tuning.tunable_hash import TunableStringHash32
import distributor.fields

class FocusComponent(Component, HasTunableFactory, AutoFactoryInit, component_name=types.FOCUS_COMPONENT):
    FACTORY_TUNABLES = {'_focus_bone':TunableStringHash32(description='\n            The bone Sims direct their attention towards when focusing on an\n            object.\n            ',
       default='_focus_'), 
     '_focus_score':TunableFocusScoreVariant()}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._current_focus_score = self._focus_score

    @distributor.fields.ComponentField(op=SetFocusScore)
    def focus_score(self):
        return self._current_focus_score

    @focus_score.setter
    def focus_score(self, value):
        self._current_focus_score = value

    @componentmethod
    def get_focus_bone(self):
        return self._focus_bone