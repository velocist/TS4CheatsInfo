# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\postures\posture_state.py
# Compiled at: 2019-03-20 22:37:33
# Size of source mod 2**32: 37930 bytes
from animation.posture_manifest import Hand, SlotManifest
from carry.carry_tuning import CarryPostureStaticTuning
from carry.carry_utils import hand_to_track, create_carry_constraint, track_to_hand
from interactions.constraints import Anywhere, Constraint
from objects.definition import Definition
from postures import PostureTrack, posture_specs
from postures.posture_specs import PostureSpecVariable, BODY_INDEX, BODY_POSTURE_TYPE_INDEX, BODY_TARGET_INDEX, SURFACE_INDEX, SURFACE_TARGET_INDEX, CARRY_INDEX, CARRY_TARGET_INDEX, CARRY_POSTURE_TYPE_INDEX, CARRY_HAND_INDEX, SURFACE_SLOT_TYPE_INDEX, PostureAspectCarry, PostureAspectSurface, get_carry_posture_aop
from postures.posture_state_spec import PostureStateSpec
from sims4.collections import frozendict
from sims4.repr_utils import standard_repr
from tag import Tag
import postures, sims4.log
logger = sims4.log.Logger('Postures')

class PostureState:

    def __init__--- This code section failed: ---

 L.  47         0  LOAD_CLOSURE             'carry_posture_overrides'
                2  LOAD_CLOSURE             'sim'
                4  BUILD_TUPLE_2         2 
                6  LOAD_CODE                <code_object _get_default_carry_aspect>
                8  LOAD_STR                 'PostureState.__init__.<locals>._get_default_carry_aspect'
               10  MAKE_FUNCTION_8          'closure'
               12  STORE_FAST               '_get_default_carry_aspect'

 L.  52        14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _constraint_intersection

 L.  53        20  LOAD_CONST               True
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _constraint_intersection_dirty

 L.  54        26  LOAD_FAST                'posture_spec'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _spec

 L.  55        32  LOAD_DEREF               'sim'
               34  LOAD_METHOD              ref
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _sim_ref

 L.  56        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _linked_posture_state

 L.  57        48  LOAD_CONST               True
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _valid

 L.  58        54  BUILD_MAP_0           0 
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _constraints

 L.  59        60  LOAD_FAST                'invalid_expected'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _invalid_expected

 L.  60        66  LOAD_FAST                'body_state_spec_only'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               body_state_spec_only

 L.  61        72  LOAD_CONST               None
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _posture_constraint

 L.  62        78  LOAD_CONST               None
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _posture_constraint_strict

 L.  64        84  LOAD_GLOBAL              BODY_INDEX
               86  STORE_FAST               'body_index'

 L.  65        88  LOAD_GLOBAL              BODY_POSTURE_TYPE_INDEX
               90  STORE_FAST               'body_posture_type_index'

 L.  66        92  LOAD_GLOBAL              BODY_TARGET_INDEX
               94  STORE_FAST               'body_target_index'

 L.  67        96  LOAD_FAST                'posture_spec'
               98  LOAD_FAST                'body_index'
              100  BINARY_SUBSCR    
              102  STORE_FAST               'spec_body'

 L.  69       104  LOAD_FAST                'spec_body'
              106  LOAD_FAST                'body_target_index'
              108  BINARY_SUBSCR    
              110  LOAD_FAST                'self'
              112  STORE_ATTR               body_target

 L.  71       114  LOAD_FAST                'current_posture_state'
              116  LOAD_CONST               None
              118  COMPARE_OP               is
              120  POP_JUMP_IF_TRUE    154  'to 154'

 L.  72       122  LOAD_FAST                'spec_body'
              124  LOAD_FAST                'body_posture_type_index'
              126  BINARY_SUBSCR    
              128  LOAD_FAST                'current_posture_state'
              130  LOAD_ATTR                body
              132  LOAD_ATTR                posture_type
              134  COMPARE_OP               !=
              136  POP_JUMP_IF_TRUE    154  'to 154'

 L.  73       138  LOAD_FAST                'spec_body'
              140  LOAD_FAST                'body_target_index'
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'current_posture_state'
              146  LOAD_ATTR                body
              148  LOAD_ATTR                target
              150  COMPARE_OP               !=
              152  POP_JUMP_IF_FALSE   224  'to 224'
            154_0  COME_FROM           136  '136'
            154_1  COME_FROM           120  '120'

 L.  76       154  LOAD_CONST               None
              156  STORE_FAST               'animation_context'

 L.  77       158  LOAD_FAST                'current_posture_state'
              160  LOAD_CONST               None
              162  COMPARE_OP               is-not
              164  POP_JUMP_IF_FALSE   192  'to 192'

 L.  78       166  LOAD_FAST                'current_posture_state'
              168  LOAD_ATTR                body
              170  LOAD_ATTR                mobile
              172  POP_JUMP_IF_TRUE    192  'to 192'

 L.  79       174  LOAD_FAST                'spec_body'
              176  LOAD_FAST                'body_posture_type_index'
              178  BINARY_SUBSCR    
              180  LOAD_ATTR                mobile
              182  POP_JUMP_IF_TRUE    192  'to 192'

 L.  80       184  LOAD_FAST                'current_posture_state'
              186  LOAD_ATTR                body
              188  LOAD_ATTR                animation_context
              190  STORE_FAST               'animation_context'
            192_0  COME_FROM           182  '182'
            192_1  COME_FROM           172  '172'
            192_2  COME_FROM           164  '164'

 L.  85       192  LOAD_GLOBAL              postures
              194  LOAD_ATTR                create_posture
              196  LOAD_FAST                'spec_body'
              198  LOAD_FAST                'body_posture_type_index'
              200  BINARY_SUBSCR    

 L.  86       202  LOAD_FAST                'self'
              204  LOAD_ATTR                sim

 L.  87       206  LOAD_FAST                'self'
              208  LOAD_ATTR                body_target

 L.  88       210  LOAD_FAST                'animation_context'

 L.  89       212  LOAD_FAST                'is_throwaway'
              214  LOAD_CONST               ('animation_context', 'is_throwaway')
              216  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              218  LOAD_FAST                'self'
              220  STORE_ATTR               _aspect_body
              222  JUMP_FORWARD        232  'to 232'
            224_0  COME_FROM           152  '152'

 L.  91       224  LOAD_FAST                'current_posture_state'
              226  LOAD_ATTR                body
              228  LOAD_FAST                'self'
              230  STORE_ATTR               _aspect_body
            232_0  COME_FROM           222  '222'

 L.  99       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _aspect_body
              236  LOAD_ATTR                get_provided_postures
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                surface_target

 L. 100       242  LOAD_CONST               True
              244  LOAD_CONST               ('surface_target', 'concrete')
              246  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              248  STORE_FAST               'posture_manifest'

 L. 102       250  LOAD_FAST                'posture_manifest'
              252  LOAD_METHOD              get_constraint_version
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                sim
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               'posture_manifest'

 L. 104       262  LOAD_GLOBAL              PostureStateSpec
              264  LOAD_FAST                'posture_manifest'
              266  LOAD_GLOBAL              SlotManifest
              268  CALL_FUNCTION_0       0  '0 positional arguments'
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                _aspect_body
              274  LOAD_ATTR                target
          276_278  JUMP_IF_TRUE_OR_POP   284  'to 284'
              280  LOAD_GLOBAL              PostureSpecVariable
              282  LOAD_ATTR                ANYTHING
            284_0  COME_FROM           276  '276'
              284  CALL_FUNCTION_3       3  '3 positional arguments'
              286  STORE_FAST               'posture_state_spec'

 L. 106       288  LOAD_GLOBAL              Constraint
              290  LOAD_STR                 'PostureStateManifestConstraint'

 L. 107       292  LOAD_FAST                'posture_state_spec'
              294  LOAD_CONST               ('debug_name', 'posture_state_spec')
              296  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              298  LOAD_FAST                'self'
              300  STORE_ATTR               body_posture_state_constraint

 L. 109       302  LOAD_FAST                'body_state_spec_only'
          304_306  POP_JUMP_IF_FALSE   324  'to 324'

 L. 110       308  LOAD_FAST                'self'
              310  LOAD_ATTR                body_posture_state_constraint
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                _constraints
              316  LOAD_CONST               None
              318  STORE_SUBSCR     

 L. 113       320  LOAD_CONST               None
              322  RETURN_VALUE     
            324_0  COME_FROM           304  '304'

 L. 124       324  LOAD_FAST                'self'
              326  LOAD_ATTR                _aspect_body
              328  LOAD_ATTR                slot_constraint
              330  STORE_FAST               'body_slot_constraint'

 L. 125       332  LOAD_FAST                'body_slot_constraint'
              334  LOAD_CONST               None
              336  COMPARE_OP               is-not
          338_340  POP_JUMP_IF_FALSE   386  'to 386'

 L. 126       342  LOAD_FAST                'self'
              344  LOAD_ATTR                _aspect_body
              346  LOAD_ATTR                is_vehicle
          348_350  POP_JUMP_IF_FALSE   372  'to 372'
              352  LOAD_FAST                'current_posture_state'
              354  LOAD_CONST               None
              356  COMPARE_OP               is-not
          358_360  POP_JUMP_IF_FALSE   372  'to 372'
              362  LOAD_FAST                'current_posture_state'
              364  LOAD_ATTR                body
              366  LOAD_ATTR                is_vehicle
          368_370  POP_JUMP_IF_TRUE    386  'to 386'
            372_0  COME_FROM           358  '358'
            372_1  COME_FROM           348  '348'

 L. 127       372  LOAD_FAST                'self'
              374  LOAD_ATTR                body_posture_state_constraint
              376  LOAD_METHOD              intersect
              378  LOAD_FAST                'body_slot_constraint'
              380  CALL_METHOD_1         1  '1 positional argument'
              382  STORE_FAST               'body_posture_constraint'
              384  JUMP_FORWARD        392  'to 392'
            386_0  COME_FROM           368  '368'
            386_1  COME_FROM           338  '338'

 L. 129       386  LOAD_FAST                'self'
              388  LOAD_ATTR                body_posture_state_constraint
              390  STORE_FAST               'body_posture_constraint'
            392_0  COME_FROM           384  '384'

 L. 131       392  LOAD_FAST                'body_posture_constraint'
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                _constraints
              398  LOAD_CONST               None
              400  STORE_SUBSCR     

 L. 133       402  LOAD_FAST                'current_posture_state'
              404  LOAD_CONST               None
              406  COMPARE_OP               is-not
          408_410  POP_JUMP_IF_FALSE   430  'to 430'

 L. 134       412  LOAD_FAST                'current_posture_state'
              414  LOAD_METHOD              get_posture_spec
              416  LOAD_FAST                'var_map'
              418  CALL_METHOD_1         1  '1 positional argument'
              420  LOAD_GLOBAL              CARRY_INDEX
              422  BINARY_SUBSCR    
              424  LOAD_GLOBAL              CARRY_TARGET_INDEX
              426  BINARY_SUBSCR    
              428  STORE_FAST               'curr_spec_carry_target'
            430_0  COME_FROM           408  '408'

 L. 136       430  LOAD_FAST                'posture_spec'
              432  LOAD_GLOBAL              CARRY_INDEX
              434  BINARY_SUBSCR    
              436  STORE_FAST               'spec_carry'

 L. 137       438  LOAD_FAST                'spec_carry'
              440  LOAD_GLOBAL              CARRY_TARGET_INDEX
              442  BINARY_SUBSCR    
              444  STORE_FAST               'spec_carry_target'

 L. 138       446  LOAD_FAST                'current_posture_state'
              448  LOAD_CONST               None
              450  COMPARE_OP               is-not
          452_454  POP_JUMP_IF_FALSE   926  'to 926'
              456  LOAD_FAST                'spec_carry_target'
              458  LOAD_FAST                'curr_spec_carry_target'
              460  COMPARE_OP               !=
          462_464  POP_JUMP_IF_FALSE   926  'to 926'

 L. 139       466  LOAD_FAST                'spec_carry_target'
              468  LOAD_CONST               None
              470  COMPARE_OP               is
          472_474  POP_JUMP_IF_FALSE   554  'to 554'

 L. 141       476  LOAD_FAST                'var_map'
              478  LOAD_METHOD              get
              480  LOAD_FAST                'curr_spec_carry_target'
              482  CALL_METHOD_1         1  '1 positional argument'
              484  STORE_FAST               'current_carry_target'

 L. 142       486  LOAD_FAST                'current_posture_state'
              488  LOAD_METHOD              get_carry_track
              490  LOAD_FAST                'current_carry_target'
              492  CALL_METHOD_1         1  '1 positional argument'
              494  STORE_FAST               'current_carry_track'

 L. 143       496  LOAD_FAST                'current_carry_track'
              498  LOAD_GLOBAL              PostureTrack
              500  LOAD_ATTR                RIGHT
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   530  'to 530'

 L. 144       508  LOAD_FAST                '_get_default_carry_aspect'
              510  LOAD_GLOBAL              PostureTrack
              512  LOAD_ATTR                RIGHT
              514  CALL_FUNCTION_1       1  '1 positional argument'
              516  LOAD_FAST                'self'
              518  STORE_ATTR               _aspect_carry_right

 L. 145       520  LOAD_FAST                'current_posture_state'
              522  LOAD_ATTR                left
              524  LOAD_FAST                'self'
              526  STORE_ATTR               _aspect_carry_left
              528  JUMP_ABSOLUTE      1186  'to 1186'
            530_0  COME_FROM           504  '504'

 L. 147       530  LOAD_FAST                '_get_default_carry_aspect'
              532  LOAD_GLOBAL              PostureTrack
              534  LOAD_ATTR                LEFT
              536  CALL_FUNCTION_1       1  '1 positional argument'
              538  LOAD_FAST                'self'
              540  STORE_ATTR               _aspect_carry_left

 L. 148       542  LOAD_FAST                'current_posture_state'
              544  LOAD_ATTR                right
              546  LOAD_FAST                'self'
              548  STORE_ATTR               _aspect_carry_right
          550_552  JUMP_ABSOLUTE      1186  'to 1186'
            554_0  COME_FROM           472  '472'

 L. 150       554  LOAD_FAST                'spec_carry'
              556  LOAD_GLOBAL              CARRY_POSTURE_TYPE_INDEX
              558  BINARY_SUBSCR    
              560  STORE_FAST               'spec_carry_posture_type'

 L. 151       562  LOAD_FAST                'spec_carry_target'
              564  LOAD_FAST                'var_map'
              566  COMPARE_OP               not-in
          568_570  POP_JUMP_IF_FALSE   594  'to 594'

 L. 152       572  LOAD_GLOBAL              KeyError
              574  LOAD_STR                 'spec_carry_target {} not in var_map:{}. Sim posture state {} and carry aspects {}, '
              576  LOAD_METHOD              format
              578  LOAD_FAST                'spec_carry_target'
              580  LOAD_FAST                'var_map'
              582  LOAD_FAST                'current_posture_state'
              584  LOAD_FAST                'current_posture_state'
              586  LOAD_ATTR                carry_aspects
              588  CALL_METHOD_4         4  '4 positional arguments'
              590  CALL_FUNCTION_1       1  '1 positional argument'
              592  RAISE_VARARGS_1       1  'exception instance'
            594_0  COME_FROM           568  '568'

 L. 153       594  LOAD_FAST                'spec_carry_posture_type'
              596  LOAD_FAST                'var_map'
              598  COMPARE_OP               not-in
          600_602  POP_JUMP_IF_FALSE   686  'to 686'

 L. 156       604  LOAD_FAST                'var_map'
              606  LOAD_FAST                'spec_carry_target'
              608  BINARY_SUBSCR    
              610  STORE_FAST               'carry_target'

 L. 157       612  LOAD_GLOBAL              posture_specs
              614  LOAD_METHOD              get_carry_posture_aop
              616  LOAD_DEREF               'sim'
              618  LOAD_FAST                'carry_target'
              620  CALL_METHOD_2         2  '2 positional arguments'
              622  STORE_FAST               'aop'

 L. 158       624  LOAD_FAST                'aop'
              626  LOAD_CONST               None
              628  COMPARE_OP               is
          630_632  POP_JUMP_IF_FALSE   650  'to 650'

 L. 159       634  LOAD_GLOBAL              RuntimeError
              636  LOAD_STR                 'Sim {} failed to find carry posture aop for carry target {}.'
              638  LOAD_METHOD              format
              640  LOAD_DEREF               'sim'
              642  LOAD_FAST                'carry_target'
              644  CALL_METHOD_2         2  '2 positional arguments'
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  RAISE_VARARGS_1       1  'exception instance'
            650_0  COME_FROM           630  '630'

 L. 160       650  LOAD_FAST                'aop'
              652  LOAD_ATTR                affordance
              654  LOAD_ATTR                _carry_posture_type
              656  STORE_FAST               'carry_posture_type'

 L. 161       658  LOAD_FAST                'carry_posture_type'
              660  LOAD_CONST               None
              662  COMPARE_OP               is
          664_666  POP_JUMP_IF_FALSE   672  'to 672'

 L. 162       668  LOAD_GLOBAL              KeyError
              670  RAISE_VARARGS_1       1  'exception instance'
            672_0  COME_FROM           664  '664'

 L. 163       672  LOAD_FAST                'var_map'
              674  LOAD_GLOBAL              PostureSpecVariable
              676  LOAD_ATTR                POSTURE_TYPE_CARRY_OBJECT
              678  LOAD_FAST                'carry_posture_type'
              680  BUILD_MAP_1           1 
              682  INPLACE_ADD      
              684  STORE_FAST               'var_map'
            686_0  COME_FROM           600  '600'

 L. 165       686  LOAD_FAST                'var_map'
              688  LOAD_FAST                'spec_carry_target'
              690  BINARY_SUBSCR    
              692  STORE_FAST               'carry_target'

 L. 166       694  LOAD_FAST                'var_map'
              696  LOAD_FAST                'spec_carry_posture_type'
              698  BINARY_SUBSCR    
              700  STORE_FAST               'carry_posture_type'

 L. 167       702  LOAD_FAST                'spec_carry'
              704  LOAD_GLOBAL              CARRY_HAND_INDEX
              706  BINARY_SUBSCR    
              708  LOAD_FAST                'var_map'
              710  COMPARE_OP               in
          712_714  POP_JUMP_IF_FALSE   730  'to 730'

 L. 168       716  LOAD_FAST                'var_map'
              718  LOAD_FAST                'spec_carry'
              720  LOAD_GLOBAL              CARRY_HAND_INDEX
              722  BINARY_SUBSCR    
              724  BINARY_SUBSCR    
              726  STORE_FAST               'hand'
              728  JUMP_FORWARD        778  'to 778'
            730_0  COME_FROM           712  '712'

 L. 180       730  SETUP_LOOP          778  'to 778'
              732  LOAD_DEREF               'sim'
              734  LOAD_ATTR                posture_state
              736  LOAD_METHOD              get_free_hands
              738  CALL_METHOD_0         0  '0 positional arguments'
              740  GET_ITER         
            742_0  COME_FROM           758  '758'
              742  FOR_ITER            768  'to 768'
              744  STORE_FAST               'hand'

 L. 181       746  LOAD_FAST                'hand'
              748  LOAD_FAST                'carry_target'
              750  LOAD_METHOD              get_allowed_hands
              752  LOAD_DEREF               'sim'
              754  CALL_METHOD_1         1  '1 positional argument'
              756  COMPARE_OP               in
          758_760  POP_JUMP_IF_FALSE   742  'to 742'

 L. 182       762  BREAK_LOOP       
          764_766  JUMP_BACK           742  'to 742'
              768  POP_BLOCK        

 L. 184       770  LOAD_GLOBAL              RuntimeError
              772  LOAD_STR                 'No allowable free hand was empty.'
              774  CALL_FUNCTION_1       1  '1 positional argument'
              776  RAISE_VARARGS_1       1  'exception instance'
            778_0  COME_FROM_LOOP      730  '730'
            778_1  COME_FROM           728  '728'

 L. 186       778  LOAD_GLOBAL              postures
              780  LOAD_ATTR                create_posture
              782  LOAD_FAST                'carry_posture_type'

 L. 187       784  LOAD_FAST                'self'
              786  LOAD_ATTR                sim

 L. 188       788  LOAD_FAST                'carry_target'

 L. 189       790  LOAD_GLOBAL              hand_to_track
              792  LOAD_FAST                'hand'
              794  CALL_FUNCTION_1       1  '1 positional argument'

 L. 190       796  LOAD_FAST                'is_throwaway'
              798  LOAD_CONST               ('track', 'is_throwaway')
              800  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              802  STORE_FAST               'new_carry_aspect'

 L. 192       804  LOAD_FAST                'hand'
              806  LOAD_GLOBAL              Hand
              808  LOAD_ATTR                LEFT
              810  COMPARE_OP               ==
          812_814  POP_JUMP_IF_FALSE   856  'to 856'

 L. 193       816  LOAD_FAST                'new_carry_aspect'
              818  LOAD_FAST                'self'
              820  STORE_ATTR               _aspect_carry_left

 L. 194       822  LOAD_FAST                'current_posture_state'
              824  LOAD_CONST               None
              826  COMPARE_OP               is-not
          828_830  POP_JUMP_IF_FALSE   842  'to 842'

 L. 195       832  LOAD_FAST                'current_posture_state'
              834  LOAD_ATTR                right
              836  LOAD_FAST                'self'
              838  STORE_ATTR               _aspect_carry_right
              840  JUMP_FORWARD        854  'to 854'
            842_0  COME_FROM           828  '828'

 L. 197       842  LOAD_FAST                '_get_default_carry_aspect'
              844  LOAD_GLOBAL              PostureTrack
              846  LOAD_ATTR                RIGHT
              848  CALL_FUNCTION_1       1  '1 positional argument'
              850  LOAD_FAST                'self'
              852  STORE_ATTR               _aspect_carry_right
            854_0  COME_FROM           840  '840'
              854  JUMP_FORWARD       1186  'to 1186'
            856_0  COME_FROM           812  '812'

 L. 198       856  LOAD_FAST                'hand'
              858  LOAD_GLOBAL              Hand
              860  LOAD_ATTR                RIGHT
              862  COMPARE_OP               ==
          864_866  POP_JUMP_IF_FALSE   908  'to 908'

 L. 199       868  LOAD_FAST                'new_carry_aspect'
              870  LOAD_FAST                'self'
              872  STORE_ATTR               _aspect_carry_right

 L. 201       874  LOAD_FAST                'current_posture_state'
              876  LOAD_CONST               None
              878  COMPARE_OP               is-not
          880_882  POP_JUMP_IF_FALSE   894  'to 894'

 L. 202       884  LOAD_FAST                'current_posture_state'
              886  LOAD_ATTR                left
              888  LOAD_FAST                'self'
              890  STORE_ATTR               _aspect_carry_left
              892  JUMP_FORWARD        906  'to 906'
            894_0  COME_FROM           880  '880'

 L. 204       894  LOAD_FAST                '_get_default_carry_aspect'
              896  LOAD_GLOBAL              PostureTrack
              898  LOAD_ATTR                LEFT
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  LOAD_FAST                'self'
              904  STORE_ATTR               _aspect_carry_right
            906_0  COME_FROM           892  '892'
              906  JUMP_FORWARD       1186  'to 1186'
            908_0  COME_FROM           864  '864'

 L. 206       908  LOAD_GLOBAL              RuntimeError
              910  LOAD_STR                 'Invalid value specified for hand: {}'
              912  LOAD_METHOD              format
              914  LOAD_FAST                'hand'
              916  CALL_METHOD_1         1  '1 positional argument'
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  RAISE_VARARGS_1       1  'exception instance'
          922_924  JUMP_FORWARD       1186  'to 1186'
            926_0  COME_FROM           462  '462'
            926_1  COME_FROM           452  '452'

 L. 209       926  LOAD_FAST                'current_posture_state'
              928  LOAD_CONST               None
              930  COMPARE_OP               is-not
          932_934  POP_JUMP_IF_FALSE   954  'to 954'

 L. 210       936  LOAD_FAST                'current_posture_state'
              938  LOAD_ATTR                left
              940  LOAD_FAST                'self'
              942  STORE_ATTR               _aspect_carry_left

 L. 211       944  LOAD_FAST                'current_posture_state'
              946  LOAD_ATTR                right
              948  LOAD_FAST                'self'
              950  STORE_ATTR               _aspect_carry_right
              952  JUMP_FORWARD       1186  'to 1186'
            954_0  COME_FROM           932  '932'

 L. 213       954  LOAD_FAST                'spec_carry_target'
              956  LOAD_CONST               None
              958  COMPARE_OP               is-not
          960_962  POP_JUMP_IF_FALSE  1162  'to 1162'

 L. 214       964  LOAD_FAST                'var_map'
              966  LOAD_FAST                'spec_carry_target'
              968  BINARY_SUBSCR    
              970  STORE_FAST               'carry_target'

 L. 215       972  LOAD_FAST                'spec_carry'
              974  LOAD_GLOBAL              CARRY_POSTURE_TYPE_INDEX
              976  BINARY_SUBSCR    
              978  STORE_FAST               'spec_carry_posture_type'

 L. 216       980  LOAD_FAST                'var_map'
              982  LOAD_METHOD              get
              984  LOAD_FAST                'spec_carry_posture_type'
              986  CALL_METHOD_1         1  '1 positional argument'
              988  STORE_FAST               'carry_posture_type'

 L. 217       990  LOAD_FAST                'carry_posture_type'
              992  LOAD_CONST               None
              994  COMPARE_OP               is
          996_998  POP_JUMP_IF_FALSE  1038  'to 1038'

 L. 218      1000  LOAD_GLOBAL              get_carry_posture_aop
             1002  LOAD_DEREF               'sim'
             1004  LOAD_FAST                'carry_target'
             1006  CALL_FUNCTION_2       2  '2 positional arguments'
             1008  STORE_FAST               'aop'

 L. 219      1010  LOAD_FAST                'aop'
             1012  LOAD_CONST               None
             1014  COMPARE_OP               is
         1016_1018  POP_JUMP_IF_FALSE  1030  'to 1030'
             1020  LOAD_FAST                'invalid_expected'
         1022_1024  POP_JUMP_IF_FALSE  1030  'to 1030'

 L. 220      1026  LOAD_CONST               None
             1028  RETURN_VALUE     
           1030_0  COME_FROM          1022  '1022'
           1030_1  COME_FROM          1016  '1016'

 L. 221      1030  LOAD_FAST                'aop'
             1032  LOAD_ATTR                affordance
             1034  LOAD_ATTR                _carry_posture_type
             1036  STORE_FAST               'carry_posture_type'
           1038_0  COME_FROM           996  '996'

 L. 223      1038  LOAD_FAST                'spec_carry'
             1040  LOAD_GLOBAL              CARRY_HAND_INDEX
             1042  BINARY_SUBSCR    
             1044  LOAD_FAST                'var_map'
             1046  COMPARE_OP               in
         1048_1050  POP_JUMP_IF_FALSE  1066  'to 1066'

 L. 224      1052  LOAD_FAST                'var_map'
             1054  LOAD_FAST                'spec_carry'
             1056  LOAD_GLOBAL              CARRY_HAND_INDEX
             1058  BINARY_SUBSCR    
             1060  BINARY_SUBSCR    
             1062  STORE_FAST               'hand'
             1064  JUMP_FORWARD       1084  'to 1084'
           1066_0  COME_FROM          1048  '1048'

 L. 226      1066  LOAD_FAST                'carry_target'
             1068  LOAD_METHOD              get_allowed_hands
             1070  LOAD_DEREF               'sim'
             1072  CALL_METHOD_1         1  '1 positional argument'
             1074  STORE_FAST               'allowed_hands'

 L. 227      1076  LOAD_FAST                'allowed_hands'
             1078  LOAD_CONST               0
             1080  BINARY_SUBSCR    
             1082  STORE_FAST               'hand'
           1084_0  COME_FROM          1064  '1064'

 L. 229      1084  LOAD_GLOBAL              postures
             1086  LOAD_ATTR                create_posture
             1088  LOAD_FAST                'carry_posture_type'

 L. 230      1090  LOAD_FAST                'self'
             1092  LOAD_ATTR                sim

 L. 231      1094  LOAD_FAST                'carry_target'

 L. 232      1096  LOAD_GLOBAL              hand_to_track
             1098  LOAD_FAST                'hand'
             1100  CALL_FUNCTION_1       1  '1 positional argument'

 L. 233      1102  LOAD_FAST                'is_throwaway'
             1104  LOAD_CONST               ('track', 'is_throwaway')
             1106  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1108  STORE_FAST               'new_carry_aspect'

 L. 234      1110  LOAD_FAST                'hand'
             1112  LOAD_GLOBAL              Hand
             1114  LOAD_ATTR                LEFT
           1116_0  COME_FROM           854  '854'
             1116  COMPARE_OP               ==
         1118_1120  POP_JUMP_IF_FALSE  1142  'to 1142'

 L. 235      1122  LOAD_FAST                'new_carry_aspect'
             1124  LOAD_FAST                'self'
             1126  STORE_ATTR               _aspect_carry_left

 L. 236      1128  LOAD_FAST                '_get_default_carry_aspect'
             1130  LOAD_GLOBAL              PostureTrack
             1132  LOAD_ATTR                RIGHT
             1134  CALL_FUNCTION_1       1  '1 positional argument'
             1136  LOAD_FAST                'self'
             1138  STORE_ATTR               _aspect_carry_right
             1140  JUMP_FORWARD       1160  'to 1160'
           1142_0  COME_FROM          1118  '1118'

 L. 238      1142  LOAD_FAST                'new_carry_aspect'
             1144  LOAD_FAST                'self'
             1146  STORE_ATTR               _aspect_carry_right

 L. 239      1148  LOAD_FAST                '_get_default_carry_aspect'
             1150  LOAD_GLOBAL              PostureTrack
             1152  LOAD_ATTR                LEFT
             1154  CALL_FUNCTION_1       1  '1 positional argument'
             1156  LOAD_FAST                'self'
             1158  STORE_ATTR               _aspect_carry_left
           1160_0  COME_FROM          1140  '1140'
             1160  JUMP_FORWARD       1186  'to 1186'
           1162_0  COME_FROM           960  '960'

 L. 241      1162  LOAD_FAST                '_get_default_carry_aspect'
             1164  LOAD_GLOBAL              PostureTrack
             1166  LOAD_ATTR                LEFT
           1168_0  COME_FROM           906  '906'
             1168  CALL_FUNCTION_1       1  '1 positional argument'
             1170  LOAD_FAST                'self'
             1172  STORE_ATTR               _aspect_carry_left

 L. 242      1174  LOAD_FAST                '_get_default_carry_aspect'
             1176  LOAD_GLOBAL              PostureTrack
             1178  LOAD_ATTR                RIGHT
             1180  CALL_FUNCTION_1       1  '1 positional argument'
             1182  LOAD_FAST                'self'
             1184  STORE_ATTR               _aspect_carry_right
           1186_0  COME_FROM          1160  '1160'
           1186_1  COME_FROM           952  '952'
           1186_2  COME_FROM           922  '922'

