# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\zone_modifier\zone_modifier_display_info.py
# Compiled at: 2018-07-13 20:17:42
# Size of source mod 2**32: 2271 bytes
from sims4.tuning.tunable import HasTunableReference, TunablePackSafeReference
from sims4.resources import Types
from sims4.tuning.tunable_base import ExportModes, GroupNames
from sims4.tuning.instances import HashedTunedInstanceMetaclass
import services
from sims4.localization import TunableLocalizedString
from interactions.utils.tunable_icon import TunableIcon

class ZoneModifierDisplayInfo(HasTunableReference, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.USER_INTERFACE_INFO)):
    base_game_only = True
    INSTANCE_TUNABLES = {'zone_modifier_icon':TunableIcon(description="\n            The zone modifier's icon.\n            ",
       export_modes=ExportModes.All,
       tuning_group=GroupNames.UI), 
     'zone_modifier_name':TunableLocalizedString(description="\n            The zone modifier's name.\n            ",
       export_modes=ExportModes.All,
       tuning_group=GroupNames.UI), 
     'zone_modifier_description':TunableLocalizedString(description="\n            The zone modifier's description.\n            ",
       export_modes=ExportModes.All,
       tuning_group=GroupNames.UI), 
     'zone_modifier_reference':TunablePackSafeReference(description='\n            The zone modifier gameplay tuning reference ID.\n            \n            This ID will be what is persisted in save data and used\n            for any lookups.\n            ',
       manager=services.zone_modifier_manager(),
       export_modes=ExportModes.All,
       tuning_group=GroupNames.UI)}