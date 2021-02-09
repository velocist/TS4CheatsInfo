# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\event_testing\resolver.py
# Compiled at: 2020-07-28 02:03:24
# Size of source mod 2**32: 61938 bytes
import itertools, random, sys, time
from event_testing.results import TestResult
from interactions import ParticipantType, ParticipantTypeSituationSims
from performance.test_profiling import TestProfileRecord, ProfileMetrics
from sims4.utils import classproperty
from singletons import DEFAULT
import caches, event_testing.test_constants, services, sims4.log, sims4.reload
logger = sims4.log.Logger('Resolver')
with sims4.reload.protected(globals()):
    RESOLVER_PARTICIPANT = 'resolver'
    test_profile = None
SINGLE_TYPES = frozenset((ParticipantType.Affordance,
 ParticipantType.InteractionContext,
 event_testing.test_constants.FROM_DATA_OBJECT,
 event_testing.test_constants.OBJECTIVE_GUID64,
 event_testing.test_constants.FROM_EVENT_DATA))

class Resolver:

    def __init__(self, skip_safe_tests=False, search_for_tooltip=False):
        self._skip_safe_tests = skip_safe_tests
        self._search_for_tooltip = search_for_tooltip

    @property
    def skip_safe_tests(self):
        return self._skip_safe_tests

    @property
    def search_for_tooltip(self):
        return self._search_for_tooltip

    @property
    def interaction(self):
        pass

    def get_resolved_args(self, expected):
        if expected is None:
            raise ValueError('Expected arguments from test instance get_expected_args are undefined: {}'.format(expected))
        ret = {}
        for event_key, participant_type in expected.items():
            if participant_type in SINGLE_TYPES:
                value = self.get_participant(participant_type, event_key=event_key)
            else:
                value = self.get_participants(participant_type, event_key=event_key)
            ret[event_key] = value

        return ret

    @property
    def profile_metric_key(self):
        pass

    def __call__(self, test):
        global test_profile
        if test.expected_kwargs is None:
            expected_args = test.get_expected_args()
            if expected_args:
                test.expected_kwargs = tuple(expected_args.items())
            else:
                test.expected_kwargs = ()
        if test_profile is not None:
            start_time = time.perf_counter()
        resolved_args = {}
        for event_key, participant_type in test.expected_kwargs:
            if participant_type in SINGLE_TYPES:
                value = self.get_participants(participant_type, event_key=event_key)
                resolved_args[event_key] = value[0] if value else None
            else:
                resolved_args[event_key] = self.get_participants(participant_type, event_key=event_key)

        if test_profile is not None:
            resolve_end_time = time.perf_counter()
        result = test(**resolved_args)
        if test_profile is not None:
            test_end_time = time.perf_counter()
            resolve_time = resolve_end_time - start_time
            test_time = test_end_time - resolve_end_time
            self._record_test_profile_metrics(test, resolve_time, test_time)
        return result

    def _record_test_profile_metrics(self, test, resolve_time, test_time):
        global test_profile
        try:
            from event_testing.tests import TestSetInstance
            from event_testing.test_based_score_threshold import TestBasedScoreThresholdTest
            is_test_set = isinstance(test, type) and issubclass(test, TestSetInstance)
            test_name = '[TS]{}'.format(test.__name__) if is_test_set else test.__class__.__name__
            if isinstance(test, TestBasedScoreThresholdTest):
                is_test_set = True
            record = test_profile.get(test_name)
            if record is None:
                record = TestProfileRecord(is_test_set=is_test_set)
                test_profile[test_name] = record
            record.metrics.update(resolve_time, test_time)
            resolver_name = type(self).__name__
            resolver_dict = record.resolvers.get(resolver_name)
            if resolver_dict is None:
                resolver_dict = dict()
                record.resolvers[resolver_name] = resolver_dict
            key_name = self.profile_metric_key
            if key_name is None:
                key_name = 'Key'
            metrics = resolver_dict.get(key_name)
            if metrics is None:
                metrics = ProfileMetrics(is_test_set=is_test_set)
                resolver_dict[key_name] = metrics
            metrics.update(resolve_time, test_time)
        except Exception as e:
            try:
                logger.exception('Resetting test_profile due to an exception {}.', e, owner='manus')
                test_profile = None
            finally:
                e = None
                del e

    def get_participant(self, participant_type, **kwargs):
        participants = (self.get_participants)(participant_type, **kwargs)
        if not participants:
            return
        if len(participants) > 1:
            raise ValueError('Too many participants returned for {}!'.format(participant_type))
        return next(iter(participants))

    def get_participants(self, participant_type, **kwargs):
        raise NotImplementedError('Attempting to use the Resolver base class, use sub-classes instead.')

    def _get_participants_base(self, participant_type, **kwargs):
        if participant_type == RESOLVER_PARTICIPANT:
            return self
        return Resolver.get_particpants_shared(participant_type)

    def get_target_id(self, test, id_type=None):
        expected_args = test.get_expected_args()
        resolved_args = self.get_resolved_args(expected_args)
        resolved_args['id_type'] = id_type
        return (test.get_target_id)(**resolved_args)

    def get_posture_id(self, test):
        expected_args = test.get_expected_args()
        resolved_args = self.get_resolved_args(expected_args)
        return (test.get_posture_id)(**resolved_args)

    def get_tags(self, test):
        expected_args = test.get_expected_args()
        resolved_args = self.get_resolved_args(expected_args)
        return (test.get_tags)(**resolved_args)

    def get_localization_tokens(self, *args, **kwargs):
        return ()

    @staticmethod
    def get_particpants_shared(participant_type):
        if participant_type == ParticipantType.Lot:
            return (
             services.active_lot(),)
        if participant_type == ParticipantType.LotOwners:
            owning_household = services.owning_household_of_active_lot()
            if owning_household is not None:
                return tuple((sim_info for sim_info in owning_household.sim_info_gen()))
            return ()
        if participant_type == ParticipantType.LotOwnersOrRenters:
            owning_household = services.owning_household_of_active_lot()
            if owning_household is not None:
                return tuple((sim_info for sim_info in owning_household.sim_info_gen()))
            current_zone = services.current_zone()
            travel_group = services.travel_group_manager().get_travel_group_by_zone_id(current_zone.id)
            if travel_group is not None:
                return tuple((sim_info for sim_info in travel_group.sim_info_gen()))
            return ()
        if participant_type == ParticipantType.LotOwnerSingleAndInstanced:
            owning_household = services.owning_household_of_active_lot()
            if owning_household is not None:
                for sim_info in owning_household.sim_info_gen():
                    if sim_info.is_instanced():
                        return (
                         sim_info,)

            return ()
        if participant_type == ParticipantType.ActiveHousehold:
            active_household = services.active_household()
            if active_household is not None:
                return tuple(active_household.sim_info_gen())
            return ()
        if participant_type == ParticipantType.AllInstancedActiveHouseholdSims:
            active_household = services.active_household()
            if active_household is not None:
                return tuple(active_household.instanced_sims_gen())
            return ()
        if participant_type == ParticipantType.CareerEventSim:
            career = services.get_career_service().get_career_in_career_event()
            if career is not None:
                return (
                 career.sim_info.get_sim_instance() or career.sim_info,)
            return ()
        if participant_type == ParticipantType.AllInstancedSims:
            return tuple(services.sim_info_manager().instanced_sims_gen())
        if participant_type == ParticipantType.Street:
            street = services.current_zone().street
            street_service = services.street_service()
            if street_service is None:
                return ()
            street_civic_policy_provider = street_service.get_provider(street)
            if street_civic_policy_provider is None:
                return ()
            return (
             street_civic_policy_provider,)
        if participant_type == ParticipantType.VenuePolicyProvider:
            venue_service = services.venue_service()
            if venue_service.source_venue is None or venue_service.source_venue.civic_policy_provider is None:
                return ()
            return (
             venue_service.source_venue.civic_policy_provider,)
        if participant_type == ParticipantType.CurrentRegion:
            region_inst = services.current_region_instance()
            if region_inst is None:
                return ()
            return (
             region_inst,)


class GlobalResolver(Resolver):

    def get_participants(self, participant_type, **kwargs):
        result = (self._get_participants_base)(participant_type, **kwargs)
        if result is not None:
            return result
        if participant_type == event_testing.test_constants.FROM_EVENT_DATA:
            return ()
        logger.error('GlobalResolver unable to resolve {}', participant_type)
        return ()


