# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\gsi_handlers\object_handlers.py
# Compiled at: 2020-08-19 03:02:49
# Size of source mod 2**32: 35996 bytes
from _collections import defaultdict
import itertools, re
from event_testing.resolver import SingleObjectResolver
from gsi_handlers.gameplay_archiver import GameplayArchiver
from gsi_handlers.gsi_utils import parse_filter_to_list
from objects.components.consumable_component import ConsumptionEffects
from objects.game_object import GameObject
from routing.portals.portal_tuning import PortalFlags
from server.live_drag_tuning import LiveDragPermission
from sims4.common import Pack, get_pack_enum
from sims4.gsi.dispatcher import GsiHandler, add_cheat_schema
from sims4.gsi.schema import GsiGridSchema, GSIGlobalCheatSchema, GsiFieldVisualizers
import build_buy, gsi_handlers.gsi_utils, objects.components.types, services, sims4, tag
global_object_cheats_schema = GSIGlobalCheatSchema()
global_object_cheats_schema.add_cheat('objects.clear_lot', label='Clear Lot')
add_cheat_schema('global_object_cheats', global_object_cheats_schema)
object_manager_schema = GsiGridSchema(label='Object Manager')
object_manager_schema.add_field('mgr', label='Manager', width=1, hidden=True)
object_manager_schema.add_field('objId', label='Object Id', width=3, unique_field=True)
object_manager_schema.add_field('classStr', label='Class', width=3)
object_manager_schema.add_field('definitionStr', label='Definition', width=3)
object_manager_schema.add_field('modelStr', label='Model', width=3)
object_manager_schema.add_field('locX', label='X', width=1)
object_manager_schema.add_field('locY', label='Y', width=1)
object_manager_schema.add_field('locZ', label='Z', width=1)
object_manager_schema.add_field('on_active_lot', label='On Active Lot', width=1, hidden=True)
object_manager_schema.add_field('current_value', label='Value', width=1)
object_manager_schema.add_field('isSurface', label='Surface', width=1)
object_manager_schema.add_field('parent', label='Parent', width=2)
object_manager_schema.add_field('bb_parent', label='BB_Parent', width=2)
object_manager_schema.add_field('lockouts', label='Lockouts', width=2)
object_manager_schema.add_field('transient', label='Transient', width=1, hidden=True)
object_manager_schema.add_field('is_interactable', label='Interactable', width=1, hidden=True)
object_manager_schema.add_field('footprint', label='Footprint', width=1, hidden=True)
object_manager_schema.add_field('inventory_owner_id', label='inventory owner id', width=2, hidden=True)
object_manager_schema.add_filter('on_active_lot')
object_manager_schema.add_filter('open_street')
object_manager_schema.add_filter('inventory')
object_manager_schema.add_filter('game_objects')
object_manager_schema.add_filter('prototype_objects')
object_manager_schema.add_filter('sim_objects')
with object_manager_schema.add_view_cheat('objects.destroy', label='Delete') as (cheat):
    cheat.add_token_param('objId')
with object_manager_schema.add_view_cheat('objects.reset', label='Reset') as (cheat):
    cheat.add_token_param('objId')
with object_manager_schema.add_view_cheat('objects.focus_camera_on_object', label='Focus On Selected Object') as (cheat):
    cheat.add_token_param('objId')
