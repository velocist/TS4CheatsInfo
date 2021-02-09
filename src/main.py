#    Copyright 2020 June Hanabi
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import services
import sims4.commands


@sims4.commands.Command('ch.version', command_type=sims4.commands.CommandType.Live)
def _ch_version(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("¡Hecho! ¡¡Mi primer Mod en los Sims 4!! =)\nChicaFerrari")


@sims4.commands.Command('ch.statuscheats', command_type=sims4.commands.CommandType.Live)
def _ch_status_cheats(_connection=None):
    output_status = sims4.commands.CheatOutput(_connection)
    output_status('Estado trucos' + sims4.commands.execute('cheats.status', _connection))


# @sims4.commands.Command('chinfocheats', command_type=sims4.commands.CommandType.Live)
# def _ch_info_cheats(_connection=None):
#     output = sims4.commands.CheatOutput(_connection)
#     output('Estado trucos: {}'.format(sims4.commands.CheatOutput('cheat.status', _connection)))


@sims4.commands.Command('ch.cheatslist', command_type=sims4.commands.CommandType.Live)
def _ch_cheats_list(_connection=None):
    output = sims4.commands.CheatOutput('cheats.list', _connection)
    output()


@sims4.commands.Command('getpopulation', command_type=sims4.commands.CommandType.Live)
def getpop(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Your town\'s population is {}'.format(len(services.sim_info_manager().get_all())))