class AffordanceResolver(Resolver):

    def __init__(self, affordance, actor):
        super().__init__(skip_safe_tests=False, search_for_tooltip=False)
        self.affordance = affordance
        self.actor = actor

    def __repr__(self):
        return 'AffordanceResolver: affordance: {}, actor {}'.format(self.affordance, self.actor)

    def get_participants(self, participant_type, **kwargs):
        if participant_type == event_testing.test_constants.FROM_DATA_OBJECT:
            return ()
        if participant_type == event_testing.test_constants.OBJECTIVE_GUID64:
            return ()
        if participant_type == event_testing.test_constants.FROM_EVENT_DATA:
            return ()
        if participant_type == event_testing.test_constants.SIM_INSTANCE or participant_type == ParticipantType.Actor:
            if self.actor is not None:
                result = _to_sim_info(self.actor)
                if result:
                    return (
                     result,)
            return ()
        if participant_type == 0:
            logger.error('Calling get_participants with no flags on {}.', self)
            return ()
        if participant_type == ParticipantType.Affordance:
            return (
             self.affordance,)
        if participant_type == ParticipantType.AllRelationships:
            return (
             ParticipantType.AllRelationships,)
        return (self._get_participants_base)(participant_type, **kwargs)

    def __call__(self, test):
        if not test.supports_early_testing():
            return True
        if test.participants_for_early_testing is None:
            test.participants_for_early_testing = tuple(test.get_expected_args().values())
        for participant in test.participants_for_early_testing:
            if self.get_participants(participant) is None:
                return TestResult.TRUE

        return super().__call__(test)


