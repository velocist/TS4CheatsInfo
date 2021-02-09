# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\restaurants\chef_tuning.py
# Compiled at: 2015-12-15 02:12:35
# Size of source mod 2**32: 3491 bytes
from interactions.utils.loot import LootActions
from sims4.tuning.tunable import TunablePackSafeReference, Tunable, TunableReference
import services, sims4.resources

class ChefTuning:
    CHEF_STATION_POT_OBJECT = TunablePackSafeReference(description="\n        The pot object to create at the chef's station.\n        ",
      manager=(services.definition_manager()))
    CHEF_STATION_PAN_OBJECT = TunablePackSafeReference(description="\n        The pan object to create at the chef's station.\n        ",
      manager=(services.definition_manager()))
    CHEF_STATION_CUTTING_BOARD_OBJECT = TunablePackSafeReference(description="\n        The cutting board object to create at the chef's station.\n        ",
      manager=(services.definition_manager()))
    CHEF_STATION_PAN_SLOT = Tunable(description='\n        The name of the slot in which the pan object should be placed.\n        ',
      tunable_type=str,
      default='_ctnm_SimInteraction_1')
    CHEF_STATION_POT_SLOT = Tunable(description='\n        The name of the slot in which the pot object should be placed.\n        ',
      tunable_type=str,
      default='_ctnm_SimInteraction_2')
    CHEF_STATION_CUTTING_BOARD_SLOT = Tunable(description='\n        The name of the slot in which the cutting board object should be placed.\n        ',
      tunable_type=str,
      default='_ctnm_SimInteraction_4')
    CHEF_STATION_SERVE_SLOT_TYPE = TunableReference(description='\n        The slot type of the serve slots on the chef station.\n        ',
      manager=(services.get_instance_manager(sims4.resources.Types.SLOT_TYPE)))
    CHEF_STATION_SERVING_PLATTER_OBJECT = TunablePackSafeReference(description="\n        The serving platter object the chef will create and place when they're\n        done cooking an order.\n        ",
      manager=(services.definition_manager()))
    CHEF_HAS_ORDER_BUFF = TunablePackSafeReference(description='\n        The buff a chef should get when they have an order. This should drive\n        them to do the active cooking animations.\n        ',
      manager=(services.buff_manager()))
    CHEF_COMPLIMENT_LOOT = LootActions.TunablePackSafeReference(description="\n        The loot action to trigger when a customer compliments a chef. This\n        won't happen until the waitstaff deliver the compliment.\n        \n        The customer Sim will be the Actor and the Chef will be TargetSim.\n        ")
    CHEF_INSULT_LOOT = LootActions.TunablePackSafeReference(description="\n        The loot action to trigger when a customer insults a chef. This won't\n        happen until the waitstaff deliver the insult.\n        \n        The customer Sim will be the Actor and the Chef will be TargetSim.\n        ")
    PICK_UP_ORDER_INTERACTION = TunablePackSafeReference(description='\n        The interaction the sim will run when they pick their order up from the\n        Chef Station. This is only used when a Sim places an order directly at\n        the chef station.\n        ',
      manager=(services.get_instance_manager(sims4.resources.Types.INTERACTION)))