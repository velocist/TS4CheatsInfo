# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Core\sims4\tuning\tunable_hash.py
# Compiled at: 2019-04-27 01:15:13
# Size of source mod 2**32: 2640 bytes
from sims4.tuning.tunable import Tunable
import sims4.hash_util

class _Hash(int):

    def __new__(cls, value, hashed_value):
        h = int.__new__(cls, hashed_value)
        h.unhash = value
        return h

    def __str__(self):
        return '{} ({:#x})'.format(self.unhash, self)

    def __getnewargs__(self):
        return (
         self.unhash, int(self))


class _TunableStringHash(Tunable):

    def __init__(self, default=None, **kwargs):
        (super().__init__)(str, default=default, **kwargs)

    def _convert_to_value(self, content):
        if content is not None:
            hash_fn = self._get_hash_fn()
            return hash_fn(content)

    def _get_hash_fn(self):
        raise NotImplementedError


class TunableStringHash32(_TunableStringHash):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.cache_key = 'TunableStringHash32'

    def _get_hash_fn(self):
        return sims4.hash_util.hash32


class TunableStringHash64(_TunableStringHash):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.cache_key = 'TunableStringHash64'

    def _get_hash_fn(self):
        return sims4.hash_util.hash64