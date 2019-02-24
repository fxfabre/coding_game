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
        score = self._minimax(self.leaves, MINUS_INF, INF, True)
        return score, self.count_cells_evaluated

    def _minimax(self, leaves: List[float], alpha: float, beta: float, maximize: bool):
        self.count_cells_evaluated += 1

        if len(leaves) == 1:
            return leaves[0]

        packet_size = len(leaves) // self.branch_factor
        childs_leaves = [leaves[i * packet_size: (i + 1) * packet_size] for i in range(self.branch_factor)]

        if maximize:
            max_score = MINUS_INF
            for child_leaves in childs_leaves:
                child_score = self._minimax(child_leaves, alpha, beta, False)
                max_score = max(max_score, child_score)
                alpha = max(alpha, child_score)
                if beta <= alpha:
                    break

            return max_score

        min_score = INF
        for child_leaves in childs_leaves:
            child_score = self._minimax(child_leaves, alpha, beta, True)
            min_score = min(min_score, child_score)
            beta = min(beta, child_score)
            if beta <= alpha:
                break
        return min_score


class TestMinimax(unittest.TestCase):

    def test_depth_1_game(self):
        score, visited_nodes = Minimax([-2, -1, 3, 0], 4).run()
        assert score == 3
        assert visited_nodes == 5

    def test_depth_2_no_cutoffs(self):
        score, visited_nodes = Minimax([1, 2, 3, 4], 2).run()
        assert score == 3
        assert visited_nodes == 7

    def test_depth_2_cutoffs(self):
        score, visited_nodes = Minimax([1, 2, 0, 4], 2).run()
        assert score == 1
        assert visited_nodes == 6

    def test_small_game(self):
        score, visited_nodes = Minimax([-1, 0, 2, 666, -3, -2, 666, 666], 2).run()
        assert score == 0
        assert visited_nodes == 11
