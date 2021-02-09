# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Core\shared_commands\reloader_commands.py
# Compiled at: 2017-05-18 20:41:07
# Size of source mod 2**32: 2439 bytes
import sys, sims4.commands, sims4.core_services, sims4.log, sims4.reload_service
logger = sims4.log.Logger('Reloader Commands')

@sims4.commands.Command('hot.files.list')
def hot_files_list(_connection=None):
    output = sims4.commands.Output(_connection)
    for name, change_set in sims4.core_services.directory_watcher_manager().get_change_sets().items():
        output("Change Set '{}':".format(name))
        filenames = list(change_set)
        filenames.sort()
        for filename in filenames:
            output('  {}'.format(filename))


@sims4.commands.Command('hot.files.consume')
def hot_files_consume(name: str, _connection=None):
    output = sims4.commands.Output(_connection)
    output("Change Set '{}':".format(name))
    filenames = list(sims4.core_services.directory_watcher_manager().consume_set(name))
    for filename in sorted(filenames):
        output('  {}'.format(filename))


@sims4.commands.Command('hot.reload')
def hot_reload(*args, _connection=None):
    output = sims4.commands.Output(_connection)
    if not args:
        sims4.reload_service.trigger_reload(output)
    else:
        module_paths = []
        for module_name in args:
            module = sys.modules.get(module_name)
            if module is None:
                output('Could not find module: {}'.format(module_name))
                continue
            if not hasattr(module, '__file__'):
                output('Cannot reload builtin module: {}'.format(module_name))
                continue
            module_paths.append(module.__file__)

        sims4.reload_service.reload_files(module_paths, output)