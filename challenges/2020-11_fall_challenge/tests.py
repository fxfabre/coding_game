#!/usr/bin/env python3

from unittest import TestCase

from solution_3 import User, Action, filter_cast_min as filter_cast_max
Sort = Action
Potion = Action


class TestCast(TestCase):

    def test_choose_sort_1(self):
        user_state = User(3, 0, 0, 0, 0)
        sorts = [
            Sort(-1, 1, 0, 0, 0, 1, 0, 0, True, True),
            Sort(-1, 2, 0, 0, 0, 2, 0, 0, True, True),
        ]
        potions = [
            Potion(1, 2, 1, 1, 0, 5, 0, 0, True, True),
        ]
        sort = filter_cast_max(sorts, potions, user_state)
        self.assertEqual(2, sort.action_id)

        sort = filter_cast_max(sorts[::-1], potions, user_state)
        self.assertEqual(2, sort.action_id)

    def test_choose_sort_max_10(self):
        user_state = User(3, 0, 0, 0, 0)
        sorts = [
            Sort(-1, 10, 0, 0, 0, 1, 0, 0, True, True),
            Sort(-1, 2, 0, 0, 0, 2, 0, 0, True, True),
        ]
        potions = [
            Potion(1, 1, 1, 1, 0, 5, 0, 0, True, True),
        ]
        sort = filter_cast_max(sorts, potions, user_state)
        self.assertEqual(2, sort.action_id)

        sort = filter_cast_max(sorts[::-1], potions, user_state)
        self.assertEqual(2, sort.action_id)

    def test_choose_sort_3_avoid_too_much_of_1_ingredient(self):
        user_state = User(3, 0, 0, 0, 0)
        sorts = [
            Sort(-1, 4, 0, 0, 0, 1, 0, 0, True, True),
            Sort(-1, 1, 1, 1, 0, 2, 0, 0, True, True),
        ]
        potions = [
            Potion(1, 1, 1, 1, 0, 5, 0, 0, True, True),
        ]
        sort = filter_cast_max(sorts, potions, user_state)
        self.assertEqual(2, sort.action_id)

        sort = filter_cast_max(sorts[::-1], potions, user_state)
        self.assertEqual(2, sort.action_id)
