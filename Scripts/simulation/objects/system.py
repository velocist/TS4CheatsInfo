# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\system.py
# Compiled at: 2020-03-06 03:59:53
# Size of source mod 2**32: 19222 bytes
from objects.gallery_tuning import ContentSource
from objects.object_enums import ResetReason
from objects.persistence_groups import PersistenceGroups
from sims4.tuning.tunable import Tunable
from sims4.utils import exception_protected
import build_buy, services, sims4, sims4.log
LOG_CHANNEL = 'Objects'
logger = sims4.log.Logger(LOG_CHANNEL)
production_logger = sims4.log.ProductionLogger(LOG_CHANNEL)

class SystemTuning:
    build_buy_lockout_duration = Tunable(int, 5, description='Number of seconds an object should stay locked for after it is manipulated in Build/Buy.')


@exception_protected
def c_api_get_object_definition(obj_id, zone_id):
    obj = find_object(obj_id)
    if obj is None:
        return
    return obj.definition.id


@exception_protected
def c_api_get_object_def_state(obj_id, zone_id):
    obj = find_object(obj_id)
    if obj is None:
        return
    return obj.state_index


def c_api_get_object_attributes(obj_id, zone_id):
    obj = find_object(obj_id)
    if obj is None:
        return
    return (
     obj.definition.id, obj.state_index, obj.transform, obj.routing_surface)


def create_script_object(definition_or_id, obj_state=0, **kwargs):
    from objects.definition import Definition
    if isinstance(definition_or_id, Definition):
        definition = definition_or_id
    else:
        definition = services.definition_manager().get(definition_or_id, obj_state=obj_state)
        if definition is None:
            logger.error('Unable to create a script object for definition id: {0}', definition_or_id)
            return
    return (definition.instantiate)(obj_state=obj_state, **kwargs)


@exception_protected
def c_api_create_object(zone_id, def_id, obj_id, obj_state, loc_type, content_source=ContentSource.DEFAULT):
    return create_object(def_id, obj_id=obj_id, obj_state=obj_state, loc_type=loc_type, content_source=content_source)


@exception_protected
def c_api_set_part_owner(zone_id, part_owner_id, part_id):
    part_owner = find_object(part_owner_id)
    part = find_object(part_id)
    if part_owner is None or part is None:
        return False
    part.part_owner = part_owner
    return True


@exception_protected
def c_api_start_delaying_posture_graph_adds():
    pass


@exception_protected
def c_api_stop_delaying_posture_graph_adds():
    pass