class InteractionResolver(Resolver):

    def __init__(self, affordance, interaction, target=DEFAULT, context=DEFAULT, custom_sim=None, super_interaction=None, skip_safe_tests=False, search_for_tooltip=False, **interaction_parameters):
        super().__init__(skip_safe_tests, search_for_tooltip)
        self.affordance = affordance
        self._interaction = interaction
        self.target = interaction.target if target is DEFAULT else target
        self.context = interaction.context if context is DEFAULT else context
        self.custom_sim = custom_sim
        self.super_interaction = super_interaction
        self.interaction_parameters = interaction_parameters

    def __repr__(self):
        return 'InteractionResolver: affordance: {}, interaction:{}, target: {}, context: {}, si: {}'.format(self.affordance, self.interaction, self.target, self.context, self.super_interaction)

    @property
    def interaction(self):
        return self._interaction

    @property
    def profile_metric_key(self):
        if self.affordance is None:
            return 'NoAffordance'
        return self.affordance.__name__

    def get_participants--- This code section failed: ---

 L. 433         0  LOAD_FAST                'participant_type'
                2  LOAD_GLOBAL              event_testing
                4  LOAD_ATTR                test_constants
                6  LOAD_ATTR                SIM_INSTANCE
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    18  'to 18'

 L. 434        12  LOAD_GLOBAL              ParticipantType
               14  LOAD_ATTR                Actor
               16  STORE_FAST               'participant_type'
             18_0  COME_FROM            10  '10'

 L. 437        18  LOAD_FAST                'participant_type'
               20  LOAD_GLOBAL              ParticipantType
               22  LOAD_ATTR                Actor
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    74  'to 74'

 L. 438        28  LOAD_FAST                'self'
               30  LOAD_ATTR                context
               32  LOAD_ATTR                sim
               34  STORE_FAST               'sim'

 L. 443        36  LOAD_FAST                'sim'
               38  LOAD_CONST               None
               40  COMPARE_OP               is-not
               42  POP_JUMP_IF_FALSE    70  'to 70'

 L. 444        44  LOAD_GLOBAL              _to_sim_info
               46  LOAD_FAST                'sim'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'result'

 L. 445        52  LOAD_FAST                'result'
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 446        60  LOAD_FAST                'result'
               62  BUILD_TUPLE_1         1 
               64  RETURN_VALUE     
             66_0  COME_FROM            58  '58'

 L. 447        66  LOAD_CONST               ()
               68  RETURN_VALUE     
             70_0  COME_FROM            42  '42'
            70_72  JUMP_FORWARD        672  'to 672'
             74_0  COME_FROM            26  '26'

 L. 448        74  LOAD_FAST                'participant_type'
               76  LOAD_GLOBAL              ParticipantType
               78  LOAD_ATTR                Object
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   122  'to 122'

 L. 449        84  LOAD_FAST                'self'
               86  LOAD_ATTR                target
               88  LOAD_CONST               None
               90  COMPARE_OP               is-not
               92  POP_JUMP_IF_FALSE   118  'to 118'

 L. 450        94  LOAD_GLOBAL              _to_sim_info
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                target
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  STORE_FAST               'result'

 L. 451       104  LOAD_FAST                'result'
              106  LOAD_CONST               None
              108  COMPARE_OP               is-not
              110  POP_JUMP_IF_FALSE   118  'to 118'

 L. 452       112  LOAD_FAST                'result'
              114  BUILD_TUPLE_1         1 
              116  RETURN_VALUE     
            118_0  COME_FROM           110  '110'
            118_1  COME_FROM            92  '92'

 L. 453       118  LOAD_CONST               ()
              120  RETURN_VALUE     
            122_0  COME_FROM            82  '82'

 L. 454       122  LOAD_FAST                'participant_type'
              124  LOAD_GLOBAL              ParticipantType
              126  LOAD_ATTR                ObjectIngredients
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   184  'to 184'

 L. 455       132  LOAD_FAST                'self'
              134  LOAD_ATTR                target
              136  LOAD_CONST               None
              138  COMPARE_OP               is-not
              140  POP_JUMP_IF_FALSE   180  'to 180'

 L. 456       142  LOAD_FAST                'self'
              144  LOAD_ATTR                target
              146  LOAD_ATTR                crafting_component
              148  POP_JUMP_IF_FALSE   180  'to 180'

 L. 457       150  LOAD_FAST                'self'
              152  LOAD_ATTR                target
              154  LOAD_METHOD              get_crafting_process
              156  CALL_METHOD_0         0  '0 positional arguments'
              158  STORE_FAST               'target_crafting_process'

 L. 458       160  LOAD_FAST                'target_crafting_process'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   180  'to 180'

 L. 459       168  LOAD_GLOBAL              tuple
              170  LOAD_FAST                'target_crafting_process'
              172  LOAD_METHOD              get_ingredients_object_definitions
              174  CALL_METHOD_0         0  '0 positional arguments'
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  RETURN_VALUE     
            180_0  COME_FROM           166  '166'
            180_1  COME_FROM           148  '148'
            180_2  COME_FROM           140  '140'

 L. 460       180  LOAD_CONST               ()
              182  RETURN_VALUE     
            184_0  COME_FROM           130  '130'

 L. 461       184  LOAD_FAST                'participant_type'
              186  LOAD_GLOBAL              ParticipantType
              188  LOAD_ATTR                TargetSim
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   240  'to 240'

 L. 462       194  LOAD_FAST                'self'
              196  LOAD_ATTR                target
              198  LOAD_CONST               None
              200  COMPARE_OP               is-not
              202  POP_JUMP_IF_FALSE   236  'to 236'
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                target
              208  LOAD_ATTR                is_sim
              210  POP_JUMP_IF_FALSE   236  'to 236'

 L. 463       212  LOAD_GLOBAL              _to_sim_info
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                target
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  STORE_FAST               'result'

 L. 464       222  LOAD_FAST                'result'
              224  LOAD_CONST               None
              226  COMPARE_OP               is-not
              228  POP_JUMP_IF_FALSE   236  'to 236'

 L. 465       230  LOAD_FAST                'result'
              232  BUILD_TUPLE_1         1 
              234  RETURN_VALUE     
            236_0  COME_FROM           228  '228'
            236_1  COME_FROM           210  '210'
            236_2  COME_FROM           202  '202'

 L. 466       236  LOAD_CONST               ()
              238  RETURN_VALUE     
            240_0  COME_FROM           192  '192'

 L. 467       240  LOAD_FAST                'participant_type'
              242  LOAD_GLOBAL              ParticipantType
              244  LOAD_ATTR                ActorPostureTarget
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   308  'to 308'

 L. 468       252  LOAD_FAST                'self'
              254  LOAD_ATTR                interaction
              256  LOAD_CONST               None
              258  COMPARE_OP               is-not
          260_262  POP_JUMP_IF_FALSE   278  'to 278'

 L. 469       264  LOAD_FAST                'self'
              266  LOAD_ATTR                interaction
              268  LOAD_ATTR                get_participants
              270  LOAD_FAST                'participant_type'
              272  LOAD_CONST               ('participant_type',)
              274  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              276  RETURN_VALUE     
            278_0  COME_FROM           260  '260'

 L. 470       278  LOAD_FAST                'self'
              280  LOAD_ATTR                super_interaction
              282  LOAD_CONST               None
              284  COMPARE_OP               is-not
          286_288  POP_JUMP_IF_FALSE   672  'to 672'

 L. 471       290  LOAD_FAST                'self'
              292  LOAD_ATTR                super_interaction
              294  LOAD_ATTR                get_participants
              296  LOAD_FAST                'participant_type'
              298  LOAD_CONST               ('participant_type',)
              300  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              302  RETURN_VALUE     
          304_306  JUMP_FORWARD        672  'to 672'
            308_0  COME_FROM           248  '248'

 L. 472       308  LOAD_FAST                'participant_type'
              310  LOAD_GLOBAL              ParticipantType
              312  LOAD_ATTR                AssociatedClub
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_TRUE    344  'to 344'

 L. 473       320  LOAD_FAST                'participant_type'
              322  LOAD_GLOBAL              ParticipantType
              324  LOAD_ATTR                AssociatedClubLeader
              326  COMPARE_OP               ==
          328_330  POP_JUMP_IF_TRUE    344  'to 344'

 L. 474       332  LOAD_FAST                'participant_type'
              334  LOAD_GLOBAL              ParticipantType
              336  LOAD_ATTR                AssociatedClubMembers
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   452  'to 452'
            344_0  COME_FROM           328  '328'
            344_1  COME_FROM           316  '316'

 L. 475       344  LOAD_FAST                'self'
              346  LOAD_ATTR                interaction_parameters
              348  LOAD_METHOD              get
              350  LOAD_STR                 'associated_club'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  STORE_FAST               'associated_club'

 L. 476       356  LOAD_FAST                'self'
              358  LOAD_ATTR                interaction
              360  LOAD_CONST               None
              362  COMPARE_OP               is
          364_366  POP_JUMP_IF_FALSE   380  'to 380'
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                super_interaction
              372  LOAD_CONST               None
              374  COMPARE_OP               is
          376_378  POP_JUMP_IF_TRUE    390  'to 390'
            380_0  COME_FROM           364  '364'

 L. 477       380  LOAD_FAST                'associated_club'
              382  LOAD_CONST               None
              384  COMPARE_OP               is-not
          386_388  POP_JUMP_IF_FALSE   672  'to 672'
            390_0  COME_FROM           376  '376'

 L. 478       390  LOAD_FAST                'participant_type'
              392  LOAD_GLOBAL              ParticipantType
              394  LOAD_ATTR                AssociatedClubLeader
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   410  'to 410'

 L. 479       402  LOAD_FAST                'associated_club'
              404  LOAD_ATTR                leader
              406  BUILD_TUPLE_1         1 
              408  RETURN_VALUE     
            410_0  COME_FROM           398  '398'

 L. 480       410  LOAD_FAST                'participant_type'
              412  LOAD_GLOBAL              ParticipantType
              414  LOAD_ATTR                AssociatedClub
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   428  'to 428'

 L. 481       422  LOAD_FAST                'associated_club'
              424  BUILD_TUPLE_1         1 
              426  RETURN_VALUE     
            428_0  COME_FROM           418  '418'

 L. 482       428  LOAD_FAST                'participant_type'
              430  LOAD_GLOBAL              ParticipantType
              432  LOAD_ATTR                AssociatedClubMembers
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   672  'to 672'

 L. 483       440  LOAD_GLOBAL              tuple
              442  LOAD_FAST                'associated_club'
              444  LOAD_ATTR                members
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  RETURN_VALUE     
              450  JUMP_FORWARD        672  'to 672'
            452_0  COME_FROM           340  '340'

 L. 484       452  LOAD_FAST                'participant_type'
              454  LOAD_GLOBAL              ParticipantType
              456  LOAD_ATTR                ObjectCrafter
              458  COMPARE_OP               ==
          460_462  POP_JUMP_IF_FALSE   546  'to 546'

 L. 485       464  LOAD_FAST                'self'
              466  LOAD_ATTR                target
              468  LOAD_CONST               None
              470  COMPARE_OP               is
          472_474  POP_JUMP_IF_TRUE    490  'to 490'
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                target
              480  LOAD_ATTR                crafting_component
              482  LOAD_CONST               None
              484  COMPARE_OP               is
          486_488  POP_JUMP_IF_FALSE   494  'to 494'
            490_0  COME_FROM           472  '472'

 L. 486       490  LOAD_CONST               ()
              492  RETURN_VALUE     
            494_0  COME_FROM           486  '486'

 L. 487       494  LOAD_FAST                'self'
              496  LOAD_ATTR                target
              498  LOAD_METHOD              get_crafting_process
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  STORE_FAST               'crafting_process'

 L. 488       504  LOAD_FAST                'crafting_process'
              506  LOAD_CONST               None
              508  COMPARE_OP               is
          510_512  POP_JUMP_IF_FALSE   518  'to 518'

 L. 489       514  LOAD_CONST               ()
              516  RETURN_VALUE     
            518_0  COME_FROM           510  '510'

 L. 490       518  LOAD_FAST                'crafting_process'
              520  LOAD_METHOD              get_crafter_sim_info
              522  CALL_METHOD_0         0  '0 positional arguments'
              524  STORE_FAST               'crafter_sim_info'

 L. 491       526  LOAD_FAST                'crafter_sim_info'
              528  LOAD_CONST               None
              530  COMPARE_OP               is
          532_534  POP_JUMP_IF_FALSE   540  'to 540'

 L. 492       536  LOAD_CONST               ()
              538  RETURN_VALUE     
            540_0  COME_FROM           532  '532'

 L. 493       540  LOAD_FAST                'crafter_sim_info'
              542  BUILD_TUPLE_1         1 
              544  RETURN_VALUE     
            546_0  COME_FROM           460  '460'

 L. 494       546  LOAD_FAST                'participant_type'
              548  LOAD_GLOBAL              ParticipantTypeSituationSims
              550  COMPARE_OP               in
          552_554  POP_JUMP_IF_FALSE   672  'to 672'

 L. 495       556  LOAD_CONST               None
              558  STORE_FAST               'provider_source'

 L. 496       560  LOAD_FAST                'self'
              562  LOAD_ATTR                _interaction
              564  LOAD_CONST               None
              566  COMPARE_OP               is-not
          568_570  POP_JUMP_IF_FALSE   580  'to 580'

 L. 497       572  LOAD_FAST                'self'
              574  LOAD_ATTR                _interaction
              576  STORE_FAST               'provider_source'
              578  JUMP_FORWARD        618  'to 618'
            580_0  COME_FROM           568  '568'

 L. 498       580  LOAD_FAST                'self'
              582  LOAD_ATTR                super_interaction
              584  LOAD_CONST               None
              586  COMPARE_OP               is-not
          588_590  POP_JUMP_IF_FALSE   600  'to 600'

 L. 499       592  LOAD_FAST                'self'
              594  LOAD_ATTR                super_interaction
              596  STORE_FAST               'provider_source'
              598  JUMP_FORWARD        618  'to 618'
            600_0  COME_FROM           588  '588'

 L. 500       600  LOAD_FAST                'self'
              602  LOAD_ATTR                affordance
              604  LOAD_CONST               None
              606  COMPARE_OP               is-not
          608_610  POP_JUMP_IF_FALSE   618  'to 618'

 L. 501       612  LOAD_FAST                'self'
              614  LOAD_ATTR                affordance
              616  STORE_FAST               'provider_source'
            618_0  COME_FROM           608  '608'
            618_1  COME_FROM           598  '598'
            618_2  COME_FROM           578  '578'

 L. 503       618  LOAD_FAST                'provider_source'
              620  LOAD_CONST               None
              622  COMPARE_OP               is-not
          624_626  POP_JUMP_IF_FALSE   672  'to 672'

 L. 504       628  LOAD_FAST                'provider_source'
              630  LOAD_METHOD              get_situation_participant_provider
              632  CALL_METHOD_0         0  '0 positional arguments'
              634  STORE_FAST               'provider'

 L. 505       636  LOAD_FAST                'provider'
              638  LOAD_CONST               None
              640  COMPARE_OP               is-not
          642_644  POP_JUMP_IF_FALSE   658  'to 658'

 L. 506       646  LOAD_FAST                'provider'
              648  LOAD_METHOD              get_participants
              650  LOAD_FAST                'participant_type'
              652  LOAD_FAST                'self'
              654  CALL_METHOD_2         2  '2 positional arguments'
              656  RETURN_VALUE     
            658_0  COME_FROM           642  '642'

 L. 508       658  LOAD_GLOBAL              logger
              660  LOAD_METHOD              error
              662  LOAD_STR                 "Requesting {} in {} that doesn't have a SituationSimParticipantProviderLiability"
              664  LOAD_FAST                'participant_type'
              666  LOAD_FAST                'provider_source'
              668  CALL_METHOD_3         3  '3 positional arguments'
              670  POP_TOP          
            672_0  COME_FROM           624  '624'
            672_1  COME_FROM           552  '552'
            672_2  COME_FROM           450  '450'
            672_3  COME_FROM           436  '436'
            672_4  COME_FROM           386  '386'
            672_5  COME_FROM           304  '304'
            672_6  COME_FROM           286  '286'
            672_7  COME_FROM            70  '70'

 L. 510       672  LOAD_FAST                'participant_type'
              674  LOAD_CONST               0
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   698  'to 698'

 L. 511       682  LOAD_GLOBAL              logger
              684  LOAD_METHOD              error
              686  LOAD_STR                 'Calling get_participants with no flags on {}.'
              688  LOAD_FAST                'self'
              690  CALL_METHOD_2         2  '2 positional arguments'
              692  POP_TOP          

 L. 512       694  LOAD_CONST               ()
              696  RETURN_VALUE     
            698_0  COME_FROM           678  '678'

 L. 513       698  LOAD_FAST                'self'
              700  LOAD_ATTR                _get_participants_base
              702  LOAD_FAST                'participant_type'
              704  BUILD_TUPLE_1         1 
              706  LOAD_FAST                'kwargs'
              708  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              710  STORE_FAST               'result'

 L. 514       712  LOAD_FAST                'result'
              714  LOAD_CONST               None
              716  COMPARE_OP               is-not
          718_720  POP_JUMP_IF_FALSE   726  'to 726'

 L. 515       722  LOAD_FAST                'result'
              724  RETURN_VALUE     
            726_0  COME_FROM           718  '718'

 L. 520       726  LOAD_FAST                'participant_type'
              728  LOAD_GLOBAL              event_testing
              730  LOAD_ATTR                test_constants
              732  LOAD_ATTR                FROM_DATA_OBJECT
              734  COMPARE_OP               ==
          736_738  POP_JUMP_IF_FALSE   744  'to 744'

 L. 521       740  LOAD_CONST               ()
              742  RETURN_VALUE     
            744_0  COME_FROM           736  '736'

 L. 522       744  LOAD_FAST                'participant_type'
              746  LOAD_GLOBAL              event_testing
              748  LOAD_ATTR                test_constants
              750  LOAD_ATTR                OBJECTIVE_GUID64
              752  COMPARE_OP               ==
          754_756  POP_JUMP_IF_FALSE   762  'to 762'

 L. 523       758  LOAD_CONST               ()
              760  RETURN_VALUE     
            762_0  COME_FROM           754  '754'

 L. 524       762  LOAD_FAST                'participant_type'
              764  LOAD_GLOBAL              event_testing
              766  LOAD_ATTR                test_constants
              768  LOAD_ATTR                FROM_EVENT_DATA
              770  COMPARE_OP               ==
          772_774  POP_JUMP_IF_FALSE   780  'to 780'

 L. 525       776  LOAD_CONST               ()
              778  RETURN_VALUE     
            780_0  COME_FROM           772  '772'

 L. 527       780  LOAD_FAST                'participant_type'
              782  LOAD_GLOBAL              ParticipantType
              784  LOAD_ATTR                Affordance
              786  COMPARE_OP               ==
          788_790  POP_JUMP_IF_FALSE   800  'to 800'

 L. 528       792  LOAD_FAST                'self'
              794  LOAD_ATTR                affordance
              796  BUILD_TUPLE_1         1 
              798  RETURN_VALUE     
            800_0  COME_FROM           788  '788'

 L. 529       800  LOAD_FAST                'participant_type'
              802  LOAD_GLOBAL              ParticipantType
              804  LOAD_ATTR                InteractionContext
              806  COMPARE_OP               ==
          808_810  POP_JUMP_IF_FALSE   820  'to 820'

 L. 530       812  LOAD_FAST                'self'
              814  LOAD_ATTR                context
              816  BUILD_TUPLE_1         1 
              818  RETURN_VALUE     
            820_0  COME_FROM           808  '808'

 L. 531       820  LOAD_FAST                'participant_type'
              822  LOAD_GLOBAL              ParticipantType
              824  LOAD_ATTR                CustomSim
              826  COMPARE_OP               ==
          828_830  POP_JUMP_IF_FALSE   864  'to 864'

 L. 532       832  LOAD_FAST                'self'
              834  LOAD_ATTR                custom_sim
              836  LOAD_CONST               None
              838  COMPARE_OP               is-not
          840_842  POP_JUMP_IF_FALSE   854  'to 854'

 L. 533       844  LOAD_FAST                'self'
              846  LOAD_ATTR                custom_sim
              848  LOAD_ATTR                sim_info
              850  BUILD_TUPLE_1         1 
              852  RETURN_VALUE     
            854_0  COME_FROM           840  '840'

 L. 535       854  LOAD_GLOBAL              ValueError
              856  LOAD_STR                 'Trying to use CustomSim without passing a custom_sim in InteractionResolver.'
              858  CALL_FUNCTION_1       1  '1 positional argument'
              860  POP_TOP          
              862  JUMP_FORWARD        884  'to 884'
            864_0  COME_FROM           828  '828'

 L. 536       864  LOAD_FAST                'participant_type'
              866  LOAD_GLOBAL              ParticipantType
              868  LOAD_ATTR                AllRelationships
              870  COMPARE_OP               ==
          872_874  POP_JUMP_IF_FALSE   884  'to 884'

 L. 540       876  LOAD_GLOBAL              ParticipantType
              878  LOAD_ATTR                AllRelationships
              880  BUILD_TUPLE_1         1 
              882  RETURN_VALUE     
            884_0  COME_FROM           872  '872'
            884_1  COME_FROM           862  '862'

 L. 542       884  LOAD_FAST                'participant_type'
              886  LOAD_GLOBAL              ParticipantType
              888  LOAD_ATTR                PickedItemId
              890  COMPARE_OP               ==
          892_894  POP_JUMP_IF_FALSE   922  'to 922'

 L. 543       896  LOAD_FAST                'self'
              898  LOAD_ATTR                interaction_parameters
              900  LOAD_METHOD              get
              902  LOAD_STR                 'picked_item_ids'
              904  CALL_METHOD_1         1  '1 positional argument'
              906  STORE_FAST               'picked_item_ids'

 L. 544       908  LOAD_FAST                'picked_item_ids'
              910  LOAD_CONST               None
              912  COMPARE_OP               is-not
          914_916  POP_JUMP_IF_FALSE   922  'to 922'

 L. 545       918  LOAD_FAST                'picked_item_ids'
              920  RETURN_VALUE     
            922_0  COME_FROM           914  '914'
            922_1  COME_FROM           892  '892'

 L. 548       922  LOAD_FAST                'self'
              924  LOAD_ATTR                interaction
              926  LOAD_CONST               None
              928  COMPARE_OP               is-not
          930_932  POP_JUMP_IF_FALSE   972  'to 972'

 L. 549       934  LOAD_FAST                'self'
              936  LOAD_ATTR                interaction
              938  LOAD_ATTR                get_participants
              940  BUILD_TUPLE_0         0 
              942  LOAD_FAST                'participant_type'

 L. 550       944  LOAD_FAST                'self'
              946  LOAD_ATTR                context
              948  LOAD_ATTR                sim
              950  LOAD_FAST                'self'
              952  LOAD_ATTR                target

 L. 551       954  LOAD_CONST               False
              956  LOAD_CONST               ('participant_type', 'sim', 'target', 'listener_filtering_enabled')
              958  BUILD_CONST_KEY_MAP_4     4 

 L. 552       960  LOAD_FAST                'self'
              962  LOAD_ATTR                interaction_parameters
              964  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              966  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              968  STORE_FAST               'participants'
              970  JUMP_FORWARD       1076  'to 1076'
            972_0  COME_FROM           930  '930'

 L. 553       972  LOAD_FAST                'self'
              974  LOAD_ATTR                super_interaction
              976  LOAD_CONST               None
              978  COMPARE_OP               is-not
          980_982  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 559       984  LOAD_FAST                'self'
              986  LOAD_ATTR                super_interaction
              988  LOAD_ATTR                get_participants
              990  BUILD_TUPLE_0         0 
              992  LOAD_FAST                'participant_type'

 L. 560       994  LOAD_FAST                'self'
              996  LOAD_ATTR                context
              998  LOAD_ATTR                sim
             1000  LOAD_FAST                'self'
             1002  LOAD_ATTR                target

 L. 561      1004  LOAD_CONST               False

 L. 562      1006  LOAD_FAST                'self'
             1008  LOAD_ATTR                affordance
             1010  LOAD_ATTR                target_type
             1012  LOAD_CONST               ('participant_type', 'sim', 'target', 'listener_filtering_enabled', 'target_type')
             1014  BUILD_CONST_KEY_MAP_5     5 

 L. 563      1016  LOAD_FAST                'self'
             1018  LOAD_ATTR                interaction_parameters
             1020  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1022  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1024  STORE_FAST               'participants'
             1026  JUMP_FORWARD       1076  'to 1076'
           1028_0  COME_FROM           980  '980'

 L. 565      1028  LOAD_FAST                'self'
             1030  LOAD_ATTR                affordance
             1032  LOAD_ATTR                get_participants
             1034  BUILD_TUPLE_0         0 
             1036  LOAD_FAST                'participant_type'

 L. 566      1038  LOAD_FAST                'self'
             1040  LOAD_ATTR                context
             1042  LOAD_ATTR                sim
             1044  LOAD_FAST                'self'
             1046  LOAD_ATTR                target

 L. 567      1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                context
             1052  LOAD_ATTR                carry_target

 L. 568      1054  LOAD_CONST               False

 L. 569      1056  LOAD_FAST                'self'
             1058  LOAD_ATTR                affordance
             1060  LOAD_ATTR                target_type
             1062  LOAD_CONST               ('participant_type', 'sim', 'target', 'carry_target', 'listener_filtering_enabled', 'target_type')
             1064  BUILD_CONST_KEY_MAP_6     6 

 L. 570      1066  LOAD_FAST                'self'
             1068  LOAD_ATTR                interaction_parameters
             1070  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1072  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1074  STORE_FAST               'participants'
           1076_0  COME_FROM          1026  '1026'
           1076_1  COME_FROM           970  '970'

 L. 571      1076  LOAD_GLOBAL              set
             1078  CALL_FUNCTION_0       0  '0 positional arguments'
             1080  STORE_FAST               'resolved_participants'

 L. 572      1082  SETUP_LOOP         1112  'to 1112'
             1084  LOAD_FAST                'participants'
             1086  GET_ITER         
             1088  FOR_ITER           1110  'to 1110'
             1090  STORE_FAST               'participant'

 L. 573      1092  LOAD_FAST                'resolved_participants'
             1094  LOAD_METHOD              add
             1096  LOAD_GLOBAL              _to_sim_info
             1098  LOAD_FAST                'participant'
             1100  CALL_FUNCTION_1       1  '1 positional argument'
             1102  CALL_METHOD_1         1  '1 positional argument'
             1104  POP_TOP          
         1106_1108  JUMP_BACK          1088  'to 1088'
             1110  POP_BLOCK        
           1112_0  COME_FROM_LOOP     1082  '1082'

 L. 575      1112  LOAD_GLOBAL              tuple
             1114  LOAD_FAST                'resolved_participants'
             1116  CALL_FUNCTION_1       1  '1 positional argument'
             1118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 1118

    def get_localization_tokens(self, *args, **kwargs):
        return (self.interaction.get_localization_tokens)(*args, **kwargs)


