import numpy as np
from enum import Enum
from .config import config as c


class Ship:
    def __init__(self, id=0):
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

    def place_on(self, board, placement_strategy=None):
        raise NotImplementedError  # todo

    @property
    def size(self):
        return c['ship']['ship_sizes'][self.__class__]

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


_ships = dict(
    Carrier=Carrier,
    Battleship=Battleship,
    Destroyer=Destroyer,
    Submarine=Submarine,
    PatrolBoat=PatrolBoat
)


__all__ = [Ship, Carrier, Battleship, Destroyer, Submarine, PatrolBoat]


class ShipEvent(Enum):
    MISS = -1
    HIT = 0
    SINK = 1


defaults = {
    "ship_counts": {
        'Carrier': 1,
        'Battleship': 1,
        'Destroyer': 1,
        'Submarine': 1,
        'PatrolBoat': 1
    },
    "ship_sizes": {
        'Carrier': 5,
        'Battleship': 4,
        'Destroyer': 3,
        'Submarine': 3,
        'PatrolBoat': 2
    }
}
