# coding=utf-8

import unittest
import numpy as np
from typing import List, Tuple

WALL = 1


class Labyrinthe:

    def __init__(self, labyrinthe: np.array, nb_cols: int, nb_rows: int, *args, **kwargs):
        super(Labyrinthe, self).__init__(*args, **kwargs)
        self.labyrinthe = labyrinthe
        self.nb_rows = nb_rows
        self.nb_cols = nb_cols
        self.path_counter = np.zeros([nb_rows, nb_cols])

    def count_path(self) -> int:
        self.path_counter[0, 0] = 1
        next_positions = [(1, 0), (0, 1)]

        while len(next_positions) > 0:
            positions_to_eval = next_positions
            next_positions = []
            for (x, y) in positions_to_eval:
                next_positions.extend(self.propagate_path(x, y))

        return int(self.path_counter[self.nb_rows - 1, self.nb_cols - 1])

    def propagate_path(self, x: int, y: int) -> List[Tuple[int, int]]:
        if not 0 <= x < self.nb_cols:
            return []
        if not 0 <= y < self.nb_rows:
            return []
        if self.labyrinthe[y, x] == WALL:
            return []

        left = self.get_value(x-1, y)
        top = self.get_value(x, y-1)
        self.set_value(x, y, left + top)
        return [(x+1, y), (x, y+1)]

    def get_value(self, x: int, y: int) -> int:
        if not 0 <= x < self.nb_cols:
            return 0
        if not 0 <= y < self.nb_rows:
            return 0
        return self.path_counter[y, x]

    def set_value(self, x: int, y: int, value: int) -> None:
        if not 0 <= x < self.nb_cols:
            return
        if not 0 <= y < self.nb_rows:
            return
        self.path_counter[y, x] = value


class TestCountPath(unittest.TestCase):

    def test_cg_1(self):
        nb_cols, nb_rows = 2, 2
        lab = Labyrinthe(np.zeros([nb_cols, nb_rows]), nb_cols, nb_rows)
        self.assertEqual(2, lab.count_path())

    def test_cg_2(self):
        nb_cols, nb_rows = 2, 2
        lab = Labyrinthe(np.array([[0, 0], [1, 0]]), nb_cols, nb_rows)
        self.assertEqual(1, lab.count_path())

    def test_cg_3(self):
        grid = np.array([
            [int(n) for n in '0 0 0 0 0 0 1 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 1 0 0 0 1 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 1 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 1 0 0 0 1 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 1 0 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 0 1 0'.split()],
        ])
        nb_cols, nb_rows = 10, 10
        lab = Labyrinthe(np.array(grid), nb_cols, nb_rows)
        self.assertEqual(2716, lab.count_path())

    def test_cg_4(self):
        grid = np.array([
            [int(n) for n in '0 0 1 0 0 0 1 0 0 0'.split()],
            [int(n) for n in '0 0 1 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 1 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '1 1 1 0 0 0 1 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 1 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 1 0 0 0 1 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 0 0 0'.split()],
            [int(n) for n in '0 0 0 0 0 0 0 1 0 1'.split()],
        ])
        nb_cols, nb_rows = 10, 9
        lab = Labyrinthe(np.array(grid), nb_cols, nb_rows)
        self.assertEqual(0, lab.count_path())

    def test_custom_1(self):
        nb_cols, nb_rows = 3, 2
        lab = Labyrinthe(np.array([[0, 0, 0], [0, 0, 0]]), nb_cols, nb_rows)
        self.assertEqual(3, lab.count_path())


def main():
    nb_rows = int(input())
    nb_cols = int(input())
    all_values = []
    for i in range(nb_rows):
        row = list(input())
        all_values += [int(n) for n in row]

    array = np.array(all_values).reshape([nb_rows, nb_cols])
    return Labyrinthe(array, nb_cols, nb_rows).count_path()
