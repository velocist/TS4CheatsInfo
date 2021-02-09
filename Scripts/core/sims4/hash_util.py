# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Core\sims4\hash_util.py
# Compiled at: 2019-10-02 21:24:51
# Size of source mod 2**32: 3154 bytes
from singletons import DEFAULT
import _hashutil
hash32 = _hashutil.hash32
hash64 = _hashutil.hash64
try:
    KEYNAMEMAPTYPE_UNUSED = _hashutil.KEYNAMEMAPTYPE_UNUSED
    KEYNAMEMAPTYPE_RESOURCES = _hashutil.KEYNAMEMAPTYPE_RESOURCES
    KEYNAMEMAPTYPE_RESOURCESTRINGS = _hashutil.KEYNAMEMAPTYPE_RESOURCESTRINGS
    KEYNAMEMAPTYPE_OBJECTINSTANCES = _hashutil.KEYNAMEMAPTYPE_OBJECTINSTANCES
    KEYNAMEMAPTYPE_SWARM = _hashutil.KEYNAMEMAPTYPE_SWARM
    KEYNAMEMAPTYPE_STRINGHASHES = _hashutil.KEYNAMEMAPTYPE_STRINGHASHES
    KEYNAMEMAPTYPE_TUNINGINSTANCES = _hashutil.KEYNAMEMAPTYPE_TUNINGINSTANCES
    KEYNAMEMAPTYPE_END = _hashutil.KEYNAMEMAPTYPE_END
except:
    pass

def unhash(value: int, table_type: int=None):
    if value < 0:
        raise ValueError('Negative numbers are not valid hashes.')
    elif table_type is None:
        result = _hashutil.unhash64(value)
    else:
        result = _hashutil.unhash64(value, table_type)
    return '#{}#'.format(result)


def unhash_with_fallback(value, fallback_pattern=DEFAULT, table_type: int=None):
    if fallback_pattern is DEFAULT:
        if value < 8589934592:
            fallback_pattern = '{:#010x}'
        else:
            fallback_pattern = '{:#018x}'
    return fallback_pattern.format(value)


def obj_str_hash(obj):
    return hash(str(obj))