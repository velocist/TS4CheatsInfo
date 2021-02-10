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
from server_commands.cheat_commands import display_cheat_list


@sims4.commands.Command('ch.version', command_type=sims4.commands.CommandType.Live)
def _ch_version(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("¡Hecho! ¡¡Mi primer Mod en los Sims 4!! =)\nChicaFerrari")


@sims4.commands.Command('ch.statuscheats', command_type=sims4.commands.CommandType.Live)
def _ch_status_cheats(_connection=None):
    output_status = sims4.commands.CheatOutput(_connection)
    output_status('Estado trucos' + sims4.commands.Command('cheats.status', _connection))


# @sims4.commands.Command('chinfocheats', command_type=sims4.commands.CommandType.Live)
# def _ch_info_cheats(_connection=None):
#     output = sims4.commands.CheatOutput(_connection)
#     output('Estado trucos: {}'.format(sims4.commands.CheatOutput('cheat.status', _connection)))


@sims4.commands.Command('ch.cheats', command_type=sims4.commands.CommandType.Live)
def _ch_cheats(enable: bool = None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    if enable is not None:
        if enable is True:
            command = '|testingcheats on'
            sims4.commands.client_cheat(command, _connection)
            output('testingcheats: ON')
        else:
            command = '|testingcheats off'
            sims4.commands.client_cheat(command, _connection)
            output('testingcheats: OFF')
    else:
        output('Falta parametro de activación', _connection)
        return
    command = '|bb.showhiddenobjects'
    sims4.commands.client_cheat(command, _connection)
    command = '|bb.showliveeditmode'
    sims4.commands.client_cheat(command, _connection)
    command = '|bb.showwipobjects'
    sims4.commands.client_cheat(command, _connection)


@sims4.commands.Command('ch.cheatsinline', command_type=sims4.commands.CommandType.Live)
def _ch_cheatsinline(enable: bool = None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    if enable is not None:
        if enable is True:
            command = '|testingcheats on'
            sims4.commands.client_cheat(command, _connection)
            output('testingcheats: ON')
        else:
            command = '|testingcheats off'
            sims4.commands.client_cheat(command, _connection)
            output('testingcheats: OFF')
    else:
        output('Falta parametro de activación')
        return
    command = 'bb.showhiddenobjects bb.showliveeditmode bb.showwipobjects'
    sims4.commands.client_cheat(command, _connection)
    output('Ejecutado')

@sims4.commands.Command('ch.help', command_type=sims4.commands.CommandType.Live)
def _help(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('CheatsInfo Ayuda:')
    output(
        'ch.cheats: ["ch.cheats {True|False} "] (Activa: testingcheats,showhiddenobjects,showliveeditmode,showwipobjects)')
    # output('cas.fulleditmode: ["fem","cas.fem", "fulleditmode"] (Also turns on testing cheats)')
    # output('grandmotherlode (runs motherlode however many times you say): ["gml {number}", "grandmotherlode {number}]')
    output('ch.version: ["ch.version"]  Muestra la versión del mod')


@sims4.commands.Command('getpopulation', command_type=sims4.commands.CommandType.Live)
def getpop(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('La población es de: {}'.format(len(services.sim_info_manager().get_all())))