def create_object--- This code section failed: ---

 L. 136         0  LOAD_CONST               0
                2  LOAD_CONST               ('BaseObject',)
                4  IMPORT_NAME_ATTR         objects.base_object
                6  IMPORT_FROM              BaseObject
                8  STORE_FAST               'BaseObject'
               10  POP_TOP          

 L. 137        12  LOAD_CONST               0
               14  LOAD_CONST               ('ItemLocation',)
               16  IMPORT_NAME_ATTR         objects.object_enums
               18  IMPORT_FROM              ItemLocation
               20  STORE_FAST               'ItemLocation'
               22  POP_TOP          

 L. 138        24  LOAD_CONST               False
               26  STORE_FAST               'added_to_object_manager'

 L. 139        28  LOAD_CONST               None
               30  STORE_FAST               'obj'

 L. 141        32  LOAD_FAST                'loc_type'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 142        40  LOAD_FAST                'ItemLocation'
               42  LOAD_ATTR                ON_LOT
               44  STORE_FAST               'loc_type'
             46_0  COME_FROM            38  '38'

 L. 144     46_48  SETUP_FINALLY       468  'to 468'

 L. 145        50  LOAD_CONST               0
               52  LOAD_CONST               ('Definition',)
               54  IMPORT_NAME_ATTR         objects.definition
               56  IMPORT_FROM              Definition
               58  STORE_FAST               'Definition'
               60  POP_TOP          

 L. 146        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'definition_or_id'
               66  LOAD_FAST                'Definition'
               68  CALL_FUNCTION_2       2  '2 positional arguments'
               70  POP_JUMP_IF_FALSE   102  'to 102'

 L. 147        72  LOAD_GLOBAL              build_buy
               74  LOAD_METHOD              get_vetted_object_defn_guid
               76  LOAD_FAST                'obj_id'
               78  LOAD_FAST                'definition_or_id'
               80  LOAD_ATTR                id
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  STORE_FAST               'fallback_definition_id'

 L. 148        86  LOAD_FAST                'fallback_definition_id'
               88  LOAD_FAST                'definition_or_id'
               90  LOAD_ATTR                id
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   114  'to 114'

 L. 149        96  LOAD_FAST                'fallback_definition_id'
               98  STORE_FAST               'definition_or_id'
              100  JUMP_FORWARD        114  'to 114'
            102_0  COME_FROM            70  '70'

 L. 151       102  LOAD_GLOBAL              build_buy
              104  LOAD_METHOD              get_vetted_object_defn_guid
              106  LOAD_FAST                'obj_id'
              108  LOAD_FAST                'definition_or_id'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  STORE_FAST               'definition_or_id'
            114_0  COME_FROM           100  '100'
            114_1  COME_FROM            94  '94'

 L. 153       114  LOAD_FAST                'definition_or_id'
              116  LOAD_CONST               None
              118  COMPARE_OP               is
              120  POP_JUMP_IF_FALSE   126  'to 126'

 L. 156       122  LOAD_CONST               None
              124  RETURN_VALUE     
            126_0  COME_FROM           120  '120'

 L. 158       126  LOAD_GLOBAL              create_script_object
              128  LOAD_FAST                'definition_or_id'
              130  BUILD_TUPLE_1         1 
              132  LOAD_FAST                'kwargs'
              134  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              136  STORE_FAST               'obj'

 L. 160       138  LOAD_FAST                'obj'
              140  LOAD_CONST               None
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   150  'to 150'

 L. 161       146  LOAD_CONST               None
              148  RETURN_VALUE     
            150_0  COME_FROM           144  '144'

 L. 163       150  LOAD_GLOBAL              isinstance
              152  LOAD_FAST                'obj'
              154  LOAD_FAST                'BaseObject'
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  POP_JUMP_IF_TRUE    180  'to 180'

 L. 164       160  LOAD_GLOBAL              logger
              162  LOAD_METHOD              error
              164  LOAD_STR                 'Type {0} is not a valid managed object.  It is not a subclass of BaseObject.'
              166  LOAD_GLOBAL              type
              168  LOAD_FAST                'obj'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  CALL_METHOD_2         2  '2 positional arguments'
              174  POP_TOP          

 L. 165       176  LOAD_CONST               None
              178  RETURN_VALUE     
            180_0  COME_FROM           158  '158'

 L. 167       180  LOAD_FAST                'init'
              182  LOAD_CONST               None
              184  COMPARE_OP               is-not
              186  POP_JUMP_IF_FALSE   196  'to 196'

 L. 168       188  LOAD_FAST                'init'
              190  LOAD_FAST                'obj'
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  POP_TOP          
            196_0  COME_FROM           186  '186'

 L. 170       196  LOAD_FAST                'loc_type'
              198  LOAD_FAST                'ItemLocation'
              200  LOAD_ATTR                FROM_WORLD_FILE
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_TRUE    216  'to 216'
              206  LOAD_FAST                'loc_type'
              208  LOAD_FAST                'ItemLocation'
              210  LOAD_ATTR                FROM_CONDITIONAL_LAYER
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   224  'to 224'
            216_0  COME_FROM           204  '204'

 L. 171       216  LOAD_GLOBAL              PersistenceGroups
              218  LOAD_ATTR                IN_OPEN_STREET
              220  LOAD_FAST                'obj'
              222  STORE_ATTR               persistence_group
            224_0  COME_FROM           214  '214'

 L. 173       224  LOAD_FAST                'loc_type'
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
              230  POP_JUMP_IF_FALSE   240  'to 240'
              232  LOAD_FAST                'ItemLocation'
              234  LOAD_FAST                'loc_type'
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  JUMP_FORWARD        244  'to 244'
            240_0  COME_FROM           230  '230'
              240  LOAD_FAST                'ItemLocation'
              242  LOAD_ATTR                INVALID_LOCATION
            244_0  COME_FROM           238  '238'
              244  LOAD_FAST                'obj'
              246  STORE_ATTR               item_location

 L. 174       248  LOAD_FAST                'obj_id'
              250  LOAD_FAST                'obj'
              252  STORE_ATTR               id

 L. 175       254  LOAD_FAST                'content_source'
              256  LOAD_FAST                'obj'
              258  STORE_ATTR               content_source

 L. 178       260  LOAD_FAST                'disable_object_commodity_callbacks'
          262_264  POP_JUMP_IF_TRUE    278  'to 278'
              266  LOAD_GLOBAL              services
              268  LOAD_METHOD              current_zone
              270  CALL_METHOD_0         0  '0 positional arguments'
              272  LOAD_ATTR                suppress_object_commodity_callbacks
          274_276  POP_JUMP_IF_FALSE   312  'to 312'
            278_0  COME_FROM           262  '262'

 L. 179       278  LOAD_FAST                'obj'
              280  LOAD_ATTR                is_sim
          282_284  POP_JUMP_IF_TRUE    312  'to 312'

 L. 180       286  LOAD_FAST                'obj'
              288  LOAD_ATTR                commodity_tracker
              290  STORE_FAST               'commodity_tracker'

 L. 181       292  LOAD_FAST                'commodity_tracker'
              294  LOAD_CONST               None
              296  COMPARE_OP               is-not
          298_300  POP_JUMP_IF_FALSE   312  'to 312'

 L. 182       302  LOAD_FAST                'commodity_tracker'
              304  LOAD_METHOD              set_callback_alarm_calculation_supression
              306  LOAD_CONST               True
              308  CALL_METHOD_1         1  '1 positional argument'
              310  POP_TOP          
            312_0  COME_FROM           298  '298'
            312_1  COME_FROM           282  '282'
            312_2  COME_FROM           274  '274'

 L. 184       312  LOAD_FAST                'loc_type'
              314  LOAD_FAST                'ItemLocation'
              316  LOAD_ATTR                ON_LOT
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_TRUE    372  'to 372'

 L. 185       324  LOAD_FAST                'loc_type'
              326  LOAD_FAST                'ItemLocation'
              328  LOAD_ATTR                FROM_WORLD_FILE
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_TRUE    372  'to 372'

 L. 186       336  LOAD_FAST                'loc_type'
              338  LOAD_FAST                'ItemLocation'
              340  LOAD_ATTR                FROM_OPEN_STREET
              342  COMPARE_OP               ==
          344_346  POP_JUMP_IF_TRUE    372  'to 372'

 L. 187       348  LOAD_FAST                'loc_type'
              350  LOAD_FAST                'ItemLocation'
              352  LOAD_ATTR                HOUSEHOLD_INVENTORY
              354  COMPARE_OP               ==
          356_358  POP_JUMP_IF_TRUE    372  'to 372'

 L. 188       360  LOAD_FAST                'loc_type'
              362  LOAD_FAST                'ItemLocation'
              364  LOAD_ATTR                FROM_CONDITIONAL_LAYER
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   386  'to 386'
            372_0  COME_FROM           356  '356'
            372_1  COME_FROM           344  '344'
            372_2  COME_FROM           332  '332'
            372_3  COME_FROM           320  '320'

 L. 189       372  LOAD_FAST                'obj'
              374  LOAD_ATTR                object_manager_for_create
              376  LOAD_METHOD              add
              378  LOAD_FAST                'obj'
              380  CALL_METHOD_1         1  '1 positional argument'
              382  POP_TOP          
              384  JUMP_FORWARD        442  'to 442'
            386_0  COME_FROM           368  '368'

 L. 190       386  LOAD_FAST                'loc_type'
              388  LOAD_FAST                'ItemLocation'
              390  LOAD_ATTR                SIM_INVENTORY
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_TRUE    410  'to 410'
              398  LOAD_FAST                'loc_type'
              400  LOAD_FAST                'ItemLocation'
              402  LOAD_ATTR                OBJECT_INVENTORY
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   428  'to 428'
            410_0  COME_FROM           394  '394'

 L. 191       410  LOAD_GLOBAL              services
              412  LOAD_METHOD              current_zone
              414  CALL_METHOD_0         0  '0 positional arguments'
              416  LOAD_ATTR                inventory_manager
              418  LOAD_METHOD              add
              420  LOAD_FAST                'obj'
              422  CALL_METHOD_1         1  '1 positional argument'
              424  POP_TOP          
              426  JUMP_FORWARD        442  'to 442'
            428_0  COME_FROM           406  '406'

 L. 193       428  LOAD_GLOBAL              logger
              430  LOAD_ATTR                error
              432  LOAD_STR                 'Unsupported loc_type passed to create_script_object.  We likely need to update this code path.'
              434  LOAD_STR                 'mduke'
              436  LOAD_CONST               ('owner',)
              438  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              440  POP_TOP          
            442_0  COME_FROM           426  '426'
            442_1  COME_FROM           384  '384'

 L. 194       442  LOAD_CONST               True
              444  STORE_FAST               'added_to_object_manager'

 L. 196       446  LOAD_FAST                'post_add'
              448  LOAD_CONST               None
              450  COMPARE_OP               is-not
          452_454  POP_JUMP_IF_FALSE   464  'to 464'

 L. 197       456  LOAD_FAST                'post_add'
              458  LOAD_FAST                'obj'
              460  CALL_FUNCTION_1       1  '1 positional argument'
              462  POP_TOP          
            464_0  COME_FROM           452  '452'

 L. 199       464  LOAD_FAST                'obj'
              466  RETURN_VALUE     
            468_0  COME_FROM_FINALLY    46  '46'

 L. 201       468  LOAD_FAST                'added_to_object_manager'
          470_472  POP_JUMP_IF_TRUE    502  'to 502'
              474  LOAD_FAST                'obj'
              476  LOAD_CONST               None
              478  COMPARE_OP               is-not
          480_482  POP_JUMP_IF_FALSE   502  'to 502'

 L. 203       484  LOAD_CONST               0
              486  LOAD_CONST               None
              488  IMPORT_NAME              _weakrefutils
              490  STORE_FAST               '_weakrefutils'

 L. 204       492  LOAD_FAST                '_weakrefutils'
              494  LOAD_METHOD              clear_weak_refs
              496  LOAD_FAST                'obj'
              498  CALL_METHOD_1         1  '1 positional argument'
              500  POP_TOP          
            502_0  COME_FROM           480  '480'
            502_1  COME_FROM           470  '470'
              502  END_FINALLY      

