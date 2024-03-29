# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\situations\complex\worker_npc_situation.py
# Compiled at: 2020-08-11 17:54:48
# Size of source mod 2**32: 6662 bytes
from event_testing.test_events import TestEvent
from event_testing.tests_with_data import TunableParticipantRanInteractionTest
from sims4.tuning.tunable import OptionalTunable, TunableVariant, TunableSimMinute
from sims4.utils import classproperty
from situations.bouncer.bouncer_types import RequestSpawningOption, BouncerRequestPriority
from situations.situation import Situation
from situations.situation_complex import SituationComplexCommon, TunableSituationJobAndRoleState, SituationState, SituationStateData
from situations.situation_guest_list import SituationGuestList, SituationGuestInfo
import services, sims4.tuning, situations.bouncer

class WorkerNpcSituation(SituationComplexCommon):
    INSTANCE_TUNABLES = {'_worker_npc_job':TunableSituationJobAndRoleState(description='\n            The job and corresponding role state for the worker NPC.\n            '), 
     '_end_work_test':TunableParticipantRanInteractionTest(description='\n            When the worker NPC runs this interaction, the situation will end.\n            ',
       locked_args={'running_time':None, 
      'tooltip':None}), 
     '_visit_duration':OptionalTunable(description='\n            If enabled, then the worker NPC will enter a visit situation for the\n            specified duration.\n            ',
       tunable=TunableVariant(description="\n                The duration of the worker NPC's visit situation.\n                ",
       specific_duration=TunableSimMinute(default=60),
       locked_args={'default_duration':None, 
      'forever':0},
       default='default_duration'),
       disabled_value=False)}
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    @classmethod
    def _states(cls):
        return (SituationStateData(1, WorkingSituationState),)

    @classmethod
    def default_job(cls):
        return cls._worker_npc_job.job

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls):
        return ((cls._worker_npc_job.job, cls._worker_npc_job.role_state),)

    @classmethod
    def get_predefined_guest_list(cls):
        guest_list = SituationGuestList(True)
        worker_filter = cls.default_job().filter
        sim_infos = services.sim_filter_service().submit_filter(worker_filter, None, allow_yielding=False, gsi_source_fn=(cls.get_sim_filter_gsi_name))
        if sim_infos:
            guest_list.add_guest_info(SituationGuestInfo(sim_infos[0].sim_info.sim_id, cls.default_job(), RequestSpawningOption.DONT_CARE, BouncerRequestPriority.GAME_BREAKER))
        else:
            guest_list.add_guest_info(SituationGuestInfo(0, (cls.default_job()), (RequestSpawningOption.DONT_CARE), (BouncerRequestPriority.GAME_BREAKER), accept_alternate_sim=True))
        return guest_list

    def start_situation(self):
        super().start_situation()
        self._change_state(WorkingSituationState())

    def on_ask_sim_to_leave(self, sim):
        return False

    def _create_next_situation(self):
        worker_sim = next(self.all_sims_in_job_gen(self.default_job()), None)
        if worker_sim is not None:
            if worker_sim.is_on_active_lot():
                if self._visit_duration != False:
                    services.get_zone_situation_manager().create_visit_situation(worker_sim, duration_override=(self._visit_duration))
                    return
            services.get_zone_situation_manager().make_sim_leave(worker_sim)

    def _end_situation(self):
        self._create_next_situation()
        self._self_destruct()


sims4.tuning.instances.lock_instance_tunables(WorkerNpcSituation, exclusivity=(situations.bouncer.bouncer_types.BouncerExclusivityCategory.WORKER),
  creation_ui_option=(situations.situation_types.SituationCreationUIOption.NOT_AVAILABLE),
  _is_unique=True)

class WorkingSituationState(SituationState):

    def on_activate(self, *args, **kwargs):
        for _, custom_key in self.owner._end_work_test.get_custom_event_registration_keys():
            self._test_event_register(TestEvent.InteractionComplete, custom_key)

        return (super().on_activate)(*args, **kwargs)

    def handle_event(self, sim_info, event, resolver):
        if self.owner.test_interaction_complete_by_job_holder(sim_info, resolver, self.owner.default_job(), self.owner._end_work_test):
            self.owner._end_situation()