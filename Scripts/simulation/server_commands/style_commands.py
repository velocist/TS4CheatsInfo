# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\style_commands.py
# Compiled at: 2020-04-01 00:05:09
# Size of source mod 2**32: 597 bytes
from sims4.commands import CommandType
from sims.sim_info_types import Gender
import services, sims4.commands

@sims4.commands.Command('style.clear_style', command_type=(CommandType.Live))
def clear_style(gender: Gender, _connection=None):
    style_service = services.get_style_service()
    if style_service is None:
        return
    style_service.clear_style_outfit_data(gender)