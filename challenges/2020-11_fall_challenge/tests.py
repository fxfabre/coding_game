#!/usr/bin/env python3

from unittest import TestCase
from user_state import Witch, BrewAction, CastAction


POTIONS = [
    BrewAction((0, 0, 0, -5), 23, 65),
    BrewAction((-3, -2, 0, 0), 8, 43),
    BrewAction((-2, -2, -2, 0), 13, 69),
    BrewAction((-2, -1, 0, -1), 9, 66),
    BrewAction((0, -2, -3, 0), 13, 56)
]
SORTS = [
    CastAction((2, 0, 0, 0), 0, 78),
    CastAction((-1, 1, 0, 0), 0, 79),
    CastAction((0, -1, 1, 0), 0, 80),
    CastAction((0, 0, -1, 1), 0, 81),
]
ALL_ACTIONS = {
    "BREW": POTIONS,
    "CAST": SORTS,
}


class TestCast(TestCase):
    def test_choose_sort_1(self):
        witch_state = Witch((3, 0, 0, 0), 0)
        sorts = [
            CastAction((-1, 1, 0, 0), 0, 1, 0, 0, True, True),
            CastAction((-1, 2, 0, 0), 0, 2, 0, 0, True, True),
        ]
        potions = [
            BrewAction((1, 2, 1, 1), 0, 5, 0, 0, True, True),
        ]
        sort = witch_state.find_best_cast(sorts, potions)
        self.assertEqual(2, sort.action_id)

        sort = witch_state.find_best_cast(sorts[::-1], potions)
        self.assertEqual(2, sort.action_id)

    def test_choose_sort_max_10(self):
        witch_state = Witch((3, 0, 0, 0), 0)
        sorts = [
            CastAction((-1, 10, 0, 0), 0, 1, 0, 0, True, True),
            CastAction((-1, 2, 0, 0), 0, 2, 0, 0, True, True),
        ]
        potions = [
            BrewAction((1, 1, 1, 1), 0, 5, 0, 0, True, True),
        ]
        sort = witch_state.find_best_cast(sorts, potions)
        self.assertEqual(2, sort.action_id)

        sort = witch_state.find_best_cast(sorts[::-1], potions)
        self.assertEqual(2, sort.action_id)

    def test_choose_sort_3_avoid_too_much_of_1_ingredient(self):
        witch_state = Witch((3, 0, 0, 0), 0)
        sorts = [
            CastAction((-1, 4, 0, 0), 0, 1, 0, 0, True, True),
            CastAction((-1, 1, 1, 1), 0, 2, 0, 0, True, True),
        ]
        potions = [
            BrewAction((1, 1, 1, 1), 0, 5, 0, 0, True, True),
        ]
        sort = witch_state.find_best_cast(sorts, potions)
        self.assertEqual(2, sort.action_id)

        sort = witch_state.find_best_cast(sorts[::-1], potions)
        self.assertEqual(2, sort.action_id)


class HeuristiqueChooseBrew(TestCase):
    def test_best_brew_heuristic(self):
        witch = Witch((3, 2, 3, 5), 0)
        brew_action = witch.heuristique_find_best_action(ALL_ACTIONS)
        self.assertEqual(65, brew_action.action_id)

    def test_brew_middle_heuristic(self):
        witch = Witch((3, 2, 2, 1), 0)
        brew_action = witch.heuristique_find_best_action(ALL_ACTIONS)
        self.assertEqual(69, brew_action.action_id)


class RecursiveChooseBrew(TestCase):
    def test_best_brew_recursive(self):
        witch = Witch((3, 2, 3, 5), 0)
        brew_action, score, brew_id = witch.find_best_action(ALL_ACTIONS, 0)
        self.assertEqual(65, brew_action.action_id)
        # self.assertEqual(23, score)
        # self.assertEqual(65, brew_id)

    def test_brew_middle_recursive(self):
        witch = Witch((3, 2, 2, 1), 0)
        brew_action, score, brew_id = witch.mcts_find_best_action(ALL_ACTIONS, 0)
        self.assertEqual(69, brew_action.action_id)
        # self.assertEqual(13, score)
        # self.assertEqual(69, brew_id)

    def test_find_cast_deep_2(self):
        witch = Witch((3, 0, 0, 0), 0)
        all_actions = {
            "BREW": POTIONS + [BrewAction((-1, -1, 0, 0), 10, 1)],
            "CAST": SORTS,
        }
        cast_action, score, brew_id = witch.recursive_find_best_action(all_actions, 2)
        self.assertEqual(79, cast_action.action_id)
        self.assertEqual(1, brew_id)

    def test_find_cast_deep_4(self):
        witch = Witch((3, 0, 0, 0), 0)
        all_actions = {
            "BREW": POTIONS + [BrewAction((0, 0, 0, -1), 100, 1)],
            "CAST": SORTS,
        }
        cast_action, score, brew_id = witch.recursive_find_best_action(all_actions, 4)
        self.assertEqual(79, cast_action.action_id)
        self.assertEqual(1, brew_id)
