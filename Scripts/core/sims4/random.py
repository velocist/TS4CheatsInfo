# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Core\sims4\random.py
# Compiled at: 2014-10-10 00:35:00
# Size of source mod 2**32: 3002 bytes
from random import uniform
import random, sims4.math

def _weighted(pairs, random=random, flipped=False):
    weight_index = 1 if flipped else 0
    weights = [x[weight_index] for x in pairs]
    total = sum(weights)
    if total == 0:
        return
    select = random.uniform(0, total)
    for index, weight in enumerate(weights):
        select -= weight
        if select <= 0 and weight > 0:
            return index


def weighted_random_item(pairs, random=random, flipped=False):
    value_index = 0 if flipped else 1
    choice_index = _weighted(pairs, random=random, flipped=flipped)
    if choice_index is not None:
        return pairs[choice_index][value_index]


def weighted_random_index(tuple_of_tuples, random=random):
    choice_index = _weighted(tuple_of_tuples, random=random)
    if choice_index is not None:
        return choice_index


def pop_weighted(pairs, random=random, flipped=False):
    value_index = 0 if flipped else 1
    choice_index = _weighted(pairs, random=random, flipped=flipped)
    if choice_index is not None:
        return pairs.pop(choice_index)[value_index]


def random_chance(chance_value, random=random):
    if chance_value == 0:
        return False
    if chance_value == 100:
        return True
    return random.randint(0, 100) < chance_value


def random_orientation():
    angle = random.randint(0, 360)
    quaternion = sims4.math.angle_to_yaw_quaternion(angle)
    return quaternion