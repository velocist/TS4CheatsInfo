# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\rabbit_hole\rabbit_hole_element.py
# Compiled at: 2020-01-24 21:44:48
# Size of source mod 2**32: 1667 bytes
import services, sims4
from interactions import ParticipantTypeSingle, ParticipantType
from interactions.utils.interaction_elements import XevtTriggeredElement
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, TunableEnumEntry, TunablePackSafeReference

class RabbitHoleElement(XevtTriggeredElement, HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'rabbit_holed_participant':TunableEnumEntry(description='\n            The participant to place in the rabbit hole.\n            ',
       tunable_type=ParticipantTypeSingle,
       default=ParticipantTypeSingle.Actor), 
     'rabbit_hole':TunablePackSafeReference(description='\n            Rabbit hole to create\n            ',
       manager=services.get_instance_manager(sims4.resources.Types.RABBIT_HOLE))}

    def _do_behavior(self):
        if self.rabbit_hole is None:
            return
        sim_or_sim_info = self.interaction.get_participant(self.rabbit_holed_participant)
        picked_skill = self.interaction.get_participant(ParticipantType.PickedStatistic)
        services.get_rabbit_hole_service().put_sim_in_managed_rabbithole((sim_or_sim_info.sim_info), (self.rabbit_hole), picked_skill=picked_skill)