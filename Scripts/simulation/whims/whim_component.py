# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\whims\whim_component.py
# Compiled at: 2018-06-08 01:23:49
# Size of source mod 2**32: 1146 bytes
from objects.components import Component
from objects.components.types import WHIM_COMPONENT
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, TunableReference
import services, sims4.resources

class WhimComponent(Component, HasTunableFactory, AutoFactoryInit, component_name=WHIM_COMPONENT):
    FACTORY_TUNABLES = {'whim_set': TunableReference(description='\n            The whim set that is active when this object is on the lot.\n            ',
                   manager=(services.get_instance_manager(sims4.resources.Types.ASPIRATION)),
                   class_restrictions=('ObjectivelessWhimSet', ))}

    def on_add(self):
        self.owner.manager.add_active_whim_set(self.whim_set)

    def on_remove(self):
        self.owner.manager.remove_active_whim_set(self.whim_set)