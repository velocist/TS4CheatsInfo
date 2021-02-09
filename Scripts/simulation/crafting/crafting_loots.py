# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\crafting\crafting_loots.py
# Compiled at: 2019-10-15 22:44:35
# Size of source mod 2**32: 956 bytes
from interactions.utils.loot_basic_op import BaseLootOperation
from objects.components import types

class RefundCraftingProcessLoot(BaseLootOperation):

    def _apply_to_subject_and_target(self, subject, target, resolver):
        subject = resolver.get_participant(self.subject)
        if subject is None:
            return
        crafting_component = subject.get_component(types.CRAFTING_COMPONENT)
        if crafting_component is None:
            return
        crafting_process = crafting_component.get_crafting_process()
        if crafting_process is None:
            return
        crafting_process.refund_payment(explicit=True)