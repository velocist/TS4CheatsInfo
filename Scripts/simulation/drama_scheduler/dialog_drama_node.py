# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\drama_scheduler\dialog_drama_node.py
# Compiled at: 2020-07-10 00:39:34
# Size of source mod 2**32: 14623 bytes
from drama_scheduler.drama_node import BaseDramaNode, CooldownOption, DramaNodeRunOutcome
from drama_scheduler.drama_node_types import DramaNodeType
from sims4.localization import TunableLocalizedStringFactory
from sims4.tuning.tunable import TunableVariant, TunableList, TunableReference, HasTunableSingletonFactory, AutoFactoryInit, TunableTuple
from sims4.utils import classproperty
from tunable_utils.tested_list import TunableTestedList
from ui.ui_dialog import UiDialogOk, UiDialogOkCancel, ButtonType, UiDialog, UiDialogResponse
from ui.ui_dialog_notification import UiDialogNotification
import services, sims4.resources

class _dialog_and_loot(HasTunableSingletonFactory, AutoFactoryInit):

    def on_node_run(self, drama_node):
        raise NotImplementedError


class _notification_and_loot(_dialog_and_loot):
    FACTORY_TUNABLES = {'notification':UiDialogNotification.TunableFactory(description='\n            The notification that will display to the drama node.\n            '), 
     'loot_list':TunableList(description='\n            A list of loot operations to apply when this notification is given.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True))}

    def on_node_run(self, drama_node):
        resolver = drama_node._get_resolver()
        target_sim_id = drama_node._sender_sim_info.id if drama_node._sender_sim_info is not None else None
        dialog = self.notification((drama_node._receiver_sim_info), target_sim_id=target_sim_id,
          resolver=resolver)
        dialog.show_dialog()
        for loot_action in self.loot_list:
            loot_action.apply_to_resolver(resolver)


class _dialog_ok_and_loot(_dialog_and_loot):
    FACTORY_TUNABLES = {'dialog':UiDialogOk.TunableFactory(description='\n            The dialog with an ok button that we will display to the user.\n            '), 
     'on_dialog_complete_loot_list':TunableList(description='\n            A list of loot that will be applied when the player responds to the\n            dialog or, if the dialog is a phone ring or text message, when the\n            dialog times out due to the player ignoring it for too long.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True)), 
     'on_dialog_seen_loot_list':TunableList(description='\n            A list of loot that will be applied when player responds to the\n            message.  If the dialog is a phone ring or text message then this\n            loot will not be triggered when the dialog times out due to the\n            player ignoring it for too long.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', ),
       pack_safe=True))}

    def on_node_run(self, drama_node):
        resolver = drama_node._get_resolver()
        target_sim_id = drama_node._sender_sim_info.id if drama_node._sender_sim_info is not None else None
        dialog = self.dialog((drama_node._receiver_sim_info), target_sim_id=target_sim_id,
          resolver=resolver)

        def response(dialog):
            for loot_action in self.on_dialog_complete_loot_list:
                loot_action.apply_to_resolver(resolver)

            if dialog.response is not None:
                if dialog.response != ButtonType.DIALOG_RESPONSE_NO_RESPONSE:
                    for loot_action in self.on_dialog_seen_loot_list:
                        loot_action.apply_to_resolver(resolver)

            DialogDramaNode.apply_cooldown_on_response(drama_node)

        dialog.show_dialog(on_response=response)


class _loot_only(_dialog_and_loot):
    FACTORY_TUNABLES = {'on_drama_node_run_loot': TunableList(description='\n            A list of loot operations to apply when the drama node runs.\n            ',
                                 tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
                                 class_restrictions=('LootActions', 'RandomWeightedLoot'),
                                 pack_safe=True))}

    def on_node_run(self, drama_node):
        resolver = drama_node._get_resolver()
        for loot_action in self.on_drama_node_run_loot:
            loot_action.apply_to_resolver(resolver)