@caches.clearable_barebones_cache
def _to_sim_info(participant):
    sim_info = getattr(participant, 'sim_info', None)
    if sim_info is None or sim_info.is_baby:
        return participant
    return sim_info


class AwayActionResolver(Resolver):
    VALID_AWAY_ACTION_PARTICIPANTS = ParticipantType.Actor | ParticipantType.TargetSim | ParticipantType.Lot

    def __init__(self, away_action, skip_safe_tests=False, search_for_tooltip=False, **away_action_parameters):
        super().__init__(skip_safe_tests, search_for_tooltip)
        self.away_action = away_action
        self.away_action_parameters = away_action_parameters

    def __repr__(self):
        return 'AwayActionResolver: away_action: {}'.format(self.away_action)

    @property
    def sim(self):
        return self.get_participant(ParticipantType.Actor)

    def get_participants(self, participant_type, **kwargs):
        if participant_type == 0:
            logger.error('Calling get_participants with no flags on {}.', self)
            return ()
        if participant_type == ParticipantType.Lot:
            return (self.away_action.get_participants)(participant_type=participant_type, **self.away_action_parameters)
        result = self._get_participants_base(participant_type)
        if result is not None:
            return result
        if participant_type == event_testing.test_constants.FROM_DATA_OBJECT:
            return ()
        if participant_type == event_testing.test_constants.OBJECTIVE_GUID64:
            return ()
        if participant_type == event_testing.test_constants.FROM_EVENT_DATA:
            return ()
        if participant_type & AwayActionResolver.VALID_AWAY_ACTION_PARTICIPANTS:
            return (self.away_action.get_participants)(participant_type=participant_type, **self.away_action_parameters)
        raise ValueError('Trying to use AwayActionResolver without a valid type: {}'.format(participant_type))

    def get_localization_tokens(self, *args, **kwargs):
        return (self.interaction.get_localization_tokens)(*args, **kwargs)


