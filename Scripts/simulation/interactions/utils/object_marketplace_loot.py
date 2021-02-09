# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\utils\object_marketplace_loot.py
# Compiled at: 2020-06-20 04:39:24
# Size of source mod 2**32: 2867 bytes
from interactions.utils.loot_basic_op import BaseLootOperation, BaseTargetedLootOperation
import sims4.log
from objects.components.types import OBJECT_MARKETPLACE_COMPONENT
from sims4.tuning.tunable import TunableVariant, AutoFactoryInit, HasTunableSingletonFactory
logger = sims4.log.Logger('ObjectMarketplaceLootOp', default_owner='rrodgers')

class ListOnMarketplace(HasTunableSingletonFactory, AutoFactoryInit):

    def __call__(self, seller, obj):
        if not obj.has_component(OBJECT_MARKETPLACE_COMPONENT):
            obj.add_dynamic_component(OBJECT_MARKETPLACE_COMPONENT, list_cost_multiplier=None, sale_price_multiplier=None, sale_chance_multplier=None)
        obj.list(seller)


class DelistOnMarketplace(HasTunableSingletonFactory, AutoFactoryInit):

    def __call__(self, seller, obj):
        if not obj.has_component(OBJECT_MARKETPLACE_COMPONENT):
            return
        marketplace_component = obj.get_component(OBJECT_MARKETPLACE_COMPONENT)
        if not marketplace_component.is_listed():
            if not marketplace_component.is_pending_sale():
                return
        obj.delist()


class SellOnMarketplace(HasTunableSingletonFactory, AutoFactoryInit):

    def __call__(self, owner, obj):
        if not obj.has_component(OBJECT_MARKETPLACE_COMPONENT):
            logger.error('Attempting to sell an object {} that is not listed on marketplace', obj)
            return
        obj.sell()


class ObjectMarketplaceLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {'marketplace_operation': TunableVariant(description='\n            The marketplace operation to perform.\n            ',
                                list=(ListOnMarketplace.TunableFactory()),
                                delist=(DelistOnMarketplace.TunableFactory()),
                                sell=(SellOnMarketplace.TunableFactory()),
                                default='list')}

    def __init__(self, marketplace_operation, **kwargs):
        (super().__init__)(**kwargs)
        self.marketplace_operation = marketplace_operation

    def _apply_to_subject_and_target(self, subject, target, resolver):
        self.marketplace_operation(subject, target)
        return True