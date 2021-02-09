# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\gsi_handlers\timeline_handlers.py
# Compiled at: 2014-03-09 04:38:57
# Size of source mod 2**32: 2328 bytes
import collections

def _label(e, label):
    if label:
        return 'label="{}"'.format(e)
    return ''


def dotviz(t, label=True):
    lines = [
     'digraph timeline {']
    lines.append('rankdir = LR;')
    times = collections.defaultdict(list)
    for when, ix, element in t.queue:
        times[when].append((ix, element))

    sorted_times = sorted(times.keys())
    lines.append('subgraph T {')
    lines.append(' rank=min;')
    lines.append(' node [shape=box];')
    lines.append(' {};'.format(' -> '.join(['T{}'.format(when) for when in sorted_times])))
    if t._active is not None:
        lines.append('Eactive [shape=ellipse;{}];'.format(_label(t._active[0], label)))
        lines.append('Eactive -> T{};'.format(sorted_times[0]))
    lines.append('}')
    for when, events in sorted(times.items()):
        lines.append('subgraph {')
        for ix, element in events:
            lines.append(' E{} [{}];'.format(abs(ix), _label(element, label)))

        row = ' T{} -> {};'.format(when, ' -> '.join(('E{}'.format(abs(ix)) for ix, _ in sorted(events))))
        lines.append(row)
        lines.append('}')
        if t._active is not None:
            for ix, elem in events:
                if elem is t._active[0]:
                    lines.append('Eactive -> E{} [dir=none; style=dashed; constraint=false];'.format(abs(ix)))

    lines.append('}')
    return '\n'.join(lines)