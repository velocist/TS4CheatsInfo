# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\situations\complex\leave_situation.py
# Compiled at: 2016-10-25 01:57:15
# Size of source mod 2**32: 8869 bytes
from sims4.tuning.tunable_base import GroupNames
from sims4.utils import classproperty
from situations.bouncer.bouncer_request import RequestSpawningOption
from situations.bouncer.bouncer_types import BouncerRequestPriority
from situations.situation import Situation
from situations.situation_complex import SituationStateData
import alarms, clock, role.role_state, sims4.tuning.tunable, situations.base_situation, situations.bouncer.bouncer_request, situations.situation_complex, situations.situation_guest_list, situations.situation_job

class LeaveSituation(situations.situation_complex.SituationComplexCommon):
    INSTANCE_TUNABLES = {'leaving_soon':sims4.tuning.tunable.TunableTuple(situation_job=situations.situation_job.SituationJob.TunableReference(description='\n                                The job given to sims that we want to have leave the lot soon.\n                                '),
       role_state=role.role_state.RoleState.TunableReference(description='\n                                The role state given to the sim that we want to have leave the lot soon.\n                                '),
       tuning_group=GroupNames.ROLES), 
     'leaving_now':sims4.tuning.tunable.TunableTuple(situation_job=situations.situation_job.SituationJob.TunableReference(description='\n                                The job given to sims that we want to have leave the lot now.\n                                '),
       role_state=role.role_state.RoleState.TunableReference(description='\n                                The role state given to the sim to get them off the lot now.\n                                '),
       tuning_group=GroupNames.ROLES)}
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    @classmethod
    def _states(cls):
        return (SituationStateData(1, ForeverState),)

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls):
        return [(cls.leaving_soon.situation_job, cls.leaving_soon.role_state), (cls.leaving_now.situation_job, cls.leaving_now.role_state)]

    @classmethod
    def default_job(cls):
        return cls.leaving_now.situation_job

    def _get_duration(self):
        return 0

    def start_situation(self):
        super().start_situation()
        self._change_state(ForeverState())

    def _create_uninvited_request(self):
        request = situations.bouncer.bouncer_request.BouncerNPCFallbackRequestFactory(self, callback_data=(situations.base_situation._RequestUserData()),
          job_type=(self.leaving_soon.situation_job),
          exclusivity=(self.exclusivity))
        self.manager.bouncer.submit_request(request)

    def invite_sim_to_leave(self, sim):
        guest_info = situations.situation_guest_list.SituationGuestInfo((sim.id), (self.leaving_soon.situation_job),
          (RequestSpawningOption.CANNOT_SPAWN),
          (BouncerRequestPriority.EVENT_VIP),
          expectation_preference=True)
        request = self._create_request_from_guest_info(guest_info)
        self.manager.bouncer.submit_request(request)

    @property
    def _should_cancel_leave_interaction_on_premature_removal(self):
        return True

    @classproperty
    def situation_serialization_option(cls):
        return situations.situation_types.SituationSerializationOption.OPEN_STREETS


class ForeverState(situations.situation_complex.SituationState):

    def on_activate(self, reader=None):
        super().on_activate(reader)
        self._handle = alarms.add_alarm(self, (clock.interval_in_sim_minutes(5)),
          (lambda _: self.timer_expired()),
          repeating=True,
          repeating_time_span=(clock.interval_in_sim_minutes(5)))

    def on_deactivate(self):
        super().on_deactivate()
        if self._handle is not None:
            alarms.cancel_alarm(self._handle)

    def timer_expired(self):
        sims = list(self.owner.all_sims_in_situation_gen())
        for sim in sims:
            if self.owner.sim_has_job(sim, self.owner.leaving_soon.situation_job):
                self.owner._set_job_for_sim(sim, self.owner.leaving_now.situation_job)