class SingleSimResolver(Resolver):

    def __init__(self, sim_info_to_test, additional_participants={}, additional_localization_tokens=(), additional_metric_key_data=None):
        super().__init__()
        self.sim_info_to_test = sim_info_to_test
        self._additional_participants = additional_participants
        self._additional_localization_tokens = additional_localization_tokens
        self._source = None
        if event_testing.resolver.test_profile is not None:
            frame = sys._getframe(self.profile_metric_stack_depth)
            qualified_name = frame.f_code.co_filename
            unqualified_name = qualified_name.split('\\')[(-1)]
            self._source = unqualified_name
            if additional_metric_key_data is not None:
                self._source = '{}:{}'.format(self._source, additional_metric_key_data)

    def __repr__(self):
        return 'SingleSimResolver: sim_to_test: {}'.format(self.sim_info_to_test)

    @property
    def profile_metric_key(self):
        return 'source:{}'.format(self._source)

    @classproperty
    def profile_metric_stack_depth(cls):
        return 1

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.Actor or participant_type == ParticipantType.CustomSim:
            return (
             self.sim_info_to_test,)
        if participant_type == ParticipantType.SignificantOtherActor:
            significant_other = self.sim_info_to_test.get_significant_other_sim_info()
            if significant_other is not None:
                return (significant_other,)
            return ()
        if participant_type == ParticipantType.PregnancyPartnerActor:
            pregnancy_partner = self.sim_info_to_test.pregnancy_tracker.get_partner()
            if pregnancy_partner is not None:
                return (pregnancy_partner,)
            return ()
        if participant_type == ParticipantType.AllRelationships:
            return ParticipantType.AllRelationships
        if participant_type == ParticipantType.ActorFeudTarget:
            feud_target = self.sim_info_to_test.get_feud_target()
            if feud_target is not None:
                return (feud_target,)
            return ()
        if participant_type == event_testing.test_constants.FROM_EVENT_DATA:
            return ()
        if participant_type == ParticipantType.InteractionContext or participant_type == ParticipantType.Affordance:
            return ()
        if participant_type == event_testing.test_constants.SIM_INSTANCE:
            return (
             self.sim_info_to_test,)
        if participant_type == ParticipantType.Familiar:
            return self._get_familiar_for_sim_info(self.sim_info_to_test)
        if participant_type in self._additional_participants:
            return self._additional_participants[participant_type]
        if participant_type == ParticipantType.PickedZoneId:
            return frozenset()
        if participant_type == ParticipantType.ActorLot:
            sim_home_lot = self.sim_info_to_test.get_home_lot()
            if sim_home_lot is None:
                return ()
            return (sim_home_lot,)
        if participant_type == ParticipantType.RoutingSlaves:
            sim_inst = self.sim_info_to_test.get_sim_instance()
            routing_slave_data = sim_inst.get_routing_slave_data() if sim_inst is not None else None
            if routing_slave_data is None:
                return ()
            return tuple({data.slave for data in routing_slave_data})
        if participant_type == ParticipantType.StoredCASPartsOnObject:
            return ()
        result = (self._get_participants_base)(participant_type, **kwargs)
        if result is not None:
            return result
        raise ValueError('Trying to use {} with unsupported participant: {}'.format(type(self).__name__, participant_type))

    def _get_familiar_for_sim_info(self, sim_info):
        familiar_tracker = self.sim_info_to_test.familiar_tracker
        if familiar_tracker is None:
            return ()
        familiar = familiar_tracker.get_active_familiar()
        if familiar is None:
            return ()
        if familiar.is_sim:
            return (
             familiar.sim_info,)
        return (
         familiar,)

    def get_localization_tokens(self, *args, **kwargs):
        return (
         self.sim_info_to_test,) + self._additional_localization_tokens

    def set_additional_participant(self, participant_type, value):
        self._additional_participants[participant_type] = value


