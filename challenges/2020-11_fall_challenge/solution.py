#!/usr/bin/env python3

"""
Ligue bois 1,
Si on peut produire une solution : on le fait
Sinon on lance un sort qui permet de diminuer le nombre d'ingredients d'écart avec
le sort le plus facile à lancer (qui requiert le moins d'ingredients supplémentaire)
"""

import sys
import math
from time import time
from collections import namedtuple
from itertools import count
import pandas as pd
from pprint import pprint
from typing import Dict, Tuple, List, Optional
from operator import itemgetter
import random

User = namedtuple("User", ["inv_0", "inv_1", "inv_2", "inv_3", "score"])
Action = namedtuple("Action", ["delta_0", "delta_1", "delta_2", "delta_3", "price", "action_id", "tome_index", "tax_count", "is_castable", "repeatable"])

GET_DELTA = (itemgetter(n) for n in range(4))
GET_PRICE = itemgetter(4)
GET_ACTION = itemgetter(5)
IS_CASTABLE = itemgetter(8)
COLUMNS = [     # CAST, OPPONENT_CAST, LEARN, BREW
    "delta_0", "delta_1", "delta_2", "delta_3", "price", "action_id",
    "tome_index",   # the index in the tome if this is a tome spell, equal to the read-ahead tax
    "tax_count",    # the amount of taxed tier-0 ingredients you gain from learning this spell
    "castable",     # 1 if this is a castable player spell
    "repeatable"    # 1 if this is a repeatable player spell
]


def read_actions() -> Dict[str, List[Action]]:
    action_count = int(input())
    actions = {
        "CAST": [],
        "OPPONENT_CAST": [],
        "LEARN": [],
        "BREW": []
    }
    for i in range(action_count):
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action = Action(
            int(delta_0), int(delta_1), int(delta_2), int(delta_3), int(price), int(action_id),
            int(tome_index), int(tax_count), castable != "0", repeatable != "0"
        )
        actions[action_type].append(action)

    return actions


def read_user_infos() -> User:
    inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
    return User(inv_0, inv_1, inv_2, inv_3, score)


def filter_brew_action(list_potions: List[Action], user_data: User) -> Optional[Action]:
    max_price = -1
    best_potion = None
    for potion in list_potions:
        if all(potion[n] >= -user_data[n] for n in range(4)):
            if potion.price > max_price:
                max_price = potion.price
                best_potion = potion
    return best_potion


def filter_castable(list_sorts: List[Action], user_data: User) -> Optional[Action]:
    action_ids = []
    for action in list_sorts:
        if all(action[n] >= -user_data[n] for n in range(4)):
            if action.is_castable:
                action_ids.append(action)
    if len(action_ids) > 0:
        return random.choice(action_ids)
    return None


def filter_cast_max(list_sorts: List[Action], list_potions: List[Action], user_data: User) -> Optional[Action]:
    """
    Maximise le nombre d'ingrédients à la fin
    """
    best_sort = None
    max_interet_sort = -1
    for sort in list_sorts:
        if not sort.is_castable:
            continue
        fin = [user_data[i] + sort[i] for i in range(4)]
        if (sum(fin) > 10) or (min(fin) < 0):
            continue

        interet_sort = sum(
            math.sqrt(max(0, fin[i] + potion[i]))   # sqrt to penalize too much ingredients
            for potion in list_potions
            for i in range(4)
        )
        if max_interet_sort < interet_sort:
            max_interet_sort = interet_sort
            best_sort = sort
    pprint(list_sorts)
    print(best_sort.action_id)
    print()
    return best_sort


def filter_cast_min(list_sorts: List[Action], list_potions: List[Action], user_data: User) -> Optional[Action]:
    """
    Minimise la distance avec la solution la plus proche
    return : quel sort il vaut mieux faire ?
    """
    best_sort = None
    best_interet_sort = 1e50   # interet d'un sort = interet pour la potion la plus facile à faire
    for sort in list_sorts:
        if not sort.is_castable:
            continue
        user_with_sort_done = [user_data[i] + sort[i] for i in range(4)]
        if (sum(user_with_sort_done) > 10) or (min(user_with_sort_done) < 0):
            continue

        for potion in list_potions:
            """combien il me manque d'ingredients pour faire la potion"""
            interet_sort = -sum(
                min(0, user_with_sort_done[i] - potion[i])
                for i in range(4)
            )
            if best_interet_sort > interet_sort:
                # cette potion a moins d'ingredients manquants
                best_interet_sort = interet_sort
                best_sort = sort

    return best_sort


def main():
    start = time()
    while True:
        actions = read_actions()

        me = read_user_infos()
        other = read_user_infos()

        brew_action = filter_brew_action(actions["BREW"], me)
        if brew_action is not None:
            print("BREW", brew_action.action_id, time() - start)
            continue

        print(me, file=sys.stderr)
        pprint(
            pd.DataFrame(actions["BREW"], columns=COLUMNS)[["delta_0", "delta_1", "delta_2", "delta_3", "price", "action_id"]],
            sys.stderr
        )

        cast_action = filter_cast_min(actions["CAST"], actions["BREW"], me)
        if cast_action is not None:
            print("CAST", cast_action.action_id, time() - start)
            continue

        print("REST")


main()
