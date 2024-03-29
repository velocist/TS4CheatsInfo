# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\household_interactions.py
# Compiled at: 2014-07-11 04:28:52
# Size of source mod 2**32: 3729 bytes
from interactions import ParticipantType
from sims4.tuning.tunable import TunableEnumEntry, OptionalTunable, TunableSet, TunableTuple
import event_testing.results, interactions.base.super_interaction, services, sims4.log, sims4.tuning, tag
logger = sims4.log.Logger('Interactions')

class PushInteractionOnAllGreetedSimsInteraction(interactions.base.super_interaction.SuperInteraction):
    INSTANCE_TUNABLES = {'_pushed_interaction_tunables':TunableTuple(affordance_to_push=sims4.tuning.tunable.TunableReference(description='\n                Affordance to push on all sims in the household and all greeted\n                sims.\n                ',
       manager=(services.affordance_manager())),
       push_on_actor=sims4.tuning.tunable.Tunable(description='\n               Whether Afforance To Push should be pushed on the actor.\n               ',
       tunable_type=bool,
       default=False),
       target_override_for_pushed_affordance=OptionalTunable(TunableEnumEntry(description='\n                ParticipantType for the target to be set on the pushed\n                affordance.\n                ',
       tunable_type=ParticipantType,
       default=(ParticipantType.Actor)))), 
     '_required_appropriateness_tags':TunableSet(description='\n            A list of tags that a Sim must have to be eligible for this\n            interaction.\n            ',
       tunable=TunableEnumEntry(tunable_type=(tag.Tag), default=(tag.Tag.INVALID)))}

    @classmethod
    def _test(cls, target, context, **interaction_parameters):
        sim = next(cls._target_sim_gen(context.sim), None)
        if sim is None:
            return event_testing.results.TestResult(False, 'No valid sims to call.')
        return (super()._test)(target, context, **interaction_parameters)

    def _run_interaction_gen(self, timeline):
        if self._pushed_interaction_tunables.target_override_for_pushed_affordance is not None:
            new_target = self.get_participant(self._pushed_interaction_tunables.target_override_for_pushed_affordance)
        else:
            new_target = self.target
        for target_sim in self._target_sim_gen(self.sim):
            target_context = self.context.clone_for_sim(target_sim)
            target_sim.push_super_affordance(self._pushed_interaction_tunables.affordance_to_push, new_target, target_context)

        return event_testing.results.ExecuteResult.NONE
        if False:
            yield None

    @classmethod
    def _target_sim_gen(cls, sim):
        for target_sim in services.sim_info_manager().instanced_sims_on_active_lot_gen():
            if target_sim.Buffs.is_appropriate(cls._required_appropriateness_tags):
                if not cls._pushed_interaction_tunables.push_on_actor:
                    if target_sim is sim:
                        continue
                yield target_sim