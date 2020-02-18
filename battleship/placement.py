from itertools import groupby
import numpy as np

defaults = {}


class AdjacentKey(object):
    __slots__ = ['obj']

    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        ret = self.obj - 1 <= other.obj <= self.obj + 1
        if ret:
            self.obj = other.obj
        return ret


def adjacent_values(a):
    groups = [np.array(list(g)).flatten() for k, g in groupby(a, AdjacentKey)]
    return groups


def strides(a, size=2, step=1):
    def _stridegen(a, size, step):
        for i in range(0, len(a), step):
            win = a[i: i + size]
            if len(win) != size:
                return
            yield win
    return np.array(list(_stridegen(a, size, step)))


def get_possible_placements(placement_mask, size, ship):
    orientations = dict(vertical=[], horizontal=[])

    # horizontal openings
    for r in range(size):
        open_spaces = np.argwhere(placement_mask[r, :] == 0).flatten()
        for segment in adjacent_values(open_spaces):
            if len(segment) >= ship.size:
                x = strides(segment, size=ship.size, step=1)
                y = np.ones_like(x) * r
                for i in range(x.shape[0]):
                    orientations['horizontal'].append((list(x[i]), list(y[i])))

    # vertical openings
    for c in range(size):
        open_spaces = np.argwhere(placement_mask[:, c] == 0).flatten()
        for segment in adjacent_values(open_spaces):
            if len(segment) >= ship.size:
                y = strides(segment, size=ship.size, step=1)
                x = np.ones_like(y) * c
                for i in range(x.shape[0]):
                    orientations['vertical'].append((list(x[i]), list(y[i])))

    for k in orientations:
        orientations[k] = np.array(orientations[k])
    return orientations


def random_placement(placement_mask, size, ship):
    poss = get_possible_placements(placement_mask, size, ship)
    v = len(poss['vertical'])
    h = len(poss['horizontal'])
    if v and h:
        d = np.random.choice(['vertical', 'horizontal'])
        p = np.random.choice(np.arange(len(poss[d])))
        p = poss[d][p]
        return p.astype(np.uint8)
    elif v:
        d = 'vertical'
        p = np.random.choice(np.arange(len(poss[d])))
        p = poss[d][p]
        return p.astype(np.uint8)
    elif h:
        d = 'horizontal'
        p = np.random.choice(np.arange(len(poss[d])))
        p = poss[d][p]
        return p.astype(np.uint8)
    else:
        raise Exception(f"no viable placements for {ship} remaining")


def get_strategy(placement_strategy):
    if placement_strategy.lower() == 'random':
        return random_placement
    else:
        raise NotImplementedError(placement_strategy)
