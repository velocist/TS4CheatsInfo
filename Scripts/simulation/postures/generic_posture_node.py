# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\postures\generic_posture_node.py
# Compiled at: 2018-10-30 00:13:01
# Size of source mod 2**32: 520 bytes
from objects.proxy import ProxyObject

class SimPostureNode(ProxyObject):

    def __str__(self):
        return 'Generic Sim Node ' + str(self._proxied_obj)

    @property
    def sim_proxied(self):
        return self._proxied_obj