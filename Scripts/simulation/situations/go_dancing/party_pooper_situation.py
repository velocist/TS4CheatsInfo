# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\situations\go_dancing\party_pooper_situation.py
# Compiled at: 2015-07-06 22:18:46
# Size of source mod 2**32: 2131 bytes
from sims4.tuning.instances import lock_instance_tunables
from situations.bouncer.bouncer_types import BouncerExclusivityCategory
from situations.situation import Situation
from situations.situation_complex import SituationComplexCommon, SituationStateData, CommonSituationState, TunableSituationJobAndRoleState
from situations.situation_types import SituationCreationUIOption

class _PartyPooperState(CommonSituationState):
    pass


class PartyPooperSituation(SituationComplexCommon):
    INSTANCE_TUNABLES = {'party_pooper_state':_PartyPooperState.TunableFactory(description='\n            ',
       tuning_group=SituationComplexCommon.SITUATION_STATE_GROUP,
       display_name='01_party_pooper_state'), 
     'party_pooper_job_and_role':TunableSituationJobAndRoleState(description='\n            The job and role state for a party pooper.\n            ')}
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    @classmethod
    def _states(cls):
        return (SituationStateData(1, _PartyPooperState, factory=(cls.party_pooper_state)),)

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls):
        return [(cls.party_pooper_job_and_role.job, cls.party_pooper_job_and_role.role_state)]

    @classmethod
    def default_job(cls):
        return cls.party_pooper_job_and_role.situation_job

    def start_situation(self):
        super().start_situation()
        self._change_state(self.party_pooper_state())


lock_instance_tunables(PartyPooperSituation, exclusivity=(BouncerExclusivityCategory.NORMAL),
  creation_ui_option=(SituationCreationUIOption.NOT_AVAILABLE),
  _implies_greeted_status=False)