# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\walkstyle\walkstyle_request.py
# Compiled at: 2017-06-24 00:16:23
# Size of source mod 2**32: 2308 bytes
from element_utils import build_critical_section_with_finally
from routing.walkstyle.walkstyle_enums import WalkStylePriority
from routing.walkstyle.walkstyle_tuning import TunableWalkstyle
from sims4.tuning.tunable import AutoFactoryInit, HasTunableFactory, TunableEnumEntry
from uid import unique_id

@unique_id('request_id')
class WalkStyleRequest(HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'walkstyle':TunableWalkstyle(description='\n            The locomotion resource (i.e. walkstyle) to request. Depending\n            on the tuned priority and other requests active on the Sim, this\n            may or may not apply immediately.\n            '), 
     'priority':TunableEnumEntry(description='\n            The priority of the walkstyle. Higher priority walkstyles will take\n            precedence over lower priority. Equal priority will favor recent\n            requests.\n            ',
       tunable_type=WalkStylePriority,
       default=WalkStylePriority.INVALID,
       invalid_enums=(
      WalkStylePriority.INVALID,))}

    def __init__(self, obj, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._obj = obj.ref()

    def start(self, *_, **__):
        obj = self._obj()
        if obj is None:
            return
        obj.request_walkstyle(self, self.request_id)

    def stop(self, *_, **__):
        obj = self._obj()
        if obj is None:
            return
        obj.remove_walkstyle(self.request_id)

    def __call__(self, sequence=()):
        return build_critical_section_with_finally(self.start, sequence, self.stop)