class DoubleSimResolver(SingleSimResolver):

    def __init__(self, sim_info, target_sim_info, **kwargs):
        (super().__init__)(sim_info, **kwargs)
        self.target_sim_info = target_sim_info

    def __repr__(self):
        return 'DoubleSimResolver: sim: {} target_sim: {}'.format(self.sim_info_to_test, self.target_sim_info)

    @classproperty
    def profile_metric_stack_depth(cls):
        return 2

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.TargetSim:
            return (
             self.target_sim_info,)
        if participant_type == ParticipantType.SignificantOtherTargetSim:
            return (
             self.target_sim_info.get_significant_other_sim_info(),)
        if participant_type == ParticipantType.FamiliarOfTarget:
            return self._get_familiar_for_sim_info(self.target_sim_info)
        return (super().get_participants)(participant_type, **kwargs)

    def get_localization_tokens(self, *args, **kwargs):
        return (
         self.sim_info_to_test, self.target_sim_info) + self._additional_localization_tokens


class DataResolver(Resolver):

    def __init__(self, sim_info, event_kwargs=None, custom_keys=()):
        super().__init__()
        self.sim_info = sim_info
        if event_kwargs is not None:
            self._interaction = event_kwargs.get('interaction', None)
            self.on_zone_load = event_kwargs.get('init', False)
        else:
            self._interaction = None
            self.on_zone_load = False
        self.event_kwargs = event_kwargs
        self.data_object = None
        self.objective_guid64 = None
        self.custom_keys = custom_keys

    def __repr__(self):
        return 'DataResolver: participant: {}'.format(self.sim_info)

    def __call__(self, test, data_object=None, objective_guid64=None):
        if data_object is not None:
            self.data_object = data_object
            self.objective_guid64 = objective_guid64
        return super().__call__(test)

    @property
    def interaction(self):
        return self._interaction

    @property
    def profile_metric_key(self):
        interaction_name = None
        if self._interaction is not None:
            interaction_name = self._interaction.aop.affordance.__name__
        objective_name = 'Invalid'
        if self.objective_guid64 is not None:
            objective_manager = services.objective_manager()
            objective = objective_manager.get(self.objective_guid64)
            objective_name = objective.__name__
        return 'objective:{} (interaction:{})'.format(objective_name, interaction_name)

    def get_resolved_arg(self, key):
        return self.event_kwargs.get(key, None)

    def get_participants(self, participant_type, event_key=None):
        result = self._get_participants_base(participant_type, event_key=event_key)
        if result is not None:
            return result
        if participant_type == event_testing.test_constants.SIM_INSTANCE:
            return (
             self.sim_info,)
        if participant_type == event_testing.test_constants.FROM_DATA_OBJECT:
            return (
             self.data_object,)
        if participant_type == event_testing.test_constants.OBJECTIVE_GUID64:
            return (
             self.objective_guid64,)
        if participant_type == event_testing.test_constants.FROM_EVENT_DATA:
            if not self.event_kwargs:
                return ()
            return (
             self.event_kwargs.get(event_key),)
        if self._interaction is not None:
            return tuple((getattr(participant, 'sim_info', participant) for participant in self._interaction.get_participants(participant_type)))
        if participant_type == ParticipantType.Actor:
            return (
             self.sim_info,)
        if participant_type == ParticipantType.AllRelationships:
            sim_mgr = services.sim_info_manager()
            relations = set((sim_mgr.get(relations.get_other_sim_id(self.sim_info.sim_id)) for relations in self.sim_info.relationship_tracker))
            return tuple(relations)
        if participant_type == ParticipantType.TargetSim:
            if not self.event_kwargs:
                return ()
            target_sim_id = self.event_kwargs.get(event_testing.test_constants.TARGET_SIM_ID)
            if target_sim_id is None:
                return ()
            return (
             services.sim_info_manager().get(target_sim_id),)
        if participant_type == ParticipantType.ActiveHousehold:
            active_household = services.active_household()
            if active_household is not None:
                return tuple(active_household.sim_info_gen())
        if self.on_zone_load:
            return ()
        raise ValueError('Trying to use DataResolver with type that is not supported by DataResolver: {}'.format(participant_type))


class SingleObjectResolver(Resolver):

    def __init__(self, obj):
        super().__init__()
        self._obj = obj

    def __repr__(self):
        return 'SingleObjectResolver: object: {}'.format(self._obj)

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.Object:
            return (
             self._obj,)
        if participant_type == ParticipantType.ObjectIngredients:
            if self._obj.crafting_component:
                crafting_process = self._obj.get_crafting_process()
                if crafting_process is not None:
                    return tuple(crafting_process.get_ingredients_object_definitions())
            return ()
        if participant_type == ParticipantType.Actor:
            return (
             self._obj,)
        if participant_type == ParticipantType.StoredSim:
            stored_sim_info = self._obj.get_stored_sim_info()
            return (stored_sim_info,)
        if participant_type == ParticipantType.StoredSimOrNameData:
            stored_sim_name_data = self._obj.get_stored_sim_info_or_name_data()
            return (stored_sim_name_data,)
        if participant_type == ParticipantType.OwnerSim:
            owner_sim_info_id = self._obj.get_sim_owner_id()
            owner_sim_info = services.sim_info_manager().get(owner_sim_info_id)
            return (owner_sim_info,)
        if participant_type == ParticipantType.ObjectParent and not self._obj is None:
            if self._obj.parent is None:
                return ()
            return (
             self._obj.parent,)
            if participant_type == ParticipantType.ObjectChildren:
                if self._obj is None:
                    return ()
                if self._obj.is_part:
                    return tuple(self._obj.part_owner.children_recursive_gen())
                return tuple(self._obj.children_recursive_gen())
            if participant_type == ParticipantType.RandomInventoryObject:
                return (
                 random.choice(tuple(self._obj.inventory_component.visible_storage)),)
        if participant_type == ParticipantType.PickedObject or participant_type == ParticipantType.CarriedObject or participant_type == ParticipantType.LiveDragActor:
            if self._obj.is_sim:
                return (
                 self._obj.sim_info,)
            return (
             self._obj,)
        if participant_type == ParticipantType.RoutingOwner:
            if self._obj.get_routing_owner().is_sim:
                return (
                 self._obj.get_routing_owner().sim_info,)
            return (self._obj.get_routing_owner(),)
        else:
            if participant_type == ParticipantType.RoutingTarget:
                if self._obj.get_routing_target().is_sim:
                    return (
                     self._obj.get_routing_target().sim_info,)
                return (self._obj.get_routing_target(),)
            else:
                if participant_type == ParticipantType.StoredCASPartsOnObject:
                    stored_cas_parts = self._obj.get_stored_cas_parts()
                    if stored_cas_parts is None:
                        return ()
                    return tuple(iter(self._obj.get_stored_cas_parts()))
                result = (self._get_participants_base)(participant_type, **kwargs)
                if result is not None:
                    return result
                if participant_type == event_testing.test_constants.FROM_EVENT_DATA:
                    return ()
                raise ValueError('Trying to use SingleObjectResolver with something that is not an Object: {}'.format(participant_type))

    def get_localization_tokens(self, *args, **kwargs):
        return (
         self._obj,)


