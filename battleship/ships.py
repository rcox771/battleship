import numpy as np
from enum import Enum
from .config import Configurable
from .rules import Rule
from . import placement


class Ship(Configurable):
    def __init__(self, id=0):
        super().__init__()
        self.id = id
        self.squares = np.zeros((self.size, 2))
        self.hp = np.ones(self.size)

    def is_sunk(self):
        return (self.hp.sum() / len(self.squares)) == 0

    def is_placed(self):
        return self.squares.flatten().sum() > 0

    def hit_by(self, y, x):
        loc = np.argwhere((self.squares[:, 0] == y)
                          & (self.squares[:, 1] == x)).flatten()
        return bool(loc), loc

    @property
    def ys(self):
        return self.squares[:, 0].copy()

    @property
    def xs(self):
        return self.squares[:, 1].copy()

    def set_xs(self, xs):
        self.squares[:, 1] = xs

    def set_ys(self, ys):
        self.squares[:, 0] = ys

    def take_damage(self, y, x):
        hit, loc = self.hit_by(y, x)
        if hit:
            self.hp[loc] = 0
            if self.is_sunk():
                return ShipEvent.SINK
            else:
                return ShipEvent.HIT
        else:
            return ShipEvent.MISS

    def bounds(self, boardsize, no_touch=False):
        ymin = self.ys.min() - 1 if no_touch else 0
        ymax = self.ys.max() + 1 if no_touch else 0
        xmin = self.xs.min() - 1 if no_touch else 0
        xmax = self.xs.max() + 1 if no_touch else 0
        return np.clip(np.array([ymin, ymax, xmin, xmax], 0, boardsize))

    def place_on(self, board, placement_strategy=None):
        success = False
        if isinstance(placement_strategy, str):
            placement_strategy = placement.get_strategy(placement_strategy)
        xs, ys = placement_strategy(board, self)
        self.set_xs(xs)
        self.set_ys(ys)

        # check coords must be within board boundary
        x_within_bounds = ((0 <= self.xs) & (self.xs < board.size)).all()
        y_within_bounds = ((0 <= self.ys) & (self.ys < board.size)).all()
        if not (x_within_bounds and y_within_bounds):
            return success, Rule.NO_OOB

        # check touching if necessary
        if Rule.NO_TOUCH in board.rules:
            # coords must not touch or overlap another ship's boundaries
            if not board.placement_mask[self.ys, self.xs].any():
                return success, Rule.NO_TOUCH

        # check overlap if necessary
        undo = board.placement_mask.copy()
        ymin, ymax, xmin, xmax = self.bounds(board.size)
        board.placement_mask[ymin:ymax, xmin:xmax] += 1
        if Rule.NO_OVERLAP in board.rules:
            if (board.placement_mask > 1).any():
                board.placement_mask = undo
                return success, Rule.NO_OVERLAP
        success = True

        return success, dict(name=self.name, xs=self.xs, ys=self.ys)

    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"{self.name}"


class Carrier(Ship):
    def __init__(self, id=0):
        super().__init__(id=id)


class Battleship(Ship):
    def __init__(self, id=0):
        super().__init__(id=id)


class Destroyer(Ship):
    def __init__(self, id=0):
        super().__init__(id=id)


class Submarine(Ship):
    def __init__(self, id=0):
        super().__init__(id=id)


class PatrolBoat(Ship):
    def __init__(self, id=0):
        super().__init__(id=id)


class ShipEvent(Enum):
    MISS = -1
    HIT = 0
    SINK = 1
