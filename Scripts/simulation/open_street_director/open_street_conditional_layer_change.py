# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\open_street_director\open_street_conditional_layer_change.py
# Compiled at: 2020-04-10 17:23:59
# Size of source mod 2**32: 2616 bytes
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, TunableReference, Tunable
import sims4, services
logger = sims4.log.Logger('OpenStreetDirector', default_owner='jjacobson')

class DirectManipulateConditionalLayer(HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'conditional_layer':TunableReference(description='\n            The conditional layer to manipulate.\n            ',
       manager=services.get_instance_manager(sims4.resources.Types.CONDITIONAL_LAYER)), 
     'show_conditional_layer':Tunable(description='\n            If checked then the specified conditional layer will be shown.\n            If unchecked then the specified conditional layer will be hidden.\n            ',
       tunable_type=bool,
       default=True), 
     'immediate':Tunable(description='\n            Whether or not the manipulation of the conditional layer is \n            immediate or can take place over longer periods of time.\n            ',
       tunable_type=bool,
       default=True)}

    def change_conditional_layer(self, invert_show=False):
        zone_director = services.venue_service().get_zone_director()
        open_street_director = zone_director.open_street_director
        if open_street_director is None:
            return
        else:
            return open_street_director.has_conditional_layer(self.conditional_layer) or None
        show_conditional_layer = self.show_conditional_layer
        if invert_show:
            show_conditional_layer = not show_conditional_layer
        elif show_conditional_layer:
            if self.immediate:
                open_street_director.load_layer_immediately(self.conditional_layer)
            else:
                open_street_director.load_layer_gradually(self.conditional_layer)
        else:
            open_street_director.remove_layer_objects(self.conditional_layer)