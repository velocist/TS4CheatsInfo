# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\occult\switch_occult_element.py
# Compiled at: 2019-04-12 03:09:17
# Size of source mod 2**32: 1899 bytes
from interactions import ParticipantTypeSingle
from interactions.utils.interaction_elements import XevtTriggeredElement
from sims.occult.occult_enums import OccultType
from sims4.tuning.tunable import TunableEnumEntry, Tunable

class SwitchOccultElement(XevtTriggeredElement):
    FACTORY_TUNABLES = {'participant':TunableEnumEntry(description='\n            The Sim whose occult type should be switched.\n            ',
       tunable_type=ParticipantTypeSingle,
       default=ParticipantTypeSingle.Actor), 
     'occult_type':TunableEnumEntry(description='\n            The occult type that this element affects\n            ',
       tunable_type=OccultType,
       default=OccultType.HUMAN), 
     'associate_occult_with_current_posture':Tunable(description="\n            If checked, the sim's current posture will *own* this occult. This\n            means that the occult will switch if the current posture is reset \n            or ended. This option is only compatible with postures which have\n            switch occult tuning to pull the new posture from. Please consult a\n            GPE about whether this option is appropriate before using it.\n            ",
       tunable_type=bool,
       default=False)}

    def _do_behavior(self):
        sim_info = self.interaction.get_participant(self.participant).sim_info
        occult_tracker = sim_info.occult_tracker
        if occult_tracker.has_occult_type(self.occult_type):
            occult_tracker.switch_to_occult_type(self.occult_type)
            if self.associate_occult_with_current_posture:
                sim_info.get_sim_instance().posture.pretend_entry_occult_switch_processed()