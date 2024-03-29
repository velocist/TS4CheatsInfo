# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\element_utils.py
# Compiled at: 2017-09-02 00:19:46
# Size of source mod 2**32: 11855 bytes
import functools, inspect, itertools, date_and_time, elements, enum

class CleanupType(enum.Int):
    NotCritical = 0
    OnCancel = 1
    OnCancelOrException = 2
    RunAll = 3


def run_child(timeline, sequence):
    element = build_element(sequence)
    if element is None:
        return
    result = yield timeline.run_child(element)
    return result


def build_element(sequence, critical=CleanupType.NotCritical):
    if critical == CleanupType.NotCritical:
        elem = _build_element(sequence)
    else:
        if critical == CleanupType.OnCancel:
            elem = _build_critical_section(sequence)
        else:
            if critical == CleanupType.OnCancelOrException:
                elem = _build_with_finally(sequence)
            else:
                if critical == CleanupType.RunAll:
                    elem = _build_element(sequence, sequence_wrapper=return_true_wrapper)
                else:
                    raise ValueError('Unknown critical value: {}'.format(critical))
    return elem


def build_critical_section(*args):
    return build_element(args, critical=(CleanupType.OnCancel))


def build_critical_section_with_finally(*args):
    return build_element(args, critical=(CleanupType.OnCancelOrException))


def _split_sequence(sequence):
    if isinstance(sequence, (tuple, list)):
        if not sequence:
            return ([], None)
        prefix, final = sequence[:-1], sequence[(-1)]
        return (prefix, final)
    return ([], sequence)


def _build_element(elem, sequence_wrapper=None):
    if isinstance(elem, functools.partial):
        canonical = elem.func
    else:
        canonical = elem
    if elem is None:
        return
    if isinstance(elem, elements.Element):
        return elem
    if isinstance(elem, (tuple, list)):
        return _build_from_iterable(elem, sequence_wrapper=sequence_wrapper)
    if inspect.isgeneratorfunction(canonical):
        return elements.GeneratorElement(elem)
    if inspect.isroutine(canonical):
        return elements.FunctionElement(elem)
    raise ValueError('Unknown element in _build_element: {}'.format(elem))


def _build_from_iterable(elem_iterable, sequence_wrapper=None):
    processed_list = [_build_element(e) for e in elem_iterable]
    if sequence_wrapper is None:
        filtered_list = [e for e in processed_list if e is not None]
    else:
        filtered_list = [sequence_wrapper(e) for e in processed_list if e is not None]
    if not filtered_list:
        return
    if len(filtered_list) == 1:
        return filtered_list[0]
    return elements.SequenceElement(filtered_list)


def _build_with_finally(sequence):
    prefix, final = _split_sequence(sequence)
    if final is not None:
        raise inspect.isgeneratorfunction(final) or inspect.isroutine(final) or ValueError('{} not a function in _build_element'.format(final))
    child = _build_from_iterable(prefix)
    if final is None:
        return child
    return elements.WithFinallyElement(child, final)


def _build_critical_section(sequence):
    prefix, final = _split_sequence(sequence)
    final_elem = _build_element(final)
    child = _build_from_iterable(prefix)
    if final is None:
        return child
    return elements.CriticalSectionElement(child, final_elem)


def build_delayed_element(sequence, delay_interval, delayed_element, soft_sleep=False):
    sleep_type = elements.SoftSleepElement if soft_sleep else elements.SleepElement
    delayed_sequence = build_element([sleep_type(delay_interval), delayed_element])
    if sequence:
        new_sequence = elements.AllElement([delayed_sequence, sequence])
    else:
        new_sequence = delayed_sequence
    return new_sequence


def return_true_wrapper(elem):
    return elements.OverrideResultElement(elem, True)


def soft_sleep_forever():
    return return_true_wrapper(elements.RepeatElement(elements.SoftSleepElement(date_and_time.create_time_span(days=28))))


def sleep_until_next_tick_element():
    return elements.BusyWaitElement(soft_sleep_forever(), lambda : True)


def maybe(predicate, sequence):
    return elements.ConditionalElement(predicate, sequence, None)


def unless(predicate, sequence):
    return elements.ConditionalElement(predicate, None, sequence)


def with_callback(target_list, callback, sequence=None):

    def add_callback(_):
        target_list.append(callback)

    def remove_callback(_):
        if callback in target_list:
            target_list.remove(callback)

    return build_critical_section_with_finally(add_callback, sequence, remove_callback)


def do_all(*parallel_elements, thread_element_map=None):
    if not thread_element_map:
        all_elements = parallel_elements
    else:
        if not parallel_elements:
            all_elements = tuple((build_element(sequence) for sequence in thread_element_map.values()))
        else:
            all_elements = itertools.chain(parallel_elements, tuple((build_element(sequence) for sequence in thread_element_map.values())))
    all_elements = tuple((element for element in all_elements if element is not None))
    if len(all_elements) == 1:
        return build_element(all_elements[0])
    return elements.AllElement(all_elements)


def must_run(sequence):
    return elements.MustRunElement(build_element(sequence))