# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\situations\special_npc_situations\ranger_greeting_situation.py
# Compiled at: 2016-10-21 01:42:24
# Size of source mod 2**32: 4473 bytes
from event_testing.test_events import TestEvent
from sims4.tuning.tunable import TunableReference
from situations.situation_complex import SituationComplexCommon, SituationState, SituationStateData
import services, sims4.resources, sims4.tuning.instances, situations.bouncer.bouncer_types, situations.situation

class RangerGreetingSituation(SituationComplexCommon):
    INSTANCE_TUNABLES = {'ranger_job':TunableReference(description='\n                The situation job that will be given to the ranger.\n                ',
       manager=services.situation_job_manager()), 
     'ranger_greet_lot_role_state':TunableReference(description='\n                The role state that will be given to the ranger npc on the\n                initial creation of the situation in order for the ranger to\n                go and greet the sims on the new household moving in.\n                ',
       manager=services.get_instance_manager(sims4.resources.Types.ROLE_STATE)), 
     'ranger_greet_lot_state_change_interaction':situations.situation_complex.TunableInteractionOfInterest(description='\n                The interaction that when run by the ranger npc will switch the\n                situation state to the wait around state.\n                '), 
     'ranger_wait_role_state':TunableReference(description='\n                The role state that will be given to the ranger npc after they\n                have completed their greet interaction.\n                ',
       manager=services.get_instance_manager(sims4.resources.Types.ROLE_STATE))}
    REMOVE_INSTANCE_TUNABLES = situations.situation.Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    @classmethod
    def _states(cls):
        return (SituationStateData(1, _RangerGreetLotSituationState),
         SituationStateData(2, _RangerWaitSituationState))

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls):
        return [(cls.ranger_job, cls.ranger_greet_lot_role_state)]

    @classmethod
    def default_job(cls):
        return cls.ranger_job

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    def start_situation(self):
        super().start_situation()
        self._change_state(_RangerGreetLotSituationState())

    @classmethod
    def get_sims_expected_to_be_in_situation(cls):
        return 1


sims4.tuning.instances.lock_instance_tunables(RangerGreetingSituation, exclusivity=(situations.bouncer.bouncer_types.BouncerExclusivityCategory.PRE_VISIT),
  creation_ui_option=(situations.situation_types.SituationCreationUIOption.NOT_AVAILABLE))

class _RangerGreetLotSituationState(SituationState):

    def on_activate(self, reader=None):
        super().on_activate(reader)
        for custom_key in self.owner.ranger_greet_lot_state_change_interaction.custom_keys_gen():
            self._test_event_register(TestEvent.InteractionComplete, custom_key)

        self.owner._set_job_role_state(self.owner.ranger_job, self.owner.ranger_greet_lot_role_state)

    def handle_event(self, sim_info, event, resolver):
        if event == TestEvent.InteractionComplete:
            if resolver(self.owner.ranger_greet_lot_state_change_interaction):
                self._change_state(_RangerWaitSituationState())


class _RangerWaitSituationState(SituationState):

    def on_activate(self, reader=None):
        super().on_activate(reader)
        self.owner._set_job_role_state(self.owner.ranger_job, self.owner.ranger_wait_role_state)