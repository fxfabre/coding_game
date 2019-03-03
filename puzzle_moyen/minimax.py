# coding=utf-8

import unittest
from typing import List

MINUS_INF = float('-inf')
INF = float('inf')


class Minimax:

    def __init__(self, leaves: List[float], branch_factor: int, *args, **kwargs):
        super(Minimax, self).__init__(*args, **kwargs)
        self.leaves = leaves
        self.branch_factor = branch_factor
        self.count_cells_evaluated = 0

    def run(self):
        score = self.max(self.leaves, MINUS_INF, INF)
        return score, self.count_cells_evaluated

    def get_child_leaves(self, leaves: List[float]):
        packet_size = len(leaves) // self.branch_factor
        return [leaves[i * packet_size: (i + 1) * packet_size] for i in range(self.branch_factor)]

    def max(self, leaves: List[float], alpha: float, beta: float):
        self.count_cells_evaluated += 1

        if len(leaves) == 1:
            return leaves[0]

        childs_leaves = self.get_child_leaves(leaves)

        max_score = MINUS_INF
        for child_leaves in childs_leaves:
            child_score = self.min(child_leaves, alpha, beta)
            max_score = max(max_score, child_score)
            alpha = max(alpha, child_score)
            if beta <= alpha:
                break

        return max_score

    def min(self, leaves: List[float], alpha: float, beta: float):
        self.count_cells_evaluated += 1

        if len(leaves) == 1:
            return leaves[0]

        childs_leaves = self.get_child_leaves(leaves)

        min_score = INF
        for child_leaves in childs_leaves:
            child_score = self.max(child_leaves, alpha, beta)
            min_score = min(min_score, child_score)
            beta = min(beta, child_score)
            if beta <= alpha:
                break
        return min_score


class TestMinimax(unittest.TestCase):

    def test_depth_1_game(self):
        score, visited_nodes = Minimax([-2, -1, 3, 0], 4).run()
        self.assertEqual(3, score)
        self.assertEqual(5, visited_nodes)

    def test_depth_2_no_cutoffs(self):
        score, visited_nodes = Minimax([1, 2, 3, 4], 2).run()
        self.assertEqual(3, score)
        self.assertEqual(7, visited_nodes)

    def test_depth_2_cutoffs(self):
        score, visited_nodes = Minimax([1, 2, 0, 4], 2).run()
        self.assertEqual(1, score)
        self.assertEqual(6, visited_nodes)

    def test_small_game(self):
        score, visited_nodes = Minimax([-1, 0, 2, 666, -3, -2, 666, 666], 2).run()
        self.assertEqual(0, score)
        self.assertEqual(11, visited_nodes)


def main():
    d, b = [int(i) for i in input().split()]
    leaves = [int(i) for i in input().split(' ')]

    score, visited_nodes = Minimax(leaves, b).run()

    print(score, visited_nodes)
