# coding=utf-8

import sys
import unittest


class HanoiTower:

    def __init__(self, nb_total_disks):
        super(HanoiTower, self).__init__()
        self.nb_total_disks = nb_total_disks
        self.count_moves = 0
        self.towers = [
            list(range(nb_total_disks, 0, -1)),
            [],
            []
        ]

    def move_disks(self, tour_origine, tour_destination, nb_disks_to_move):
        if nb_disks_to_move == 1:
            self.record_move(tour_origine, tour_destination)
            return

        self.move_disks(tour_origine, 6 - tour_origine - tour_destination, nb_disks_to_move - 1)
        self.move_disks(tour_origine, tour_destination, 1)
        self.move_disks(6 - tour_origine - tour_destination, tour_destination, nb_disks_to_move - 1)

    def move_n_steps(self, nb_steps=sys.maxsize):
        moves = [(1, 3, self.nb_total_disks)]

        while (len(moves) > 0) and (nb_steps > self.count_moves):
            (tour_origine, tour_destination, nb_disks) = moves.pop(0)
            new_moves = self.move_one_step(tour_origine, tour_destination, nb_disks)
            moves = new_moves + moves

    def move_one_step(self, tour_origine, tour_destination, nb_disks):
        if nb_disks == 1:
            self.record_move(tour_origine, tour_destination)
            return []

        return [
            (tour_origine, 6 - tour_origine - tour_destination, nb_disks - 1),
            (tour_origine, tour_destination, 1),
            (6 - tour_origine - tour_destination, tour_destination, nb_disks - 1)
        ]

    def display_current_state(self):
        towers_display = []
        for tower in self.towers:
            rows_for_tower = [
                ' ' * (self.nb_total_disks - size) + '#' * (2 * size + 1) + ' ' * (self.nb_total_disks - size)
                for size in tower
            ] + [
                ' ' * self.nb_total_disks + '|' + ' ' * self.nb_total_disks
                for _ in range(self.nb_total_disks - len(tower))
            ]
            towers_display.append(rows_for_tower)

        str_out = []
        for towers_str in zip(*towers_display):
            str_out.append(' '.join(towers_str))
        return str_out[::-1]

    def record_move(self, tour_origine, tour_destination):
        disk_pop = self.towers[tour_origine - 1].pop()
        self.towers[tour_destination - 1].append(disk_pop)
        self.count_moves += 1


class TestHanoiTower(unittest.TestCase):

    def test_display_state_1(self):
        nb_total_disks = 1
        expected = ['###  |   | ']
        actual = HanoiTower(nb_total_disks).display_current_state()
        self.assertEqual(expected, actual)

    def test_display_state_3(self):
        nb_total_disks = 3
        expected = ['  ###      |       |   ', ' #####     |       |   ', '#######    |       |   ']
        actual = HanoiTower(nb_total_disks).display_current_state()
        self.assertEqual(expected, actual)

    def test_1_step(self):
        nb_total_disks = 2
        hanoi = HanoiTower(nb_total_disks)
        hanoi.move_n_steps(1)
        expected = ['  |     |     |  ', '#####  ###    |  ']
        actual = hanoi.display_current_state()
        self.assertEqual(expected, actual)

    def test_2_steps(self):
        nb_total_disks = 2
        hanoi = HanoiTower(nb_total_disks)
        hanoi.move_n_steps(2)
        expected = ['  |     |     |  ', '  |    ###  #####']
        actual = hanoi.display_current_state()
        self.assertEqual(expected, actual)

    def test_move_recursif(self):
        nb_total_disks = 2
        hanoi = HanoiTower(nb_total_disks)
        hanoi.move_disks(1, 3, nb_total_disks)
        expected = ['  |     |    ### ', '  |     |   #####']
        actual = hanoi.display_current_state()
        self.assertEqual(expected, actual)

    def test_total_number_moves(self):
        nb_total_disks = 3
        hanoi = HanoiTower(nb_total_disks)
        hanoi.move_disks(1, 3, nb_total_disks)
        expected = ['  |     |    ### ', '  |     |   #####']
        actual = hanoi.display_current_state()
        self.assertEqual(expected, actual)


def main():
    nb_total_disk = int(input())
    nb_turn = int(input())

    hanoi = HanoiTower(nb_total_disk)
    hanoi.move_n_steps(nb_turn)
    state_after_n_moves = hanoi.display_current_state()

    hanoi = HanoiTower(nb_total_disk)
    hanoi.move_n_steps()
    nb_total_moves = hanoi.count_moves

    print('\n'.join(map(str.rstrip, state_after_n_moves)))
    print(nb_total_moves)
