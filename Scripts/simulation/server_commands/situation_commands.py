# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\situation_commands.py
# Compiled at: 2020-09-22 01:49:58
# Size of source mod 2**32: 66156 bytes
from contextlib import contextmanager
import collections
from protocolbuffers import Consts_pb2, Situations_pb2, Lot_pb2, Localization_pb2
from protocolbuffers.ResourceKey_pb2 import ResourceKey
from date_and_time import DateAndTime
from distributor import shared_messages
from distributor.rollback import ProtocolBufferRollback
from distributor.shared_messages import IconInfoData
from event_testing.results import TestResult
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target, TunableInstanceParam, get_tunable_instance
from situations import situation
from situations.base_situation import BaseSituation
from situations.situation_excursion import ExcursionSituation
from situations.situation_guest_list import SituationGuestList, SituationGuestInfo, SituationInvitationPurpose
from situations.situation_types import SituationCreationUIOption, SituationCallbackOption, SituationMedal
from world.region import Region
import build_buy, date_and_time, mtx, services, sims4.commands, sims4.log, situations
logger = sims4.log.Logger('Situations')
allow_debug_situations_in_ui = False

def should_display_situation(situation_instance, sim, target_sim_id, from_situation_subset):
    global allow_debug_situations_in_ui
    tuned_to_show = situation_instance.creation_ui_option == SituationCreationUIOption.AVAILABLE or situation_instance.creation_ui_option == SituationCreationUIOption.DEBUG_AVAILABLE and allow_debug_situations_in_ui or from_situation_subset and situation_instance.creation_ui_option == SituationCreationUIOption.SPECIFIED_ONLY
    result = situation_instance.is_situation_available(sim, target_sim_id)
    if tuned_to_show:
        mtx_id = 0
        if situation_instance.entitlement:
            if mtx.has_entitlement(situation_instance.entitlement):
                mtx_id = situation_instance.entitlement
            else:
                return (
                 TestResult(False), 0)
        return (
         result, mtx_id)
    return (TestResult(False), 0)


SITUATION_ID_BATCH_REPEATED_FIELDS = ('situation_resource_id', 'situation_name', 'category_id',
                                      'mtx_id', 'highest_medal_earned', 'tooltip',
                                      'allow_user_facing_goals', 'medal_icon_override',
                                      'scoring_lock_reason', 'new_entry')

class SituationIdEntry:
    __slots__ = SITUATION_ID_BATCH_REPEATED_FIELDS

    def __init__(self):
        for field in SITUATION_ID_BATCH_REPEATED_FIELDS:
            setattr(self, field, None)

    def append_to_message(self, msg):
        num_populated_fields = 0
        try:
            for field in SITUATION_ID_BATCH_REPEATED_FIELDS:
                value = getattr(self, field)
                repeated_field = getattr(msg, field)
                repeated_field.append(value)
                num_populated_fields += 1

        except:
            logger.exception('Exception while filling out a SituationIDBatch message')
            for i in range(num_populated_fields):
                field = SITUATION_ID_BATCH_REPEATED_FIELDS[i]
                repeated_field = getattr(msg, field)
                del repeated_field[-1]

    @classmethod
    @contextmanager
    def get_entry_with_rollback(cls, msg):
        entry = cls()
        try:
            yield entry
            entry.append_to_message(msg)
        except:
            logger.exception('Exception populating get_situation_ids')


@sims4.commands.Command('situations.set_situation_as_viewed', command_type=(sims4.commands.CommandType.Live))
def set_situation_as_viewed(sim_id: OptionalTargetParam, situation_id: int, _connection=None):
    sim = get_optional_target(sim_id, _connection)
    if sim is None:
        sims4.commands.output('Sim id {} is invalid.'.format(sim_id), _connection)
        return
    sim.household.set_is_situation_new_entry(situation_id, False)


@sims4.commands.Command('situations.get_situation_ids', command_type=(sims4.commands.CommandType.Live))
def get_situation_ids(session_id: int=0, sim_id: OptionalTargetParam=None, opt_target_id: int=None, *situation_ids, _connection=None):
    sim = get_optional_target(sim_id, _connection)
    if opt_target_id is None or opt_target_id == 0:
        target_sim_id = 0
    else:
        target_sim_id = opt_target_id
    household = sim.household
    instance_manager = services.get_instance_manager(sims4.resources.Types.SITUATION)
    situation_batch_msg = Situations_pb2.SituationIDBatch()
    situation_batch_msg.situation_session_id = session_id
    situation_batch_msg.scoring_enabled = household.situation_scoring_enabled
    valid_situations = []
    for situation_id in situation_ids:
        instance = instance_manager.get(situation_id)
        result, mtx_id = should_display_situation(instance, sim, target_sim_id, True)
        if result or result.tooltip is not None:
            valid_situations.append((instance, mtx_id, result.tooltip))

    if not valid_situations:
        for instance in instance_manager.types.values():
            if instance.guid64 in situation_ids:
                continue
            result, mtx_id = should_display_situation(instance, sim, target_sim_id, False)
            if result or result.tooltip is not None:
                valid_situations.append((instance, mtx_id, result.tooltip))

    for instance, mtx_id, tooltip in valid_situations:
        situation_id = instance.guid64
        with SituationIdEntry.get_entry_with_rollback(situation_batch_msg) as (entry):
            entry.situation_resource_id = situation_id
            entry.situation_name = instance._display_name
            entry.category_id = instance.category
            entry.mtx_id = mtx_id
            entry.highest_medal_earned = household.get_highest_medal_for_situation(situation_id)
            entry.new_entry = household.get_is_situation_new_entry(situation_id)
            resource_key = ResourceKey()
            icon = instance.medal_icon_override
            if icon is None:
                resource_key.type, resource_key.group, resource_key.instance = (0,
                                                                                0,
                                                                                0)
            else:
                resource_key.type, resource_key.group, resource_key.instance = icon.type, icon.group, icon.instance
            entry.medal_icon_override = resource_key
            if instance.scoring_lock_reason is None:
                entry.scoring_lock_reason = Localization_pb2.LocalizedString()
                entry.scoring_lock_reason.hash = 0
            else:
                entry.scoring_lock_reason = instance.scoring_lock_reason
            if tooltip is not None:
                entry.tooltip = tooltip()
            else:
                entry.tooltip = Localization_pb2.LocalizedString()
                entry.tooltip.hash = 0
            entry.allow_user_facing_goals = instance.allow_user_facing_goals

    shared_messages.add_message_if_selectable(sim, Consts_pb2.MSG_SITUATION_ID_BATCH, situation_batch_msg, True)


