# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\venues\secret_lab_venue\secret_lab_commands.py
# Compiled at: 2018-11-26 19:43:38
# Size of source mod 2**32: 1358 bytes
from sims4.commands import CommandType
from venues.secret_lab_venue.secret_lab_zone_director import SecretLabCommand
import services, sims4.commands

@sims4.commands.Command('secret_lab.reveal_next_section', command_type=(sims4.commands.CommandType.Automation))
def reveal_next_section(_connection=None):
    zone_director = services.venue_service().get_zone_director()
    zone_director.handle_command(SecretLabCommand.RevealNextSection)


@sims4.commands.Command('secret_lab.reveal_all_sections', command_type=(sims4.commands.CommandType.Automation))
def reveal_all_sections(_connection=None):
    zone_director = services.venue_service().get_zone_director()
    zone_director.handle_command(SecretLabCommand.RevealAllSections)


@sims4.commands.Command('secret_lab.reset_lab', command_type=(sims4.commands.CommandType.Automation))
def reset_lab(_connection=None):
    zone_director = services.venue_service().get_zone_director()
    zone_director.handle_command(SecretLabCommand.ResetLab)