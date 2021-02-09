# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\__init__.py
# Compiled at: 2017-10-27 22:39:22
# Size of source mod 2**32: 977 bytes
from sims4.commands import CommandType
import paths, services, sims4.commands

def is_command_available(command_type: CommandType):
    if command_type >= CommandType.Live:
        return True
    else:
        cheat_service = services.get_cheat_service()
        cheats_enabled = cheat_service.cheats_enabled
        if command_type >= CommandType.Cheat:
            if cheats_enabled:
                return True
        if command_type >= CommandType.Automation and paths.AUTOMATION_MODE:
            return True
    return False


sims4.commands.is_command_available = is_command_available