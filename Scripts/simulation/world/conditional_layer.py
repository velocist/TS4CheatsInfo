# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\world\conditional_layer.py
# Compiled at: 2019-02-02 02:21:13
# Size of source mod 2**32: 3552 bytes
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableReference, TunableList, Tunable, OptionalTunable, TunableTuple, TunableRange
from sims4.tuning.tunable_hash import TunableStringHash32
import services, sims4.resources
logger = sims4.log.Logger('Conditional Layer')

class ConditionalLayer(metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(sims4.resources.Types.CONDITIONAL_LAYER)):
    INSTANCE_TUNABLES = {'layer_name':TunableStringHash32(description='\n            The name of the layer that will be loaded.\n            World Building should tell you what this should be.\n            '), 
     'conflicting_layers':TunableList(description='\n            A List of Zone Layers that conflict with this layer. If this layer\n            is present and one of the listed Zone Layers attempts to load it \n            will fail.        \n            ',
       tunable=TunableReference(description='\n                A Zone Layer that conflicts with this Zone Layer.\n                ',
       manager=(services.get_instance_manager(sims4.resources.Types.CONDITIONAL_LAYER))),
       unique_entries=True), 
     'client_only':Tunable(description='\n            If checked, this layer is loaded as a client side layer. All \n            objects on the layer will exist as scene models only and have no\n            gameplay (e.g. no interactions, no footprint).\n            \n            This is useful for layers that are purely decorative. And unlike\n            regular game objects, client side objects can be placed outside of\n            routable/interactable areas, e.g. decorative cards in the distance.\n            \n            We do not support mixing game objects and client only objects on\n            the same layer. Please separate them out onto their on layers.\n            ',
       tunable_type=bool,
       default=False), 
     'fade_data':OptionalTunable(description='\n            If enabled, the conditional layer will fade in rather than pop.\n            ',
       tunable=TunableTuple(fade_duration=Tunable(description='\n                    The duration of the fade in sim minutes.\n                    ',
       tunable_type=float,
       default=10.0),
       delay_min=TunableRange(description='\n                    The minimum length of the fade delay in sim minutes.\n                    ',
       tunable_type=float,
       default=10.0,
       minimum=0.0),
       delay_max=TunableRange(description='\n                    The maximum length of the fade delay in sim minutes.\n                    ',
       tunable_type=float,
       default=20.0,
       minimum=0.0)))}

    @classmethod
    def _verify_tuning_callback(cls):
        if cls.fade_data is not None:
            if cls.fade_data.delay_min >= cls.fade_data.delay_max:
                logger.error('The fade data for {} has a delay min ({}) greater than the delay max ({}). This is not allowed.', cls, cls.fade_data.delay_min, cls.fade_data.delay_max)