@sims4.commands.Command('situations.get_situation_data', command_type=(sims4.commands.CommandType.Live))
def get_situation_data(session_id: int=0, sim_id: OptionalTargetParam=None, *situation_ids, _connection=None):
    sim = get_optional_target(sim_id, _connection)
    instance_manager = services.situation_manager()
    situation_batch_msg = Situations_pb2.SituationDataBatch()
    situation_batch_msg.situation_session_id = session_id
    for situation_id in situation_ids:
        with ProtocolBufferRollback(situation_batch_msg.situations) as (situation_data):
            instance = instance_manager.get(situation_id)
            if instance is not None:
                shared_messages.build_icon_info_msg(IconInfoData(icon_resource=(instance._icon)), instance._display_name, situation_data.icon_info)
                situation_data.icon_info.desc = instance.situation_description
                situation_data.cost = instance._cost
                situation_data.max_participants = instance.max_participants
                for medal in SituationMedal:
                    with ProtocolBufferRollback(situation_data.rewards) as (reward_msg):
                        level = instance.get_level_data(medal)
                        reward_msg.level = int(medal)
                        if level is not None:
                            if level.reward is not None:
                                if level.reward.reward_description is not None:
                                    reward_msg.display_name.extend([level.reward.reward_description])

                jobs = list(instance.get_tuned_jobs())
                jobs.sort(key=(lambda job: job.guid64))
                if instance.job_display_ordering is not None:
                    for ordered_job in reversed(instance.job_display_ordering):
                        if ordered_job in jobs:
                            jobs.remove(ordered_job)
                            jobs.insert(0, ordered_job)

                for job in jobs:
                    if job.sim_count.upper_bound > 0:
                        with ProtocolBufferRollback(situation_data.jobs) as (job_msg):
                            job_msg.job_resource_id = job.guid64
                            shared_messages.build_icon_info_msg(IconInfoData(icon_resource=(job.icon)), job.display_name, job_msg.icon_info)
                            job_msg.icon_info.desc = job.job_description
                            job_msg.is_hireable = job.can_be_hired
                            job_msg.min_required = job.sim_count.lower_bound
                            job_msg.max_allowed = job.sim_count.upper_bound
                            job_msg.hire_cost = job.hire_cost

    shared_messages.add_message_if_selectable(sim, Consts_pb2.MSG_SITUATION_DATA_BATCH, situation_batch_msg, True)


@sims4.commands.Command('situations.get_prepopulated_job_for_sims', command_type=(sims4.commands.CommandType.Live))
def get_prepopulated_job_for_sims(session_id: int, situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), sim_id: OptionalTargetParam=None, opt_target_id: int=None, _connection=None):
    sim = get_optional_target(sim_id, _connection)
    prepopulate = situation_type.get_prepopulated_job_for_sims(sim, opt_target_id)
    assign_msg = Situations_pb2.SituationAssignJob()
    assign_msg.situation_session_id = session_id
    if prepopulate is not None:
        for sim_id, job_type_id in prepopulate:
            assign_msg.sim_ids.append(sim_id)
            assign_msg.job_resource_ids.append(job_type_id)

    shared_messages.add_object_message(sim, Consts_pb2.MSG_SITUATION_ASSIGN_JOB, assign_msg, True)


JobCallbackData = collections.namedtuple('JobCallbackData', ['session_id', 'sim_id', 'job_id', 'job_requirements'])