class _dialog_ok_cancel_and_loot(_dialog_and_loot):
    FACTORY_TUNABLES = {'dialog':UiDialogOkCancel.TunableFactory(description='\n            The ok cancel dialog that will display to the user.\n            '), 
     'on_dialog_complete_loot_list':TunableList(description='\n            A list of loot that will be applied when the player responds to the\n            dialog or, if the dialog is a phone ring or text message, when the\n            dialog times out due to the player ignoring it for too long.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True)), 
     'on_dialog_accetped_loot_list':TunableList(description='\n            A list of loot operations to apply when the player chooses ok.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True)), 
     'on_dialog_canceled_loot_list':TunableList(description='\n            A list of loot operations to apply when the player chooses cancel.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True)), 
     'on_dialog_no_response_loot_list':TunableList(description="\n            A list of loot operations to apply when the player ignores and doesn't respond, timing out the dialog.\n            ",
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True))}

    def on_node_run(self, drama_node):
        resolver = drama_node._get_resolver()
        target_sim_id = drama_node._sender_sim_info.id if drama_node._sender_sim_info is not None else None
        dialog = self.dialog((drama_node._receiver_sim_info), target_sim_id=target_sim_id,
          resolver=resolver)

        def response--- This code section failed: ---

 L. 193         0  SETUP_LOOP           26  'to 26'
                2  LOAD_DEREF               'self'
                4  LOAD_ATTR                on_dialog_complete_loot_list
                6  GET_ITER         
                8  FOR_ITER             24  'to 24'
               10  STORE_FAST               'loot_action'

 L. 194        12  LOAD_FAST                'loot_action'
               14  LOAD_METHOD              apply_to_resolver
               16  LOAD_DEREF               'resolver'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_TOP          
               22  JUMP_BACK             8  'to 8'
               24  POP_BLOCK        
             26_0  COME_FROM_LOOP        0  '0'

 L. 198        26  LOAD_FAST                'dialog'
               28  LOAD_ATTR                response
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_FALSE   154  'to 154'

 L. 199        36  LOAD_FAST                'dialog'
               38  LOAD_ATTR                response
               40  LOAD_GLOBAL              ButtonType
               42  LOAD_ATTR                DIALOG_RESPONSE_OK
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    76  'to 76'

 L. 200        48  SETUP_LOOP          154  'to 154'
               50  LOAD_DEREF               'self'
               52  LOAD_ATTR                on_dialog_accetped_loot_list
               54  GET_ITER         
               56  FOR_ITER             72  'to 72'
               58  STORE_FAST               'loot_action'

 L. 201        60  LOAD_FAST                'loot_action'
               62  LOAD_METHOD              apply_to_resolver
               64  LOAD_DEREF               'resolver'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  POP_TOP          
               70  JUMP_BACK            56  'to 56'
               72  POP_BLOCK        
               74  JUMP_FORWARD        154  'to 154'
             76_0  COME_FROM            46  '46'

 L. 202        76  LOAD_FAST                'dialog'
               78  LOAD_ATTR                response
               80  LOAD_GLOBAL              ButtonType
               82  LOAD_ATTR                DIALOG_RESPONSE_CANCEL
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   116  'to 116'

 L. 203        88  SETUP_LOOP          154  'to 154'
               90  LOAD_DEREF               'self'
               92  LOAD_ATTR                on_dialog_canceled_loot_list
               94  GET_ITER         
               96  FOR_ITER            112  'to 112'
               98  STORE_FAST               'loot_action'

 L. 204       100  LOAD_FAST                'loot_action'
              102  LOAD_METHOD              apply_to_resolver
              104  LOAD_DEREF               'resolver'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  POP_TOP          
              110  JUMP_BACK            96  'to 96'
              112  POP_BLOCK        
              114  JUMP_FORWARD        154  'to 154'
            116_0  COME_FROM            86  '86'

 L. 205       116  LOAD_FAST                'dialog'
              118  LOAD_ATTR                response
              120  LOAD_GLOBAL              ButtonType
              122  LOAD_ATTR                DIALOG_RESPONSE_NO_RESPONSE
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   154  'to 154'

 L. 206       128  SETUP_LOOP          154  'to 154'
              130  LOAD_DEREF               'self'
              132  LOAD_ATTR                on_dialog_no_response_loot_list
              134  GET_ITER         
              136  FOR_ITER            152  'to 152'
              138  STORE_FAST               'loot_action'

 L. 207       140  LOAD_FAST                'loot_action'
              142  LOAD_METHOD              apply_to_resolver
              144  LOAD_DEREF               'resolver'
              146  CALL_METHOD_1         1  '1 positional argument'
              148  POP_TOP          
              150  JUMP_BACK           136  'to 136'
              152  POP_BLOCK        
            154_0  COME_FROM_LOOP      128  '128'
            154_1  COME_FROM           126  '126'
            154_2  COME_FROM           114  '114'
            154_3  COME_FROM_LOOP       88  '88'
            154_4  COME_FROM            74  '74'
            154_5  COME_FROM_LOOP       48  '48'
            154_6  COME_FROM            34  '34'

 L. 209       154  LOAD_GLOBAL              DialogDramaNode
              156  LOAD_METHOD              apply_cooldown_on_response
              158  LOAD_DEREF               'drama_node'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_TOP          

Parse error at or near `COME_FROM_LOOP' instruction at offset 154_3

        dialog.show_dialog(on_response=response)


class _dialog_multi_tested_response(_dialog_and_loot):
    FACTORY_TUNABLES = {'dialog':UiDialog.TunableFactory(description='\n            The dialog that will display to the user.\n            '), 
     'on_dialog_complete_loot_list':TunableList(description='\n            A list of loot that will be applied when the player responds to the\n            dialog or, if the dialog is a phone ring or text message, when the\n            dialog times out due to the player ignoring it for too long.\n            ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True)), 
     'possible_responses':TunableTestedList(description='\n            A tunable tested list of the possible responses to this dialog.\n            ',
       tunable_type=TunableTuple(description='\n                A possible response for this dialog.\n                ',
       text=TunableLocalizedStringFactory(description='\n                    The text of the response field.\n                    '),
       loot=TunableList(description='\n                    A list of loot that will be applied when the player selects this response.\n                    ',
       tunable=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.ACTION)),
       class_restrictions=('LootActions', 'RandomWeightedLoot'),
       pack_safe=True))))}

    def on_node_run(self, drama_node):
        resolver = drama_node._get_resolver()
        responses = []
        for index, possible_response in enumerate(self.possible_responses(resolver=resolver)):
            responses.append(UiDialogResponse(dialog_response_id=index, text=(possible_response.text),
              ui_request=(UiDialogResponse.UiDialogUiRequest.NO_REQUEST)))

        target_sim_id = drama_node._sender_sim_info.id if drama_node._sender_sim_info is not None else None
        dialog = self.dialog((drama_node._receiver_sim_info), target_sim_id=target_sim_id,
          resolver=resolver)
        dialog.set_responses(responses)

        def response(dialog):
            for loot_action in self.on_dialog_complete_loot_list:
                loot_action.apply_to_resolver(resolver)

            if 0 <= dialog.response < len(self.possible_responses):
                for loot_action in self.possible_responses[dialog.response].item.loot:
                    loot_action.apply_to_resolver(resolver)

            DialogDramaNode.apply_cooldown_on_response(drama_node)

        dialog.show_dialog(on_response=response)


class DialogDramaNode(BaseDramaNode):
    INSTANCE_TUNABLES = {'dialog_and_loot': TunableVariant(description='\n            The type of dialog and loot that will be applied.\n            ',
                          notification=(_notification_and_loot.TunableFactory()),
                          dialog_ok=(_dialog_ok_and_loot.TunableFactory()),
                          dialog_ok_cancel=(_dialog_ok_cancel_and_loot.TunableFactory()),
                          dialog_multi_response=(_dialog_multi_tested_response.TunableFactory()),
                          loot_only=(_loot_only.TunableFactory()),
                          default='notification')}

    @classproperty
    def drama_node_type(cls):
        return DramaNodeType.DIALOG

    def _run(self):
        self.dialog_and_loot.on_node_run(self)
        return DramaNodeRunOutcome.SUCCESS_NODE_COMPLETE

    @classmethod
    def apply_cooldown_on_response(cls, drama_node):
        if drama_node.cooldown is not None:
            if drama_node.cooldown.cooldown_option == CooldownOption.ON_DIALOG_RESPONSE:
                services.drama_scheduler_service().start_cooldown(drama_node)