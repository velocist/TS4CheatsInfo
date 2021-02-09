# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\story_progression\story_progression_agents.py
# Compiled at: 2015-04-18 00:58:33
# Size of source mod 2**32: 1125 bytes
from careers.career_enums import CareerCategory
from singletons import DEFAULT

class StoryProgressionAgentSimInfo:

    def __init__(self, sim_info, career=DEFAULT):
        self._sim_info = sim_info
        self._career = career

    @property
    def sim_id(self):
        return self._sim_info.sim_id

    def get_agent_clone(self, **kwargs):
        return StoryProgressionAgentSimInfo((self._sim_info), **kwargs)

    def get_work_career(self):
        if self._career is not DEFAULT:
            return self._career
        return self._sim_info.career_tracker.get_career_by_category(CareerCategory.Work)