@sims4.commands.Command('situations.get_sims_for_job', command_type=(sims4.commands.CommandType.Live))
def get_sims_for_job--- This code section failed: ---

 L. 301         0  LOAD_GLOBAL              get_optional_target
                2  LOAD_FAST                'sim_id'
                4  LOAD_FAST                '_connection'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'sim'

 L. 304        10  LOAD_GLOBAL              services
               12  LOAD_METHOD              time_service
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  LOAD_ATTR                sim_now
               18  STORE_FAST               'situation_start_time'

 L. 305        20  LOAD_FAST                'situation_type'
               22  LOAD_ATTR                duration
               24  STORE_FAST               'duration'

 L. 306        26  LOAD_FAST                'duration'
               28  LOAD_CONST               0
               30  COMPARE_OP               >
               32  POP_JUMP_IF_FALSE    54  'to 54'

 L. 307        34  LOAD_FAST                'situation_start_time'
               36  LOAD_GLOBAL              date_and_time
               38  LOAD_METHOD              create_time_span
               40  LOAD_CONST               0
               42  LOAD_CONST               0
               44  LOAD_FAST                'duration'
               46  CALL_METHOD_3         3  '3 positional arguments'
               48  BINARY_ADD       
               50  STORE_FAST               'situation_end_time'
               52  JUMP_FORWARD         66  'to 66'
             54_0  COME_FROM            32  '32'

 L. 309        54  LOAD_GLOBAL              date_and_time
               56  LOAD_ATTR                INVALID_DATE_AND_TIME
               58  STORE_FAST               'situation_start_time'

 L. 310        60  LOAD_GLOBAL              date_and_time
               62  LOAD_ATTR                INVALID_DATE_AND_TIME
               64  STORE_FAST               'situation_end_time'
             66_0  COME_FROM            52  '52'

 L. 313        66  LOAD_CLOSURE             'job_type'
               68  BUILD_TUPLE_1         1 
               70  LOAD_CODE                <code_object get_sim_filter_gsi_name>
               72  LOAD_STR                 'get_sims_for_job.<locals>.get_sim_filter_gsi_name'
               74  MAKE_FUNCTION_8          'closure'
               76  STORE_FAST               'get_sim_filter_gsi_name'

 L. 316        78  LOAD_GLOBAL              services
               80  LOAD_METHOD              sim_filter_service
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  LOAD_ATTR                submit_filter
               86  LOAD_DEREF               'job_type'
               88  LOAD_ATTR                filter

 L. 317        90  LOAD_CONST               None

 L. 318        92  LOAD_FAST                'sim'
               94  LOAD_ATTR                sim_info

 L. 319        96  LOAD_FAST                'situation_start_time'

 L. 320        98  LOAD_FAST                'situation_end_time'

 L. 321       100  LOAD_CONST               False

 L. 322       102  LOAD_FAST                'get_sim_filter_gsi_name'
              104  LOAD_CONST               ('requesting_sim_info', 'start_time', 'end_time', 'allow_yielding', 'gsi_source_fn')
              106  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              108  STORE_FAST               'results'

 L. 327       110  LOAD_DEREF               'job_type'
              112  LOAD_ATTR                additional_filter_for_user_selection
              114  POP_JUMP_IF_TRUE    124  'to 124'
              116  LOAD_DEREF               'job_type'
              118  LOAD_ATTR                additional_filter_list_for_user_selection
          120_122  POP_JUMP_IF_FALSE   398  'to 398'
            124_0  COME_FROM           114  '114'

 L. 328       124  BUILD_MAP_0           0 
              126  STORE_FAST               'conflicting_career_track_ids'

 L. 329       128  LOAD_GLOBAL              set
              130  CALL_FUNCTION_0       0  '0 positional arguments'
              132  STORE_FAST               'sim_constraints'

 L. 330       134  SETUP_LOOP          176  'to 176'
              136  LOAD_FAST                'results'
              138  GET_ITER         
              140  FOR_ITER            174  'to 174'
              142  STORE_FAST               'result'

 L. 331       144  LOAD_FAST                'sim_constraints'
              146  LOAD_METHOD              add
              148  LOAD_FAST                'result'
              150  LOAD_ATTR                sim_info
              152  LOAD_ATTR                id
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          

 L. 332       158  LOAD_FAST                'result'
              160  LOAD_ATTR                conflicting_career_track_id
              162  LOAD_FAST                'conflicting_career_track_ids'
              164  LOAD_FAST                'result'
              166  LOAD_ATTR                sim_info
              168  LOAD_ATTR                id
              170  STORE_SUBSCR     
              172  JUMP_BACK           140  'to 140'
              174  POP_BLOCK        
            176_0  COME_FROM_LOOP      134  '134'

 L. 333       176  BUILD_LIST_0          0 
              178  STORE_FAST               'results'

 L. 334       180  LOAD_DEREF               'job_type'
              182  LOAD_ATTR                additional_filter_for_user_selection
              184  POP_JUMP_IF_FALSE   252  'to 252'

 L. 336       186  LOAD_GLOBAL              services
              188  LOAD_METHOD              sim_filter_service
              190  CALL_METHOD_0         0  '0 positional arguments'
              192  LOAD_ATTR                submit_filter
              194  LOAD_DEREF               'job_type'
              196  LOAD_ATTR                additional_filter_for_user_selection

 L. 337       198  LOAD_CONST               None

 L. 338       200  LOAD_FAST                'sim'
              202  LOAD_ATTR                sim_info

 L. 339       204  LOAD_FAST                'situation_start_time'

 L. 340       206  LOAD_FAST                'situation_end_time'

 L. 341       208  LOAD_FAST                'sim_constraints'

 L. 342       210  LOAD_CONST               False

 L. 343       212  LOAD_FAST                'get_sim_filter_gsi_name'
              214  LOAD_CONST               ('requesting_sim_info', 'start_time', 'end_time', 'sim_constraints', 'allow_yielding', 'gsi_source_fn')
              216  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              218  STORE_FAST               'or_results'

 L. 344       220  LOAD_FAST                'or_results'
              222  STORE_FAST               'results'

 L. 346       224  LOAD_FAST                'or_results'
              226  POP_JUMP_IF_FALSE   252  'to 252'

 L. 347       228  LOAD_SETCOMP             '<code_object <setcomp>>'
              230  LOAD_STR                 'get_sims_for_job.<locals>.<setcomp>'
              232  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              234  LOAD_FAST                'or_results'
              236  GET_ITER         
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  STORE_FAST               'used_ids'

 L. 348       242  LOAD_FAST                'sim_constraints'
              244  LOAD_METHOD              difference
              246  LOAD_FAST                'used_ids'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  STORE_FAST               'sim_constraints'
            252_0  COME_FROM           226  '226'
            252_1  COME_FROM           184  '184'

 L. 350       252  LOAD_FAST                'sim_constraints'
          254_256  POP_JUMP_IF_FALSE   356  'to 356'

 L. 351       258  SETUP_LOOP          356  'to 356'
              260  LOAD_DEREF               'job_type'
              262  LOAD_ATTR                additional_filter_list_for_user_selection
              264  GET_ITER         
            266_0  COME_FROM           344  '344'
            266_1  COME_FROM           314  '314'
              266  FOR_ITER            354  'to 354'
              268  STORE_FAST               'additional_filter'

 L. 352       270  LOAD_GLOBAL              services
              272  LOAD_METHOD              sim_filter_service
              274  CALL_METHOD_0         0  '0 positional arguments'
              276  LOAD_ATTR                submit_filter
              278  LOAD_FAST                'additional_filter'

 L. 353       280  LOAD_CONST               None

 L. 354       282  LOAD_FAST                'sim'
              284  LOAD_ATTR                sim_info

 L. 355       286  LOAD_FAST                'situation_start_time'

 L. 356       288  LOAD_FAST                'situation_end_time'

 L. 357       290  LOAD_FAST                'sim_constraints'

 L. 358       292  LOAD_CONST               False

 L. 359       294  LOAD_FAST                'get_sim_filter_gsi_name'
              296  LOAD_CONST               ('requesting_sim_info', 'start_time', 'end_time', 'sim_constraints', 'allow_yielding', 'gsi_source_fn')
              298  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              300  STORE_FAST               'or_results'

 L. 360       302  LOAD_FAST                'results'
              304  LOAD_METHOD              extend
              306  LOAD_FAST                'or_results'
              308  CALL_METHOD_1         1  '1 positional argument'
              310  POP_TOP          

 L. 362       312  LOAD_FAST                'or_results'
          314_316  POP_JUMP_IF_FALSE   266  'to 266'

 L. 363       318  LOAD_SETCOMP             '<code_object <setcomp>>'
              320  LOAD_STR                 'get_sims_for_job.<locals>.<setcomp>'
              322  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              324  LOAD_FAST                'or_results'
              326  GET_ITER         
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  STORE_FAST               'used_ids'

 L. 364       332  LOAD_FAST                'sim_constraints'
              334  LOAD_METHOD              difference
              336  LOAD_FAST                'used_ids'
              338  CALL_METHOD_1         1  '1 positional argument'
              340  STORE_FAST               'sim_constraints'

 L. 365       342  LOAD_FAST                'sim_constraints'
          344_346  POP_JUMP_IF_TRUE    266  'to 266'

 L. 366       348  BREAK_LOOP       
          350_352  JUMP_BACK           266  'to 266'
              354  POP_BLOCK        
            356_0  COME_FROM_LOOP      258  '258'
            356_1  COME_FROM           254  '254'

 L. 369       356  SETUP_LOOP          398  'to 398'
              358  LOAD_FAST                'results'
              360  GET_ITER         
            362_0  COME_FROM           374  '374'
              362  FOR_ITER            396  'to 396'
              364  STORE_FAST               'result'

 L. 370       366  LOAD_FAST                'result'
              368  LOAD_ATTR                conflicting_career_track_id
              370  LOAD_CONST               None
              372  COMPARE_OP               is
          374_376  POP_JUMP_IF_FALSE   362  'to 362'

 L. 371       378  LOAD_FAST                'conflicting_career_track_ids'
              380  LOAD_FAST                'result'
              382  LOAD_ATTR                sim_info
              384  LOAD_ATTR                id
              386  BINARY_SUBSCR    
              388  LOAD_FAST                'result'
              390  STORE_ATTR               conflicting_career_track_id
          392_394  JUMP_BACK           362  'to 362'
              396  POP_BLOCK        
            398_0  COME_FROM_LOOP      356  '356'
            398_1  COME_FROM           120  '120'

 L. 374       398  LOAD_GLOBAL              Situations_pb2
              400  LOAD_METHOD              SituationJobSims
              402  CALL_METHOD_0         0  '0 positional arguments'
              404  STORE_FAST               'msg'

 L. 375       406  LOAD_FAST                'session_id'
              408  LOAD_FAST                'msg'
              410  STORE_ATTR               situation_session_id

 L. 376       412  LOAD_DEREF               'job_type'
              414  LOAD_ATTR                guid
              416  LOAD_FAST                'msg'
              418  STORE_ATTR               job_resource_id

 L. 377       420  LOAD_DEREF               'job_type'
              422  LOAD_ATTR                requirement_text
              424  LOAD_FAST                'msg'
              426  STORE_ATTR               requirements

 L. 380       428  LOAD_FAST                'results'
              430  LOAD_ATTR                sort
              432  LOAD_LAMBDA              '<code_object <lambda>>'
              434  LOAD_STR                 'get_sims_for_job.<locals>.<lambda>'
              436  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              438  LOAD_CONST               ('key',)
              440  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              442  POP_TOP          

 L. 382       444  SETUP_LOOP          554  'to 554'
              446  LOAD_FAST                'results'
              448  GET_ITER         
              450  FOR_ITER            552  'to 552'
              452  STORE_FAST               'result'

 L. 385       454  LOAD_FAST                'msg'
              456  LOAD_ATTR                sim_ids
              458  LOAD_METHOD              append
              460  LOAD_FAST                'result'
              462  LOAD_ATTR                sim_info
              464  LOAD_ATTR                id
              466  CALL_METHOD_1         1  '1 positional argument'
              468  POP_TOP          

 L. 387       470  LOAD_GLOBAL              ProtocolBufferRollback
              472  LOAD_FAST                'msg'
              474  LOAD_ATTR                sims
              476  CALL_FUNCTION_1       1  '1 positional argument'
              478  SETUP_WITH          542  'to 542'
              480  STORE_FAST               'situation_job_sim'

 L. 388       482  LOAD_FAST                'result'
              484  LOAD_ATTR                sim_info
              486  LOAD_ATTR                id
              488  LOAD_FAST                'situation_job_sim'
              490  STORE_ATTR               sim_id

 L. 389       492  LOAD_FAST                'result'
              494  LOAD_ATTR                sim_info
              496  LOAD_ATTR                household
              498  LOAD_ATTR                id
              500  LOAD_GLOBAL              services
              502  LOAD_METHOD              active_household_id
              504  CALL_METHOD_0         0  '0 positional arguments'
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   522  'to 522'

 L. 391       512  LOAD_FAST                'result'
              514  LOAD_ATTR                sim_info
              516  LOAD_ATTR                account_id
              518  LOAD_FAST                'situation_job_sim'
              520  STORE_ATTR               account_id
            522_0  COME_FROM           508  '508'

 L. 392       522  LOAD_FAST                'result'
              524  LOAD_ATTR                conflicting_career_track_id
          526_528  POP_JUMP_IF_FALSE   538  'to 538'

 L. 393       530  LOAD_FAST                'result'
              532  LOAD_ATTR                conflicting_career_track_id
              534  LOAD_FAST                'situation_job_sim'
              536  STORE_ATTR               career_track_id
            538_0  COME_FROM           526  '526'
              538  POP_BLOCK        
              540  LOAD_CONST               None
            542_0  COME_FROM_WITH      478  '478'
              542  WITH_CLEANUP_START
              544  WITH_CLEANUP_FINISH
              546  END_FINALLY      
          548_550  JUMP_BACK           450  'to 450'
              552  POP_BLOCK        
            554_0  COME_FROM_LOOP      444  '444'

 L. 395       554  LOAD_GLOBAL              shared_messages
              556  LOAD_METHOD              add_message_if_selectable
              558  LOAD_GLOBAL              services
              560  LOAD_METHOD              object_manager
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  LOAD_METHOD              get
              566  LOAD_FAST                'sim'
              568  LOAD_ATTR                id
              570  CALL_METHOD_1         1  '1 positional argument'
              572  LOAD_GLOBAL              Consts_pb2
              574  LOAD_ATTR                MSG_SITUATION_JOB_SIMS
              576  LOAD_FAST                'msg'
              578  LOAD_CONST               True
              580  CALL_METHOD_4         4  '4 positional arguments'
              582  POP_TOP          

