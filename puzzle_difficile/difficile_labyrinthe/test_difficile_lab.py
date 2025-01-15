#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
from difficile_labyrinthe import Labyrinthe, main, read_line_file


class TestDifficileLab(unittest.TestCase):

    def test_parse_lab(self):
        np.set_printoptions(linewidth=150)
        lab = Labyrinthe(10, 26, -1, -1)
        lab.parse_labyrinthe(LabContainerStr())
        self.assertEqual(lab.grid.shape, (12, 28))
        self.assertTrue(lab.can_see_cmd_room)
        # print(lab)

    def test_propagate_distance(self):
        np.set_printoptions(linewidth=150)
        print("test_propagate_distance")
        lab = Labyrinthe(10, 26, -1, -1)
        lab.parse_labyrinthe(LabContainerStr())
        lab.propagate_distance_from_position(4, 5)
        self.assertEqual(lab.grid[9, 25], 46)
        # print(lab)

    def test_move_cmd_cell(self):
        np.set_printoptions(linewidth=150)
        print("test_move_cmd_cell")
        lab = Labyrinthe(10, 26, -1, -1)
        lab.parse_labyrinthe(LabContainerStr())
        lab.propagate_distance_from_position(4, 5)
        lab.try_go_to_cmd_room()

    def test_go_to_unknown(self):
        np.set_printoptions(linewidth=150)
        print("test_go_to_unknown")
        lab = Labyrinthe(10, 26, -1, -1)
        lab.parse_labyrinthe(LabContainerStr())
        lab.propagate_distance_from_position(4, 5)
        lab.one_step_to_closest_unknown()


############################
# Tests
############################
class LabContainerStr:
    def __init__(self):
        self.count_call = 0
        self.lab = [
            "??????????????????????????",
            "............??????????????",
            ".###########??????????????",
            "...T........??????????????",
            ".....................#.#..",
            ".#####################.#..",
            "...##......##......#....##",
            ".####..##..##..##..#..#...",
            ".......##......##.....#.C.",
            "##########################"
        ]

    def __call__(self, *args, **kwargs):
        if self.count_call == 0:
            print('\n'.join(self.lab))

        to_return = self.lab[self.count_call % len(self.lab)]
        self.count_call += 1
        return to_return


# def test_main():
#     with open("test_files/test_1.txt", "r") as f:
#         main(get_line_func=lambda: read_line_file(f))


# test_main()

# test_parse_lab()
# test_propagate_distance()
# test_move_cmd_cell()
# test_go_to_unknown()