class DoubleObjectResolver(Resolver):

    def __init__(self, source_obj, target_obj):
        super().__init__()
        self._source_obj = source_obj
        self._target_obj = target_obj

    def __repr__(self):
        return 'DoubleObjectResolver: actor_object: {}, target_object:{}'.format(self._source_obj, self._target_obj)

    def get_participants--- This code section failed: ---

 L.1059         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _get_participants_base
                4  LOAD_FAST                'participant_type'
                6  BUILD_TUPLE_1         1 
                8  LOAD_FAST                'kwargs'
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  STORE_FAST               'result'

 L.1060        14  LOAD_FAST                'result'
               16  LOAD_CONST               None
               18  COMPARE_OP               is-not
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L.1061        22  LOAD_FAST                'result'
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L.1063        26  LOAD_FAST                'participant_type'
               28  LOAD_GLOBAL              ParticipantType
               30  LOAD_ATTR                Actor
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     66  'to 66'

 L.1064        36  LOAD_FAST                'participant_type'
               38  LOAD_GLOBAL              ParticipantType
               40  LOAD_ATTR                PickedObject
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_TRUE     66  'to 66'

 L.1065        46  LOAD_FAST                'participant_type'
               48  LOAD_GLOBAL              ParticipantType
               50  LOAD_ATTR                CarriedObject
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_TRUE     66  'to 66'

 L.1066        56  LOAD_FAST                'participant_type'
               58  LOAD_GLOBAL              ParticipantType
               60  LOAD_ATTR                LiveDragActor
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    92  'to 92'
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            44  '44'
             66_2  COME_FROM            34  '34'

 L.1067        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _source_obj
               70  LOAD_ATTR                is_sim
               72  POP_JUMP_IF_FALSE    84  'to 84'

 L.1068        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _source_obj
               78  LOAD_ATTR                sim_info
               80  BUILD_TUPLE_1         1 
               82  RETURN_VALUE     
             84_0  COME_FROM            72  '72'

 L.1069        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _source_obj
               88  BUILD_TUPLE_1         1 
               90  RETURN_VALUE     
             92_0  COME_FROM            64  '64'

 L.1071        92  LOAD_FAST                'participant_type'
               94  LOAD_GLOBAL              ParticipantType
               96  LOAD_ATTR                Listeners
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    132  'to 132'

 L.1072       102  LOAD_FAST                'participant_type'
              104  LOAD_GLOBAL              ParticipantType
              106  LOAD_ATTR                Object
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_TRUE    132  'to 132'

 L.1073       112  LOAD_FAST                'participant_type'
              114  LOAD_GLOBAL              ParticipantType
              116  LOAD_ATTR                TargetSim
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_TRUE    132  'to 132'

 L.1074       122  LOAD_FAST                'participant_type'
              124  LOAD_GLOBAL              ParticipantType
              126  LOAD_ATTR                LiveDragTarget
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   158  'to 158'
            132_0  COME_FROM           120  '120'
            132_1  COME_FROM           110  '110'
            132_2  COME_FROM           100  '100'

 L.1075       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _target_obj
              136  LOAD_ATTR                is_sim
              138  POP_JUMP_IF_FALSE   150  'to 150'

 L.1076       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _target_obj
              144  LOAD_ATTR                sim_info
              146  BUILD_TUPLE_1         1 
              148  RETURN_VALUE     
            150_0  COME_FROM           138  '138'

 L.1077       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _target_obj
              154  BUILD_TUPLE_1         1 
              156  RETURN_VALUE     
            158_0  COME_FROM           130  '130'

 L.1079       158  LOAD_FAST                'participant_type'
              160  LOAD_GLOBAL              event_testing
              162  LOAD_ATTR                test_constants
              164  LOAD_ATTR                FROM_EVENT_DATA
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   174  'to 174'

 L.1080       170  LOAD_CONST               ()
              172  RETURN_VALUE     
            174_0  COME_FROM           168  '168'

 L.1082       174  LOAD_FAST                'participant_type'
              176  LOAD_GLOBAL              ParticipantType
              178  LOAD_ATTR                LinkedPostureSim
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   218  'to 218'

 L.1083       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _source_obj
              188  LOAD_ATTR                is_sim
              190  POP_JUMP_IF_FALSE   218  'to 218'

 L.1084       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _source_obj
              196  LOAD_ATTR                posture
              198  STORE_FAST               'posture'

 L.1085       200  LOAD_FAST                'posture'
              202  LOAD_ATTR                multi_sim
              204  POP_JUMP_IF_FALSE   218  'to 218'

 L.1086       206  LOAD_FAST                'posture'
              208  LOAD_ATTR                linked_posture
              210  LOAD_ATTR                sim
              212  LOAD_ATTR                sim_info
              214  BUILD_TUPLE_1         1 
              216  RETURN_VALUE     
            218_0  COME_FROM           204  '204'
            218_1  COME_FROM           190  '190'
            218_2  COME_FROM           182  '182'

 L.1088       218  LOAD_FAST                'participant_type'
              220  LOAD_GLOBAL              ParticipantType
              222  LOAD_ATTR                ObjectParent
              224  COMPARE_OP               ==
          226_228  POP_JUMP_IF_FALSE   268  'to 268'

 L.1089       230  LOAD_FAST                'self'
              232  LOAD_ATTR                _target_obj
              234  LOAD_CONST               None
              236  COMPARE_OP               is
              238  POP_JUMP_IF_TRUE    254  'to 254'
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                _target_obj
              244  LOAD_ATTR                parent
              246  LOAD_CONST               None
              248  COMPARE_OP               is
          250_252  POP_JUMP_IF_FALSE   258  'to 258'
            254_0  COME_FROM           238  '238'

 L.1090       254  LOAD_CONST               ()
              256  RETURN_VALUE     
            258_0  COME_FROM           250  '250'

 L.1091       258  LOAD_FAST                'self'
              260  LOAD_ATTR                _target_obj
              262  LOAD_ATTR                parent
              264  BUILD_TUPLE_1         1 
              266  RETURN_VALUE     
            268_0  COME_FROM           226  '226'

 L.1093       268  LOAD_FAST                'participant_type'
              270  LOAD_GLOBAL              ParticipantType
              272  LOAD_ATTR                RoutingOwner
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   320  'to 320'

 L.1094       280  LOAD_FAST                'self'
              282  LOAD_ATTR                _source_obj
              284  LOAD_METHOD              get_routing_owner
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  LOAD_ATTR                is_sim
          290_292  POP_JUMP_IF_FALSE   308  'to 308'

 L.1095       294  LOAD_FAST                'self'
              296  LOAD_ATTR                _source_obj
              298  LOAD_METHOD              get_routing_owner
              300  CALL_METHOD_0         0  '0 positional arguments'
              302  LOAD_ATTR                sim_info
              304  BUILD_TUPLE_1         1 
              306  RETURN_VALUE     
            308_0  COME_FROM           290  '290'

 L.1097       308  LOAD_FAST                'self'
              310  LOAD_ATTR                _source_obj
              312  LOAD_METHOD              get_routing_owner
              314  CALL_METHOD_0         0  '0 positional arguments'
              316  BUILD_TUPLE_1         1 
              318  RETURN_VALUE     
            320_0  COME_FROM           276  '276'

 L.1098       320  LOAD_FAST                'participant_type'
              322  LOAD_GLOBAL              ParticipantType
              324  LOAD_ATTR                RoutingTarget
              326  COMPARE_OP               ==
          328_330  POP_JUMP_IF_FALSE   372  'to 372'

 L.1099       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _source_obj
              336  LOAD_METHOD              get_routing_target
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  LOAD_ATTR                is_sim
          342_344  POP_JUMP_IF_FALSE   360  'to 360'

 L.1100       346  LOAD_FAST                'self'
              348  LOAD_ATTR                _source_obj
              350  LOAD_METHOD              get_routing_target
              352  CALL_METHOD_0         0  '0 positional arguments'
              354  LOAD_ATTR                sim_info
              356  BUILD_TUPLE_1         1 
              358  RETURN_VALUE     
            360_0  COME_FROM           342  '342'

 L.1102       360  LOAD_FAST                'self'
              362  LOAD_ATTR                _source_obj
              364  LOAD_METHOD              get_routing_target
              366  CALL_METHOD_0         0  '0 positional arguments'
              368  BUILD_TUPLE_1         1 
              370  RETURN_VALUE     
            372_0  COME_FROM           328  '328'

 L.1104       372  LOAD_GLOBAL              ValueError
              374  LOAD_STR                 'Trying to use DoubleObjectResolver with something that is not supported: Participant {}, Resolver {}'
              376  LOAD_METHOD              format
              378  LOAD_FAST                'participant_type'
              380  LOAD_FAST                'self'
              382  CALL_METHOD_2         2  '2 positional arguments'
              384  CALL_FUNCTION_1       1  '1 positional argument'
              386  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 384

    def get_localization_tokens(self, *args, **kwargs):
        return (
         self._source_obj, self._target_obj)