Parse error at or near `COME_FROM_LOOP' instruction at offset 356_0


@sims4.commands.Command('situations.get_valid_situation_locations', command_type=(sims4.commands.CommandType.Live))
def get_valid_situation_locations(sim_id: OptionalTargetParam, situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), *guests, _connection=None):
    sim = get_optional_target(sim_id, _connection)
    if not sim:
        sims4.commands.output('Invalid Sim ID: {}'.format(sim_id), _connection)
        return
    sim_info = sim.sim_info
    current_region = services.current_region()
    possible_zones = situation_type.get_possible_zone_ids_for_situation(host_sim_info=sim_info, guest_ids=guests)
    venue_manager = services.get_instance_manager(sims4.resources.Types.VENUE)
    persistence_service = services.get_persistence_service()
    locations_msg = Situations_pb2.SituationLocations()
    for zone_id in possible_zones:
        zone_data = persistence_service.get_zone_proto_buff(zone_id)
        if zone_data is None:
            continue
        neighborhood_data = persistence_service.get_neighborhood_proto_buff(zone_data.neighborhood_id)
        if neighborhood_data is None:
            continue
        region_description_id = neighborhood_data.region_id
        region_instance = Region.REGION_DESCRIPTION_TUNING_MAP.get(region_description_id)
        if not current_region.is_region_compatible(region_instance):
            continue
        lot_data = None
        for lot_owner_data in neighborhood_data.lots:
            if zone_id == lot_owner_data.zone_instance_id:
                lot_data = lot_owner_data
                break

        if zone_data is not None:
            if lot_data is not None:
                location_data = Lot_pb2.LotInfoItem()
                location_data.zone_id = zone_data.zone_id
                location_data.name = zone_data.name
                location_data.world_id = zone_data.world_id
                location_data.lot_template_id = zone_data.lot_template_id
                location_data.lot_description_id = zone_data.lot_description_id
                venue_tuning_id = build_buy.get_current_venue(zone_id)
                venue_tuning = venue_manager.get(venue_tuning_id)
                send_lot_owner = True
                if venue_tuning is not None:
                    location_data.venue_type_name = venue_tuning.display_name
                    send_lot_owner = venue_tuning.is_residential or venue_tuning.is_university_housing
            if lot_data.lot_owner:
                if send_lot_owner:
                    household_id = lot_data.lot_owner[0].household_id
                    household = services.household_manager().get(household_id)
                    if household is not None:
                        location_data.household_name = household.name
            locations_msg.situation_locations.append(location_data)

    shared_messages.add_object_message_for_sim_id(sim.id, Consts_pb2.MSG_SITUATION_LOCATIONS, locations_msg)


@sims4.commands.Command('situations.create')
def create_situation(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), opt_sim: OptionalTargetParam=None, user_facing: bool=True, zone_id: int=0, _connection=None):
    situation_manager = services.get_zone_situation_manager()
    sim = get_optional_target(opt_sim, _connection)
    guest_list = SituationGuestList(False, sim.id)
    situation_id = situation_manager.create_situation(situation_type, guest_list=guest_list, user_facing=user_facing, zone_id=zone_id)
    if situation_id is not None:
        sims4.commands.output('Successfully created situation: {}.'.format(situation_id), _connection)
    else:
        sims4.commands.output('Insufficient funds to create situation', _connection)


@sims4.commands.Command('situations.create_walkby')
def create_walkby_situation(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), _connection=None):
    situation_id = services.current_zone().ambient_service.start_specific_situation(situation_type)
    if situation_id is not None:
        sims4.commands.output('Started situation {} with id {}'.format(situation_type, situation_id), _connection)
    else:
        sims4.commands.output('Could not start {}'.format(situation_type), _connection)


@sims4.commands.Command('situations.create_with_predefined_guest_list')
def create_situation_with_predefined_guest_list(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), zone_id: int=0, _connection=None):
    situation_manager = services.get_zone_situation_manager()
    guest_list = situation_type.get_predefined_guest_list()
    if guest_list is None:
        sims4.commands.output('Unable to create guest list!', _connection)
        return
    else:
        situation_id = situation_manager.create_situation(situation_type, guest_list=guest_list, user_facing=False, zone_id=zone_id)
        if situation_id is not None:
            sims4.commands.output('Successfully created situation: {}.'.format(situation_id), _connection)
        else:
            sims4.commands.output('Insufficient funds to create situation', _connection)


@sims4.commands.Command('situations.create_for_venue', command_type=(sims4.commands.CommandType.DebugOnly))
def create_situation_for_venue_type(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), venue_tuning: TunableInstanceParam(sims4.resources.Types.VENUE), opt_sim: OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if not services.current_zone().venue_service.has_zone_for_venue_type((venue_tuning,)):
        sims4.commands.output('There are no zones that support the venue tuning provided, {}.'.format(venue_tuning), _connection)
        return False
    else:
        situation_manager = services.get_zone_situation_manager()
        zone_id, _ = services.current_zone().venue_service.get_zone_and_venue_type_for_venue_types((venue_tuning,))
        guest_list = SituationGuestList(False, sim.id)
        situation_id = situation_manager.create_situation(situation_type, guest_list=guest_list, user_facing=True, zone_id=zone_id)
        if situation_id is None:
            sims4.commands.output('Insufficient funds to create situation', _connection)
        else:
            sims4.commands.output('Successfully created situation: {}.'.format(situation_id), _connection)


@sims4.commands.Command('situations.create_gl', command_type=(sims4.commands.CommandType.Live))
def create_situation_with_guest_list(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), scoring_enabled: bool, zone_id: int=0, scheduled_time: int=0, *args, _connection=None):
    if len(args) % 3 != 0:
        sims4.commands.output('Invalid guest list, its length must be a multiple of 3', _connection)
        return False
        situation_manager = services.get_zone_situation_manager()
        client = services.client_manager().get(_connection)
        if client.active_sim is not None:
            host_sim_id = client.active_sim.id
            client.active_sim.household.set_situation_scoring(scoring_enabled)
        else:
            host_sim_id = 0
        guest_list = SituationGuestList(situation_type.force_invite_only, host_sim_id)
        guest_list_is_good = True
        for job_name_or_key, sim_id_or_name, purpose_name in zip(args[0::3], args[1::3], args[2::3]):
            job_type = services.situation_job_manager().get(job_name_or_key)
            if job_type is None:
                sims4.commands.output('Invalid job name or key: {}'.format(job_name_or_key), _connection)
                guest_list_is_good = False
                continue
            try:
                purpose = SituationInvitationPurpose(purpose_name)
            except ValueError:
                sims4.commands.output('Invalid Purpose: {}. Use INVITED, HIRED, or PREFERRED'.format(purpose_name), _connection)
                guest_list_is_good = False
                continue

            try:
                sim_id = int(sim_id_or_name)
            except (ValueError, TypeError):
                sims4.commands.output('Incorrectly formatted sim_id {}'.format(sim_id_or_name), _connection)
                guest_list_is_good = False
                continue

            guest_info = SituationGuestInfo.construct_from_purpose(sim_id, job_type, purpose)
            guest_list.add_guest_info(guest_info)

        if not guest_list_is_good:
            sims4.commands.output('FAILURE: bad guest list {}.'.format(situation_type), _connection)
            return False
        guest_list = situation_type.get_extended_guest_list(guest_list=guest_list)
        scheduled_time_day_time = DateAndTime(scheduled_time) if scheduled_time != 0 else None
        situation_id = situation_manager.create_situation(situation_type, guest_list=guest_list, zone_id=zone_id, scoring_enabled=scoring_enabled, scheduled_time=scheduled_time_day_time)
        if situation_id is not None and scheduled_time == 0:
            sims4.commands.output('Successfully created situation: {}.'.format(situation_id), _connection)
    elif situation_id is not None:
        sims4.commands.output('Successfully scheduled situation for the future: {}.'.format(situation_id), _connection)
    else:
        sims4.commands.output('Insufficient funds to create situation', _connection)
    return True


@sims4.commands.Command('qa.situations.create', command_type=(sims4.commands.CommandType.Automation))
def automation_create_situation(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), opt_sim: OptionalTargetParam=None, _connection=None):
    if situation_type is None:
        sims4.commands.automation_output('SituationCreate; Status:Failed', _connection)
        return False
    else:
        situation_manager = services.get_zone_situation_manager()
        sim_spawner_service = services.sim_spawner_service()
        sim = get_optional_target(opt_sim, _connection)
        if sim is None:
            sims4.commands.automation_output('SituationCreate; Status:Failed', _connection)
            return False
            sim_spawner_service.enable_gui_smoke_notification()
            guest_list = SituationGuestList(invite_only=False, host_sim_id=(sim.id))
            situation_id = situation_manager.create_situation(situation_type, guest_list=guest_list)
            if situation_id is not None:
                sims4.commands.automation_output('SituationCreate; Status:Success, Id:{}'.format(situation_id), _connection)
        else:
            sims4.commands.automation_output('SituationCreate; Status:Failed', _connection)


@sims4.commands.Command('situations.allow_debug_situations')
def allow_debug_situations(allow: bool=True, _connection=None):
    global allow_debug_situations_in_ui
    allow_debug_situations_in_ui = allow


@sims4.commands.Command('situations.destroy')
def destroy_situation(situation_id: int, _connection=None):
    sit_man = services.get_zone_situation_manager()
    if situation_id is None:
        sims4.commands.output('No situation id specified.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sit_man.destroy_situation_by_id(situation_id)


@sims4.commands.Command('situations.destroy_all_situations')
def destroy_all_situations(_connection=None):
    services.get_zone_situation_manager().destroy_all_situations()


@sims4.commands.Command('situations.advance_phase')
def advance_situation_phase(situation_id: int=None, _connection=None):
    sit_man = services.get_zone_situation_manager()
    if situation_id is None:
        sims4.commands.output('No situation id specified.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sit = sit_man.get(situation_id)
    if sit is None:
        sims4.commands.output('Invalid situation id.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sit._transition_to_next_phase()


@sims4.commands.Command('qa.situations.advance_phase', command_type=(sims4.commands.CommandType.Automation))
def automation_advance_situation_phase(situation_id: int=None, _connection=None):
    situation_manager = services.get_zone_situation_manager()
    situation = situation_manager.get(situation_id)
    if situation is None:
        sims4.commands.automation_output('AdvancePhase; Success:False', _connection)
        return
    situation._transition_to_next_phase()
    sims4.commands.automation_output('AdvancePhase; Success:True', _connection)
    return True


@sims4.commands.Command('situations.on_situation_goal_button_clicked', command_type=(sims4.commands.CommandType.Live))
def on_situation_goal_button_clicked(situation_id: int, _connection=None):
    situation_manager = services.get_zone_situation_manager()
    situation = situation_manager.get(situation_id)
    if situation is None:
        sims4.commands.output('FAILURE: Situation with id {} is not found.'.format(situation_id), _connection)
        return False
    situation.on_situation_goal_button_clicked()
    return True


@sims4.commands.Command('situations.refresh_goals', command_type=(sims4.commands.CommandType.Live))
def refresh_goals(_connection=None):
    sit_man = services.get_zone_situation_manager()
    situations = sit_man.running_situations()
    for situation in situations:
        situation.refresh_situation_goals()

    sims4.commands.output("Sim's goals refreshed.", _connection)


@sims4.commands.Command('situations.complete_goal')
def complete_goal(goal_name, target_sim_id=None, _connection=None):
    if target_sim_id is None or target_sim_id == 0:
        target_sim = None
    else:
        target_sim = services.object_manager().get(int(target_sim_id, base=0))
    situations = services.get_zone_situation_manager().running_situations()
    success = False
    for situation in situations:
        success = situation.debug_force_complete_named_goal(goal_name, target_sim)
        if success:
            break

    if success:
        sims4.commands.output('Success: Goal {} Completed'.format(goal_name), _connection)
    else:
        sims4.commands.output('FAILURE: Goal {} NOT Completed'.format(goal_name), _connection)
    return success


@sims4.commands.Command('qa.situations.complete_goal', command_type=(sims4.commands.CommandType.Automation))
def automation_complete_goal(situation_id: int, goal_name, _connection=None):
    situation_manager = services.get_zone_situation_manager()
    situation = situation_manager.get(situation_id)
    if situation is None:
        sims4.commands.automation_output('CompleteGoal; Success:False', _connection)
        return False
    else:
        result = situation.debug_force_complete_named_goal(goal_name, None)
        if result:
            sims4.commands.automation_output('CompleteGoal; Success:True', _connection)
        else:
            sims4.commands.automation_output('CompleteGoal; Success:False', _connection)
    return result


@sims4.commands.Command('situations.excursions.advance_activity')
def excursions_advance_activity(_connection=None):
    situations = services.get_zone_situation_manager().running_situations()
    excursion_situation = None
    for situation in situations:
        if isinstance(situation, ExcursionSituation):
            excursion_situation = situation
            break

    if excursion_situation is None:
        sims4.commands.output('FAILURE: No Excursion Situation is currently running.', _connection)
        return False
    else:
        success = excursion_situation.debug_advance_activity()
        if success:
            sims4.commands.output('Success: Situation {} advanced to next activity.'.format(str(excursion_situation)), _connection)
        else:
            sims4.commands.output('FAILURE: Situation {} NOT advanced to next activity.'.format(str(excursion_situation)), _connection)
    return success


@sims4.commands.Command('situations.excursions.goto_activity')
def excursions_goto_activity(activity_key, _connection=None):
    situations = services.get_zone_situation_manager().running_situations()
    excursion_situation = None
    for situation in situations:
        if isinstance(situation, ExcursionSituation):
            excursion_situation = situation
            break

    if excursion_situation is None:
        sims4.commands.output('FAILURE: No Excursion Situation is currently running.', _connection)
        return False
    else:
        success = excursion_situation.debug_goto_activity(activity_key)
        if success:
            sims4.commands.output('Success: Situation {} set to activity {}.'.format(str(excursion_situation), activity_key), _connection)
        else:
            sims4.commands.output('FAILURE: Situation {} NOT set to activity {}'.format(str(excursion_situation), activity_key), _connection)
    return success


@sims4.commands.Command('situations.save_load_test')
def situation_save_load_seed_test(_connection=None):
    seeds = []
    situation_manager = services.get_zone_situation_manager()
    for situation in situation_manager.running_situations():
        seed = situation.save_situation()
        if seed is not None:
            seeds.append(seed)

    situation_manager.reset(create_system_situations=False)
    for seed in seeds:
        situation_manager.create_situation_from_seed(seed)


@sims4.commands.Command('situations.jobs')
def jobs_for_situation(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), _connection=None):
    jobs = situation_type._get_tuned_jobs()
    for job in jobs:
        sims4.commands.output(str(job), _connection)


def _list_jobs(situation, _connection=None):
    sims4.commands.output('Default job:', _connection)
    sims4.commands.output('   {} '.format(situation.default_job()), _connection)
    sims4.commands.output('All jobs: ({})'.format(len(situation._jobs)), _connection)
    sims4.commands.output('    count{:>50} : {:<50}'.format('Job Name', 'Default Role'), _connection)
    index = 0
    for job_data in situation._jobs.values():
        count = situation.get_num_sims_in_job(job_data.get_job_type())
        sims4.commands.output(' {:2} {:3}  {:>50} : {:<50}'.format(index, count, job_data.get_job_type(), job_data.default_role_state_type), _connection)
        index = index + 1


def _list_sims_in_jobs(situation, _connection=None):
    sims4.commands.output('All jobs: ({})'.format(len(situation._jobs)), _connection)
    sims4.commands.output('    count{:>50} : {:<50}'.format('Job Name', 'Default Role'), _connection)
    index = 0
    for job_data in situation._jobs.values():
        count = situation.get_num_sims_in_job(job_data.get_job_type())
        sims4.commands.output(' {:2} {:3}  {:>50} : {:<50}'.format(index, count, job_data.get_job_type(), job_data.default_role_state_type), _connection)
        index = index + 1
        for sim in situation.all_sims_in_job_gen(job_data.get_job_type()):
            sims4.commands.output('        {:>50}  : {:<50}'.format(sim, situation.get_current_role_state_for_sim(sim)), _connection)


def _list_phases(situation, _connection=None):
    sims4.commands.output('Current phase: ({:3}/{:3})'.format(situation._phase_index, len(situation._phases)), _connection)
    sims4.commands.output('      {} '.format(situation._phase), _connection)
    sims4.commands.output('All phases:', _connection)
    count = 0
    for phase in situation._phases:
        sims4.commands.output(' {:3}: {} '.format(count, phase), _connection)
        count = count + 1


def _list_situations(sit_man, _connection=None):
    sims4.commands.output('Situation: ', _connection)
    situations = list(sit_man._objects.values())
    if not situations:
        sims4.commands.output('   None', _connection)
    else:
        for sit in situations:
            sims4.commands.output('   {}  {} '.format(sit.id, sit), _connection)


@sims4.commands.Command('situations.list_jobs')
def list_situation_jobs(situation_id: int=None, _connection=None):
    sit_man = services.get_zone_situation_manager()
    if situation_id is None:
        sims4.commands.output('You must specify a valid situation id', _connection)
        return
    sit = sit_man.get(situation_id)
    if sit is None:
        sims4.commands.output('Invalid situation id.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sims4.commands.output('===========================================================================', _connection)
    sims4.commands.output('{} '.format(sit), _connection)
    _list_sims_in_jobs(sit, _connection)
    sims4.commands.output('===========================================================================', _connection)


@sims4.commands.Command('situations.show')
def list_active_situations(situation_id: int=None, _connection=None):
    sit_man = services.get_zone_situation_manager()
    if situation_id is None:
        sims4.commands.output('===========================================================================', _connection)
        _list_situations(sit_man, _connection)
        sims4.commands.output('For info about a particular situation, provide the id as an argument.', _connection)
        sims4.commands.output('===========================================================================', _connection)
        return
    sit = sit_man.get(situation_id)
    if sit is None:
        sims4.commands.output('Invalid situation id.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sims4.commands.output('===========================================================================', _connection)
    sims4.commands.output('Name:        {} '.format(sit), _connection)
    sims4.commands.output('ID:          {} '.format(sit.id), _connection)
    sims4.commands.output('Sim count:   {} '.format(len(sit._situation_sims)), _connection)
    sims4.commands.output('Level|Score: {}|{}'.format(sit.get_level(), sit.score), _connection)
    sims4.commands.output('Phase/State: {} '.format(sit.get_phase_state_name_for_gsi()), _connection)
    sims4.commands.output('===============================', _connection)
    _list_jobs(sit, _connection)
    sims4.commands.output('===============================', _connection)


@sims4.commands.Command('qa.situations.num_sims_in_role_state', command_type=(sims4.commands.CommandType.Automation))
def automation_get_num_sims_in_role_state(situation_id: int, role_state_type: TunableInstanceParam(sims4.resources.Types.ROLE_STATE), _connection=None):
    situation_manager = services.get_zone_situation_manager()
    situation = situation_manager.get(situation_id)
    if situation is None:
        sims4.commands.automation_output('NumInRoleState; Number:0', _connection)
        return
    if role_state_type is None:
        sims4.commands.automation_output('NumInRoleState; Number:0', _connection)
    count = situation.get_num_sims_in_role_state(role_state_type)
    sims4.commands.automation_output('NumInRoleState; Number:{}'.format(count), _connection)


@sims4.commands.Command('qa.situations.info', command_type=(sims4.commands.CommandType.Automation))
def automation_list_active_situations(situation_id: int=None, _connection=None):
    sit_man = services.get_zone_situation_manager()
    sit = sit_man.get(situation_id)
    if sit is None:
        sims4.commands.automation_output('SituationInfo; Exists:No', _connection)
        return
    sims4.commands.output('SituationInfo; Exists:Yes, Id:{}, ClassName:{}, NumSims:{}, Level:{}, Score:{}, State:{} '.format(sit.id, sit.__class__.__name__, len(sit._situation_sims), int(sit.get_level()), sit.score, sit.get_phase_state_name_for_gsi()), _connection)
    sims4.commands.automation_output('SituationInfo; Exists:Yes, Id:{}, ClassName:{}, NumSims:{}, Level:{}, Score:{}, State:{}'.format(sit.id, sit.__class__.__name__, len(sit._situation_sims), int(sit.get_level()), sit.score, sit.get_phase_state_name_for_gsi()), _connection)


@sims4.commands.Command('situations.get_sim_score')
def get_sim_score_in_situation(sim_id: OptionalTargetParam, situation_id: int=None, _connection=None):
    sim = get_optional_target(sim_id, _connection)
    if situation_id is None or sim is None:
        sims4.commands.output('Invalid arguments provided.  Syntax:', _connection)
        sims4.commands.output('    |situations.get_sim_score <sim_id> <situation_id>', _connection)
        sims4.commands.output('         <sim_id>: Ctrl+click on a sim in the window to paste their sim_id into the command prompt', _connection)
        sims4.commands.output('         <situation_id>: id to situation ', _connection)
        return
    sit_man = services.get_zone_situation_manager()
    sit = sit_man.get(situation_id)
    if sit is None:
        sims4.commands.output('Invalid situation id.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sims4.commands.output('Score in situation: {}'.format(sit.get_sim_total_score(sim)), _connection)


@sims4.commands.Command('situations.update_sim_score')
def update_sim_score(sim_id: OptionalTargetParam, situation_id: int=None, delta: int=None, _connection=None):
    sim = get_optional_target(sim_id, _connection)
    if situation_id is None or sim is None or delta is None:
        sims4.commands.output('Invalid arguments provided.  Syntax:', _connection)
        sims4.commands.output('    |situations.get_sim_score <sim_id> <situation_id> <int>', _connection)
        sims4.commands.output('         <sim_id>: Ctrl+click on a sim in the window to paste their sim_id into the command prompt', _connection)
        sims4.commands.output('         <situation_id>: id to situation ', _connection)
        sims4.commands.output("         <int>: delta to apply to sim's score ", _connection)
        return
    sit_man = services.get_zone_situation_manager()
    sit = sit_man.get(situation_id)
    if sit is None:
        sims4.commands.output('Invalid situation id.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sit.sim_score_update(sim, delta)
    sims4.commands.output('Score in situation: {}'.format(sit.get_sim_total_score(sim)), _connection)


@sims4.commands.Command('situations.set_situation_score')
def set_situation_score(situation_id: int=None, score: int=None, _connection=None):
    if situation_id is None or score is None:
        sims4.commands.output('Invalid arguments provided.  Syntax:', _connection)
        sims4.commands.output('    |situations.set_situation_score <situation_id> <score>', _connection)
        sims4.commands.output('         <situation_id>: id to situation ', _connection)
        sims4.commands.output('         <score> : Override the score of the entire situation', _connection)
        return
    sit_man = services.get_zone_situation_manager()
    sit = sit_man.get(situation_id)
    if sit is None:
        sims4.commands.output('Invalid situation id.  Valid options are: ', _connection)
        _list_situations(sit_man, _connection=_connection)
        return
    sit.debug_set_overall_score(score)
    sims4.commands.output('Situation Score: {}'.format(sit.score), _connection)


@sims4.commands.Command('situations.set_situation_medal')
def set_situation_medal(situation_id: int=None, medal: SituationMedal=None, _connection=None):
    if situation_id is None or medal is None:
        sims4.commands.output('Invalid arguments provided.  Syntax:', _connection)
        sims4.commands.output('    |situations.set_situation_medal <situation_id> <TIN/BRONZE/SILVER/GOLD>', _connection)
        return
    else:
        sit_man = services.get_zone_situation_manager()
        situation = sit_man.get(situation_id)
        if situation is None:
            sims4.commands.output('Invalid situation id.', _connection)
            return
        situation.should_track_score or sims4.commands.output('Invalid non-scoring situation {}'.format(situation), _connection)
        return
    score = 0
    for m in SituationMedal:
        data = situation.get_level_data(m)
        if data is not None:
            score += data.score_delta
        else:
            if m == medal:
                sims4.commands.output('Situation {} has no tuning data for the required medal {}.'.format(situation, medal), _connection)
                return
        if m == medal:
            break

    situation.debug_set_overall_score(score)
    sims4.commands.output('Situation Score: {} and Medal: {}'.format(situation.score, medal), _connection)


@sims4.commands.Command('situations.add_score')
def add_score(situation_id: int, delta: int, _connection=None):
    sit_man = services.get_zone_situation_manager()
    situation = sit_man.get(situation_id)
    if situation is None:
        sims4.commands.output('Invalid situation id.', _connection)
        return
    if not situation.should_track_score:
        sims4.commands.output('Invalid non-scoring situation {}'.format(situation), _connection)
        return
    situation.score_update(delta)
    sims4.commands.output('Resulting Situation Score: {}'.format(situation.score), _connection)


@sims4.commands.Command('situations.add_score_to_all')
def add_score_to_all(delta: int, _connection=None):
    for situation in services.get_zone_situation_manager().get_all():
        if not situation.should_track_score:
            continue
        old_score = situation.score
        situation.score_update(delta)
        sims4.commands.output('Changed {} score from {} to {}'.format(str(situation), old_score, situation.score), _connection)


@sims4.commands.Command('situations.set_constrained_goal_list')
def set_constrained_goal_list(*goal_names: str, _connection=None):
    constrained_goals = set()
    for goal_name in goal_names:
        goal_type = get_tunable_instance(sims4.resources.Types.SITUATION_GOAL, goal_name)
        if goal_type is None:
            sims4.commands.output('Invalid goal name: {} skipping.'.format(goal_name), _connection)
            continue
        constrained_goals.add(goal_type)

    situations.situation_goal_tracker.SituationGoalTracker.constrained_goals = constrained_goals


@sims4.commands.Command('situations.test_end_score_callback')
def test_end_score_callback(situation_id: int, _connection=None):
    situation_manager = services.get_zone_situation_manager()
    situation_manager.register_for_callback(situation_id, SituationCallbackOption.END_OF_SITUATION_SCORING, _end_score_callback)


def _end_score_callback(situation_id, option, end_score_data):
    logger.debug('data {}', end_score_data)


@sims4.commands.Command('situations.test_situation_available')
def test_situation_available(situation_type: TunableInstanceParam(sims4.resources.Types.SITUATION), opt_sim: OptionalTargetParam=None, target_sim_id: int=0, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        sims4.commands.output('Invalid sim: {} provided.'.format(opt_sim), _connection)
        return
    else:
        situation_name = str(situation_type)
        if situation_type.is_situation_available(sim, target_sim_id):
            sims4.commands.output('Situation {} with initiating sim {} and target sim {} is available.'.format(situation_name, sim, target_sim_id), _connection)
        else:
            sims4.commands.output('Situation {} with initiating sim {} and target sim {} is not available.'.format(situation_name, sim, target_sim_id), _connection)


@sims4.commands.Command('situations.reset')
def reset(_connection=None):
    services.get_zone_situation_manager().reset()
    for sim in services.sim_info_manager().instanced_sims_gen():
        try:
            sim.reset_role_tracker()
        except Exception:
            logger.error('Error while resetting role tracker for sim {}', sim)


@sims4.commands.Command('situations.pre_destroy_user_facing_situation', command_type=(sims4.commands.CommandType.Live))
def pre_destroy_user_facing_situation(situation_id: int=None, _connection=None):
    sit_man = services.get_zone_situation_manager()
    if situation_id is None:
        for situation in tuple(sit_man.get_user_facing_situations_gen()):
            sit_man.pre_destroy_situation_by_id(situation.id)

        return
    situation = sit_man.get(situation_id)
    if not (situation is None or situation.is_user_facing):
        sims4.commands.output('Invalid player facing situation id.', _connection)
        return
    sit_man.pre_destroy_situation_by_id(situation.id)


@sims4.commands.Command('situations.destroy_user_facing_situation', command_type=(sims4.commands.CommandType.Live))
def destroy_user_facing_situation(situation_id: int=None, _connection=None):
    sit_man = services.get_zone_situation_manager()
    if situation_id is None:
        for situation in tuple(sit_man.get_user_facing_situations_gen()):
            sit_man.destroy_situation_by_id(situation.id)

        return
    situation = sit_man.get(situation_id)
    if not (situation is None or situation.is_user_facing):
        sims4.commands.output('Invalid player facing situation id.', _connection)
        return
    sit_man.destroy_situation_by_id(situation.id)


@sims4.commands.Command('situations.change_user_facing_situation_duration', command_type=(sims4.commands.CommandType.DebugOnly))
def change_user_facing_situation_duration(situation_id: int, duration: int, _connection=None):
    sit_man = services.get_zone_situation_manager()
    situation = sit_man.get(situation_id)
    if not (situation is None or situation.is_user_facing):
        sims4.commands.output('Invalid player facing situation id.', _connection)
        return
    situation.change_duration(duration)


@sims4.commands.Command('situations.force_loot_actions')
def force_loot_actions(loot_actions_type: TunableInstanceParam(sims4.resources.Types.ACTION), _connection=None):
    BaseSituation.constrained_emotional_loot = loot_actions_type


@sims4.commands.Command('situations.churn_jobs')
def churn_jobs(_connection=None):
    situation_manager = services.get_zone_situation_manager()
    for situation in situation_manager.running_situations():
        situation.churn_jobs()


@sims4.commands.Command('situations.shift_change')
def shift_change(_connection=None):
    situation_manager = services.get_zone_situation_manager()
    for situation in situation_manager.running_situations():
        situation.shift_change_jobs()


@sims4.commands.Command('situations.blacklist')
def show_blacklist(_connection=None):
    situation_manager = services.get_zone_situation_manager()
    blacklist = situation_manager.get_auto_fill_blacklist()
    for sim_id in blacklist:
        sim = services.sim_info_manager().get(sim_id)
        if sim is not None:
            blacklist_info = situation_manager.get_blacklist_info(sim.id)
            for bi in blacklist_info:
                sims4.commands.output('Sim: {} Tag: {} Time remaining: {}'.format(sim, bi[0], bi[1]), _connection)


@sims4.commands.Command('situations.set_npc_soft_cap', 'sim_spawner_service.set_npc_soft_cap', command_type=(sims4.commands.CommandType.Automation))
def set_npc_soft_cap(soft_cap: int, _connection=None):
    services.sim_spawner_service().set_npc_soft_cap_override(soft_cap)
    sims4.commands.output('Npc soft cap override set to {}'.format(soft_cap), _connection)


@sims4.commands.Command('situations.enable_perf_cheats', 'sim_spawner_service.enable_perf_cheats', command_type=(sims4.commands.CommandType.Automation))
def enable_perf_cheats(enable: bool=True, _connection=None):
    situation_manager = services.get_zone_situation_manager()
    situation_manager.enable_perf_cheat(enable)
    services.sim_spawner_service().enable_perf_cheat()
    sims4.commands.output('Perf cheats={}'.format(enable), _connection)


@sims4.commands.Command('situations.make_greeted', command_type=(sims4.commands.CommandType.Live))
def make_greeted(opt_sim: OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        sims4.commands.output('Invalid sim: {} provided.'.format(opt_sim), _connection)
        return
    situation_manager = services.get_zone_situation_manager()
    situation_manager.make_waiting_player_greeted(sim)


@sims4.commands.Command('situations.start_situation_creation', command_type=(sims4.commands.CommandType.Live))
def start_situation_creation(opt_sim: OptionalTargetParam=None, creation_time: int=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        sims4.commands.output('Invalid sim: {} provided.'.format(opt_sim), _connection)
        return
    situation_manager = services.get_zone_situation_manager()
    situation_manager.send_situation_start_ui(sim, creation_time=creation_time)


@sims4.commands.Command('situations.push_make_sim_leave_now_situation', command_type=(sims4.commands.CommandType.DebugOnly))
def push_make_sim_leave_now_situation(opt_sim: OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        sims4.commands.output('Invalid sim: {} provided.'.format(opt_sim), _connection)
        return
    situation_manager = services.get_zone_situation_manager()
    situation_manager.make_sim_leave_now_must_run(sim)


@sims4.commands.Command('situations.enable_welcome_wagon', command_type=(sims4.commands.CommandType.Automation))
def enable_welcome_wagon(enable: bool=True, _connection=None):
    npc_hosted_situation_service = services.npc_hosted_situation_service()
    if npc_hosted_situation_service is not None:
        if enable:
            npc_hosted_situation_service.resume_welcome_wagon()
        else:
            npc_hosted_situation_service.suspend_welcome_wagon()