# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\services\object_routing_service.py
# Compiled at: 2019-07-27 01:18:42
# Size of source mod 2**32: 1294 bytes
from _weakrefset import WeakSet
from event_testing.register_test_event_mixin import RegisterTestEventMixin
from sims4.service_manager import Service
from _collections import defaultdict

class ObjectRoutingService(RegisterTestEventMixin, Service):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._active_objects = defaultdict(WeakSet)

    def on_routing_start(self, obj, tracking_category, behavior):
        self._active_objects[tracking_category].add(obj)

    def on_routing_stop(self, obj, tracking_category):
        self._active_objects[tracking_category].remove(obj)

    def get_routing_object_set(self, tracking_category):
        return self._active_objects[tracking_category]

    def get_routing_object_count(self, tracking_category):
        return len(self.get_routing_object_set(tracking_category))