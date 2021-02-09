# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\gsi_handlers\state_handlers.py
# Compiled at: 2018-02-08 03:32:59
# Size of source mod 2**32: 2885 bytes
from gsi_handlers.gameplay_archiver import GameplayArchiver
from sims4.gsi.schema import GsiGridSchema
import gsi_handlers
state_trigger_schema = GsiGridSchema(label='State Triggers/State Trigger Log')
state_trigger_schema.add_field('objId', label='Object Id', unique_field=True, width=1.2)
state_trigger_schema.add_field('def', label='Definition', width=2)
state_trigger_schema.add_field('parent', label='Parent', width=1.5)
state_trigger_schema.add_field('state', label='Trigger State', width=1.5)
state_trigger_schema.add_field('state_value', label='Trigger State Value', width=2)
state_trigger_schema.add_field('at_state', label='Triggered At State', width=2.5)
state_trigger_schema.add_field('at_states', label='At States', width=2.5)
state_trigger_schema.add_field('src', label='Source', width=1.3)
state_trigger_archiver = GameplayArchiver('StateTriggerLog', state_trigger_schema)

def archive_state_trigger(obj, triggered_state, at_state, at_states, source=''):
    archive_data = {'objId':hex(obj.id), 
     'def':obj.definition.name, 
     'state':str(triggered_state.state), 
     'state_value':str(triggered_state), 
     'at_state':str(at_state), 
     'at_states':str(at_states), 
     'src':source}
    if obj.parent is not None:
        archive_data['parent'] = gsi_handlers.gsi_utils.format_object_name(obj.parent)
    state_trigger_archiver.archive(data=archive_data)


timed_state_trigger_schema = GsiGridSchema(label='State Triggers/Timed State Trigger Log')
timed_state_trigger_schema.add_field('objId', label='Object Id', unique_field=True)
timed_state_trigger_schema.add_field('def', label='Definition', width=2)
timed_state_trigger_schema.add_field('state', label='Trigger State', width=2)
timed_state_trigger_schema.add_field('state_value', label='Trigger State Value', width=2)
timed_state_trigger_schema.add_field('at_state', label='At State', width=2)
timed_state_trigger_schema.add_field('trigger_time', label='Trigger Time')
timed_state_trigger_archiver = GameplayArchiver('TimedStateTriggerLog', timed_state_trigger_schema)

def archive_timed_state_trigger(obj, triggered_state, at_state, trigger_time):
    archive_data = {'objId':hex(obj.id), 
     'def':obj.definition.name, 
     'state':str(triggered_state.state), 
     'state_value':str(triggered_state), 
     'at_state':str(at_state), 
     'trigger_time':trigger_time}
    timed_state_trigger_archiver.archive(data=archive_data)