Parse error at or near `COME_FROM' instruction at offset 1116_0

    def __repr__(self):
        return standard_repr(self, *self.aspects)

    @property
    def valid(self):
        return self._valid and bool(self.constraint_intersection)

    @property
    def spec(self):
        return self._spec

    def get_posture_spec(self, var_map):
        if not var_map:
            return self._spec.clone
        else:
            carry_target = var_map.get(PostureSpecVariable.CARRY_TARGET)
            if carry_target is not None:
                if carry_target.definition is not carry_target:
                    carry_posture = self.get_carry_posture(carry_target)
                else:
                    carry_posture = None
            elif carry_posture is not None:
                if PostureSpecVariable.HAND in var_map:
                    required_hand = track_to_hand(carry_posture.track)
                    if required_hand != var_map[PostureSpecVariable.HAND]:
                        return
                source_carry = PostureAspectCarry((PostureSpecVariable.POSTURE_TYPE_CARRY_OBJECT, PostureSpecVariable.CARRY_TARGET, PostureSpecVariable.HAND))
            else:
                source_carry = PostureAspectCarry((PostureSpecVariable.POSTURE_TYPE_CARRY_NOTHING, None, PostureSpecVariable.HAND))
            surface_spec = self._spec[SURFACE_INDEX]
            surface_target = surface_spec[SURFACE_TARGET_INDEX]
            if surface_target is not None:
                var_map_surface_target = var_map.getPostureSpecVariable.SURFACE_TARGETNone
                if var_map_surface_target is None or surface_target == var_map_surface_target:
                    if carry_target is not None:
                        if carry_posture is None:
                            if carry_target.definition is not carry_target:
                                surface_spec = PostureAspectSurface((surface_target, PostureSpecVariable.SLOT, PostureSpecVariable.CARRY_TARGET))
                                spec = self._spec.clone(carry=source_carry, surface=surface_spec)
                                if spec._validate_surface(var_map):
                                    if carry_target.parent is surface_target:
                                        return spec
                    interaction_target = var_map.getPostureSpecVariable.INTERACTION_TARGETPostureSpecVariable.INTERACTION_TARGET
                    if interaction_target is not None:
                        surface_spec = PostureAspectSurface((surface_target, PostureSpecVariable.SLOT, PostureSpecVariable.SLOT_TARGET))
                        spec = self._spec.clone(carry=source_carry, surface=surface_spec)
                        if spec._validate_surface(var_map) and not isinstance(interaction_target, PostureSpecVariable):
                            if interaction_target.parent is surface_target:
                                return spec
                    surface_spec = PostureAspectSurface((surface_target, PostureSpecVariable.SLOT, None))
                    spec = self._spec.clone(carry=source_carry, surface=surface_spec)
                    if spec._validate_surface(var_map):
                        return spec
                surface_spec = PostureAspectSurface((surface_target, None, None))
                spec = self._spec.clone(carry=source_carry, surface=surface_spec)
                if spec._validate_surface(var_map):
                    return spec
        surface_spec = PostureAspectSurface((None, None, None))
        spec = self._spec.clone(carry=source_carry, surface=surface_spec)
        if spec._validate_surface(var_map):
            return spec

    def _get_posture_constraint(self, strict=False):
        posture_state_constraint = self.body_posture_state_constraint
        posture_state_constraint = posture_state_constraint.get_holster_version
        if posture_state_constraint.valid:
            if not self.body_state_spec_only:
                carry_left_constraint = create_carry_constraint((self.left.target), (Hand.LEFT), strict=strict)
                posture_state_constraint = posture_state_constraint.intersect(carry_left_constraint)
                if posture_state_constraint.valid:
                    carry_right_constraint = create_carry_constraint((self.right.target), (Hand.RIGHT), strict=strict)
                    posture_state_constraint = posture_state_constraint.intersect(carry_right_constraint)
        return posture_state_constraint

    @property
    def posture_constraint(self):
        if self._posture_constraint is None:
            self._posture_constraint = self._get_posture_constraint
        return self._posture_constraint

    @property
    def posture_constraint_strict(self):
        if self._posture_constraint_strict is None:
            self._posture_constraint_strict = self._get_posture_constraint(strict=True)
        return self._posture_constraint_strict

    @property
    def sim(self):
        if self._sim_ref is not None:
            return self._sim_ref

    @property
    def linked_posture_state(self):
        return self._linked_posture_state

    @linked_posture_state.setter
    def linked_posture_state(self, posture_state):
        self._set_linked_posture_state(posture_state)
        posture_state._set_linked_posture_state(self)
        self.body.linked_posture = posture_state.body

    def _set_linked_posture_state(self, posture_state):
        self._linked_posture_state = posture_state

    @property
    def body(self):
        return self._aspect_body

    @property
    def left(self):
        return self._aspect_carry_left

    @property
    def right(self):
        return self._aspect_carry_right

    @property
    def aspects(self):
        if self.body_state_spec_only:
            return ()
        return (
         self.body, self.left, self.right)

    @property
    def carry_aspects(self):
        return (self.left, self.right)

    @property
    def surface_target(self):
        surface = self._spec[SURFACE_INDEX][SURFACE_TARGET_INDEX]
        if surface is None or self.body.mobile:
            if self.body.target is not None:
                if self.body.target.is_surface:
                    return self.body.target
        return surface

    @property
    def carry_targets(self):
        return (self.left.target, self.right.target)

    def get_aspect(self, track):
        if track == PostureTrack.BODY:
            return self.body
        if track == PostureTrack.LEFT:
            return self.left
        if track == PostureTrack.RIGHT:
            return self.right

    def add_constraint(self, handle, constraint):
        if not self._invalid_expected:
            if not constraint.valid:
                logger.warn('Attempt to add an invalid constraint {} to posture_state {}.', constraint, self, owner='bhill', trigger_breakpoint=True)
            test_constraint = self.constraint_intersection.intersect(constraint)
            if not test_constraint.valid:
                logger.warn'Attempt to add a constraint to {} which is incompatible with already-registered constraints: {} + {}.'selfconstraintself.constraint_intersection
        self._constraints[handle] = constraint
        self._constraint_intersection_dirty = True

    def remove_constraint(self, handle):
        if handle in self._constraints:
            del self._constraints[handle]
            self._constraint_intersection_dirty = True
            self._constraint_intersection = None

    @property
    def constraint_intersection(self):
        if self._constraint_intersection_dirty or self._constraint_intersection is None:
            intersection = Anywhere()
            for constraint in set(self._constraints.values):
                new_intersection = intersection.intersect(constraint)
                if not self._invalid_expected:
                    if not new_intersection.valid:
                        indent_text = '                '
                        logger.error('Invalid constraint intersection for PostureState: {}.\n    A: {} \n    A Geometry: {}    B: {} \n    B Geometry: {}', self, intersection, intersection.get_geometry_text(indent_text), constraint, constraint.get_geometry_text(indent_text))
                        intersection = new_intersection
                        break
                intersection = new_intersection

            self._constraint_intersection_dirty = False
            self._constraint_intersection = intersection
        return self._constraint_intersection

    def compatible_with(self, constraint):
        intersection = self.constraint_intersection
        if not intersection.valid:
            return False
        else:
            intersection = constraint.intersect(intersection)
            return intersection.valid or False
        return True

    def compatible_with_pre_resolve(self, constraint):
        for constraint_existing in self._constraints.values:
            if constraint_existing is constraint:
                return True

        return self.compatible_with(constraint)

    def get_slot_info(self):
        surface = self._spec[SURFACE_INDEX]
        return (surface[SURFACE_TARGET_INDEX], surface[SURFACE_SLOT_TYPE_INDEX])

    def is_source_interaction(self, si):
        if si is not None:
            for aspect in self.aspects:
                if aspect.source_interaction is si:
                    return True

        return False

    def is_source_or_owning_interaction(self, si):
        return self.get_source_or_owned_posture_for_si(si) is not None

    def is_carry_source_or_owning_interaction(self, si):
        return self.get_source_or_owned_posture_for_si(si, carry_only=True) is not None

    def get_source_or_owned_posture_for_si(self, si, carry_only=False):
        if self.left.source_interaction is si or si in self.left.owning_interactions:
            return self.left
        if self.right.source_interaction is si or si in self.right.owning_interactions:
            return self.right
        if carry_only:
            return
        if self.body.source_interaction is si or si in self.body.owning_interactions:
            return self.body

    @property
    def connectivity_handles(self):
        if self.body.target is not None:
            return self.body.target.connectivity_handles

    def kickstart_gen(self, timeline, routing_surface, target_override=None):
        for aspect in self.aspects:
            yield from aspect.kickstart_gen(timeline, self, routing_surface, target_override=target_override)

        self._valid = True
        if False:
            yield None

    def on_reset(self, reset_reason):
        for aspect in self.aspects:
            aspect.reset

        self._valid = False

    def _carrying(self, track, **kwargs):
        posture = self.left if track == PostureTrack.LEFT else self.right
        return (self._carrying_posture)(posture, **kwargs)

    def _carrying_posture(self, posture, ignore_target=None, only_target=None):
        if posture is not None:
            if posture.is_active_carry:
                if ignore_target is None:
                    if only_target is None:
                        return True
                else:
                    target = posture.target

                    def target_is(other):
                        if target is None:
                            return False
                        if isinstance(other, Tag):
                            return target.has_tag(other)
                        if isinstance(other, int):
                            return target.definition.id == other
                        if isinstance(other, Definition):
                            return target.definition is other
                        return target is other

                    if not (ignore_target is None or target_is(ignore_target)):
                        if only_target is None or target_is(only_target):
                            return True
        return False

    def get_carry_state(self, target=None, override_posture=None):
        if override_posture is not None:
            if override_posture.track == PostureTrack.LEFT:
                carry_state = (
                 self._carrying_posture(override_posture, ignore_target=target),
                 self._carrying((PostureTrack.RIGHT), ignore_target=target))
            else:
                carry_state = (
                 self._carrying((PostureTrack.LEFT), ignore_target=target),
                 self._carrying_posture(override_posture, ignore_target=target))
        else:
            carry_state = (
             self._carrying((PostureTrack.LEFT), ignore_target=target),
             self._carrying((PostureTrack.RIGHT), ignore_target=target))
        return carry_state

    def get_carry_track(self, target):
        if target is None:
            return
        if self._carrying((PostureTrack.LEFT), only_target=target):
            return PostureTrack.LEFT
        if self._carrying((PostureTrack.RIGHT), only_target=target):
            return PostureTrack.RIGHT

    def is_carrying(self, target):
        if self.get_carry_track(target) is not None:
            return True
        return False

    def get_carry_posture(self, target):
        if self.left.target is target:
            return self.left
        if self.right.target is target:
            return self.right

    def get_posture_for_si(self, si):
        for posture in self.aspects:
            if posture is not None and posture.source_interaction == si:
                return posture

    def get_other_carry_posture(self, target):
        track = self.get_carry_track(target)
        if track is None:
            return
        elif track is PostureTrack.LEFT:
            result = self.get_aspect(PostureTrack.RIGHT)
        else:
            result = self.get_aspect(PostureTrack.LEFT)
        if result is not None:
            if result.target is not None:
                return result

    def get_free_carry_track(self, obj=None) -> PostureTrack:
        if obj is not None:
            if obj.carryable_component is None:
                logger.error('Obj {} has no carryable component.', obj, owner='tastle')
                return
        else:
            if obj is None:
                allowed_hands = (
                 Hand.RIGHT, Hand.LEFT)
            else:
                allowed_hands = obj.get_allowed_hands(self.sim)
            preferred_hand = self.sim.get_preferred_hand
            if preferred_hand == Hand.RIGHT:
                preferred_track = PostureTrack.RIGHT
                unpreferred_track = PostureTrack.LEFT
            else:
                preferred_track = PostureTrack.LEFT
                unpreferred_track = PostureTrack.RIGHT
            if track_to_hand(preferred_track) in allowed_hands:
                if not self._carrying(preferred_track):
                    return preferred_track
            if track_to_hand(unpreferred_track) in allowed_hands:
                return self._carrying(unpreferred_track) or unpreferred_track

    def get_free_hands(self):
        if not self._carrying(PostureTrack.RIGHT):
            if not self._carrying(PostureTrack.LEFT):
                return (
                 Hand.RIGHT, Hand.LEFT)
        else:
            return (
             Hand.RIGHT,)
            return self._carrying(PostureTrack.LEFT) or (
             Hand.LEFT,)
        return ()