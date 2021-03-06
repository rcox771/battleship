from __future__ import absolute_import

import random
import numpy as np
from matplotlib import pyplot as plt
from .utils import get_ax_labels, get_short_uuid
import inspect
from . import ships
from .rules import Rule
from .config import read_config
from . import placement


def get_ships():
    d = dict(inspect.getmembers(ships))
    d = {k: d[k] for k in d if k in list(read_config()['Ship'])}
    return d


class Board:
    def __init__(self, board_size=10,
                 placement_strategy=None):
        self.size = board_size
        self.board = np.zeros((board_size, board_size), dtype=np.uint8)
        self.placement_mask = np.zeros_like(self.board)
        self.rows, self.cols = get_ax_labels(board_size)
        self.ships = []
        self.rules = [Rule.NO_OVERLAP, Rule.NO_TOUCH, Rule.NO_OOB]
        self.place_ships(placement_strategy)

    def place_ships(self, placement_strategy=None):
        if not placement_strategy:
            placement_strategy = 'random'
        _ships = get_ships()
        for ship in _ships:
            to_place = _ships[ship]().count
            for _ in range(to_place):
                ship = _ships[ship](id=len(self.ships))
                self.place(ship, placement_strategy)
                assert ship.is_placed()
                self.ships.append(ship)

    def place(self, ship, placement_strategy=None):
        if isinstance(placement_strategy, str):
            placement_strategy = placement.get_strategy(placement_strategy)
        xs, ys = placement_strategy(self.placement_mask, self.size, ship)

        ship.set_xs(xs)
        ship.set_ys(ys)

        ymin, ymax, xmin, xmax = ship.bounds(
            self.size, no_touch=bool(Rule.NO_TOUCH in self.rules))
        self.placement_mask[ymin:ymax, xmin:xmax] = 1

        # check coords must be within board boundary
        x_within_bounds = ((0 <= ship.xs) & (ship.xs < self.size)).all()
        y_within_bounds = ((0 <= ship.ys) & (ship.ys < self.size)).all()
        assert (x_within_bounds and y_within_bounds)
        #

        # check touching if necessary
        # if Rule.NO_TOUCH in board.rules:
        #     # coords must not touch or overlap another ship's boundaries
        #     if not board.placement_mask[self.ys, self.xs].any():
        #         return success, board, Rule.NO_TOUCH

    def plot(self, ax=None, figsize=(5, 5)):
        if not ax:
            fig, ax = plt.subplots(figsize=figsize)

        view = np.zeros_like(self.board)

        for ship in self.ships:
            view[ship.ys, ship.xs] = ship.id + 1

        ax.pcolor(view,
                  cmap='viridis',
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