with object_manager_schema.add_has_many('commodities', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('commodity', label='Commodity')
    sub_schema.add_field('value', label='value')
    sub_schema.add_field('convergence_value', label='convergence value')
    sub_schema.add_field('decay_rate', label='decay')
    sub_schema.add_field('decay_rate_modifier', label='decay modifier')
    sub_schema.add_field('change_rate', label='change rate')
with object_manager_schema.add_has_many('postures', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('interactionName', label='Interaction Name')
    sub_schema.add_field('providedPosture', label='Provided Posture')
with object_manager_schema.add_has_many('states', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('state_type', label='State')
    sub_schema.add_field('state_value', label='Value')
with object_manager_schema.add_has_many('reservations', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('reservation_sim', label='Owner', width=1)
    sub_schema.add_field('reservation_target', label='Target', width=1)
    sub_schema.add_field('reservation_type', label='Type', width=1)
    sub_schema.add_field('reservation_interaction', label='Interaction', width=1)
with object_manager_schema.add_has_many('parts', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('part_group_index', label='Part Group Index', width=0.5)
    sub_schema.add_field('part_suffix', label='Part Suffix', width=0.5)
    sub_schema.add_field('subroot_index', label='SubRoot', width=0.5)
    sub_schema.add_field('is_mirrored', label='Mirrored', width=0.5)
with object_manager_schema.add_has_many('slots', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('slot', label='Slot')
    sub_schema.add_field('children', label='Children')
with object_manager_schema.add_has_many('inventory', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('objId', label='Object Id', width=2, unique_field=True)
    sub_schema.add_field('classStr', label='Class', width=2)
    sub_schema.add_field('stack_count', label='Stack Count', width=1, type=(GsiFieldVisualizers.INT))
    sub_schema.add_field('stack_sort_order', label='Stack Sort Order', width=1, type=(GsiFieldVisualizers.INT))
    sub_schema.add_field('hidden', label='In Hidden', width=1)
with object_manager_schema.add_has_many('additional_data', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('dataId', label='Data', unique_field=True)
    sub_schema.add_field('dataValue', label='Value')
with object_manager_schema.add_has_many('object_relationships', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('relationshipNumber', label='Relationship Number', width=0.5)
    sub_schema.add_field('simValue', label='Sim', width=0.25, unique_field=True)
    sub_schema.add_field('relationshipValue', label='Relationship Value', width=0.25)
    sub_schema.add_field('relationshipStatInfo', label='Relationship Stat Info')
with object_manager_schema.add_has_many('locking_component', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('lock_type', label='Lock Type', width=0.5)
    sub_schema.add_field('lock_priority', label='Lock Priority', width=0.25)
    sub_schema.add_field('lock_side', label='Lock Side', width=0.25)
    sub_schema.add_field('should_persist', label='Should Persist', width=0.25)
    sub_schema.add_field('exceptions', label='Exceptions')
with object_manager_schema.add_has_many('awareness', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('awareness_role', label='Role', width=0.25)
    sub_schema.add_field('awareness_channel', label='Channel', width=0.25)
    sub_schema.add_field('awareness_data', label='Data', width=2)
with object_manager_schema.add_has_many('component', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('component_name', label='Name', width=0.25)
with object_manager_schema.add_has_many('live_drag', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('live_drag_data_name', label='Data', unique_field=True)
    sub_schema.add_field('live_drag_data_value', label='Value')
with object_manager_schema.add_has_many('ownership', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('ownership_household_owner', label='Household Owner')
    sub_schema.add_field('ownership_sim_owner', label='Sim Owner')
    sub_schema.add_field('ownership_crafter_sim', label='Crafter Sim')
    sub_schema.add_field('ownership_preference_sim', label='Preference Sims')
with object_manager_schema.add_has_many('walkstyles', GsiGridSchema, label='Walkstyles') as (sub_schema):
    sub_schema.add_field('walkstyle_priority', label='Priority', width=0.5)
    sub_schema.add_field('walkstyle_type', label='Style', width=0.75)
    sub_schema.add_field('walkstyle_short', label='Short Replacement', width=0.75)
    sub_schema.add_field('walkstyle_combo_replacement', label='Combo replacement', width=1)
    sub_schema.add_field('walkstyle_is_current', label='Is Current', width=0.25)
    sub_schema.add_field('walkstyle_is_default', label='Is Default', width=0.25)
with object_manager_schema.add_has_many('portals', GsiGridSchema, label='Routable Portal Flags') as (sub_schema):
    sub_schema.add_field('portal_flag', label='Flags')
INFINITY_SYMBOL = '∞'

def _get_model_name(cur_obj):
    model_name = 'Unexpected Repr'
    model = getattr(cur_obj, 'model', None)
    if model is not None:
        split_model_name = re.split('[\\(\\)]', str(cur_obj.model))
        if len(split_model_name) > 1:
            model_name = split_model_name[1]
    return model_name


@GsiHandler('object_manager', object_manager_schema)
def generate_object_manager_data--- This code section failed: ---

 L. 167         0  LOAD_GLOBAL              parse_filter_to_list
                2  LOAD_FAST                'filter'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'filter_list'

 L. 168         8  BUILD_MAP_0           0 
               10  STORE_FAST               'lockout_data'

 L. 169        12  LOAD_GLOBAL              defaultdict
               14  LOAD_GLOBAL              list
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  STORE_FAST               'obj_preference_data'

 L. 170        20  LOAD_GLOBAL              services
               22  LOAD_METHOD              get_zone
               24  LOAD_FAST                'zone_id'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  STORE_FAST               'zone'

 L. 171        30  LOAD_GLOBAL              services
               32  LOAD_METHOD              sim_info_manager
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  STORE_FAST               'sim_info_manager'

 L. 172        38  SETUP_LOOP          210  'to 210'
               40  LOAD_GLOBAL              list
               42  LOAD_FAST                'sim_info_manager'
               44  LOAD_ATTR                objects
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  GET_ITER         
             50_0  COME_FROM            68  '68'
               50  FOR_ITER            208  'to 208'
               52  STORE_FAST               'sim_info'

 L. 173        54  LOAD_FAST                'sim_info'
               56  LOAD_METHOD              get_sim_instance
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  STORE_FAST               'sim'

 L. 174        62  LOAD_FAST                'sim'
               64  LOAD_CONST               None
               66  COMPARE_OP               is-not
               68  POP_JUMP_IF_FALSE    50  'to 50'

 L. 175        70  SETUP_LOOP          118  'to 118'
               72  LOAD_FAST                'sim'
               74  LOAD_METHOD              get_lockouts_gen
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  GET_ITER         
               80  FOR_ITER            116  'to 116'
               82  UNPACK_SEQUENCE_2     2 
               84  STORE_FAST               'obj'
               86  STORE_FAST               'time'

 L. 176        88  LOAD_FAST                'lockout_data'
               90  LOAD_METHOD              setdefault
               92  LOAD_FAST                'obj'
               94  BUILD_LIST_0          0 
               96  CALL_METHOD_2         2  '2 positional arguments'
               98  STORE_FAST               'lockouts'

 L. 177       100  LOAD_FAST                'lockouts'
              102  LOAD_METHOD              append
              104  LOAD_FAST                'sim'
              106  LOAD_FAST                'time'
              108  BUILD_TUPLE_2         2 
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          
              114  JUMP_BACK            80  'to 80'
              116  POP_BLOCK        
            118_0  COME_FROM_LOOP       70  '70'

 L. 178       118  SETUP_LOOP          162  'to 162'
              120  LOAD_FAST                'sim'
              122  LOAD_ATTR                sim_info
              124  LOAD_ATTR                autonomy_scoring_preferences
              126  LOAD_METHOD              items
              128  CALL_METHOD_0         0  '0 positional arguments'
              130  GET_ITER         
              132  FOR_ITER            160  'to 160'
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               '_'
              138  STORE_FAST               'obj_id'

 L. 179       140  LOAD_FAST                'obj_preference_data'
              142  LOAD_FAST                'obj_id'
              144  BINARY_SUBSCR    
              146  LOAD_METHOD              append
              148  LOAD_FAST                'sim'
              150  LOAD_ATTR                sim_info
              152  LOAD_ATTR                id
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          
              158  JUMP_BACK           132  'to 132'
              160  POP_BLOCK        
            162_0  COME_FROM_LOOP      118  '118'

 L. 180       162  SETUP_LOOP          206  'to 206'
              164  LOAD_FAST                'sim'
              166  LOAD_ATTR                sim_info
              168  LOAD_ATTR                autonomy_use_preferences
              170  LOAD_METHOD              items
              172  CALL_METHOD_0         0  '0 positional arguments'
              174  GET_ITER         
              176  FOR_ITER            204  'to 204'
              178  UNPACK_SEQUENCE_2     2 
              180  STORE_FAST               '_'
              182  STORE_FAST               'obj_id'

 L. 181       184  LOAD_FAST                'obj_preference_data'
              186  LOAD_FAST                'obj_id'
              188  BINARY_SUBSCR    
              190  LOAD_METHOD              append
              192  LOAD_FAST                'sim'
              194  LOAD_ATTR                sim_info
              196  LOAD_ATTR                id
              198  CALL_METHOD_1         1  '1 positional argument'
              200  POP_TOP          
              202  JUMP_BACK           176  'to 176'
              204  POP_BLOCK        
            206_0  COME_FROM_LOOP      162  '162'
              206  JUMP_BACK            50  'to 50'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP       38  '38'

 L. 182       210  BUILD_LIST_0          0 
              212  STORE_FAST               'all_object_data'

 L. 183   214_216  SETUP_LOOP         3656  'to 3656'
              218  LOAD_GLOBAL              list
              220  LOAD_GLOBAL              itertools
              222  LOAD_METHOD              chain
              224  LOAD_FAST                'zone'
              226  LOAD_ATTR                object_manager
              228  LOAD_ATTR                objects

 L. 184       230  LOAD_FAST                'zone'
              232  LOAD_ATTR                prop_manager
              234  LOAD_ATTR                objects

 L. 185       236  LOAD_FAST                'zone'
              238  LOAD_ATTR                inventory_manager
              240  LOAD_ATTR                objects
              242  CALL_METHOD_3         3  '3 positional arguments'
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  GET_ITER         
            248_0  COME_FROM           416  '416'
            248_1  COME_FROM           412  '412'
          248_250  FOR_ITER           3654  'to 3654'
              252  STORE_FAST               'cur_obj'

 L. 186       254  LOAD_GLOBAL              gsi_handlers
              256  LOAD_ATTR                gsi_utils
              258  LOAD_METHOD              format_object_name
              260  LOAD_FAST                'cur_obj'
              262  CALL_METHOD_1         1  '1 positional argument'
              264  STORE_FAST               'class_str'

 L. 187       266  LOAD_GLOBAL              str
              268  LOAD_FAST                'cur_obj'
              270  LOAD_ATTR                definition
              272  LOAD_ATTR                name
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  STORE_FAST               'definition_str'

 L. 188       278  LOAD_GLOBAL              hasattr
              280  LOAD_FAST                'cur_obj'
              282  LOAD_STR                 'is_on_active_lot'
              284  CALL_FUNCTION_2       2  '2 positional arguments'
          286_288  POP_JUMP_IF_FALSE   298  'to 298'
              290  LOAD_FAST                'cur_obj'
              292  LOAD_METHOD              is_on_active_lot
              294  CALL_METHOD_0         0  '0 positional arguments'
              296  JUMP_FORWARD        300  'to 300'
            298_0  COME_FROM           286  '286'
              298  LOAD_CONST               False
            300_0  COME_FROM           296  '296'
              300  STORE_FAST               'on_active_lot'

 L. 190       302  LOAD_FAST                'filter_list'
              304  LOAD_CONST               None
              306  COMPARE_OP               is
          308_310  POP_JUMP_IF_TRUE    418  'to 418'

 L. 191       312  LOAD_STR                 'sim_objects'
              314  LOAD_FAST                'filter_list'
              316  COMPARE_OP               in
          318_320  POP_JUMP_IF_FALSE   330  'to 330'
              322  LOAD_FAST                'cur_obj'
              324  LOAD_ATTR                is_sim
          326_328  POP_JUMP_IF_TRUE    418  'to 418'
            330_0  COME_FROM           318  '318'

 L. 192       330  LOAD_STR                 'inventory'
              332  LOAD_FAST                'filter_list'
              334  COMPARE_OP               in
          336_338  POP_JUMP_IF_FALSE   350  'to 350'
              340  LOAD_FAST                'cur_obj'
              342  LOAD_METHOD              is_in_inventory
              344  CALL_METHOD_0         0  '0 positional arguments'
          346_348  POP_JUMP_IF_TRUE    418  'to 418'
            350_0  COME_FROM           336  '336'

 L. 193       350  LOAD_STR                 'prototype_objects'
              352  LOAD_FAST                'filter_list'
              354  COMPARE_OP               in
          356_358  POP_JUMP_IF_FALSE   370  'to 370'
              360  LOAD_FAST                'class_str'
              362  LOAD_STR                 'prototype'
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_TRUE    418  'to 418'
            370_0  COME_FROM           356  '356'

 L. 194       370  LOAD_STR                 'game_objects'
              372  LOAD_FAST                'filter_list'
              374  COMPARE_OP               in
          376_378  POP_JUMP_IF_FALSE   390  'to 390'
              380  LOAD_FAST                'class_str'
              382  LOAD_STR                 'prototype'
              384  COMPARE_OP               !=
          386_388  POP_JUMP_IF_TRUE    418  'to 418'
            390_0  COME_FROM           376  '376'

 L. 195       390  LOAD_STR                 'open_street'
              392  LOAD_FAST                'filter_list'
              394  COMPARE_OP               in
          396_398  POP_JUMP_IF_FALSE   406  'to 406'
              400  LOAD_FAST                'on_active_lot'
          402_404  POP_JUMP_IF_FALSE   418  'to 418'
            406_0  COME_FROM           396  '396'

 L. 196       406  LOAD_STR                 'on_active_lot'
              408  LOAD_FAST                'filter_list'
              410  COMPARE_OP               in
              412  POP_JUMP_IF_FALSE   248  'to 248'
              414  LOAD_FAST                'on_active_lot'
              416  POP_JUMP_IF_FALSE   248  'to 248'
            418_0  COME_FROM           402  '402'
            418_1  COME_FROM           386  '386'
            418_2  COME_FROM           366  '366'
            418_3  COME_FROM           346  '346'
            418_4  COME_FROM           326  '326'
            418_5  COME_FROM           308  '308'

 L. 197       418  LOAD_FAST                'cur_obj'
              420  LOAD_ATTR                position
              422  STORE_FAST               'obj_loc'

 L. 198       424  LOAD_GLOBAL              _get_model_name
              426  LOAD_FAST                'cur_obj'
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  STORE_FAST               'model_name'

 L. 201       432  LOAD_GLOBAL              str
              434  LOAD_FAST                'cur_obj'
              436  LOAD_ATTR                manager
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  LOAD_METHOD              replace
              442  LOAD_STR                 '_manager'
              444  LOAD_STR                 ''
              446  CALL_METHOD_2         2  '2 positional arguments'

 L. 202       448  LOAD_GLOBAL              hex
              450  LOAD_FAST                'cur_obj'
              452  LOAD_ATTR                id
              454  CALL_FUNCTION_1       1  '1 positional argument'

 L. 203       456  LOAD_FAST                'class_str'

 L. 204       458  LOAD_FAST                'definition_str'

 L. 205       460  LOAD_FAST                'model_name'

 L. 206       462  LOAD_GLOBAL              round
              464  LOAD_FAST                'obj_loc'
              466  LOAD_ATTR                x
              468  LOAD_CONST               3
              470  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 207       472  LOAD_GLOBAL              round
              474  LOAD_FAST                'obj_loc'
              476  LOAD_ATTR                y
              478  LOAD_CONST               3
              480  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 208       482  LOAD_GLOBAL              round
              484  LOAD_FAST                'obj_loc'
              486  LOAD_ATTR                z
              488  LOAD_CONST               3
              490  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 209       492  LOAD_GLOBAL              str
              494  LOAD_FAST                'on_active_lot'
              496  CALL_FUNCTION_1       1  '1 positional argument'

 L. 210       498  LOAD_FAST                'cur_obj'
              500  LOAD_ATTR                current_value

 L. 211       502  LOAD_GLOBAL              getattr
              504  LOAD_FAST                'cur_obj'
              506  LOAD_STR                 'interactable'
              508  LOAD_CONST               False
              510  CALL_FUNCTION_3       3  '3 positional arguments'
          512_514  POP_JUMP_IF_FALSE   520  'to 520'
              516  LOAD_STR                 'x'
              518  JUMP_FORWARD        522  'to 522'
            520_0  COME_FROM           512  '512'
              520  LOAD_STR                 ''
            522_0  COME_FROM           518  '518'

 L. 212       522  LOAD_GLOBAL              getattr
              524  LOAD_FAST                'cur_obj'
              526  LOAD_STR                 'footprint_polygon'
              528  LOAD_CONST               None
              530  CALL_FUNCTION_3       3  '3 positional arguments'
          532_534  POP_JUMP_IF_FALSE   546  'to 546'
              536  LOAD_GLOBAL              str
              538  LOAD_FAST                'cur_obj'
              540  LOAD_ATTR                footprint_polygon
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  JUMP_FORWARD        548  'to 548'
            546_0  COME_FROM           532  '532'
              546  LOAD_STR                 ''
            548_0  COME_FROM           544  '544'
              548  LOAD_CONST               ('mgr', 'objId', 'classStr', 'definitionStr', 'modelStr', 'locX', 'locY', 'locZ', 'on_active_lot', 'current_value', 'is_interactable', 'footprint')
              550  BUILD_CONST_KEY_MAP_12    12 
              552  STORE_FAST               'ret_dict'

 L. 215       554  BUILD_LIST_0          0 
              556  LOAD_FAST                'ret_dict'
              558  LOAD_STR                 'additional_data'
              560  STORE_SUBSCR     

 L. 217       562  LOAD_FAST                'cur_obj'
              564  LOAD_ATTR                location
              566  LOAD_CONST               None
              568  COMPARE_OP               is-not
          570_572  POP_JUMP_IF_FALSE   600  'to 600'

 L. 218       574  LOAD_FAST                'ret_dict'
              576  LOAD_STR                 'additional_data'
              578  BINARY_SUBSCR    
              580  LOAD_METHOD              append
              582  LOAD_STR                 'Location'
              584  LOAD_GLOBAL              str
              586  LOAD_FAST                'cur_obj'
              588  LOAD_ATTR                location
              590  CALL_FUNCTION_1       1  '1 positional argument'
              592  LOAD_CONST               ('dataId', 'dataValue')
              594  BUILD_CONST_KEY_MAP_2     2 
              596  CALL_METHOD_1         1  '1 positional argument'
              598  POP_TOP          
            600_0  COME_FROM           570  '570'

 L. 220       600  LOAD_FAST                'cur_obj'
              602  LOAD_ATTR                visibility
              604  LOAD_CONST               None
              606  COMPARE_OP               is-not
          608_610  POP_JUMP_IF_FALSE   666  'to 666'

 L. 221       612  LOAD_FAST                'ret_dict'
              614  LOAD_STR                 'additional_data'
              616  BINARY_SUBSCR    
              618  LOAD_METHOD              append
              620  LOAD_STR                 'Visibility'
              622  LOAD_GLOBAL              str
              624  LOAD_FAST                'cur_obj'
              626  LOAD_ATTR                visibility
              628  LOAD_ATTR                visibility
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  LOAD_CONST               ('dataId', 'dataValue')
              634  BUILD_CONST_KEY_MAP_2     2 
              636  CALL_METHOD_1         1  '1 positional argument'
              638  POP_TOP          

 L. 222       640  LOAD_FAST                'ret_dict'
              642  LOAD_STR                 'additional_data'
              644  BINARY_SUBSCR    
              646  LOAD_METHOD              append
              648  LOAD_STR                 'Opacity'
              650  LOAD_GLOBAL              str
              652  LOAD_FAST                'cur_obj'
              654  LOAD_ATTR                opacity
              656  CALL_FUNCTION_1       1  '1 positional argument'
              658  LOAD_CONST               ('dataId', 'dataValue')
              660  BUILD_CONST_KEY_MAP_2     2 
              662  CALL_METHOD_1         1  '1 positional argument'
              664  POP_TOP          
            666_0  COME_FROM           608  '608'

 L. 224       666  LOAD_FAST                'ret_dict'
              668  LOAD_STR                 'additional_data'
              670  BINARY_SUBSCR    
              672  LOAD_METHOD              append
              674  LOAD_STR                 'Model State'
              676  LOAD_GLOBAL              str
              678  LOAD_FAST                'cur_obj'
              680  LOAD_ATTR                state_index
              682  CALL_FUNCTION_1       1  '1 positional argument'
              684  LOAD_CONST               ('dataId', 'dataValue')
              686  BUILD_CONST_KEY_MAP_2     2 
              688  CALL_METHOD_1         1  '1 positional argument'
              690  POP_TOP          

 L. 226       692  LOAD_GLOBAL              hasattr
              694  LOAD_FAST                'cur_obj'
              696  LOAD_STR                 'commodity_flags'
              698  CALL_FUNCTION_2       2  '2 positional arguments'
          700_702  POP_JUMP_IF_FALSE   726  'to 726'

 L. 227       704  LOAD_GLOBAL              sorted
              706  LOAD_LISTCOMP            '<code_object <listcomp>>'
              708  LOAD_STR                 'generate_object_manager_data.<locals>.<listcomp>'
              710  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              712  LOAD_FAST                'cur_obj'
              714  LOAD_ATTR                commodity_flags
              716  GET_ITER         
              718  CALL_FUNCTION_1       1  '1 positional argument'
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  STORE_FAST               'commodity_flags_by_name'
              724  JUMP_FORWARD        730  'to 730'
            726_0  COME_FROM           700  '700'

 L. 229       726  BUILD_LIST_0          0 
              728  STORE_FAST               'commodity_flags_by_name'
            730_0  COME_FROM           724  '724'

 L. 230       730  LOAD_FAST                'ret_dict'
              732  LOAD_STR                 'additional_data'
              734  BINARY_SUBSCR    
              736  LOAD_METHOD              append
              738  LOAD_STR                 'Commodity Flags'
              740  LOAD_STR                 '\n'
              742  LOAD_METHOD              join
              744  LOAD_FAST                'commodity_flags_by_name'
              746  CALL_METHOD_1         1  '1 positional argument'
              748  LOAD_CONST               ('dataId', 'dataValue')
              750  BUILD_CONST_KEY_MAP_2     2 
              752  CALL_METHOD_1         1  '1 positional argument'
              754  POP_TOP          

 L. 232       756  LOAD_FAST                'cur_obj'
              758  LOAD_ATTR                parent
              760  STORE_FAST               'parent'

 L. 233       762  LOAD_FAST                'cur_obj'
              764  LOAD_ATTR                bb_parent
              766  STORE_FAST               'bb_parent'

 L. 234       768  LOAD_FAST                'parent'
              770  LOAD_CONST               None
              772  COMPARE_OP               is-not
          774_776  POP_JUMP_IF_FALSE   844  'to 844'

 L. 235       778  LOAD_GLOBAL              gsi_handlers
              780  LOAD_ATTR                gsi_utils
              782  LOAD_METHOD              format_object_name
              784  LOAD_FAST                'parent'
              786  CALL_METHOD_1         1  '1 positional argument'
              788  LOAD_FAST                'ret_dict'
              790  LOAD_STR                 'parent'
              792  STORE_SUBSCR     

 L. 236       794  LOAD_FAST                'ret_dict'
              796  LOAD_STR                 'additional_data'
              798  BINARY_SUBSCR    
              800  LOAD_METHOD              append
              802  LOAD_STR                 'Parent Id'
              804  LOAD_GLOBAL              hex
              806  LOAD_FAST                'parent'
              808  LOAD_ATTR                id
              810  CALL_FUNCTION_1       1  '1 positional argument'
              812  LOAD_CONST               ('dataId', 'dataValue')
              814  BUILD_CONST_KEY_MAP_2     2 
              816  CALL_METHOD_1         1  '1 positional argument'
              818  POP_TOP          

 L. 237       820  LOAD_FAST                'ret_dict'
              822  LOAD_STR                 'additional_data'
              824  BINARY_SUBSCR    
              826  LOAD_METHOD              append
              828  LOAD_STR                 'Parent Slot'
              830  LOAD_FAST                'cur_obj'
              832  LOAD_ATTR                parent_slot
              834  LOAD_ATTR                slot_name_or_hash
              836  LOAD_CONST               ('dataId', 'dataValue')
              838  BUILD_CONST_KEY_MAP_2     2 
              840  CALL_METHOD_1         1  '1 positional argument'
              842  POP_TOP          
            844_0  COME_FROM           774  '774'

 L. 238       844  LOAD_FAST                'bb_parent'
              846  LOAD_CONST               None
              848  COMPARE_OP               is-not
          850_852  POP_JUMP_IF_FALSE   870  'to 870'

 L. 239       854  LOAD_GLOBAL              gsi_handlers
              856  LOAD_ATTR                gsi_utils
              858  LOAD_METHOD              format_object_name
              860  LOAD_FAST                'bb_parent'
              862  CALL_METHOD_1         1  '1 positional argument'
              864  LOAD_FAST                'ret_dict'
              866  LOAD_STR                 'bb_parent'
              868  STORE_SUBSCR     
            870_0  COME_FROM           850  '850'

 L. 241       870  LOAD_FAST                'cur_obj'
              872  LOAD_ATTR                focus_component
              874  STORE_FAST               'focus_component'

 L. 242       876  LOAD_FAST                'focus_component'
              878  LOAD_CONST               None
              880  COMPARE_OP               is-not
          882_884  POP_JUMP_IF_FALSE   940  'to 940'

 L. 243       886  LOAD_FAST                'ret_dict'
              888  LOAD_STR                 'additional_data'
              890  BINARY_SUBSCR    
              892  LOAD_METHOD              append

 L. 244       894  LOAD_STR                 'Focus Bone'

 L. 245       896  LOAD_GLOBAL              str
              898  LOAD_FAST                'focus_component'
              900  LOAD_METHOD              get_focus_bone
              902  CALL_METHOD_0         0  '0 positional arguments'
              904  CALL_FUNCTION_1       1  '1 positional argument'
              906  LOAD_CONST               ('dataId', 'dataValue')
              908  BUILD_CONST_KEY_MAP_2     2 
              910  CALL_METHOD_1         1  '1 positional argument'
              912  POP_TOP          

 L. 247       914  LOAD_FAST                'ret_dict'
              916  LOAD_STR                 'additional_data'
              918  BINARY_SUBSCR    
              920  LOAD_METHOD              append

 L. 248       922  LOAD_STR                 'Focus Score'

 L. 249       924  LOAD_GLOBAL              str
              926  LOAD_FAST                'focus_component'
              928  LOAD_ATTR                focus_score
              930  CALL_FUNCTION_1       1  '1 positional argument'
              932  LOAD_CONST               ('dataId', 'dataValue')
              934  BUILD_CONST_KEY_MAP_2     2 
              936  CALL_METHOD_1         1  '1 positional argument'
              938  POP_TOP          
            940_0  COME_FROM           882  '882'

 L. 252       940  LOAD_FAST                'cur_obj'
              942  LOAD_ATTR                consumable_component
              944  STORE_FAST               'consumable_component'

 L. 253       946  LOAD_FAST                'consumable_component'
              948  LOAD_CONST               None
              950  COMPARE_OP               is-not
          952_954  POP_JUMP_IF_FALSE  1040  'to 1040'

 L. 254       956  LOAD_FAST                'ret_dict'
              958  LOAD_STR                 'additional_data'
              960  BINARY_SUBSCR    
              962  LOAD_METHOD              append
              964  LOAD_STR                 'Base Calories'
              966  LOAD_GLOBAL              str
              968  LOAD_FAST                'consumable_component'
              970  LOAD_ATTR                fitness_info
              972  LOAD_ATTR                calories
              974  CALL_FUNCTION_1       1  '1 positional argument'
              976  LOAD_CONST               ('dataId', 'dataValue')
              978  BUILD_CONST_KEY_MAP_2     2 
              980  CALL_METHOD_1         1  '1 positional argument'
              982  POP_TOP          

 L. 255       984  LOAD_FAST                'ret_dict'
              986  LOAD_STR                 'additional_data'
              988  BINARY_SUBSCR    
              990  LOAD_METHOD              append
              992  LOAD_STR                 'Consumption Effect'
              994  LOAD_GLOBAL              str
              996  LOAD_FAST                'consumable_component'
              998  LOAD_ATTR                fitness_info
             1000  LOAD_ATTR                consumption_effect
             1002  CALL_FUNCTION_1       1  '1 positional argument'
             1004  LOAD_CONST               ('dataId', 'dataValue')
             1006  BUILD_CONST_KEY_MAP_2     2 
             1008  CALL_METHOD_1         1  '1 positional argument'
             1010  POP_TOP          

 L. 256      1012  LOAD_FAST                'ret_dict'
             1014  LOAD_STR                 'additional_data'
             1016  BINARY_SUBSCR    
             1018  LOAD_METHOD              append
             1020  LOAD_STR                 'Actual Calories'
             1022  LOAD_GLOBAL              str
             1024  LOAD_FAST                'consumable_component'
             1026  LOAD_METHOD              get_calorie_amount
             1028  CALL_METHOD_0         0  '0 positional arguments'
             1030  CALL_FUNCTION_1       1  '1 positional argument'
             1032  LOAD_CONST               ('dataId', 'dataValue')
             1034  BUILD_CONST_KEY_MAP_2     2 
             1036  CALL_METHOD_1         1  '1 positional argument'
             1038  POP_TOP          
           1040_0  COME_FROM           952  '952'

 L. 258      1040  BUILD_LIST_0          0 
             1042  LOAD_FAST                'ret_dict'
             1044  LOAD_STR                 'object_relationships'
             1046  STORE_SUBSCR     

 L. 259      1048  LOAD_FAST                'cur_obj'
             1050  LOAD_ATTR                objectrelationship_component
             1052  LOAD_CONST               None
             1054  COMPARE_OP               is-not
         1056_1058  POP_JUMP_IF_FALSE  1352  'to 1352'

 L. 260      1060  LOAD_GLOBAL              list
             1062  LOAD_FAST                'cur_obj'
             1064  LOAD_ATTR                objectrelationship_component
             1066  LOAD_ATTR                relationships
             1068  LOAD_METHOD              keys
             1070  CALL_METHOD_0         0  '0 positional arguments'
             1072  CALL_FUNCTION_1       1  '1 positional argument'
             1074  STORE_FAST               'sims_in_relationships'

 L. 261      1076  LOAD_GLOBAL              len
             1078  LOAD_FAST                'sims_in_relationships'
             1080  CALL_FUNCTION_1       1  '1 positional argument'
             1082  LOAD_CONST               0
             1084  COMPARE_OP               ==
         1086_1088  POP_JUMP_IF_FALSE  1118  'to 1118'

 L. 262      1090  LOAD_STR                 "This object hasn't formed any relationships, but could if it wanted to."

 L. 263      1092  LOAD_STR                 ''

 L. 264      1094  LOAD_STR                 ''

 L. 265      1096  LOAD_STR                 ''
             1098  LOAD_CONST               ('relationshipNumber', 'simValue', 'relationshipValue', 'relationshipStatInfo')
             1100  BUILD_CONST_KEY_MAP_4     4 
             1102  STORE_FAST               'relationship_entry'

 L. 266      1104  LOAD_FAST                'ret_dict'
             1106  LOAD_STR                 'object_relationships'
             1108  BINARY_SUBSCR    
             1110  LOAD_METHOD              append
             1112  LOAD_FAST                'relationship_entry'
             1114  CALL_METHOD_1         1  '1 positional argument'
             1116  POP_TOP          
           1118_0  COME_FROM          1086  '1086'

 L. 268      1118  SETUP_LOOP         1350  'to 1350'
             1120  LOAD_GLOBAL              enumerate
             1122  LOAD_FAST                'sims_in_relationships'
             1124  CALL_FUNCTION_1       1  '1 positional argument'
             1126  GET_ITER         
             1128  FOR_ITER           1348  'to 1348'
             1130  UNPACK_SEQUENCE_2     2 
             1132  STORE_FAST               'sim_number'
             1134  STORE_FAST               'sim_id'

 L. 269      1136  LOAD_GLOBAL              services
             1138  LOAD_METHOD              sim_info_manager
             1140  CALL_METHOD_0         0  '0 positional arguments'
             1142  LOAD_METHOD              get
             1144  LOAD_FAST                'sim_id'
             1146  CALL_METHOD_1         1  '1 positional argument'
             1148  STORE_FAST               'sim'

 L. 270      1150  LOAD_FAST                'sim'
             1152  LOAD_CONST               None
             1154  COMPARE_OP               is
         1156_1158  POP_JUMP_IF_FALSE  1170  'to 1170'

 L. 271      1160  LOAD_GLOBAL              str
             1162  LOAD_FAST                'sim_id'
             1164  CALL_FUNCTION_1       1  '1 positional argument'
             1166  STORE_FAST               'sim_name'
             1168  JUMP_FORWARD       1176  'to 1176'
           1170_0  COME_FROM          1156  '1156'

 L. 273      1170  LOAD_FAST                'sim'
             1172  LOAD_ATTR                full_name
             1174  STORE_FAST               'sim_name'
           1176_0  COME_FROM          1168  '1168'

 L. 275      1176  LOAD_GLOBAL              str
             1178  LOAD_FAST                'sim_number'
             1180  LOAD_CONST               1
             1182  BINARY_ADD       
             1184  CALL_FUNCTION_1       1  '1 positional argument'
             1186  LOAD_STR                 ' out of '
             1188  BINARY_ADD       
             1190  STORE_FAST               'relationship_number_value'

 L. 276      1192  LOAD_FAST                'cur_obj'
             1194  LOAD_ATTR                objectrelationship_component
             1196  LOAD_METHOD              get_number_of_allowed_relationships
             1198  CALL_METHOD_0         0  '0 positional arguments'
             1200  STORE_FAST               'number_of_allowed_relationships'

 L. 277      1202  LOAD_FAST                'number_of_allowed_relationships'
             1204  LOAD_CONST               None
             1206  COMPARE_OP               is
         1208_1210  POP_JUMP_IF_FALSE  1222  'to 1222'

 L. 278      1212  LOAD_FAST                'relationship_number_value'
             1214  LOAD_GLOBAL              INFINITY_SYMBOL
             1216  INPLACE_ADD      
             1218  STORE_FAST               'relationship_number_value'
             1220  JUMP_FORWARD       1234  'to 1234'
           1222_0  COME_FROM          1208  '1208'

 L. 280      1222  LOAD_FAST                'relationship_number_value'
             1224  LOAD_GLOBAL              str
             1226  LOAD_FAST                'number_of_allowed_relationships'
             1228  CALL_FUNCTION_1       1  '1 positional argument'
             1230  INPLACE_ADD      
             1232  STORE_FAST               'relationship_number_value'
           1234_0  COME_FROM          1220  '1220'

 L. 282      1234  LOAD_FAST                'cur_obj'
             1236  LOAD_ATTR                objectrelationship_component
             1238  LOAD_METHOD              get_relationship_value
             1240  LOAD_FAST                'sim_id'
             1242  CALL_METHOD_1         1  '1 positional argument'
             1244  STORE_FAST               'relationship_value'

 L. 283      1246  LOAD_GLOBAL              str
             1248  LOAD_FAST                'relationship_value'
             1250  CALL_FUNCTION_1       1  '1 positional argument'
             1252  STORE_FAST               'relationship_str'

 L. 285      1254  LOAD_STR                 'Max: '
             1256  LOAD_GLOBAL              str
             1258  LOAD_FAST                'cur_obj'
             1260  LOAD_ATTR                objectrelationship_component
             1262  LOAD_METHOD              get_relationship_max_value
             1264  CALL_METHOD_0         0  '0 positional arguments'
             1266  CALL_FUNCTION_1       1  '1 positional argument'
             1268  BINARY_ADD       
             1270  STORE_FAST               'relationship_info_str'

 L. 286      1272  LOAD_FAST                'relationship_info_str'
             1274  LOAD_STR                 ' Min: '
             1276  LOAD_GLOBAL              str
             1278  LOAD_FAST                'cur_obj'
             1280  LOAD_ATTR                objectrelationship_component
             1282  LOAD_METHOD              get_relationship_min_value
             1284  CALL_METHOD_0         0  '0 positional arguments'
             1286  CALL_FUNCTION_1       1  '1 positional argument'
             1288  BINARY_ADD       
             1290  INPLACE_ADD      
             1292  STORE_FAST               'relationship_info_str'

 L. 287      1294  LOAD_FAST                'relationship_info_str'
             1296  LOAD_STR                 ' Initial: '
             1298  LOAD_GLOBAL              str
             1300  LOAD_FAST                'cur_obj'
             1302  LOAD_ATTR                objectrelationship_component
             1304  LOAD_METHOD              get_relationship_initial_value
             1306  CALL_METHOD_0         0  '0 positional arguments'
             1308  CALL_FUNCTION_1       1  '1 positional argument'
             1310  BINARY_ADD       
             1312  INPLACE_ADD      
             1314  STORE_FAST               'relationship_info_str'

 L. 289      1316  LOAD_FAST                'relationship_number_value'

 L. 290      1318  LOAD_FAST                'sim_name'

 L. 291      1320  LOAD_FAST                'relationship_str'

 L. 292      1322  LOAD_FAST                'relationship_info_str'
             1324  LOAD_CONST               ('relationshipNumber', 'simValue', 'relationshipValue', 'relationshipStatInfo')
             1326  BUILD_CONST_KEY_MAP_4     4 
             1328  STORE_FAST               'relationship_entry'

 L. 293      1330  LOAD_FAST                'ret_dict'
             1332  LOAD_STR                 'object_relationships'
             1334  BINARY_SUBSCR    
             1336  LOAD_METHOD              append
             1338  LOAD_FAST                'relationship_entry'
             1340  CALL_METHOD_1         1  '1 positional argument'
             1342  POP_TOP          
         1344_1346  JUMP_BACK          1128  'to 1128'
             1348  POP_BLOCK        
           1350_0  COME_FROM_LOOP     1118  '1118'
             1350  JUMP_FORWARD       1380  'to 1380'
           1352_0  COME_FROM          1056  '1056'

 L. 295      1352  LOAD_STR                 'This object has no capacity for love.'

 L. 296      1354  LOAD_STR                 ''

 L. 297      1356  LOAD_STR                 ''

 L. 298      1358  LOAD_STR                 ''
             1360  LOAD_CONST               ('relationshipNumber', 'simValue', 'relationshipValue', 'relationshipStatInfo')
             1362  BUILD_CONST_KEY_MAP_4     4 
             1364  STORE_FAST               'relationship_entry'

 L. 299      1366  LOAD_FAST                'ret_dict'
             1368  LOAD_STR                 'object_relationships'
             1370  BINARY_SUBSCR    
             1372  LOAD_METHOD              append
             1374  LOAD_FAST                'relationship_entry'
             1376  CALL_METHOD_1         1  '1 positional argument'
             1378  POP_TOP          
           1380_0  COME_FROM          1350  '1350'

 L. 301      1380  LOAD_FAST                'cur_obj'
             1382  LOAD_METHOD              is_surface
             1384  CALL_METHOD_0         0  '0 positional arguments'
             1386  LOAD_FAST                'ret_dict'
             1388  LOAD_STR                 'isSurface'
             1390  STORE_SUBSCR     

 L. 302      1392  LOAD_FAST                'cur_obj'
             1394  LOAD_FAST                'lockout_data'
             1396  COMPARE_OP               in
         1398_1400  POP_JUMP_IF_FALSE  1430  'to 1430'

 L. 303      1402  LOAD_GENEXPR             '<code_object <genexpr>>'
             1404  LOAD_STR                 'generate_object_manager_data.<locals>.<genexpr>'
             1406  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1408  LOAD_FAST                'lockouts'
             1410  GET_ITER         
             1412  CALL_FUNCTION_1       1  '1 positional argument'
             1414  STORE_FAST               'lockouts'

 L. 304      1416  LOAD_STR                 ', '
             1418  LOAD_METHOD              join
             1420  LOAD_FAST                'lockouts'
             1422  CALL_METHOD_1         1  '1 positional argument'
             1424  LOAD_FAST                'ret_dict'
             1426  LOAD_STR                 'lockouts'
             1428  STORE_SUBSCR     
           1430_0  COME_FROM          1398  '1398'

 L. 306      1430  BUILD_LIST_0          0 
             1432  LOAD_FAST                'ret_dict'
             1434  LOAD_STR                 'states'
             1436  STORE_SUBSCR     

 L. 307      1438  LOAD_FAST                'cur_obj'
             1440  LOAD_ATTR                state_component
         1442_1444  POP_JUMP_IF_FALSE  1504  'to 1504'

 L. 308      1446  SETUP_LOOP         1504  'to 1504'
             1448  LOAD_FAST                'cur_obj'
             1450  LOAD_ATTR                state_component
             1452  LOAD_METHOD              items
             1454  CALL_METHOD_0         0  '0 positional arguments'
             1456  GET_ITER         
             1458  FOR_ITER           1502  'to 1502'
             1460  UNPACK_SEQUENCE_2     2 
             1462  STORE_FAST               'state_type'
             1464  STORE_FAST               'state_value'

 L. 310      1466  LOAD_GLOBAL              str
             1468  LOAD_FAST                'state_type'
             1470  CALL_FUNCTION_1       1  '1 positional argument'

 L. 311      1472  LOAD_GLOBAL              str
             1474  LOAD_FAST                'state_value'
             1476  CALL_FUNCTION_1       1  '1 positional argument'
             1478  LOAD_CONST               ('state_type', 'state_value')
             1480  BUILD_CONST_KEY_MAP_2     2 
             1482  STORE_FAST               'state_entry'

 L. 313      1484  LOAD_FAST                'ret_dict'
             1486  LOAD_STR                 'states'
             1488  BINARY_SUBSCR    
             1490  LOAD_METHOD              append
             1492  LOAD_FAST                'state_entry'
             1494  CALL_METHOD_1         1  '1 positional argument'
             1496  POP_TOP          
         1498_1500  JUMP_BACK          1458  'to 1458'
             1502  POP_BLOCK        
           1504_0  COME_FROM_LOOP     1446  '1446'
           1504_1  COME_FROM          1442  '1442'

 L. 315      1504  LOAD_GLOBAL              isinstance
             1506  LOAD_FAST                'cur_obj'
             1508  LOAD_GLOBAL              GameObject
             1510  CALL_FUNCTION_2       2  '2 positional arguments'
         1512_1514  POP_JUMP_IF_FALSE  3642  'to 3642'

 L. 316      1516  LOAD_STR                 'None'
             1518  STORE_FAST               'users'

 L. 317      1520  LOAD_FAST                'cur_obj'
             1522  LOAD_ATTR                transient
             1524  LOAD_FAST                'ret_dict'
             1526  LOAD_STR                 'transient'
             1528  STORE_SUBSCR     

 L. 319      1530  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1532  LOAD_STR                 'generate_object_manager_data.<locals>.<listcomp>'
             1534  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1536  LOAD_FAST                'cur_obj'
             1538  LOAD_METHOD              get_tags
             1540  CALL_METHOD_0         0  '0 positional arguments'
             1542  GET_ITER         
             1544  CALL_FUNCTION_1       1  '1 positional argument'
             1546  STORE_FAST               'object_tags_by_name'

 L. 320      1548  LOAD_FAST                'ret_dict'
             1550  LOAD_STR                 'additional_data'
             1552  BINARY_SUBSCR    
             1554  LOAD_METHOD              append
             1556  LOAD_STR                 'Category Tags'
             1558  LOAD_STR                 ', '
             1560  LOAD_METHOD              join
             1562  LOAD_FAST                'object_tags_by_name'
             1564  CALL_METHOD_1         1  '1 positional argument'
             1566  LOAD_CONST               ('dataId', 'dataValue')
             1568  BUILD_CONST_KEY_MAP_2     2 
             1570  CALL_METHOD_1         1  '1 positional argument'
             1572  POP_TOP          

 L. 322      1574  LOAD_FAST                'cur_obj'
             1576  LOAD_METHOD              is_in_inventory
             1578  CALL_METHOD_0         0  '0 positional arguments'
         1580_1582  POP_JUMP_IF_FALSE  1638  'to 1638'

 L. 323      1584  LOAD_FAST                'cur_obj'
             1586  LOAD_ATTR                inventoryitem_component
             1588  LOAD_ATTR                last_inventory_owner
             1590  LOAD_CONST               None
             1592  COMPARE_OP               is-not
         1594_1596  POP_JUMP_IF_FALSE  1616  'to 1616'

 L. 324      1598  LOAD_GLOBAL              hex
             1600  LOAD_FAST                'cur_obj'
             1602  LOAD_ATTR                inventoryitem_component
             1604  LOAD_ATTR                last_inventory_owner
             1606  LOAD_ATTR                id
             1608  CALL_FUNCTION_1       1  '1 positional argument'
             1610  LOAD_FAST                'ret_dict'
             1612  LOAD_STR                 'inventory_owner_id'
             1614  STORE_SUBSCR     
           1616_0  COME_FROM          1594  '1594'

 L. 325      1616  LOAD_FAST                'ret_dict'
             1618  LOAD_STR                 'additional_data'
             1620  BINARY_SUBSCR    
             1622  LOAD_METHOD              append
             1624  LOAD_STR                 'New In Inventory'
             1626  LOAD_FAST                'cur_obj'
             1628  LOAD_ATTR                new_in_inventory
             1630  LOAD_CONST               ('dataId', 'dataValue')
             1632  BUILD_CONST_KEY_MAP_2     2 
             1634  CALL_METHOD_1         1  '1 positional argument'
             1636  POP_TOP          
           1638_0  COME_FROM          1580  '1580'

 L. 327      1638  BUILD_LIST_0          0 
             1640  LOAD_FAST                'ret_dict'
             1642  LOAD_STR                 'commodities'
             1644  STORE_SUBSCR     

 L. 328      1646  SETUP_LOOP         1760  'to 1760'
             1648  LOAD_GLOBAL              list
             1650  LOAD_FAST                'cur_obj'
             1652  LOAD_METHOD              get_all_stats_gen
             1654  CALL_METHOD_0         0  '0 positional arguments'
             1656  CALL_FUNCTION_1       1  '1 positional argument'
             1658  GET_ITER         
             1660  FOR_ITER           1758  'to 1758'
             1662  STORE_FAST               'commodity'

 L. 329      1664  LOAD_GLOBAL              type
             1666  LOAD_FAST                'commodity'
             1668  CALL_FUNCTION_1       1  '1 positional argument'
             1670  LOAD_ATTR                __name__

 L. 330      1672  LOAD_FAST                'commodity'
             1674  LOAD_METHOD              get_value
             1676  CALL_METHOD_0         0  '0 positional arguments'
             1678  LOAD_CONST               ('commodity', 'value')
             1680  BUILD_CONST_KEY_MAP_2     2 
             1682  STORE_FAST               'com_entry'

 L. 332      1684  LOAD_FAST                'commodity'
             1686  LOAD_ATTR                continuous
         1688_1690  POP_JUMP_IF_FALSE  1740  'to 1740'

 L. 333      1692  LOAD_FAST                'commodity'
             1694  LOAD_ATTR                convergence_value
             1696  BUILD_TUPLE_1         1 
             1698  LOAD_FAST                'com_entry'
             1700  LOAD_STR                 'convergence_value'
             1702  STORE_SUBSCR     

 L. 334      1704  LOAD_FAST                'commodity'
             1706  LOAD_ATTR                base_decay_rate
             1708  BUILD_TUPLE_1         1 
             1710  LOAD_FAST                'com_entry'
             1712  LOAD_STR                 'decay_rate'
             1714  STORE_SUBSCR     

 L. 335      1716  LOAD_FAST                'commodity'
             1718  LOAD_ATTR                get_decay_rate_modifier
             1720  BUILD_TUPLE_1         1 
             1722  LOAD_FAST                'com_entry'
             1724  LOAD_STR                 'decay_rate_modifier'
             1726  STORE_SUBSCR     

 L. 336      1728  LOAD_FAST                'commodity'
             1730  LOAD_ATTR                get_change_rate
             1732  BUILD_TUPLE_1         1 
             1734  LOAD_FAST                'com_entry'
             1736  LOAD_STR                 'change_rate'
             1738  STORE_SUBSCR     
           1740_0  COME_FROM          1688  '1688'

 L. 337      1740  LOAD_FAST                'ret_dict'
             1742  LOAD_STR                 'commodities'
             1744  BINARY_SUBSCR    
             1746  LOAD_METHOD              append
             1748  LOAD_FAST                'com_entry'
             1750  CALL_METHOD_1         1  '1 positional argument'
             1752  POP_TOP          
         1754_1756  JUMP_BACK          1660  'to 1660'
             1758  POP_BLOCK        
           1760_0  COME_FROM_LOOP     1646  '1646'

 L. 339      1760  BUILD_LIST_0          0 
             1762  LOAD_FAST                'ret_dict'
             1764  LOAD_STR                 'postures'
             1766  STORE_SUBSCR     

 L. 340      1768  SETUP_LOOP         1834  'to 1834'
             1770  LOAD_GLOBAL              list
             1772  LOAD_FAST                'cur_obj'
             1774  LOAD_METHOD              super_affordances
             1776  CALL_METHOD_0         0  '0 positional arguments'
             1778  CALL_FUNCTION_1       1  '1 positional argument'
             1780  GET_ITER         
           1782_0  COME_FROM          1794  '1794'
             1782  FOR_ITER           1832  'to 1832'
             1784  STORE_FAST               'affordance'

 L. 341      1786  LOAD_FAST                'affordance'
             1788  LOAD_ATTR                provided_posture_type
             1790  LOAD_CONST               None
             1792  COMPARE_OP               is-not
         1794_1796  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 342      1798  LOAD_FAST                'affordance'
             1800  LOAD_ATTR                __name__

 L. 343      1802  LOAD_FAST                'affordance'
             1804  LOAD_ATTR                provided_posture_type
             1806  LOAD_ATTR                __name__
             1808  LOAD_CONST               ('interactionName', 'providedPosture')
             1810  BUILD_CONST_KEY_MAP_2     2 
             1812  STORE_FAST               'posture_entry'

 L. 344      1814  LOAD_FAST                'ret_dict'
             1816  LOAD_STR                 'postures'
             1818  BINARY_SUBSCR    
             1820  LOAD_METHOD              append
             1822  LOAD_FAST                'posture_entry'
             1824  CALL_METHOD_1         1  '1 positional argument'
             1826  POP_TOP          
         1828_1830  JUMP_BACK          1782  'to 1782'
             1832  POP_BLOCK        
           1834_0  COME_FROM_LOOP     1768  '1768'

 L. 346      1834  BUILD_LIST_0          0 
             1836  LOAD_FAST                'ret_dict'
             1838  LOAD_STR                 'reservations'
             1840  STORE_SUBSCR     

 L. 348      1842  SETUP_LOOP         1960  'to 1960'
             1844  LOAD_GLOBAL              itertools
             1846  LOAD_METHOD              chain
             1848  LOAD_FAST                'cur_obj'
             1850  BUILD_TUPLE_1         1 
             1852  LOAD_FAST                'cur_obj'
             1854  LOAD_ATTR                parts
             1856  LOAD_CONST               None
             1858  COMPARE_OP               is-not
         1860_1862  POP_JUMP_IF_FALSE  1870  'to 1870'
             1864  LOAD_FAST                'cur_obj'
             1866  LOAD_ATTR                parts
             1868  JUMP_FORWARD       1872  'to 1872'
           1870_0  COME_FROM          1860  '1860'
             1870  LOAD_CONST               ()
           1872_0  COME_FROM          1868  '1868'
             1872  CALL_METHOD_2         2  '2 positional arguments'
             1874  GET_ITER         
             1876  FOR_ITER           1958  'to 1958'
             1878  STORE_FAST               'reservation_target'

 L. 349      1880  SETUP_LOOP         1954  'to 1954'
             1882  LOAD_FAST                'reservation_target'
             1884  LOAD_METHOD              get_reservation_handlers
             1886  CALL_METHOD_0         0  '0 positional arguments'
             1888  GET_ITER         
             1890  FOR_ITER           1952  'to 1952'
             1892  STORE_FAST               'reservation_handler'

 L. 351      1894  LOAD_GLOBAL              str
             1896  LOAD_FAST                'reservation_handler'
             1898  LOAD_ATTR                sim
             1900  CALL_FUNCTION_1       1  '1 positional argument'

 L. 352      1902  LOAD_GLOBAL              str
             1904  LOAD_FAST                'reservation_handler'
             1906  LOAD_ATTR                target
             1908  CALL_FUNCTION_1       1  '1 positional argument'

 L. 353      1910  LOAD_GLOBAL              str
             1912  LOAD_GLOBAL              type
             1914  LOAD_FAST                'reservation_handler'
             1916  CALL_FUNCTION_1       1  '1 positional argument'
             1918  CALL_FUNCTION_1       1  '1 positional argument'

 L. 354      1920  LOAD_GLOBAL              str
             1922  LOAD_FAST                'reservation_handler'
             1924  LOAD_ATTR                reservation_interaction
             1926  CALL_FUNCTION_1       1  '1 positional argument'
             1928  LOAD_CONST               ('reservation_sim', 'reservation_target', 'reservation_type', 'reservation_interaction')
             1930  BUILD_CONST_KEY_MAP_4     4 
             1932  STORE_FAST               'reservation_entry'

 L. 356      1934  LOAD_FAST                'ret_dict'
             1936  LOAD_STR                 'reservations'
             1938  BINARY_SUBSCR    
             1940  LOAD_METHOD              append
             1942  LOAD_FAST                'reservation_entry'
             1944  CALL_METHOD_1         1  '1 positional argument'
             1946  POP_TOP          
         1948_1950  JUMP_BACK          1890  'to 1890'
             1952  POP_BLOCK        
           1954_0  COME_FROM_LOOP     1880  '1880'
         1954_1956  JUMP_BACK          1876  'to 1876'
             1958  POP_BLOCK        
           1960_0  COME_FROM_LOOP     1842  '1842'

 L. 358      1960  BUILD_LIST_0          0 
             1962  LOAD_FAST                'ret_dict'
             1964  LOAD_STR                 'parts'
             1966  STORE_SUBSCR     

 L. 359      1968  LOAD_FAST                'cur_obj'
             1970  LOAD_ATTR                parts
             1972  LOAD_CONST               None
             1974  COMPARE_OP               is-not
         1976_1978  POP_JUMP_IF_FALSE  2040  'to 2040'

 L. 360      1980  SETUP_LOOP         2040  'to 2040'
             1982  LOAD_FAST                'cur_obj'
             1984  LOAD_ATTR                parts
             1986  GET_ITER         
             1988  FOR_ITER           2038  'to 2038'
             1990  STORE_FAST               'part'

 L. 361      1992  LOAD_FAST                'part'
             1994  LOAD_ATTR                part_group_index

 L. 362      1996  LOAD_FAST                'part'
             1998  LOAD_ATTR                part_suffix

 L. 363      2000  LOAD_FAST                'part'
             2002  LOAD_ATTR                subroot_index

 L. 364      2004  LOAD_GLOBAL              str
             2006  LOAD_FAST                'part'
             2008  LOAD_METHOD              is_mirrored
             2010  CALL_METHOD_0         0  '0 positional arguments'
             2012  CALL_FUNCTION_1       1  '1 positional argument'
             2014  LOAD_CONST               ('part_group_index', 'part_suffix', 'subroot_index', 'is_mirrored')
             2016  BUILD_CONST_KEY_MAP_4     4 
             2018  STORE_FAST               'part_entry'

 L. 366      2020  LOAD_FAST                'ret_dict'
             2022  LOAD_STR                 'parts'
             2024  BINARY_SUBSCR    
             2026  LOAD_METHOD              append
             2028  LOAD_FAST                'part_entry'
             2030  CALL_METHOD_1         1  '1 positional argument'
             2032  POP_TOP          
         2034_2036  JUMP_BACK          1988  'to 1988'
             2038  POP_BLOCK        
           2040_0  COME_FROM_LOOP     1980  '1980'
           2040_1  COME_FROM          1976  '1976'

 L. 368      2040  BUILD_LIST_0          0 
             2042  LOAD_FAST                'ret_dict'
             2044  LOAD_STR                 'slots'
             2046  STORE_SUBSCR     

 L. 369      2048  SETUP_LOOP         2114  'to 2114'
             2050  LOAD_FAST                'cur_obj'
             2052  LOAD_METHOD              get_runtime_slots_gen
             2054  CALL_METHOD_0         0  '0 positional arguments'
             2056  GET_ITER         
             2058  FOR_ITER           2112  'to 2112'
             2060  STORE_FAST               'runtime_slot'

 L. 370      2062  LOAD_GLOBAL              str
             2064  LOAD_FAST                'runtime_slot'
             2066  CALL_FUNCTION_1       1  '1 positional argument'

 L. 371      2068  LOAD_STR                 ', '
             2070  LOAD_METHOD              join
             2072  LOAD_GENEXPR             '<code_object <genexpr>>'
             2074  LOAD_STR                 'generate_object_manager_data.<locals>.<genexpr>'
             2076  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2078  LOAD_FAST                'runtime_slot'
             2080  LOAD_ATTR                children
             2082  GET_ITER         
             2084  CALL_FUNCTION_1       1  '1 positional argument'
             2086  CALL_METHOD_1         1  '1 positional argument'
             2088  LOAD_CONST               ('slot', 'children')
             2090  BUILD_CONST_KEY_MAP_2     2 
             2092  STORE_FAST               'slot_entry'

 L. 372      2094  LOAD_FAST                'ret_dict'
             2096  LOAD_STR                 'slots'
             2098  BINARY_SUBSCR    
             2100  LOAD_METHOD              append
             2102  LOAD_FAST                'slot_entry'
             2104  CALL_METHOD_1         1  '1 positional argument'
             2106  POP_TOP          
         2108_2110  JUMP_BACK          2058  'to 2058'
             2112  POP_BLOCK        
           2114_0  COME_FROM_LOOP     2048  '2048'

 L. 374      2114  BUILD_LIST_0          0 
             2116  LOAD_FAST                'ret_dict'
             2118  LOAD_STR                 'inventory'
             2120  STORE_SUBSCR     

 L. 375      2122  LOAD_FAST                'cur_obj'
             2124  LOAD_ATTR                inventory_component
             2126  STORE_FAST               'inventory'

 L. 376      2128  LOAD_FAST                'inventory'
             2130  LOAD_CONST               None
             2132  COMPARE_OP               is-not
         2134_2136  POP_JUMP_IF_FALSE  2244  'to 2244'

 L. 377      2138  SETUP_LOOP         2244  'to 2244'
             2140  LOAD_FAST                'inventory'
             2142  GET_ITER         
             2144  FOR_ITER           2242  'to 2242'
             2146  STORE_FAST               'obj'

 L. 378      2148  BUILD_MAP_0           0 
             2150  STORE_FAST               'inv_entry'

 L. 379      2152  LOAD_GLOBAL              hex
             2154  LOAD_FAST                'obj'
             2156  LOAD_ATTR                id
             2158  CALL_FUNCTION_1       1  '1 positional argument'
             2160  LOAD_FAST                'inv_entry'
             2162  LOAD_STR                 'objId'
             2164  STORE_SUBSCR     

 L. 380      2166  LOAD_GLOBAL              gsi_handlers
             2168  LOAD_ATTR                gsi_utils
             2170  LOAD_METHOD              format_object_name
             2172  LOAD_FAST                'obj'
             2174  CALL_METHOD_1         1  '1 positional argument'
             2176  LOAD_FAST                'inv_entry'
             2178  LOAD_STR                 'classStr'
             2180  STORE_SUBSCR     

 L. 381      2182  LOAD_FAST                'obj'
             2184  LOAD_METHOD              stack_count
             2186  CALL_METHOD_0         0  '0 positional arguments'
             2188  LOAD_FAST                'inv_entry'
             2190  LOAD_STR                 'stack_count'
             2192  STORE_SUBSCR     

 L. 382      2194  LOAD_FAST                'obj'
             2196  LOAD_ATTR                get_stack_sort_order
             2198  LOAD_CONST               True
             2200  LOAD_CONST               ('inspect_only',)
             2202  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2204  LOAD_FAST                'inv_entry'
             2206  LOAD_STR                 'stack_sort_order'
             2208  STORE_SUBSCR     

 L. 383      2210  LOAD_FAST                'inventory'
             2212  LOAD_METHOD              is_object_hidden
             2214  LOAD_FAST                'obj'
             2216  CALL_METHOD_1         1  '1 positional argument'
             2218  LOAD_FAST                'inv_entry'
             2220  LOAD_STR                 'hidden'
             2222  STORE_SUBSCR     

 L. 384      2224  LOAD_FAST                'ret_dict'
             2226  LOAD_STR                 'inventory'
             2228  BINARY_SUBSCR    
             2230  LOAD_METHOD              append
             2232  LOAD_FAST                'inv_entry'
             2234  CALL_METHOD_1         1  '1 positional argument'
             2236  POP_TOP          
         2238_2240  JUMP_BACK          2144  'to 2144'
             2242  POP_BLOCK        
           2244_0  COME_FROM_LOOP     2138  '2138'
           2244_1  COME_FROM          2134  '2134'

 L. 386      2244  BUILD_LIST_0          0 
             2246  LOAD_FAST                'ret_dict'
             2248  LOAD_STR                 'locking_component'
             2250  STORE_SUBSCR     

 L. 387      2252  LOAD_FAST                'cur_obj'
             2254  LOAD_METHOD              get_locking_component
             2256  CALL_METHOD_0         0  '0 positional arguments'
             2258  STORE_FAST               'locking_component'

 L. 388      2260  LOAD_FAST                'locking_component'
             2262  LOAD_CONST               None
             2264  COMPARE_OP               is-not
         2266_2268  POP_JUMP_IF_FALSE  2374  'to 2374'

 L. 389      2270  SETUP_LOOP         2374  'to 2374'
             2272  LOAD_FAST                'locking_component'
             2274  LOAD_ATTR                lock_datas
             2276  LOAD_METHOD              values
             2278  CALL_METHOD_0         0  '0 positional arguments'
             2280  GET_ITER         
             2282  FOR_ITER           2372  'to 2372'
             2284  STORE_FAST               'lock_data'

 L. 390      2286  BUILD_MAP_0           0 
             2288  STORE_FAST               'inv_entry'

 L. 391      2290  LOAD_GLOBAL              str
             2292  LOAD_FAST                'lock_data'
             2294  LOAD_ATTR                lock_type
             2296  CALL_FUNCTION_1       1  '1 positional argument'
             2298  LOAD_FAST                'inv_entry'
             2300  LOAD_STR                 'lock_type'
             2302  STORE_SUBSCR     

 L. 392      2304  LOAD_GLOBAL              str
             2306  LOAD_FAST                'lock_data'
             2308  LOAD_ATTR                lock_priority
             2310  CALL_FUNCTION_1       1  '1 positional argument'
             2312  LOAD_FAST                'inv_entry'
             2314  LOAD_STR                 'lock_priority'
             2316  STORE_SUBSCR     

 L. 393      2318  LOAD_GLOBAL              str
             2320  LOAD_FAST                'lock_data'
             2322  LOAD_ATTR                lock_sides
             2324  CALL_FUNCTION_1       1  '1 positional argument'
             2326  LOAD_FAST                'inv_entry'
             2328  LOAD_STR                 'lock_side'
             2330  STORE_SUBSCR     

 L. 394      2332  LOAD_FAST                'lock_data'
             2334  LOAD_ATTR                should_persist
             2336  LOAD_FAST                'inv_entry'
             2338  LOAD_STR                 'should_persist'
             2340  STORE_SUBSCR     

 L. 395      2342  LOAD_FAST                'lock_data'
             2344  LOAD_METHOD              get_exception_data
             2346  CALL_METHOD_0         0  '0 positional arguments'
             2348  LOAD_FAST                'inv_entry'
             2350  LOAD_STR                 'exceptions'
             2352  STORE_SUBSCR     

 L. 396      2354  LOAD_FAST                'ret_dict'
             2356  LOAD_STR                 'locking_component'
             2358  BINARY_SUBSCR    
             2360  LOAD_METHOD              append
             2362  LOAD_FAST                'inv_entry'
             2364  CALL_METHOD_1         1  '1 positional argument'
             2366  POP_TOP          
         2368_2370  JUMP_BACK          2282  'to 2282'
             2372  POP_BLOCK        
           2374_0  COME_FROM_LOOP     2270  '2270'
           2374_1  COME_FROM          2266  '2266'

 L. 398      2374  BUILD_LIST_0          0 
             2376  LOAD_FAST                'ret_dict'
             2378  LOAD_STR                 'awareness'
             2380  STORE_SUBSCR     

 L. 399      2382  LOAD_FAST                'cur_obj'
             2384  LOAD_ATTR                awareness_scores
             2386  STORE_FAST               'awareness_scores'

 L. 400      2388  LOAD_FAST                'awareness_scores'
             2390  LOAD_CONST               None
             2392  COMPARE_OP               is-not
         2394_2396  POP_JUMP_IF_FALSE  2454  'to 2454'

 L. 401      2398  SETUP_LOOP         2454  'to 2454'
             2400  LOAD_FAST                'awareness_scores'
             2402  LOAD_METHOD              items
             2404  CALL_METHOD_0         0  '0 positional arguments'
             2406  GET_ITER         
             2408  FOR_ITER           2452  'to 2452'
             2410  UNPACK_SEQUENCE_2     2 
             2412  STORE_FAST               'awareness_channel'
             2414  STORE_FAST               'awareness_score'

 L. 402      2416  LOAD_FAST                'ret_dict'
             2418  LOAD_STR                 'awareness'
             2420  BINARY_SUBSCR    
             2422  LOAD_METHOD              append

 L. 403      2424  LOAD_STR                 'Provider'

 L. 404      2426  LOAD_GLOBAL              str
             2428  LOAD_FAST                'awareness_channel'
             2430  CALL_FUNCTION_1       1  '1 positional argument'

 L. 405      2432  LOAD_STR                 'Score: {}'
             2434  LOAD_METHOD              format
             2436  LOAD_FAST                'awareness_score'
             2438  CALL_METHOD_1         1  '1 positional argument'
             2440  LOAD_CONST               ('awareness_role', 'awareness_channel', 'awareness_data')
             2442  BUILD_CONST_KEY_MAP_3     3 
             2444  CALL_METHOD_1         1  '1 positional argument'
             2446  POP_TOP          
         2448_2450  JUMP_BACK          2408  'to 2408'
             2452  POP_BLOCK        
           2454_0  COME_FROM_LOOP     2398  '2398'
           2454_1  COME_FROM          2394  '2394'

 L. 407      2454  LOAD_FAST                'cur_obj'
             2456  LOAD_ATTR                awareness_component
             2458  LOAD_CONST               None
             2460  COMPARE_OP               is-not
         2462_2464  POP_JUMP_IF_FALSE  2552  'to 2552'

 L. 408      2466  SETUP_LOOP         2552  'to 2552'
             2468  LOAD_FAST                'cur_obj'
             2470  LOAD_ATTR                awareness_component
             2472  LOAD_ATTR                awareness_modifiers
             2474  LOAD_METHOD              items
             2476  CALL_METHOD_0         0  '0 positional arguments'
             2478  GET_ITER         
             2480  FOR_ITER           2550  'to 2550'
             2482  UNPACK_SEQUENCE_2     2 
             2484  STORE_FAST               'awareness_channel'
             2486  STORE_FAST               'awareness_options'

 L. 409      2488  LOAD_FAST                'ret_dict'
             2490  LOAD_STR                 'awareness'
             2492  BINARY_SUBSCR    
             2494  LOAD_METHOD              append

 L. 410      2496  LOAD_STR                 'Recipient'

 L. 411      2498  LOAD_GLOBAL              str
             2500  LOAD_FAST                'awareness_channel'
             2502  CALL_FUNCTION_1       1  '1 positional argument'

 L. 412      2504  LOAD_STR                 'Modifiers: {}'
             2506  LOAD_METHOD              format
             2508  LOAD_FAST                'awareness_options'
         2510_2512  POP_JUMP_IF_FALSE  2534  'to 2534'
             2514  LOAD_STR                 ', '
             2516  LOAD_METHOD              join
             2518  LOAD_GENEXPR             '<code_object <genexpr>>'
             2520  LOAD_STR                 'generate_object_manager_data.<locals>.<genexpr>'
             2522  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2524  LOAD_FAST                'awareness_options'
             2526  GET_ITER         
             2528  CALL_FUNCTION_1       1  '1 positional argument'
             2530  CALL_METHOD_1         1  '1 positional argument'
             2532  JUMP_FORWARD       2536  'to 2536'
           2534_0  COME_FROM          2510  '2510'
             2534  LOAD_STR                 'Default'
           2536_0  COME_FROM          2532  '2532'
             2536  CALL_METHOD_1         1  '1 positional argument'
             2538  LOAD_CONST               ('awareness_role', 'awareness_channel', 'awareness_data')
             2540  BUILD_CONST_KEY_MAP_3     3 
             2542  CALL_METHOD_1         1  '1 positional argument'
             2544  POP_TOP          
         2546_2548  JUMP_BACK          2480  'to 2480'
             2550  POP_BLOCK        
           2552_0  COME_FROM_LOOP     2466  '2466'
           2552_1  COME_FROM          2462  '2462'

 L. 415      2552  BUILD_LIST_0          0 
             2554  LOAD_FAST                'ret_dict'
             2556  LOAD_STR                 'component'
             2558  STORE_SUBSCR     

 L. 416      2560  SETUP_LOOP         2618  'to 2618'
             2562  LOAD_FAST                'cur_obj'
             2564  LOAD_ATTR                components
             2566  GET_ITER         
           2568_0  COME_FROM          2578  '2578'
             2568  FOR_ITER           2616  'to 2616'
             2570  STORE_FAST               'component'

 L. 417      2572  LOAD_FAST                'component'
             2574  LOAD_CONST               None
             2576  COMPARE_OP               is-not
         2578_2580  POP_JUMP_IF_FALSE  2568  'to 2568'

 L. 418      2582  BUILD_MAP_0           0 
             2584  STORE_FAST               'inv_entry'

 L. 419      2586  LOAD_FAST                'component'
             2588  LOAD_ATTR                __class__
             2590  LOAD_ATTR                __name__
             2592  LOAD_FAST                'inv_entry'
             2594  LOAD_STR                 'component_name'
             2596  STORE_SUBSCR     

 L. 420      2598  LOAD_FAST                'ret_dict'
             2600  LOAD_STR                 'component'
             2602  BINARY_SUBSCR    
             2604  LOAD_METHOD              append
             2606  LOAD_FAST                'inv_entry'
             2608  CALL_METHOD_1         1  '1 positional argument'
             2610  POP_TOP          
         2612_2614  JUMP_BACK          2568  'to 2568'
             2616  POP_BLOCK        
           2618_0  COME_FROM_LOOP     2560  '2560'

 L. 421      2618  LOAD_FAST                'cur_obj'
             2620  LOAD_ATTR                is_sim
         2622_2624  POP_JUMP_IF_FALSE  2690  'to 2690'

 L. 422      2626  SETUP_LOOP         2690  'to 2690'
             2628  LOAD_FAST                'cur_obj'
             2630  LOAD_ATTR                sim_info
             2632  LOAD_ATTR                components
             2634  GET_ITER         
           2636_0  COME_FROM          2646  '2646'
             2636  FOR_ITER           2688  'to 2688'
             2638  STORE_FAST               'component'

 L. 423      2640  LOAD_FAST                'component'
             2642  LOAD_CONST               None
             2644  COMPARE_OP               is-not
         2646_2648  POP_JUMP_IF_FALSE  2636  'to 2636'

 L. 424      2650  BUILD_MAP_0           0 
             2652  STORE_FAST               'inv_entry'

 L. 425      2654  LOAD_FAST                'component'
             2656  LOAD_ATTR                __class__
             2658  LOAD_ATTR                __name__
             2660  LOAD_STR                 ' - SIM_INFO'
             2662  BINARY_ADD       
             2664  LOAD_FAST                'inv_entry'
             2666  LOAD_STR                 'component_name'
             2668  STORE_SUBSCR     

 L. 426      2670  LOAD_FAST                'ret_dict'
             2672  LOAD_STR                 'component'
             2674  BINARY_SUBSCR    
             2676  LOAD_METHOD              append
             2678  LOAD_FAST                'inv_entry'
             2680  CALL_METHOD_1         1  '1 positional argument'
             2682  POP_TOP          
         2684_2686  JUMP_BACK          2636  'to 2636'
             2688  POP_BLOCK        
           2690_0  COME_FROM_LOOP     2626  '2626'
           2690_1  COME_FROM          2622  '2622'

 L. 428      2690  BUILD_LIST_0          0 
             2692  LOAD_FAST                'ret_dict'
             2694  LOAD_STR                 'ownership'
             2696  STORE_SUBSCR     

 L. 429      2698  BUILD_MAP_0           0 
             2700  STORE_FAST               'data'

 L. 431      2702  LOAD_STR                 'None'
             2704  STORE_FAST               'household_name'

 L. 432      2706  LOAD_FAST                'cur_obj'
             2708  LOAD_METHOD              get_household_owner_id
             2710  CALL_METHOD_0         0  '0 positional arguments'
             2712  STORE_FAST               'house_id'

 L. 433      2714  LOAD_FAST                'house_id'
             2716  LOAD_CONST               None
             2718  COMPARE_OP               is-not
         2720_2722  POP_JUMP_IF_FALSE  2774  'to 2774'

 L. 434      2724  LOAD_GLOBAL              services
             2726  LOAD_METHOD              household_manager
             2728  CALL_METHOD_0         0  '0 positional arguments'
             2730  LOAD_METHOD              get
             2732  LOAD_FAST                'house_id'
             2734  CALL_METHOD_1         1  '1 positional argument'
             2736  STORE_FAST               'household'

 L. 435      2738  LOAD_FAST                'household'
             2740  LOAD_CONST               None
             2742  COMPARE_OP               is-not
         2744_2746  POP_JUMP_IF_FALSE  2774  'to 2774'

 L. 436      2748  LOAD_FAST                'household'
             2750  LOAD_ATTR                name
             2752  STORE_FAST               'household_name'

 L. 437      2754  LOAD_GLOBAL              str
             2756  LOAD_FAST                'house_id'
             2758  CALL_FUNCTION_1       1  '1 positional argument'
             2760  LOAD_STR                 ', '
             2762  BINARY_ADD       
             2764  LOAD_FAST                'household_name'
             2766  BINARY_ADD       
             2768  LOAD_FAST                'data'
             2770  LOAD_STR                 'ownership_household_owner'
             2772  STORE_SUBSCR     
           2774_0  COME_FROM          2744  '2744'
           2774_1  COME_FROM          2720  '2720'

 L. 439      2774  LOAD_FAST                'cur_obj'
             2776  LOAD_METHOD              get_sim_owner_id
             2778  CALL_METHOD_0         0  '0 positional arguments'
             2780  STORE_FAST               'sim_id'

 L. 440      2782  LOAD_FAST                'sim_id'
             2784  LOAD_CONST               None
             2786  COMPARE_OP               is-not
         2788_2790  POP_JUMP_IF_FALSE  2828  'to 2828'

 L. 441      2792  LOAD_FAST                'sim_info_manager'
             2794  LOAD_METHOD              get
             2796  LOAD_FAST                'sim_id'
             2798  CALL_METHOD_1         1  '1 positional argument'
             2800  STORE_FAST               'sim_info'

 L. 442      2802  LOAD_FAST                'sim_info'
             2804  LOAD_ATTR                full_name
             2806  STORE_FAST               'sim_name'

 L. 443      2808  LOAD_GLOBAL              str
             2810  LOAD_FAST                'sim_id'
             2812  CALL_FUNCTION_1       1  '1 positional argument'
             2814  LOAD_STR                 ', '
             2816  BINARY_ADD       
             2818  LOAD_FAST                'sim_name'
             2820  BINARY_ADD       
             2822  LOAD_FAST                'data'
             2824  LOAD_STR                 'ownership_sim_owner'
             2826  STORE_SUBSCR     
           2828_0  COME_FROM          2788  '2788'

 L. 445      2828  LOAD_FAST                'cur_obj'
             2830  LOAD_METHOD              has_component
             2832  LOAD_GLOBAL              objects
             2834  LOAD_ATTR                components
             2836  LOAD_ATTR                types
             2838  LOAD_ATTR                CRAFTING_COMPONENT
             2840  CALL_METHOD_1         1  '1 positional argument'
         2842_2844  POP_JUMP_IF_FALSE  2926  'to 2926'

 L. 446      2846  LOAD_FAST                'cur_obj'
             2848  LOAD_METHOD              get_crafting_process
             2850  CALL_METHOD_0         0  '0 positional arguments'
             2852  STORE_FAST               'crafting_process'

 L. 447      2854  LOAD_FAST                'crafting_process'
             2856  LOAD_CONST               None
             2858  COMPARE_OP               is-not
         2860_2862  POP_JUMP_IF_FALSE  2926  'to 2926'

 L. 448      2864  LOAD_FAST                'crafting_process'
             2866  LOAD_ATTR                crafter_sim_id
             2868  STORE_FAST               'crafter_sim_id'

 L. 449      2870  LOAD_FAST                'crafter_sim_id'
             2872  LOAD_CONST               None
             2874  COMPARE_OP               is-not
         2876_2878  POP_JUMP_IF_FALSE  2926  'to 2926'

 L. 450      2880  LOAD_FAST                'sim_info_manager'
             2882  LOAD_METHOD              get
             2884  LOAD_FAST                'crafter_sim_id'
             2886  CALL_METHOD_1         1  '1 positional argument'
             2888  STORE_FAST               'crafter_sim_info'

 L. 451      2890  LOAD_FAST                'crafter_sim_info'
             2892  LOAD_CONST               None
             2894  COMPARE_OP               is-not
         2896_2898  POP_JUMP_IF_FALSE  2926  'to 2926'

 L. 452      2900  LOAD_FAST                'crafter_sim_info'
             2902  LOAD_ATTR                full_name
             2904  STORE_FAST               'crafter_sim_name'

 L. 453      2906  LOAD_GLOBAL              str
             2908  LOAD_FAST                'crafter_sim_id'
             2910  CALL_FUNCTION_1       1  '1 positional argument'
             2912  LOAD_STR                 ', '
             2914  BINARY_ADD       
             2916  LOAD_FAST                'crafter_sim_name'
             2918  BINARY_ADD       
             2920  LOAD_FAST                'data'
             2922  LOAD_STR                 'ownership_crafter_sim'
             2924  STORE_SUBSCR     
           2926_0  COME_FROM          2896  '2896'
           2926_1  COME_FROM          2876  '2876'
           2926_2  COME_FROM          2860  '2860'
           2926_3  COME_FROM          2842  '2842'

 L. 455      2926  LOAD_FAST                'cur_obj'
             2928  LOAD_ATTR                id
             2930  LOAD_FAST                'obj_preference_data'
             2932  COMPARE_OP               in
         2934_2936  POP_JUMP_IF_FALSE  3062  'to 3062'

 L. 456      2938  LOAD_CONST               True
             2940  STORE_FAST               'is_head'

 L. 457      2942  LOAD_FAST                'obj_preference_data'
             2944  LOAD_FAST                'cur_obj'
             2946  LOAD_ATTR                id
             2948  BINARY_SUBSCR    
             2950  STORE_FAST               'preference_sims_list'

 L. 458      2952  SETUP_LOOP         3076  'to 3076'
             2954  LOAD_FAST                'preference_sims_list'
             2956  GET_ITER         
             2958  FOR_ITER           3058  'to 3058'
             2960  STORE_FAST               'sim_id'

 L. 459      2962  LOAD_FAST                'sim_info_manager'
             2964  LOAD_METHOD              get
             2966  LOAD_FAST                'sim_id'
             2968  CALL_METHOD_1         1  '1 positional argument'
             2970  STORE_FAST               'sim_info'

 L. 460      2972  LOAD_FAST                'sim_info'
             2974  LOAD_ATTR                full_name
             2976  STORE_FAST               'sim_name'

 L. 461      2978  LOAD_FAST                'is_head'
         2980_2982  POP_JUMP_IF_FALSE  3024  'to 3024'

 L. 462      2984  LOAD_CONST               False
             2986  STORE_FAST               'is_head'

 L. 463      2988  LOAD_GLOBAL              str
             2990  LOAD_FAST                'sim_id'
             2992  CALL_FUNCTION_1       1  '1 positional argument'
             2994  LOAD_STR                 ', '
             2996  BINARY_ADD       
             2998  LOAD_FAST                'sim_name'
             3000  BINARY_ADD       
             3002  LOAD_FAST                'data'
             3004  LOAD_STR                 'ownership_preference_sim'
             3006  STORE_SUBSCR     

 L. 464      3008  LOAD_FAST                'ret_dict'
             3010  LOAD_STR                 'ownership'
             3012  BINARY_SUBSCR    
             3014  LOAD_METHOD              append
             3016  LOAD_FAST                'data'
             3018  CALL_METHOD_1         1  '1 positional argument'
             3020  POP_TOP          
             3022  JUMP_BACK          2958  'to 2958'
           3024_0  COME_FROM          2980  '2980'

 L. 466      3024  LOAD_FAST                'ret_dict'
             3026  LOAD_STR                 'ownership'
             3028  BINARY_SUBSCR    
             3030  LOAD_METHOD              append
             3032  LOAD_STR                 'ownership_preference_sim'
             3034  LOAD_GLOBAL              str
             3036  LOAD_FAST                'sim_id'
             3038  CALL_FUNCTION_1       1  '1 positional argument'
             3040  LOAD_STR                 ', '
             3042  BINARY_ADD       
             3044  LOAD_FAST                'sim_name'
             3046  BINARY_ADD       
             3048  BUILD_MAP_1           1 
             3050  CALL_METHOD_1         1  '1 positional argument'
             3052  POP_TOP          
         3054_3056  JUMP_BACK          2958  'to 2958'
             3058  POP_BLOCK        
             3060  JUMP_FORWARD       3076  'to 3076'
           3062_0  COME_FROM          2934  '2934'

 L. 468      3062  LOAD_FAST                'ret_dict'
             3064  LOAD_STR                 'ownership'
             3066  BINARY_SUBSCR    
             3068  LOAD_METHOD              append
             3070  LOAD_FAST                'data'
             3072  CALL_METHOD_1         1  '1 positional argument'
             3074  POP_TOP          
           3076_0  COME_FROM          3060  '3060'
           3076_1  COME_FROM_LOOP     2952  '2952'

 L. 470      3076  BUILD_LIST_0          0 
             3078  LOAD_FAST                'ret_dict'
             3080  LOAD_STR                 'live_drag'
             3082  STORE_SUBSCR     

 L. 471      3084  LOAD_FAST                'cur_obj'
             3086  LOAD_ATTR                live_drag_component
             3088  STORE_FAST               'live_drag_component'

 L. 472      3090  LOAD_FAST                'live_drag_component'
             3092  LOAD_CONST               None
             3094  COMPARE_OP               is-not
         3096_3098  POP_JUMP_IF_FALSE  3302  'to 3302'

 L. 473      3100  LOAD_FAST                'ret_dict'
             3102  LOAD_STR                 'live_drag'
             3104  BINARY_SUBSCR    
             3106  LOAD_METHOD              append
             3108  LOAD_STR                 'Can Live Drag'
             3110  LOAD_FAST                'live_drag_component'
             3112  LOAD_ATTR                can_live_drag
             3114  LOAD_CONST               ('live_drag_data_name', 'live_drag_data_value')
             3116  BUILD_CONST_KEY_MAP_2     2 
             3118  CALL_METHOD_1         1  '1 positional argument'
             3120  POP_TOP          

 L. 476      3122  LOAD_FAST                'live_drag_component'
             3124  LOAD_METHOD              get_permission
             3126  LOAD_GLOBAL              LiveDragPermission
             3128  LOAD_ATTR                NOT_IN_USE
             3130  CALL_METHOD_1         1  '1 positional argument'
             3132  STORE_FAST               'in_use_permission'

 L. 477      3134  LOAD_FAST                'in_use_permission'
         3136_3138  POP_JUMP_IF_TRUE   3152  'to 3152'

 L. 478      3140  LOAD_STR                 'Disallowed, In use by: {}'
             3142  LOAD_METHOD              format
             3144  LOAD_FAST                'users'
             3146  CALL_METHOD_1         1  '1 positional argument'
             3148  STORE_FAST               'in_use_by'
             3150  JUMP_FORWARD       3156  'to 3156'
           3152_0  COME_FROM          3136  '3136'

 L. 480      3152  LOAD_STR                 'Allowed, Not in use'
             3154  STORE_FAST               'in_use_by'
           3156_0  COME_FROM          3150  '3150'

 L. 481      3156  LOAD_FAST                'ret_dict'
             3158  LOAD_STR                 'live_drag'
             3160  BINARY_SUBSCR    
             3162  LOAD_METHOD              append
             3164  LOAD_STR                 'In Use Permission'
             3166  LOAD_FAST                'in_use_by'
             3168  LOAD_CONST               ('live_drag_data_name', 'live_drag_data_value')
             3170  BUILD_CONST_KEY_MAP_2     2 
             3172  CALL_METHOD_1         1  '1 positional argument'
             3174  POP_TOP          

 L. 484      3176  LOAD_FAST                'live_drag_component'
             3178  LOAD_METHOD              get_permission
             3180  LOAD_GLOBAL              LiveDragPermission
             3182  LOAD_ATTR                HOUSEHOLD
             3184  CALL_METHOD_1         1  '1 positional argument'
             3186  STORE_FAST               'household_permission'

 L. 485      3188  LOAD_FAST                'household_permission'
         3190_3192  POP_JUMP_IF_FALSE  3206  'to 3206'

 L. 486      3194  LOAD_STR                 'Allowed, Owned by: {}'
             3196  LOAD_METHOD              format
             3198  LOAD_FAST                'household_name'
             3200  CALL_METHOD_1         1  '1 positional argument'
             3202  STORE_FAST               'owned_by'
             3204  JUMP_FORWARD       3216  'to 3216'
           3206_0  COME_FROM          3190  '3190'

 L. 488      3206  LOAD_STR                 'Disallowed, Owned by: {}'
             3208  LOAD_METHOD              format
             3210  LOAD_FAST                'household_name'
             3212  CALL_METHOD_1         1  '1 positional argument'
             3214  STORE_FAST               'owned_by'
           3216_0  COME_FROM          3204  '3204'

 L. 489      3216  LOAD_FAST                'ret_dict'
             3218  LOAD_STR                 'live_drag'
             3220  BINARY_SUBSCR    
             3222  LOAD_METHOD              append
             3224  LOAD_STR                 'Active Household Permission'
             3226  LOAD_FAST                'owned_by'
             3228  LOAD_CONST               ('live_drag_data_name', 'live_drag_data_value')
             3230  BUILD_CONST_KEY_MAP_2     2 
             3232  CALL_METHOD_1         1  '1 positional argument'
             3234  POP_TOP          

 L. 492      3236  LOAD_FAST                'live_drag_component'
             3238  LOAD_METHOD              get_permission
             3240  LOAD_GLOBAL              LiveDragPermission
             3242  LOAD_ATTR                STATE
             3244  CALL_METHOD_1         1  '1 positional argument'
             3246  STORE_FAST               'state_permission'

 L. 493      3248  LOAD_FAST                'state_permission'
         3250_3252  POP_JUMP_IF_TRUE   3278  'to 3278'

 L. 494      3254  LOAD_STR                 'Disallowed, Disabled by: {}'
             3256  LOAD_METHOD              format
             3258  LOAD_GLOBAL              gsi_handlers
             3260  LOAD_ATTR                gsi_utils
             3262  LOAD_METHOD              format_object_list_names
             3264  LOAD_FAST                'live_drag_component'
             3266  LOAD_METHOD              get_state_op_owners
             3268  CALL_METHOD_0         0  '0 positional arguments'
             3270  CALL_METHOD_1         1  '1 positional argument'
             3272  CALL_METHOD_1         1  '1 positional argument'
             3274  STORE_FAST               'states_disabling'
             3276  JUMP_FORWARD       3282  'to 3282'
           3278_0  COME_FROM          3250  '3250'

 L. 496      3278  LOAD_STR                 'Allowed'
             3280  STORE_FAST               'states_disabling'
           3282_0  COME_FROM          3276  '3276'

 L. 497      3282  LOAD_FAST                'ret_dict'
             3284  LOAD_STR                 'live_drag'
             3286  BINARY_SUBSCR    
             3288  LOAD_METHOD              append
             3290  LOAD_STR                 'State Permission'
             3292  LOAD_FAST                'states_disabling'
             3294  LOAD_CONST               ('live_drag_data_name', 'live_drag_data_value')
             3296  BUILD_CONST_KEY_MAP_2     2 
             3298  CALL_METHOD_1         1  '1 positional argument'
             3300  POP_TOP          
           3302_0  COME_FROM          3096  '3096'

 L. 499      3302  BUILD_LIST_0          0 
             3304  STORE_FAST               'walkstyle_info'

 L. 500      3306  LOAD_FAST                'walkstyle_info'
             3308  LOAD_FAST                'ret_dict'
             3310  LOAD_STR                 'walkstyles'
             3312  STORE_SUBSCR     

 L. 501      3314  BUILD_LIST_0          0 
             3316  LOAD_FAST                'ret_dict'
             3318  LOAD_STR                 'portals'
             3320  STORE_SUBSCR     

 L. 503      3322  LOAD_FAST                'cur_obj'
             3324  LOAD_ATTR                routing_component
             3326  STORE_FAST               'routing_component'

 L. 504      3328  LOAD_FAST                'routing_component'
             3330  LOAD_CONST               None
             3332  COMPARE_OP               is-not
         3334_3336  POP_JUMP_IF_FALSE  3642  'to 3642'

 L. 505      3338  LOAD_FAST                'cur_obj'
             3340  LOAD_METHOD              get_walkstyle
             3342  CALL_METHOD_0         0  '0 positional arguments'
             3344  STORE_FAST               'walkstyle'

 L. 506      3346  LOAD_FAST                'cur_obj'
             3348  LOAD_METHOD              get_walkstyle_behavior
             3350  CALL_METHOD_0         0  '0 positional arguments'
             3352  STORE_FAST               'walkstyle_behavior'

 L. 507      3354  LOAD_FAST                'cur_obj'
             3356  LOAD_METHOD              get_walkstyle_list
             3358  CALL_METHOD_0         0  '0 positional arguments'
             3360  STORE_FAST               'walkstyle_list'

 L. 509      3362  SETUP_LOOP         3604  'to 3604'
             3364  LOAD_FAST                'cur_obj'
             3366  LOAD_METHOD              get_walkstyle_requests
             3368  CALL_METHOD_0         0  '0 positional arguments'
             3370  GET_ITER         
             3372  FOR_ITER           3602  'to 3602'
             3374  STORE_FAST               'walkstyle_request'

 L. 510      3376  LOAD_FAST                'walkstyle_behavior'
             3378  LOAD_METHOD              get_combo_replacement
             3380  LOAD_FAST                'walkstyle_request'
             3382  LOAD_ATTR                walkstyle
             3384  LOAD_FAST                'walkstyle_list'
             3386  CALL_METHOD_2         2  '2 positional arguments'
             3388  STORE_FAST               'combo_replacement_tuple'

 L. 511      3390  LOAD_FAST                'combo_replacement_tuple'
             3392  LOAD_CONST               None
             3394  COMPARE_OP               is-not
         3396_3398  POP_JUMP_IF_FALSE  3466  'to 3466'

 L. 512      3400  LOAD_STR                 '{}({})'
             3402  LOAD_METHOD              format
             3404  LOAD_FAST                'combo_replacement_tuple'
             3406  LOAD_ATTR                result
             3408  LOAD_STR                 ','
             3410  LOAD_METHOD              join
             3412  LOAD_GENEXPR             '<code_object <genexpr>>'
             3414  LOAD_STR                 'generate_object_manager_data.<locals>.<genexpr>'
             3416  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3418  LOAD_FAST                'combo_replacement_tuple'
             3420  LOAD_ATTR                key_combo_list
             3422  GET_ITER         
             3424  CALL_FUNCTION_1       1  '1 positional argument'
             3426  CALL_METHOD_1         1  '1 positional argument'
             3428  CALL_METHOD_2         2  '2 positional arguments'
             3430  STORE_FAST               'combo_replacement_str'

 L. 513      3432  LOAD_STR                 '{} (Combo: {})'
             3434  LOAD_METHOD              format
             3436  LOAD_FAST                'walkstyle_behavior'
             3438  LOAD_METHOD              get_short_walkstyle
             3440  LOAD_FAST                'walkstyle_request'
             3442  LOAD_ATTR                walkstyle
             3444  LOAD_FAST                'cur_obj'
             3446  CALL_METHOD_2         2  '2 positional arguments'

 L. 514      3448  LOAD_FAST                'walkstyle_behavior'
             3450  LOAD_METHOD              get_short_walkstyle
             3452  LOAD_FAST                'combo_replacement_tuple'
             3454  LOAD_ATTR                result
             3456  LOAD_FAST                'cur_obj'
             3458  CALL_METHOD_2         2  '2 positional arguments'
             3460  CALL_METHOD_2         2  '2 positional arguments'
             3462  STORE_FAST               'short_replacement_str'
             3464  JUMP_FORWARD       3490  'to 3490'
           3466_0  COME_FROM          3396  '3396'

 L. 516      3466  LOAD_STR                 ''
             3468  STORE_FAST               'combo_replacement_str'

 L. 517      3470  LOAD_STR                 '{}'
             3472  LOAD_METHOD              format
             3474  LOAD_FAST                'walkstyle_behavior'
             3476  LOAD_METHOD              get_short_walkstyle
             3478  LOAD_FAST                'walkstyle_request'
             3480  LOAD_ATTR                walkstyle
             3482  LOAD_FAST                'cur_obj'
             3484  CALL_METHOD_2         2  '2 positional arguments'
             3486  CALL_METHOD_1         1  '1 positional argument'
             3488  STORE_FAST               'short_replacement_str'
           3490_0  COME_FROM          3464  '3464'

 L. 520      3490  LOAD_STR                 '{} ({})'
             3492  LOAD_METHOD              format
             3494  LOAD_GLOBAL              str
             3496  LOAD_FAST                'walkstyle_request'
             3498  LOAD_ATTR                priority
             3500  CALL_FUNCTION_1       1  '1 positional argument'
             3502  LOAD_GLOBAL              int
             3504  LOAD_FAST                'walkstyle_request'
             3506  LOAD_ATTR                priority
             3508  CALL_FUNCTION_1       1  '1 positional argument'
             3510  CALL_METHOD_2         2  '2 positional arguments'

 L. 521      3512  LOAD_GLOBAL              str
             3514  LOAD_FAST                'walkstyle_request'
             3516  LOAD_ATTR                walkstyle
             3518  CALL_FUNCTION_1       1  '1 positional argument'

 L. 522      3520  LOAD_FAST                'short_replacement_str'

 L. 523      3522  LOAD_FAST                'combo_replacement_str'

 L. 524      3524  LOAD_FAST                'sim'
             3526  LOAD_CONST               None
             3528  COMPARE_OP               is-not
         3530_3532  POP_JUMP_IF_FALSE  3550  'to 3550'
             3534  LOAD_FAST                'walkstyle'
             3536  LOAD_FAST                'walkstyle_request'
             3538  LOAD_ATTR                walkstyle
             3540  COMPARE_OP               is
         3542_3544  POP_JUMP_IF_FALSE  3550  'to 3550'
             3546  LOAD_STR                 'X'
             3548  JUMP_FORWARD       3552  'to 3552'
           3550_0  COME_FROM          3542  '3542'
           3550_1  COME_FROM          3530  '3530'
             3550  LOAD_STR                 ''
           3552_0  COME_FROM          3548  '3548'

 L. 525      3552  LOAD_FAST                'sim'
             3554  LOAD_CONST               None
             3556  COMPARE_OP               is-not
         3558_3560  POP_JUMP_IF_FALSE  3580  'to 3580'
             3562  LOAD_FAST                'walkstyle_behavior'
             3564  LOAD_ATTR                default_walkstyle
             3566  LOAD_FAST                'walkstyle_request'
             3568  LOAD_ATTR                walkstyle
             3570  COMPARE_OP               is
         3572_3574  POP_JUMP_IF_FALSE  3580  'to 3580'
             3576  LOAD_STR                 'X'
             3578  JUMP_FORWARD       3582  'to 3582'
           3580_0  COME_FROM          3572  '3572'
           3580_1  COME_FROM          3558  '3558'
             3580  LOAD_STR                 ''
           3582_0  COME_FROM          3578  '3578'
             3582  LOAD_CONST               ('walkstyle_priority', 'walkstyle_type', 'walkstyle_short', 'walkstyle_combo_replacement', 'walkstyle_is_current', 'walkstyle_is_default')
             3584  BUILD_CONST_KEY_MAP_6     6 
             3586  STORE_FAST               'walkstyle_entry'

 L. 527      3588  LOAD_FAST                'walkstyle_info'
             3590  LOAD_METHOD              append
             3592  LOAD_FAST                'walkstyle_entry'
             3594  CALL_METHOD_1         1  '1 positional argument'
             3596  POP_TOP          
         3598_3600  JUMP_BACK          3372  'to 3372'
             3602  POP_BLOCK        
           3604_0  COME_FROM_LOOP     3362  '3362'

 L. 529      3604  LOAD_FAST                'routing_component'
             3606  LOAD_METHOD              get_routing_context
             3608  CALL_METHOD_0         0  '0 positional arguments'
             3610  STORE_FAST               'routing_context'

 L. 530      3612  LOAD_FAST                'routing_context'
             3614  LOAD_METHOD              get_portal_key_mask
             3616  CALL_METHOD_0         0  '0 positional arguments'
             3618  STORE_DEREF              'portal_key_mask'

 L. 531      3620  LOAD_CLOSURE             'portal_key_mask'
             3622  BUILD_TUPLE_1         1 
             3624  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3626  LOAD_STR                 'generate_object_manager_data.<locals>.<listcomp>'
             3628  MAKE_FUNCTION_8          'closure'
             3630  LOAD_GLOBAL              PortalFlags
             3632  GET_ITER         
             3634  CALL_FUNCTION_1       1  '1 positional argument'
             3636  LOAD_FAST                'ret_dict'
             3638  LOAD_STR                 'portals'
             3640  STORE_SUBSCR     
           3642_0  COME_FROM          3334  '3334'
           3642_1  COME_FROM          1512  '1512'

 L. 534      3642  LOAD_FAST                'all_object_data'
             3644  LOAD_METHOD              append
             3646  LOAD_FAST                'ret_dict'
             3648  CALL_METHOD_1         1  '1 positional argument'
             3650  POP_TOP          
             3652  JUMP_BACK           248  'to 248'
             3654  POP_BLOCK        
           3656_0  COME_FROM_LOOP      214  '214'

 L. 535      3656  LOAD_FAST                'all_object_data'
             3658  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 3656_0


object_definitions_schema = GsiGridSchema(label='Object Definitions', auto_refresh=False, exclude_from_dump=True)
object_definitions_schema.add_field('obj_name', label='Name', width=4)
object_definitions_schema.add_field('instance_id', label='Inst ID', unique_field=True, type=(GsiFieldVisualizers.INT))
object_definitions_schema.add_field('pack_id', label='Pack')
object_definitions_schema.add_view_cheat('objects.clear_lot', label='Clear Objs', refresh_view=False)
pack_names = []
for pack in sims4.common.get_available_packs():
    pack_names.append(str(pack))

for pack_name in sorted(pack_names):
    object_definitions_schema.add_filter(pack_name)

with object_definitions_schema.add_view_cheat('objects.gsi_create_obj', label='Create Obj', dbl_click=True, refresh_view=False) as (cheat):
    cheat.add_token_param('instance_id')
with object_definitions_schema.add_view_cheat('objects.gsi_create_objs_from_pack', label='Create Obj From Pack', refresh_view=False) as (cheat):
    cheat.add_token_param('instance_id')
with object_definitions_schema.add_view_cheat('objects.gsi_create_obj_and_variants', label='Create Variants', refresh_view=False) as (cheat):
    cheat.add_token_param('instance_id')
with object_definitions_schema.add_view_cheat('objects.gsi_create_obj_in_inventory', label='Inv +1', refresh_view=False) as (cheat):
    cheat.add_token_param('instance_id')
with object_definitions_schema.add_view_cheat('objects.gsi_create_obj_in_inventory', label='Inv +20', refresh_view=False) as (cheat):
    cheat.add_token_param('instance_id')
    cheat.add_static_param('20')

@GsiHandler('object_definitions', object_definitions_schema)
def generate_object_instances_data(*args, zone_id: int=None, filter=None, **kwargs):
    filter_list = parse_filter_to_list(filter)
    all_objects = []
    for key in sorted(sims4.resources.list(type=(sims4.resources.Types.OBJECTDEFINITION))):
        pack_id = str(Pack(build_buy.get_object_pack_by_keykey.typekey.instancekey.group))
        if filter_list is not None:
            if pack_id not in filter_list:
                continue
        all_objects.append({'obj_name':sims4.resources.get_debug_name(key, table_type=sims4.hash_util.KEYNAMEMAPTYPE_OBJECTINSTANCES),  'instance_id':str(key.instance), 
         'pack_id':pack_id})

    return all_objects


object_removed_schema = GsiGridSchema(label='Object Removed Log')
object_removed_schema.add_field('mgr', label='Manager', width=1, hidden=True)
object_removed_schema.add_field('objId', label='Object Id', width=3, unique_field=True)
object_removed_schema.add_field('classStr', label='Class', width=3)
object_removed_schema.add_field('modelStr', label='Model', width=3)
object_removed_schema.add_field('parent', label='Parent', width=2)
object_removed_archiver = GameplayArchiver('ObjectRemoved', object_removed_schema)

def archive_object_removal(obj_removed):
    class_str = gsi_handlers.gsi_utils.format_object_name(obj_removed)
    model_name = _get_model_name(obj_removed)
    ret_dict = {'mgr':str(obj_removed.manager).replace('_manager', ''), 
     'objId':hex(obj_removed.id), 
     'classStr':class_str, 
     'modelStr':model_name}
    parent = getattr(obj_removed, 'parent', None)
    if parent is not None:
        ret_dict['parent'] = gsi_handlers.gsi_utils.format_object_name(parent)
    object_removed_archiver.archive(data=ret_dict)