class SingleActorAndObjectResolver(Resolver):

    def __init__(self, actor_sim_info, obj, source):
        super().__init__()
        self._sim_info = actor_sim_info
        self._obj = obj
        self._source = source

    def __repr__(self):
        return 'SingleActorAndObjectResolver: sim_info: {}, object: {}'.format(self._sim_info, self._obj)

    @property
    def profile_metric_key(self):
        return 'source:{} object:{}'.format(self._source, self._obj)

    def get_participants(self, participant_type, **kwargs):
        result = (self._get_participants_base)(participant_type, **kwargs)
        if result is not None:
            return result
        if participant_type == ParticipantType.Actor or participant_type == ParticipantType.CustomSim or participant_type == event_testing.test_constants.SIM_INSTANCE:
            return (
             self._sim_info,)
        if participant_type == ParticipantType.Object:
            return (
             self._obj,)
        if participant_type == ParticipantType.ObjectIngredients:
            if self._obj.crafting_component:
                crafting_process = self._obj.get_crafting_process()
                if crafting_process is not None:
                    return tuple(crafting_process.get_ingredients_object_definitions())
            return ()
        if participant_type == ParticipantType.ObjectParent and not self._obj is None:
            if self._obj.parent is None:
                return ()
            return (
             self._obj.parent,)
            if participant_type == ParticipantType.StoredSim:
                stored_sim_info = self._obj.get_stored_sim_info()
                return (stored_sim_info,)
            if participant_type == ParticipantType.StoredCASPartsOnObject:
                stored_cas_parts = self._obj.get_stored_cas_parts()
                if stored_cas_parts is None:
                    return ()
                return tuple(iter(self._obj.get_stored_cas_parts()))
            if participant_type == ParticipantType.OwnerSim:
                owner_sim_info_id = self._obj.get_sim_owner_id()
                owner_sim_info = services.sim_info_manager().get(owner_sim_info_id)
                return (owner_sim_info,)
        if participant_type == ParticipantType.Affordance or participant_type == ParticipantType.InteractionContext or participant_type == event_testing.test_constants.FROM_EVENT_DATA:
            return ()
        raise ValueError('Trying to use SingleActorAndObjectResolver with something that is not supported: {}'.format(participant_type))

    def get_localization_tokens(self, *args, **kwargs):
        return (
         self._sim_info, self._obj)


class DoubleSimAndObjectResolver(Resolver):

    def __init__(self, actor_sim_info, target_sim_info, obj, source):
        super().__init__()
        self._actor_sim_info = actor_sim_info
        self._target_sim_info = target_sim_info
        self._obj = obj
        self._source = source

    def __repr__(self):
        return f"DoubleActorAndObjectResolver: actor_sim_info: {self._actor_sim_info}, target_sim_info: {self._target_sim_info}, object: {self._obj}"

    @property
    def profile_metric_key(self):
        return f"source:{self._source} object:{self._obj}"

    def get_participants(self, participant_type, **kwargs):
        result = (self._get_participants_base)(participant_type, **kwargs)
        if result is not None:
            return result
        if participant_type == ParticipantType.Actor or participant_type == ParticipantType.CustomSim or participant_type == event_testing.test_constants.SIM_INSTANCE:
            return (
             self._actor_sim_info,)
        if participant_type == ParticipantType.TargetSim:
            return (
             self._target_sim_info,)
        if participant_type == ParticipantType.SignificantOtherTargetSim:
            return (
             self._target_sim_info.get_significant_other_sim_info(),)
        if participant_type == ParticipantType.Object:
            return (
             self._obj,)
        if participant_type == ParticipantType.ObjectIngredients:
            if self._obj.crafting_component:
                crafting_process = self._obj.get_crafting_process()
                if crafting_process is not None:
                    return tuple(crafting_process.get_ingredients_object_definitions())
            return ()
        if participant_type == ParticipantType.ObjectParent and not self._obj is None:
            if self._obj.parent is None:
                return ()
            return (
             self._obj.parent,)
            if participant_type == ParticipantType.StoredSim:
                stored_sim_info = self._obj.get_stored_sim_info()
                return (stored_sim_info,)
            if participant_type == ParticipantType.StoredCASPartsOnObject:
                stored_cas_parts = self._obj.get_stored_cas_parts()
                if stored_cas_parts is None:
                    return ()
                return tuple(iter(self._obj.get_stored_cas_parts()))
            if participant_type == ParticipantType.OwnerSim:
                owner_sim_info_id = self._obj.get_sim_owner_id()
                owner_sim_info = services.sim_info_manager().get(owner_sim_info_id)
                return (owner_sim_info,)
            if participant_type == ParticipantType.Affordance:
                return ()
            if participant_type == ParticipantType.InteractionContext:
                return ()
            if participant_type == event_testing.test_constants.FROM_EVENT_DATA:
                return ()
        raise ValueError(f"Trying to use DoubleActorAndObjectResolver with something that is not supported: {participant_type}")

    def get_localization_tokens(self, *args, **kwargs):
        return (
         self._sim_info, self._target_sim_info, self._obj)


class PhotoResolver(SingleActorAndObjectResolver):

    def __init__(self, photographer, photo_object, photo_targets, source):
        super().__init__(photographer, photo_object, source)
        self._photo_targets = photo_targets

    def __repr__(self):
        return 'PhotoResolver: photographer: {}, photo_object:{}, photo_targets:{}'.format(self._sim_info, self._obj, self._photo_targets)

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.PhotographyTargets:
            return self._photo_targets
        return (super().get_participants)(participant_type, **kwargs)


class ZoneResolver(GlobalResolver):

    def __init__(self, zone_id, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._zone_id = zone_id

    def __repr__(self):
        return 'ZoneResolver: zone_id: {}'.format(self._zone_id)

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.PickedZoneId:
            return (
             self._zone_id,)
        return (super().get_participants)(participant_type, **kwargs)


class StreetResolver(GlobalResolver):

    def __init__(self, street, **kwargs):
        (super().__init__)(**kwargs)
        self._street = street

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.Street:
            street_service = services.street_service()
            if street_service is None:
                return ()
            street_civic_policy_provider = street_service.get_provider(self._street)
            if street_civic_policy_provider is None:
                return ()
            return (
             street_civic_policy_provider,)
        return (super().get_participants)(participant_type, **kwargs)


class VenuePolicyProviderResolver(GlobalResolver):

    def __init__(self, venue_policy_provider, **kwargs):
        (super().__init__)(**kwargs)
        self._venue_policy_provider = venue_policy_provider

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.VenuePolicyProvider:
            return (
             self._venue_policy_provider,)
        return (super().get_participants)(participant_type, **kwargs)


class LotResolver(GlobalResolver):

    def __init__(self, lot, **kwargs):
        (super().__init__)(**kwargs)
        self._lot = lot

    def get_participants(self, participant_type, **kwargs):
        if participant_type == ParticipantType.Lot:
            return (
             self._lot,)
        return (super().get_participants)(participant_type, **kwargs)