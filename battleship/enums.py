from enum import Enum
from .ships import (Carrier, Battleship, Destroyer, Submarine, PatrolBoat)


class ShipEvent(Enum):
    MISS = -1
    HIT = 0
    SINK = 1


class ShipCounts(Enum):
    Standard = {
        Carrier: 1,
        Battleship: 1,
        Destroyer: 1,
        Submarine: 1,
        PatrolBoat: 1
    }


class ShipSizes(Enum):
    Standard = {
        Carrier: 5,
        Battleship: 4,
        Destroyer: 3,
        Submarine: 3,
        PatrolBoat: 2
    }