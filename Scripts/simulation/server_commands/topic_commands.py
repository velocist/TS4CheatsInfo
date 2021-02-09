# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\topic_commands.py
# Compiled at: 2012-08-18 02:08:43
# Size of source mod 2**32: 2742 bytes
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
import services, sims4.commands

@sims4.commands.Command('topic.add_topic')
def add_topic(name: str=None, opt_sim: OptionalTargetParam=None, topic_target_id: int=0, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None or name is None:
        return False
    topic_type = services.topic_manager().get(name)
    if topic_type is None:
        sims4.commands.output('({0}) is not a valid topic'.format(name), _connection)
        return False
    target = None
    if topic_target_id:
        target = services.object_manager().get(topic_target_id)
        if target is None:
            sims4.commands.output('({0}) is not a valid target for topic'.format(topic_target_id), _connection)
            return False
    sim.add_topic(topic_type, target=target)
    sims4.commands.output('({0}) has been added'.format(name), _connection)
    return True


@sims4.commands.Command('topic.remove_topic')
def remove_topic(name: str=None, opt_sim: OptionalTargetParam=None, topic_target_id: int=0, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None or name is None:
        return False
    topic_type = services.topic_manager().get(name)
    if topic_type is None:
        sims4.commands.output('({0}) is not a valid topic'.format(name), _connection)
        return False
    target = None
    if topic_target_id:
        target = services.object_manager().get(topic_target_id)
        if target is None:
            sims4.commands.output('({0}) is not a valid target for topic'.format(topic_target_id), _connection)
            return False
    sim.remove_topic(topic_type, target=target)
    return True


@sims4.commands.Command('topic.remove_all_topics')
def remove_all_topic_of_type(name: str=None, opt_sim: OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None or name is None:
        return False
    topic_type = services.topic_manager().get(name)
    if topic_type is None:
        sims4.commands.output('({0}) is not a valid topic'.format(name), _connection)
        return False
    sim.remove_all_topic_of_type(topic_type)
    return True