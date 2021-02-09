# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\gsi_handlers\statistics_removed_handlers.py
# Compiled at: 2020-01-10 00:01:06
# Size of source mod 2**32: 1083 bytes
from gsi_handlers.gameplay_archiver import GameplayArchiver
from sims4.gsi.schema import GsiGridSchema, GsiFieldVisualizers
removed_statistics_archive_schema = GsiGridSchema(label='Removed Statistics Archive', sim_specific=False)
removed_statistics_archive_schema.add_field('statistic', label='Statistic', type=(GsiFieldVisualizers.STRING))
removed_statistics_archive_schema.add_field('owner', label='Owner', type=(GsiFieldVisualizers.STRING))
archiver = GameplayArchiver('removed_statistics', removed_statistics_archive_schema, add_to_archive_enable_functions=True, max_records=10000, enable_archive_by_default=True)

def is_archive_enabled():
    return archiver.enabled


def archive_removed_statistic(statistic, owner):
    archive_data = {'statistic':statistic, 
     'owner':owner}
    archiver.archive(archive_data)