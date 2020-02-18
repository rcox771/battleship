from enum import Enum


class Rule(Enum):
    NO_OVERLAP = "coords must not overlap with another allied ship"
    NO_TOUCH = "coords must not touch with another allied ship"
    NO_OOB = "coords must be enclosed within board size"
