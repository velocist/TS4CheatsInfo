# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\gsi_handlers\outfit_change_handlers.py
# Compiled at: 2019-03-20 21:33:47
# Size of source mod 2**32: 1122 bytes
from gsi_handlers.gameplay_archiver import GameplayArchiver
from sims4.gsi.schema import GsiGridSchema
outfit_change_archive_schema = GsiGridSchema(label='Outfit Change Archive', sim_specific=True)
outfit_change_archive_schema.add_field('change_from', label='Change From')
outfit_change_archive_schema.add_field('change_to', label='Change To')
outfit_change_archive_schema.add_field('change_reason', label='Change Reason')
archiver = GameplayArchiver('OutfitChanges', outfit_change_archive_schema, add_to_archive_enable_functions=True)

def log_outfit_change(sim_info, change_to, change_reason):
    if sim_info is None:
        return
    entry = {'change_from':repr(sim_info._current_outfit), 
     'change_to':repr(change_to), 
     'change_reason':repr(change_reason)}
    archiver.archive(data=entry, object_id=(sim_info.id))