# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\mutex.py
# Compiled at: 2017-05-19 00:02:59
# Size of source mod 2**32: 1211 bytes
from collections import defaultdict
import element_utils, sims4.reload
with sims4.reload.protected(globals()):
    mutex_data = defaultdict(list)

def with_mutex(key, sequence):

    def do_acquire(timeline):
        key_data = mutex_data[key]
        if key_data:
            waiting_element = element_utils.soft_sleep_forever()
            key_data.append(waiting_element)
            yield from element_utils.run_child(timeline, waiting_element)
        else:
            key_data.append(None)
        yield from element_utils.run_child(timeline, sequence)
        key_data = mutex_data[key]
        del key_data[0]
        if key_data:
            key_data[0].trigger_soft_stop()
        else:
            del mutex_data[key]
        return True
        if False:
            yield None

    return do_acquire