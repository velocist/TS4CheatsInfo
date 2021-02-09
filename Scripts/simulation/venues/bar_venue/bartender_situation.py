# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\venues\bar_venue\bartender_situation.py
# Compiled at: 2015-07-25 02:48:55
# Size of source mod 2**32: 1855 bytes
from sims4.tuning.instances import lock_instance_tunables
from sims4.utils import classproperty
from situations.bouncer.bouncer_types import BouncerExclusivityCategory
from situations.situation import Situation
from situations.situation_complex import SituationState, SituationComplexCommon, TunableSituationJobAndRoleState, SituationStateData
from situations.situation_types import SituationCreationUIOption

class _BartenderSituationState(SituationState):
    pass


class BartenderSituation(SituationComplexCommon):
    INSTANCE_TUNABLES = {'bartender_job_and_role': TunableSituationJobAndRoleState(description='\n            The job and role of the bartender.\n            ')}
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    @classmethod
    def _states(cls):
        return (SituationStateData(1, _BartenderSituationState),)

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls):
        return [(cls.bartender_job_and_role.job, cls.bartender_job_and_role.role_state)]

    @classmethod
    def default_job(cls):
        pass

    def start_situation(self):
        super().start_situation()
        self._change_state(_BartenderSituationState())


lock_instance_tunables(BartenderSituation, exclusivity=(BouncerExclusivityCategory.VENUE_EMPLOYEE),
  creation_ui_option=(SituationCreationUIOption.NOT_AVAILABLE),
  duration=0,
  _implies_greeted_status=False)