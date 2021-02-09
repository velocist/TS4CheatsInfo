# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\seasons\season_aware_component.py
# Compiled at: 2018-10-10 19:42:06
# Size of source mod 2**32: 2485 bytes
from objects.components import Component
from objects.components.state import TunableStateValueReference
from objects.components.types import SEASON_AWARE_COMPONENT
from seasons.seasons_enums import SeasonType
from sims4.common import Pack
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, TunableMapping, TunableEnumEntry, TunableList
from sims4.utils import classproperty
import services

class SeasonAwareComponent(Component, HasTunableFactory, AutoFactoryInit, component_name=SEASON_AWARE_COMPONENT):
    FACTORY_TUNABLES = {'seasonal_state_mapping': TunableMapping(description='\n            A tunable mapping linking a season to the state the component\n            owner should have.\n            ',
                                 key_type=TunableEnumEntry(description='\n                The season we are interested in.\n                ',
                                 tunable_type=SeasonType,
                                 default=None),
                                 value_type=TunableList(description='\n                A tunable list of states to apply to the owning object of\n                this component when it transitions to this season.\n                ',
                                 tunable=TunableStateValueReference(pack_safe=True)))}

    @classproperty
    def required_packs(cls):
        return (
         Pack.EP05,)

    def on_add(self):
        self.on_season_set(services.season_service().season)

    def on_finalize_load(self):
        self.on_season_set(services.season_service().season)

    def on_season_set(self, season_type):
        if season_type in self.seasonal_state_mapping:
            for state_value in self.seasonal_state_mapping[season_type]:
                self.owner.set_state(state_value.state, state_value)