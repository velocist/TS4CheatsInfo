# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\open_street_director\open_street_director_commands.py
# Compiled at: 2016-07-18 22:40:09
# Size of source mod 2**32: 1189 bytes
from server_commands.argument_helpers import TunableInstanceParam
from sims4.commands import CommandType
import sims4.commands, services

@sims4.commands.Command('open_street.add_open_street_director')
def add_open_street_director(open_street_director_type: TunableInstanceParam(sims4.resources.Types.OPEN_STREET_DIRECTOR), _connection=None):
    zone_director = services.venue_service().get_zone_director()
    zone_director.set_open_street_director(open_street_director_type())
    sims4.commands.output('Open Street Director changed to {}.'.format(zone_director.open_street_director), _connection)


@sims4.commands.Command('open_street.remove_open_street_director', command_type=(CommandType.Automation))
def remove_open_street_director(_connection=None):
    zone_director = services.venue_service().get_zone_director()
    zone_director.destroy_current_open_street_director()