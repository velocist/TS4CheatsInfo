# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\conditional_layers\conditional_layer_commands.py
# Compiled at: 2017-08-03 21:31:09
# Size of source mod 2**32: 3433 bytes
from conditional_layers.conditional_layer_service import ConditionalLayerRequestSpeedType
from server_commands.argument_helpers import TunableInstanceParam
import services, sims4.commands

@sims4.commands.Command('layers.load_layer')
def load_conditional_layer(conditional_layer: TunableInstanceParam(sims4.resources.Types.CONDITIONAL_LAYER), immediate: bool=True, timer_interval: int=1, timer_object_count: int=5):
    if conditional_layer is None:
        sims4.commands.output('Unable to find the conditional_layer instance specified.')
        return
    conditional_layer_service = services.conditional_layer_service()
    speed = ConditionalLayerRequestSpeedType.IMMEDIATELY if immediate else ConditionalLayerRequestSpeedType.GRADUALLY
    conditional_layer_service.load_conditional_layer(conditional_layer, speed=speed,
      timer_interval=timer_interval,
      timer_object_count=timer_object_count)


@sims4.commands.Command('layers.destroy_layer')
def destroy_conditional_layer(conditional_layer: TunableInstanceParam(sims4.resources.Types.CONDITIONAL_LAYER), immediate: bool=True, timer_interval: int=1, timer_object_count: int=5):
    conditional_layer_service = services.conditional_layer_service()
    speed = ConditionalLayerRequestSpeedType.IMMEDIATELY if immediate else ConditionalLayerRequestSpeedType.GRADUALLY
    conditional_layer_service.destroy_conditional_layer(conditional_layer, speed=speed,
      timer_interval=timer_interval,
      timer_object_count=timer_object_count)


@sims4.commands.Command('layers.reload_layer')
def reload_conditional_layer(conditional_layer: TunableInstanceParam(sims4.resources.Types.CONDITIONAL_LAYER), immediate: bool=True, timer_interval: int=1, timer_object_count: int=5):
    conditional_layer_service = services.conditional_layer_service()
    speed = ConditionalLayerRequestSpeedType.IMMEDIATELY if immediate else ConditionalLayerRequestSpeedType.GRADUALLY
    conditional_layer_service.destroy_conditional_layer(conditional_layer, speed=speed,
      timer_interval=timer_interval,
      timer_object_count=timer_object_count)
    conditional_layer_service.load_conditional_layer(conditional_layer, speed=speed,
      timer_interval=timer_interval,
      timer_object_count=timer_object_count)