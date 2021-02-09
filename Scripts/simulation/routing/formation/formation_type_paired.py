# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\formation\formation_type_paired.py
# Compiled at: 2018-10-24 18:56:03
# Size of source mod 2**32: 707 bytes
from protocolbuffers import Routing_pb2
from routing.formation.formation_type_base import FormationTypeBase, FormationRoutingType
from sims4.utils import classproperty

class FormationTypePaired(FormationTypeBase):

    @classproperty
    def routing_type():
        return FormationRoutingType.PARIED

    @property
    def slave_attachment_type(self):
        return Routing_pb2.SlaveData.SLAVE_PAIRED_CHILD