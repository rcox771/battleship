from __future__ import absolute_import

import random
import numpy as np
from matplotlib import pyplot as plt
from .utils import get_ax_labels, get_short_uuid
import inspect
from . import ships


def get_ships():
    d = dict(inspect.getmembers(ships))
    d = {k: d[k] for k in d if 'ships.' in repr(
        d[k]).lower() and not k.startswith('__')}
    return d


class Board:
    def __init__(self, board_size=10,
                 placement_strategy=None):

        self.board = np.zeros((board_size, board_size), dtype=np.uint8)
        self.rows, self.cols = get_ax_labels(board_size)
        self.ships = []
        self.place_ships(placement_strategy)

    def place_ships(self, placement_strategy):
        _ships = get_ships()
        for ship in _ships:
            to_place = _ships[ship]().count
            for _ in range(to_place):
                ship = _ships[ship](id=len(self.ships))
                ship.place_on(self.board,
                              placement_strategy=self.placement_strategy)
                assert ship.is_placed()

    def plot(self, ax=None, figsize=(5, 5)):
        if not ax:
            fig, ax = plt.subplots(figsize=figsize)
        ax.pcolor(self.board,
                  cmap='gray',
                  edgecolor='black',
                  linestyle='dashed',
                  lw=1)
        for axis, labels in zip([ax.xaxis, ax.yaxis], [self.rows, self.cols]):
            axis.set(ticks=np.arange(0.5, len(labels)), ticklabels=labels)


class Player:
    def __init__(self, name=None, targeting_func=None, placement_func=None):
        if not name:
            name = f'bot_{get_short_uuid()}'
        self.name = name
        self.targeting_func, self.placement_func = (targeting_func,
                                                    placement_func)
        self.board = Board(placement_strategy=self.placement_func)
        self.targeting_board = np.zeros_like(self.board.board)

    def take_turn(self):
        raise NotImplementedError  # todo


class Game:
    def __init__(self, *players, id=None):
        self.players = players
        if not id:
            id = f'game-{get_short_uuid()}'
        self.id = id
        random.shuffle(self.players)

    def reset(self):
        raise NotImplementedError  # todo

    def is_over(self):
        raise NotImplementedError  # todo
