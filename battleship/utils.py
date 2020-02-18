from string import ascii_uppercase
from uuid import uuid4


def get_short_uuid():
    return str(uuid4()).split('-')[-1]


def get_ax_labels(board_size):
    cols = ascii_uppercase[:board_size][::-1]
    rows = list(map(str, range(board_size)))
    return rows, cols
