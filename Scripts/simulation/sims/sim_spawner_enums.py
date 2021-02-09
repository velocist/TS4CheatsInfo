# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\sim_spawner_enums.py
# Compiled at: 2017-03-18 00:27:02
# Size of source mod 2**32: 7885 bytes
from protocolbuffers import FileSerialization_pb2
from sims4.tuning.dynamic_enum import DynamicEnum
import enum

class SimNameType(DynamicEnum):
    DEFAULT = 0


class SimInfoCreationSource(enum.IntFlags, export=False):

    class SimInfoCreationSourceMixin:

        def __init__(self, *args, **kwargs):
            (super().__init__)(*args, **kwargs)
            self._creation_source = SimInfoCreationSource.UNKNOWN

        @property
        def creation_source(self):
            return self._creation_source

        @creation_source.setter
        def creation_source(self, value):
            if isinstance(value, str):
                value = SimInfoCreationSource.get_creation_source_from_legacy_creation_source(value)
            self._creation_source = value

    class SimInfoCreationSourceData:
        __slots__ = ('creation_source', 'creation_source_data')

        def __init__(self, creation_source, creation_source_data):
            self.creation_source = creation_source
            self.creation_source_data = creation_source_data

        def __str__(self):
            return '{} ({})'.format(str(self.creation_source), self.creation_source_data)

        def is_creation_source(self, creation_source):
            if self.creation_source & creation_source:
                return True
            return False

        def write_creation_source(self, telemetry_hook):
            telemetry_hook.write_string('cstr', str(self.creation_source_data))
            self.creation_source.write_creation_source(telemetry_hook)

    UNKNOWN = 0
    CAS_INITIAL = 1
    CAS_REENTRY = 2
    PRE_MADE = 4
    CLONED = 8
    GALLERY = 16
    HOUSEHOLD_TEMPLATE = 32
    NEIGHBORHOOD_POPULATION_SERVICE = 64
    ADOPTION = 128
    PREGNANCY = 256
    CHEAT = 512
    FILTER = 1024
    _CREATION_PATH_TO_CREATION_SOURCE = {FileSerialization_pb2.SimData.SIMCREATION_INIT: CAS_INITIAL, 
     FileSerialization_pb2.SimData.SIMCREATION_REENTRY_ADDSIM: CAS_REENTRY, 
     FileSerialization_pb2.SimData.SIMCREATION_PRE_MADE: PRE_MADE, 
     FileSerialization_pb2.SimData.SIMCREATION_CLONED: CLONED, 
     FileSerialization_pb2.SimData.SIMCREATION_GALLERY: GALLERY}
    _LEGACY_SOURCE_TO_CREATION_SOURCE = {'cas: initial':CAS_INITIAL, 
     'cas: re-entry':CAS_REENTRY, 
     'pre-made':PRE_MADE, 
     'cloned':CLONED, 
     'gallery':GALLERY, 
     'pregnancy':PREGNANCY, 
     'premade_household':HOUSEHOLD_TEMPLATE, 
     'unknown':UNKNOWN, 
     'cheat':CHEAT, 
     'adoption':ADOPTION, 
     'neigh_pop_service':NEIGHBORHOOD_POPULATION_SERVICE, 
     'filter':FILTER}

    @staticmethod
    def create_creation_source(creation_source, creation_source_data=None):
        creation_source = SimInfoCreationSource.SimInfoCreationSourceData(creation_source, creation_source_data)
        return creation_source

    @staticmethod
    def get_creation_source_from_creation_path(creation_path):
        creation_source = SimInfoCreationSource._CREATION_PATH_TO_CREATION_SOURCE.get(creation_path, SimInfoCreationSource.UNKNOWN)
        return SimInfoCreationSource(creation_source)

    @staticmethod
    def get_creation_source_from_legacy_creation_source(legacy_creation_source):
        for k, v in SimInfoCreationSource._LEGACY_SOURCE_TO_CREATION_SOURCE.items():
            if k.lower() in legacy_creation_source.lower():
                creation_source = SimInfoCreationSource(v)
                break
        else:
            creation_source = SimInfoCreationSource.UNKNOWN

        creation_source = SimInfoCreationSource.SimInfoCreationSourceData(creation_source, legacy_creation_source)
        return creation_source

    def is_creation_source(self, creation_source):
        if self & creation_source:
            return True
        return False

    @staticmethod
    def save_creation_source(creation_source_data, sim_info_msg):
        if isinstance(creation_source_data, SimInfoCreationSource.SimInfoCreationSourceData):
            creation_source = creation_source_data.creation_source
            creation_source_data = creation_source_data.creation_source_data
        else:
            if isinstance(creation_source_data, SimInfoCreationSource):
                creation_source = creation_source_data
                creation_source_data = None
            else:
                if isinstance(creation_source_data, str):
                    creation_source = SimInfoCreationSource.get_creation_source_from_legacy_creation_source(creation_source_data).creation_source
        sim_info_msg.gameplay_data.creation_source = creation_source
        if creation_source_data is not None:
            sim_info_msg.gameplay_data.creation_source_data = creation_source_data

    @staticmethod
    def load_creation_source(sim_info_msg):
        creation_source = SimInfoCreationSource(sim_info_msg.gameplay_data.creation_source)
        creation_source_data = sim_info_msg.gameplay_data.creation_source_data
        if not creation_source:
            creation_source = SimInfoCreationSource.get_creation_source_from_legacy_creation_source(creation_source_data).creation_source
        else:
            return creation_source_data or creation_source
        return SimInfoCreationSource.SimInfoCreationSourceData(creation_source, creation_source_data)

    def write_creation_source(self, telemetry_hook):
        telemetry_hook.write_int('csfl', self)