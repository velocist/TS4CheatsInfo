# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\careers\odd_job_picker_interaction.py
# Compiled at: 2019-02-09 01:14:43
# Size of source mod 2**32: 1607 bytes
from drama_scheduler.drama_node_picker_interaction import DramaNodePickerInteraction
from sims4.tuning.tunable import TunableReference
from sims4.tuning.tunable_base import GroupNames
from sims4.utils import flexmethod
from ui.ui_dialog_picker import UiOddJobPicker
import services, sims4

class OddJobPickerInteraction(DramaNodePickerInteraction):
    INSTANCE_TUNABLES = {'picker_dialog':UiOddJobPicker.TunableFactory(description='\n            The odd job picker dialog.\n            ',
       tuning_group=GroupNames.PICKERTUNING), 
     'odd_job_career':TunableReference(description='\n            The career this gig is associated with.\n            ',
       manager=services.get_instance_manager(sims4.resources.Types.CAREER),
       tuning_group=GroupNames.PICKERTUNING)}

    def _setup_dialog(self, dialog, **kwargs):
        (super()._setup_dialog)(dialog, **kwargs)
        odd_job_career = self.sim.career_tracker.get_career_by_uid(self.odd_job_career.guid64)
        if odd_job_career is not None:
            dialog.star_ranking = odd_job_career.level