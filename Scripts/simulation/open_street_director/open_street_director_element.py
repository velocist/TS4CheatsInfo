# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\open_street_director\open_street_director_element.py
# Compiled at: 2019-08-21 02:06:33
# Size of source mod 2**32: 618 bytes
from interactions.utils.interaction_elements import XevtTriggeredElement
from open_street_director.open_street_conditional_layer_change import DirectManipulateConditionalLayer

class ManipulateConditionalLayer(XevtTriggeredElement, DirectManipulateConditionalLayer):

    def _do_behavior(self):
        self.change_conditional_layer()