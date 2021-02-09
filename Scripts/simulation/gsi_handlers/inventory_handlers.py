# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\gsi_handlers\inventory_handlers.py
# Compiled at: 2020-03-03 03:56:51
# Size of source mod 2**32: 4487 bytes
import itertools, gsi_handlers, services
from gsi_handlers.gsi_utils import parse_filter_to_list
from sims4.gsi.dispatcher import GsiHandler
from sims4.gsi.schema import GsiGridSchema
inventory_schema = GsiGridSchema(label='Inventories')
inventory_schema.add_field('objId', label='Object Id', width=1, unique_field=True, hidden=True)
inventory_schema.add_field('inventoryOwner', label='Inventory Owner', width=3)
inventory_schema.add_field('instancedCount', label='Count (Instanced)', width=2)
inventory_schema.add_field('shelvedCount', label='Count (Shelved)', width=2)
inventory_schema.add_filter('active_household_inventories')
inventory_schema.add_filter('npc_sim_inventories')
inventory_schema.add_filter('on_lot_object_inventories')
inventory_schema.add_filter('off_lot_object_inventories')
with inventory_schema.add_view_cheat('objects.focus_camera_on_object', label='Focus On Selected Object') as (cheat):
    cheat.add_token_param('objId')
with inventory_schema.add_has_many('instanced_contents', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('stackId', label='Stack ID')
    sub_schema.add_field('definition', label='Definition', width=3)
    sub_schema.add_field('objectCount', label='Object Count')
    sub_schema.add_field('isHidden', label='Is Hidden')
with inventory_schema.add_has_many('shelved_contents', GsiGridSchema) as (sub_schema):
    sub_schema.add_field('definition', label='Definition', width=3)
    sub_schema.add_field('objectCount', label='Object Count')

@GsiHandler('inventories', inventory_schema)
def generate_inventories_data--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              parse_filter_to_list
                2  LOAD_FAST                'filter'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'filter_list'

 L.  40         8  LOAD_GLOBAL              services
               10  LOAD_METHOD              get_zone
               12  LOAD_FAST                'zone_id'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  STORE_FAST               'zone'

 L.  41        18  BUILD_LIST_0          0 
               20  STORE_FAST               'all_object_data'

 L.  43        22  LOAD_GLOBAL              services
               24  LOAD_METHOD              active_household
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  STORE_DEREF              'active_household'

 L.  44        30  LOAD_GLOBAL              services
               32  LOAD_METHOD              definition_manager
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  STORE_FAST               'def_manager'

 L.  46        38  LOAD_CLOSURE             'active_household'
               40  BUILD_TUPLE_1         1 
               42  LOAD_CODE                <code_object _active_household_sim>
               44  LOAD_STR                 'generate_inventories_data.<locals>._active_household_sim'
               46  MAKE_FUNCTION_8          'closure'
               48  STORE_FAST               '_active_household_sim'

 L.  51        50  LOAD_CLOSURE             'active_household'
               52  BUILD_TUPLE_1         1 
               54  LOAD_CODE                <code_object _npc_sim>
               56  LOAD_STR                 'generate_inventories_data.<locals>._npc_sim'
               58  MAKE_FUNCTION_8          'closure'
               60  STORE_FAST               '_npc_sim'

 L.  56     62_64  SETUP_LOOP          448  'to 448'
               66  LOAD_GLOBAL              list
               68  LOAD_GLOBAL              itertools
               70  LOAD_METHOD              chain
               72  LOAD_FAST                'zone'
               74  LOAD_ATTR                object_manager
               76  LOAD_ATTR                objects

 L.  57        78  LOAD_FAST                'zone'
               80  LOAD_ATTR                inventory_manager
               82  LOAD_ATTR                objects
               84  CALL_METHOD_2         2  '2 positional arguments'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  GET_ITER         
             90_0  COME_FROM           218  '218'
             90_1  COME_FROM           214  '214'
             90_2  COME_FROM           210  '210'
            90_92  FOR_ITER            446  'to 446'
               94  STORE_FAST               'cur_obj'

 L.  58        96  LOAD_FAST                'cur_obj'
               98  LOAD_ATTR                inventory_component
              100  STORE_FAST               'inventory'

 L.  59       102  LOAD_FAST                'inventory'
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   112  'to 112'

 L.  60       110  CONTINUE             90  'to 90'
            112_0  COME_FROM           108  '108'

 L.  62       112  LOAD_GLOBAL              hasattr
              114  LOAD_FAST                'cur_obj'
              116  LOAD_STR                 'is_on_active_lot'
              118  CALL_FUNCTION_2       2  '2 positional arguments'
              120  POP_JUMP_IF_FALSE   130  'to 130'
              122  LOAD_FAST                'cur_obj'
              124  LOAD_METHOD              is_on_active_lot
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           120  '120'
              130  LOAD_CONST               False
            132_0  COME_FROM           128  '128'
              132  STORE_FAST               'on_active_lot'

 L.  63       134  LOAD_FAST                'cur_obj'
              136  LOAD_ATTR                is_sim
              138  STORE_FAST               'is_sim'

 L.  65       140  LOAD_FAST                'filter_list'
              142  LOAD_CONST               None
              144  COMPARE_OP               is
              146  POP_JUMP_IF_TRUE    220  'to 220'

 L.  66       148  LOAD_STR                 'active_household_inventories'
              150  LOAD_FAST                'filter_list'
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   168  'to 168'
              156  LOAD_FAST                'is_sim'
              158  POP_JUMP_IF_FALSE   168  'to 168'
              160  LOAD_FAST                '_active_household_sim'
              162  LOAD_FAST                'cur_obj'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  POP_JUMP_IF_TRUE    220  'to 220'
            168_0  COME_FROM           158  '158'
            168_1  COME_FROM           154  '154'

 L.  67       168  LOAD_STR                 'npc_sim_inventories'
              170  LOAD_FAST                'filter_list'
              172  COMPARE_OP               in
              174  POP_JUMP_IF_FALSE   188  'to 188'
              176  LOAD_FAST                'is_sim'
              178  POP_JUMP_IF_FALSE   188  'to 188'
              180  LOAD_FAST                '_npc_sim'
              182  LOAD_FAST                'cur_obj'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  POP_JUMP_IF_TRUE    220  'to 220'
            188_0  COME_FROM           178  '178'
            188_1  COME_FROM           174  '174'

 L.  68       188  LOAD_STR                 'on_lot_object_inventories'
              190  LOAD_FAST                'filter_list'
              192  COMPARE_OP               in
              194  POP_JUMP_IF_FALSE   204  'to 204'
              196  LOAD_FAST                'is_sim'
              198  POP_JUMP_IF_TRUE    204  'to 204'
              200  LOAD_FAST                'on_active_lot'
              202  POP_JUMP_IF_TRUE    220  'to 220'
            204_0  COME_FROM           198  '198'
            204_1  COME_FROM           194  '194'

 L.  69       204  LOAD_STR                 'off_lot_object_inventories'
              206  LOAD_FAST                'filter_list'
              208  COMPARE_OP               in
              210  POP_JUMP_IF_FALSE    90  'to 90'
              212  LOAD_FAST                'is_sim'
              214  POP_JUMP_IF_TRUE     90  'to 90'
              216  LOAD_FAST                'on_active_lot'
              218  POP_JUMP_IF_TRUE     90  'to 90'
            220_0  COME_FROM           202  '202'
            220_1  COME_FROM           186  '186'
            220_2  COME_FROM           166  '166'
            220_3  COME_FROM           146  '146'

 L.  72       220  LOAD_GLOBAL              hex
              222  LOAD_FAST                'cur_obj'
              224  LOAD_ATTR                id
              226  CALL_FUNCTION_1       1  '1 positional argument'

 L.  73       228  LOAD_GLOBAL              gsi_handlers
              230  LOAD_ATTR                gsi_utils
              232  LOAD_METHOD              format_object_name
              234  LOAD_FAST                'cur_obj'
              236  CALL_METHOD_1         1  '1 positional argument'

 L.  74       238  LOAD_GLOBAL              str
              240  LOAD_GLOBAL              len
              242  LOAD_FAST                'inventory'
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  LOAD_CONST               ('objId', 'inventoryOwner', 'instancedCount')
              250  BUILD_CONST_KEY_MAP_3     3 
              252  STORE_FAST               'obj_entry'

 L.  76       254  LOAD_FAST                'inventory'
          256_258  POP_JUMP_IF_FALSE   342  'to 342'

 L.  77       260  BUILD_LIST_0          0 
              262  STORE_FAST               'instanced_contents'

 L.  78       264  SETUP_LOOP          334  'to 334'
              266  LOAD_FAST                'inventory'
              268  GET_ITER         
              270  FOR_ITER            332  'to 332'
              272  STORE_FAST               'item'

 L.  79       274  LOAD_FAST                'item'
              276  LOAD_ATTR                inventoryitem_component
              278  STORE_FAST               'item_component'

 L.  80       280  LOAD_FAST                'instanced_contents'
              282  LOAD_METHOD              append

 L.  81       284  LOAD_GLOBAL              str
              286  LOAD_FAST                'item_component'
              288  LOAD_METHOD              get_stack_id
              290  CALL_METHOD_0         0  '0 positional arguments'
              292  CALL_FUNCTION_1       1  '1 positional argument'

 L.  82       294  LOAD_GLOBAL              str
              296  LOAD_FAST                'item'
              298  LOAD_ATTR                definition
              300  CALL_FUNCTION_1       1  '1 positional argument'

 L.  83       302  LOAD_GLOBAL              str
              304  LOAD_FAST                'item_component'
              306  LOAD_METHOD              stack_count
              308  CALL_METHOD_0         0  '0 positional arguments'
              310  CALL_FUNCTION_1       1  '1 positional argument'

 L.  84       312  LOAD_GLOBAL              str
              314  LOAD_FAST                'item_component'
              316  LOAD_ATTR                is_hidden
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  LOAD_CONST               ('stackId', 'definition', 'objectCount', 'isHidden')
              322  BUILD_CONST_KEY_MAP_4     4 
              324  CALL_METHOD_1         1  '1 positional argument'
              326  POP_TOP          
          328_330  JUMP_BACK           270  'to 270'
              332  POP_BLOCK        
            334_0  COME_FROM_LOOP      264  '264'

 L.  86       334  LOAD_FAST                'instanced_contents'
              336  LOAD_FAST                'obj_entry'
              338  LOAD_STR                 'instanced_contents'
              340  STORE_SUBSCR     
            342_0  COME_FROM           256  '256'

 L.  88       342  LOAD_FAST                'is_sim'
          344_346  POP_JUMP_IF_FALSE   434  'to 434'

 L.  89       348  LOAD_GLOBAL              str
              350  LOAD_FAST                'inventory'
              352  LOAD_METHOD              get_shelved_object_count
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  CALL_FUNCTION_1       1  '1 positional argument'
              358  LOAD_FAST                'obj_entry'
              360  LOAD_STR                 'shelvedCount'
              362  STORE_SUBSCR     

 L.  90       364  BUILD_LIST_0          0 
              366  STORE_FAST               'shelved_contents'

 L.  91       368  SETUP_LOOP          426  'to 426'
              370  LOAD_FAST                'inventory'
              372  LOAD_METHOD              get_shelved_object_data
              374  CALL_METHOD_0         0  '0 positional arguments'
              376  GET_ITER         
              378  FOR_ITER            424  'to 424'
              380  STORE_FAST               'shelved'

 L.  92       382  LOAD_FAST                'shelved_contents'
              384  LOAD_METHOD              append

 L.  93       386  LOAD_GLOBAL              str
              388  LOAD_FAST                'def_manager'
              390  LOAD_METHOD              get
              392  LOAD_FAST                'shelved'
              394  LOAD_STR                 'guid'
              396  BINARY_SUBSCR    
              398  CALL_METHOD_1         1  '1 positional argument'
              400  CALL_FUNCTION_1       1  '1 positional argument'

 L.  94       402  LOAD_GLOBAL              str
              404  LOAD_FAST                'shelved'
              406  LOAD_STR                 'objectCount'
              408  BINARY_SUBSCR    
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  LOAD_CONST               ('definition', 'objectCount')
              414  BUILD_CONST_KEY_MAP_2     2 
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          
          420_422  JUMP_BACK           378  'to 378'
              424  POP_BLOCK        
            426_0  COME_FROM_LOOP      368  '368'

 L.  96       426  LOAD_FAST                'shelved_contents'
              428  LOAD_FAST                'obj_entry'
              430  LOAD_STR                 'shelved_contents'
              432  STORE_SUBSCR     
            434_0  COME_FROM           344  '344'

 L.  98       434  LOAD_FAST                'all_object_data'
              436  LOAD_METHOD              append
              438  LOAD_FAST                'obj_entry'
              440  CALL_METHOD_1         1  '1 positional argument'
              442  POP_TOP          
              444  JUMP_BACK            90  'to 90'
              446  POP_BLOCK        
            448_0  COME_FROM_LOOP       62  '62'

 L.  99       448  LOAD_FAST                'all_object_data'
              450  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 446