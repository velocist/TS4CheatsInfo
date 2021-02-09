# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\gardening\gardening_component_variant.py
# Compiled at: 2018-02-01 22:59:26
# Size of source mod 2**32: 949 bytes
from objects.gardening.gardening_component_fruit import GardeningFruitComponent
from objects.gardening.gardening_component_plant import GardeningPlantComponent
from objects.gardening.gardening_component_shoot import GardeningShootComponent
from sims4.tuning.tunable import TunableVariant

class TunableGardeningComponentVariant(TunableVariant):

    def __init__(self, **kwargs):
        (super().__init__)(fruit_component=GardeningFruitComponent.TunableFactory(), 
         plant_component=GardeningPlantComponent.TunableFactory(), 
         shoot=GardeningShootComponent.TunableFactory(), 
         locked_args={'disabled': None}, 
         default='disabled', **kwargs)