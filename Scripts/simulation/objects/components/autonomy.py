# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\components\autonomy.py
# Compiled at: 2016-09-08 20:44:53
# Size of source mod 2**32: 5426 bytes
from autonomy.settings import AutonomyRandomization
from sims4.tuning.tunable import TunableTuple, TunableSet, TunableReference, Tunable, OptionalTunable, TunableEnumEntry
import services

class TunableParameterizedAutonomy(TunableTuple, is_fragment=True):

    def __init__(self):
        super().__init__(commodities=TunableSet(TunableReference((services.statistic_manager()), description='The type of commodity to search for.'),
          description='List of commodities to run parameterized autonomy against after running this interaction.'),
          static_commodities=TunableSet(TunableReference((services.static_commodity_manager()), description='The type of static commodity to search for.'),
          description='List of static commodities to run parameterized autonomy against after running this interaction.'),
          same_target_only=Tunable(bool, False, description='If checked, only interactions on the same target as this interaction will be considered.'),
          retain_priority=Tunable(bool, True, description='If checked, this autonomy request is run at the same priority level as the interaction creating it.  If unchecked, the interaction chosen will run at low priority.'),
          consider_same_target=Tunable(bool, True, description='If checked, parameterized autonomy will consider interactions on the current Target.'),
          retain_carry_target=Tunable(bool, True, description="If checked, the interactions considered for autonomy will retain this interaction's carry target. It is useful to uncheck this if the desired autonomous interactions need not to consider carry, e.g. the Grim Reaper finding arbitrary interactions while in an interaction holding his scythe as a carry target."),
          randomization_override=OptionalTunable(description='\n                    If enabled then the parameterized autonomy will run with\n                    an overwritten autonomy randomization settings.\n                    ',
          tunable=TunableEnumEntry(description='\n                        The autonomy randomization setting that will be used.\n                        ',
          tunable_type=AutonomyRandomization,
          default=(AutonomyRandomization.UNDEFINED))),
          radius_to_consider=Tunable(description='\n                    The radius around the sim that targets must be in to be valid for Parameterized \n                    Autonomy.  Anything outside this radius will be ignored.  A radius of 0 is considered\n                    infinite.\n                    ',
          tunable_type=float,
          default=0),
          consider_scores_of_zero=Tunable(description='\n                    The autonomy request will consider scores of zero.  This allows sims to to choose things they \n                    might not desire.\n                    ',
          tunable_type=bool,
          default=False),
          test_connectivity_to_target=Tunable(description='\n                    If checked, this test will ensure the Sim can pass a pt to\n                    pt connectivity check to the advertising object.\n                    ',
          tunable_type=bool,
          default=True),
          retain_context_source=Tunable(description='\n                    If True, any interactions that run as a result of\n                    this request will run with the same context source as the creating\n                    interaction. If False, it will default to InteractionContext.SOURCE_AUTONOMY.\n                    ',
          tunable_type=bool,
          default=False),
          ignore_user_directed_and_autonomous=Tunable(description='\n                    If True, parametrized request will ignore autonomous and\n                    user directed checks.  This means, that the request may\n                    push a user directed or autonomous interaction without\n                    restriction.\n                    A use case for this is when a vampire runs pre run autonomy\n                    to enable its dark form, we want to keep the context as \n                    user directed (to keep the high priority of the\n                    interaction), but the interaction being run can normally\n                    not be user directed (since we dont want it on the pie\n                    menu). \n                    ',
          tunable_type=bool,
          default=False),
          description='Commodities and StaticCommodities will be combined, so interactions must support at least one commodity from both lists.')