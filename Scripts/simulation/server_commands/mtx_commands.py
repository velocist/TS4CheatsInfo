# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\mtx_commands.py
# Compiled at: 2015-01-26 22:25:18
# Size of source mod 2**32: 553 bytes
import sims4.commands, sims4.common

@sims4.commands.Command('mtx.show_pack_entitlements')
def show_pack_entitlements(_connection=None):
    output = sims4.commands.Output(_connection)
    output('Available packs:')
    for pack in sims4.common.get_available_packs():
        output('    {}'.format(pack))

    return True