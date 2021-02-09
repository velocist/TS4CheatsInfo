# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\gsi_handlers\command_handlers.py
# Compiled at: 2014-06-09 04:42:14
# Size of source mod 2**32: 1793 bytes
import time
from sims4.gsi.dispatcher import GsiHandler
from sims4.gsi.schema import GsiSchema
import services, sims4.core_services
SLEEP_TIME = 0.1
TIMEOUT = int(1 / SLEEP_TIME)
command_schema = GsiSchema()
command_schema.add_field('response', label='Response')

@GsiHandler('command', command_schema)
def invoke_command(command=None, zone_id: int=None):
    ready = False
    output_accum = ''
    response = ''

    def _callback(result):
        nonlocal ready
        nonlocal response
        if result:
            response = 'Success<br>' + output_accum
        else:
            response = 'Failure<br>' + output_accum
        ready = True

    if command is not None:

        def _fake_output(s, context=None):
            nonlocal response
            response += '<br>' + s

        connection = services.client_manager().get_first_client()
        sims4.core_services.command_buffer_service().add_command(command, _callback, _fake_output, zone_id, connection.id)
    timeout_counter = 0
    while not ready:
        time.sleep(SLEEP_TIME)
        timeout_counter += 1
        if timeout_counter > TIMEOUT:
            ready = True

    return {'response': response}