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


def get_possible_placements(board, ship):
    orientations = dict(vertical=[], horizontal=[])

    # horizontal openings
    for r in range(board.size):
        open_spaces = np.argwhere(board.placement_mask[r, :] == 0).flatten()
        for segment in adjacent_values(open_spaces):
            if len(segment) >= ship.size:
                x = strides(segment, size=ship.size, step=1)
                y = np.ones_like(x) * r
                orientations['horizontal'].append((tuple(x), tuple(y)))

    # vertical openings
    for c in range(board.size):
        open_spaces = np.argwhere(board.placement_mask[:, c] == 0).flatten()
        for segment in adjacent_values(open_spaces):
            if len(segment) >= ship.size:
                y = strides(segment, size=ship.size, step=1)
                x = np.ones_like(y) * c
                orientations['vertical'].append((tuple(x), tuple(y)))
    return orientations  # todo: datastructure cleanup


def random_placement(board, ship):
    poss = get_possible_placements(board, ship)
    v = len(poss['vertical'])
    h = len(poss['horizontal'])
    if v and h:
        d = np.random.choice(['vertical', 'horizontal'])
        ix = np.random.choice(np.arange(len(poss[d])))

        p = poss[d][ix]
        print(ship.name, ship.size, p)
        return p
    elif v:
        d = 'vertical'
        p = np.random.choice(np.arange(len(poss[d])))
        p = poss[d][p]
        return p
    elif h:
        d = 'horizontal'
        p = np.random.choice(np.arange(len(poss[d])))
        p = poss[d][p]
        return p
    else:
        raise Exception("no viable placements for {ship} remaining")


def get_strategy(placement_strategy):
    if placement_strategy.lower() == 'random':
        return random_placement
    else:
        raise NotImplementedError(placement_strategy)
