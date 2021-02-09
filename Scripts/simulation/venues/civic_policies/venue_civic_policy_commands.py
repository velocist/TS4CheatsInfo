# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\venues\civic_policies\venue_civic_policy_commands.py
# Compiled at: 2020-03-12 00:02:38
# Size of source mod 2**32: 4362 bytes
import sims4
from distributor.ops import CommunityBoardDialog
from distributor.system import Distributor
from server_commands.argument_helpers import OptionalSimInfoParam, get_optional_target, TunableInstanceParam
from sims4.common import Pack
import services

@sims4.commands.Command('civic_policy.venue.enact', pack=(Pack.EP09), command_type=(sims4.commands.CommandType.Live))
def venue_civic_policy_enact--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              services
                2  LOAD_METHOD              venue_service
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  LOAD_ATTR                source_venue
                8  STORE_FAST               'source_venue'

 L.  23        10  LOAD_FAST                'source_venue'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_TRUE     40  'to 40'

 L.  24        18  LOAD_FAST                'source_venue'
               20  LOAD_ATTR                civic_policy_provider
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_TRUE     40  'to 40'

 L.  25        28  LOAD_FAST                'source_venue'
               30  LOAD_ATTR                civic_policy_provider
               32  LOAD_METHOD              enact
               34  LOAD_FAST                'policy'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_JUMP_IF_TRUE     80  'to 80'
             40_0  COME_FROM            26  '26'
             40_1  COME_FROM            16  '16'

 L.  26        40  LOAD_GLOBAL              sims4
               42  LOAD_ATTR                commands
               44  LOAD_METHOD              automation_output
               46  LOAD_STR                 '{} not enacted'
               48  LOAD_METHOD              format
               50  LOAD_FAST                'policy'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  LOAD_FAST                '_connection'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  POP_TOP          

 L.  27        60  LOAD_GLOBAL              sims4
               62  LOAD_ATTR                commands
               64  LOAD_METHOD              cheat_output
               66  LOAD_STR                 '{} not enacted'
               68  LOAD_METHOD              format
               70  LOAD_FAST                'policy'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  LOAD_FAST                '_connection'
               76  CALL_METHOD_2         2  '2 positional arguments'
               78  POP_TOP          
             80_0  COME_FROM            38  '38'

Parse error at or near `POP_TOP' instruction at offset 78


@sims4.commands.Command('civic_policy.venue.repeal', pack=(Pack.EP09), command_type=(sims4.commands.CommandType.Live))
def venue_civic_policy_repeal--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL              services
                2  LOAD_METHOD              venue_service
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  LOAD_ATTR                source_venue
                8  STORE_FAST               'source_venue'

 L.  35        10  LOAD_FAST                'source_venue'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_TRUE     40  'to 40'

 L.  36        18  LOAD_FAST                'source_venue'
               20  LOAD_ATTR                civic_policy_provider
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_TRUE     40  'to 40'

 L.  37        28  LOAD_FAST                'source_venue'
               30  LOAD_ATTR                civic_policy_provider
               32  LOAD_METHOD              repeal
               34  LOAD_FAST                'policy'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_JUMP_IF_TRUE     80  'to 80'
             40_0  COME_FROM            26  '26'
             40_1  COME_FROM            16  '16'

 L.  38        40  LOAD_GLOBAL              sims4
               42  LOAD_ATTR                commands
               44  LOAD_METHOD              automation_output
               46  LOAD_STR                 '{} not repealed'
               48  LOAD_METHOD              format
               50  LOAD_FAST                'policy'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  LOAD_FAST                '_connection'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  POP_TOP          

 L.  39        60  LOAD_GLOBAL              sims4
               62  LOAD_ATTR                commands
               64  LOAD_METHOD              cheat_output
               66  LOAD_STR                 '{} not repealed'
               68  LOAD_METHOD              format
               70  LOAD_FAST                'policy'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  LOAD_FAST                '_connection'
               76  CALL_METHOD_2         2  '2 positional arguments'
               78  POP_TOP          
             80_0  COME_FROM            38  '38'

Parse error at or near `POP_TOP' instruction at offset 78


@sims4.commands.Command('civic_policy.venue.vote', pack=(Pack.EP09), command_type=(sims4.commands.CommandType.Live))
def venue_civic_policy_vote--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              services
                2  LOAD_METHOD              venue_service
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  LOAD_ATTR                source_venue
                8  STORE_FAST               'source_venue'

 L.  47        10  LOAD_FAST                'source_venue'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_TRUE     42  'to 42'

 L.  48        18  LOAD_FAST                'source_venue'
               20  LOAD_ATTR                civic_policy_provider
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_TRUE     42  'to 42'

 L.  49        28  LOAD_FAST                'source_venue'
               30  LOAD_ATTR                civic_policy_provider
               32  LOAD_METHOD              vote
               34  LOAD_FAST                'policy'
               36  LOAD_FAST                'count'
               38  CALL_METHOD_2         2  '2 positional arguments'
               40  POP_JUMP_IF_TRUE     62  'to 62'
             42_0  COME_FROM            26  '26'
             42_1  COME_FROM            16  '16'

 L.  50        42  LOAD_GLOBAL              sims4
               44  LOAD_ATTR                commands
               46  LOAD_METHOD              cheat_output
               48  LOAD_STR                 'Could not add vote to {}'
               50  LOAD_METHOD              format
               52  LOAD_FAST                'policy'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  LOAD_FAST                '_connection'
               58  CALL_METHOD_2         2  '2 positional arguments'
               60  POP_TOP          
             62_0  COME_FROM            40  '40'

Parse error at or near `POP_TOP' instruction at offset 60


@sims4.commands.Command('civic_policy.venue.force_end_voting', pack=(Pack.EP09), command_type=(sims4.commands.CommandType.DebugOnly))
def venue_civic_policy_force_end_voting(_connection=None):
    source_venue = services.venue_service.source_venue
    if source_venue is None:
        return False
    provider = source_venue.civic_policy_provider
    if provider is None:
        return False

    def output_enacted_policy_list():
        policies = provider.get_enacted_policies
        for policy in policies:
            sims4.commands.cheat_output'    {}'.formatpolicy_connection

    sims4.commands.cheat_output'Before Enacted Policies'_connection
    output_enacted_policy_list()
    provider.close_voting
    sims4.commands.cheat_output'After Enacted Policies'_connection
    output_enacted_policy_list()


@sims4.commands.Command('civic_policy.venue.show_community_board', pack=(Pack.EP09), command_type=(sims4.commands.CommandType.Live))
def venue_civic_policy_show_community_board(opt_sim: OptionalSimInfoParam=None, opt_target_id: int=0, _connection=None):
    street_service = services.street_service
    if street_service is None:
        sims4.commands.automation_output'Pack not loaded'_connection
        sims4.commands.cheat_output'Pack not loaded'_connection
        return
    sim_info = get_optional_target(opt_sim, _connection, target_type=OptionalSimInfoParam)
    source_venue = services.venue_service.source_venue
    if source_venue is None:
        return
    provider = source_venue.civic_policy_provider
    if provider is None:
        return
    op = CommunityBoardDialog(provider, sim_info, opt_target_id)
    Distributor.instance.add_op_with_no_ownerop