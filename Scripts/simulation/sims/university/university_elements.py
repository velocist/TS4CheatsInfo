# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\university\university_elements.py
# Compiled at: 2019-08-16 23:36:49
# Size of source mod 2**32: 1296 bytes
from interactions.utils.interaction_elements import XevtTriggeredElement
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, Tunable
import sims4.log
logger = sims4.log.Logger('UniversityElements', default_owner='mkartika')

class UniversityEnrollmentElement(XevtTriggeredElement, HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'is_reenrollment': Tunable(description='\n            If checked, the enrollment UI will be considered re-enrollment\n            where the dialog has preselected university and major.\n            ',
                          tunable_type=bool,
                          default=False)}

    def _do_behavior(self):
        sim = self.interaction.sim
        degree_tracker = sim.sim_info.degree_tracker
        if degree_tracker is None:
            logger.error("Trying to display University Enrollment on {} but that Sim doesn't have a degree tracker.", sim)
            return False
        degree_tracker.generate_enrollment_information(is_reenrollment=(self.is_reenrollment))
        return True