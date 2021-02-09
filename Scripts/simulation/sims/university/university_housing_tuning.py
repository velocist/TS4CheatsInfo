# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\university\university_housing_tuning.py
# Compiled at: 2019-11-14 00:54:46
# Size of source mod 2**32: 3801 bytes
from event_testing.tests import TunableTestSet
from filters.tunable import FilterTermVariant
from sims.sim_info_types import Gender
from sims.university.university_enums import UniversityHousingRoommateRequirementCriteria
from sims4.tuning.tunable import TunableReference, TunableMapping, TunableEnumEntry, TunablePackSafeReference, TunableEnumWithFilter
from tag import Tag
from tunable_time import TunableTimeSpan
import services, sims4
logger = sims4.log.Logger('UniversityHousingTuning', default_owner='bnguyen')

class UniversityHousingTuning:
    UNIVERSITY_HOUSING_KICK_OUT_SITUATION = TunableReference(description='\n        The situation to kick a sim out of university housing.\n        ',
      manager=(services.get_instance_manager(sims4.resources.Types.SITUATION)),
      class_restrictions=('UniversityHousingKickOutSituation', ),
      pack_safe=True)
    UNIVERSITY_HOUSING_ROOMMATE_FILTER_TERM_TEMPLATES = TunableMapping(description="\n        Template filter terms for each university housing roommate requirement criteria.\n        We will be modifying these terms in code based on what the player sets\n        in the venue's configuration UI. For example, the template gender filter\n        term is set to male, but if the player sets their university housing\n        venue as female only, we will modify this filter term before retrieving\n        roommates.  These values are set in tuning so the majority of the filter\n        terms' values are initialized to their defaults, instead of having\n        to do so in code.\n        ",
      key_type=TunableEnumEntry(tunable_type=UniversityHousingRoommateRequirementCriteria,
      default=(UniversityHousingRoommateRequirementCriteria.NONE),
      invalid_enums=(UniversityHousingRoommateRequirementCriteria.NONE),
      pack_safe=True),
      key_name='Requirement Criteria',
      value_type=(FilterTermVariant()),
      value_name='Filter Term Template')
    UNIVERSITY_HOUSING_VENUE_TUNING = TunablePackSafeReference(description='\n        The university housing venue.\n        ',
      manager=(services.get_instance_manager(sims4.resources.Types.VENUE)))
    UNIVERSITY_HOUSING_PREGNANCY_TEST = TunableTestSet(description='\n        Test to determine if a sim is at the appropriate stage in a pregnancy\n        in order to be kicked out of university housing.\n        ')
    UNIVERSITY_HOUSING_VALIDATION_CADENCE = TunableTimeSpan(description='\n        When a university housing venue is loaded, the timespan between updates\n        where we validate household sims to decide if they need to be kicked out.\n        ')
    UNIVERSITY_HOUSING_KICKOUT_SITUATION_BLOCKER_TAG = TunableEnumWithFilter(description="\n        If a situation with this tag is running, we won't start any kickout situations.  We use this tag to prevent\n        edge cases such as multiple kickouts running at the same time, or kicking out sims who have died.\n        ",
      tunable_type=Tag,
      filter_prefixes=[
     'situation'],
      default=(Tag.INVALID),
      pack_safe=True)

    @staticmethod
    def get_university_housing_zone_ids():
        university_venue_tuning = UniversityHousingTuning.UNIVERSITY_HOUSING_VENUE_TUNING
        if university_venue_tuning is None:
            return ()
        return tuple(services.venue_service().get_zones_for_venue_type_gen(university_venue_tuning))