Parse error at or near `JUMP_FORWARD' instruction at offset 384


def _get_id_for_obj_or_id(obj_or_id):
    from objects.base_object import BaseObject
    if isinstance(obj_or_id, BaseObject):
        return obj_or_id.id
    return int(obj_or_id)


def _get_obj_for_obj_or_id(obj_or_id):
    from objects.base_object import BaseObject
    if not isinstance(obj_or_id, BaseObject):
        obj = services.object_manager().get(obj_or_id)
        if obj is None:
            logger.error('Could not find the target id {} for a RequiredTargetParam in the object manager.', obj_or_id)
        return obj
    return obj_or_id


@exception_protected
def c_api_destroy_object(zone_id, obj_or_id):
    obj = _get_obj_for_obj_or_id(obj_or_id)
    if obj is not None:
        return obj.destroy(source=obj, cause='Destruction request from C.')
    return False


@exception_protected
def c_api_reset_object(zone_id, obj_or_id):
    return reset_object(obj_or_id, expected=True, cause='Build/Buy')


def reset_object(obj_or_id, expected, cause=None):
    obj = _get_obj_for_obj_or_id(obj_or_id)
    if obj is not None:
        obj.reset(ResetReason.RESET_EXPECTED if expected else ResetReason.RESET_ON_ERROR, None, cause)
        return True
    return False


def remove_object_from_client(obj_or_id, **kwargs):
    obj = _get_obj_for_obj_or_id(obj_or_id)
    manager = obj.manager
    if obj.id in manager:
        (manager.remove_from_client)(obj, **kwargs)
        return True
    return False


def create_prop(definition_or_id, is_basic=False, **kwargs):
    from objects.prop_object import BasicPropObject, PropObject
    cls_override = BasicPropObject if is_basic else PropObject
    return create_object(definition_or_id, cls_override=cls_override, **kwargs)


def create_prop_with_footprint(definition_or_id, **kwargs):
    from objects.prop_object import PropObjectWithFootprint
    return create_object(definition_or_id, cls_override=PropObjectWithFootprint, **kwargs)


@exception_protected
def c_api_find_object(obj_id, zone_id):
    return find_object(obj_id)


def find_object(obj_id, **kwargs):
    return (services.current_zone().find_object)(obj_id, **kwargs)


@exception_protected
def c_api_get_objects(zone_id):
    return get_objects()


def get_objects():
    return services.object_manager().get_all()


@exception_protected
def c_api_set_object_state_index(obj_id, state_index, zone_id):
    obj = find_object(obj_id)
    obj.set_object_def_state_index(state_index)


@exception_protected(default_return=False)
def c_api_set_build_buy_lockout(zone_id, obj_or_id, lockout_state, permanent_lock=False):
    obj = _get_obj_for_obj_or_id(obj_or_id)
    if obj is not None:
        obj.set_build_buy_lockout_state(False, None)
        return True
        obj.set_build_buy_lockout_state(lockout_state, SystemTuning.build_buy_lockout_duration)
        return True
    return False


@exception_protected(default_return=(-1))
def c_api_set_parent_object(obj_id, parent_id, transform, joint_name, slot_hash, zone_id):
    set_parent_object(obj_id, parent_id, transform, joint_name, slot_hash)


@exception_protected
def c_api_get_buildbuy_use_flags(zone_id, object_id):
    obj = find_object(object_id)
    return obj.build_buy_use_flags


@exception_protected
def c_api_set_buildbuy_use_flags(zone_id, object_id, build_buy_use_flags):
    obj = find_object(object_id)
    if obj is not None:
        obj.build_buy_use_flags = build_buy_use_flags
        return True
    return False


def set_parent_object(obj_id, parent_id, transform=sims4.math.Transform.IDENTITY(), joint_name=None, slot_hash=0):
    obj = find_object(obj_id)
    parent_obj = find_object(parent_id)
    obj.set_parent(parent_obj, transform, joint_name_or_hash=joint_name, slot_hash=slot_hash)


@exception_protected(default_return=(-1))
def c_api_clear_parent_object(obj_id, transform, zone_id, surface):
    obj = find_object(obj_id)
    obj.clear_parent(transform, surface)


@exception_protected
def c_api_get_parent(obj_id, zone_id):
    obj = find_object(obj_id, include_props=True)
    if obj is not None:
        return obj.bb_parent


@exception_protected(default_return=0)
def c_api_get_slot_hash(obj_id, zone_id):
    obj = find_object(obj_id, include_props=True)
    if obj is not None:
        return obj.bone_name_hash
    return 0


@exception_protected(default_return=0)
def c_api_set_slot_hash(obj_id, zone_id, slot_hash):
    obj = find_object(obj_id)
    if obj is not None:
        obj.slot_hash = slot_hash


@exception_protected(default_return=(iter(())))
def c_api_get_all_children_gen(obj_id):
    obj = find_object(obj_id)
    if obj is not None:
        try:
            yield from obj.get_all_children_gen()
        except AttributeError:
            pass

    if False:
        yield None


@exception_protected(default_return=True)
def c_api_clear_default_children(obj_id):
    obj = find_object(obj_id, include_props=True)
    if obj is not None:
        try:
            obj.clear_default_children()
            return True
        except AttributeError:
            logger.error('Trying to clear children, but obj({}) does not support functionality', obj)

    return False