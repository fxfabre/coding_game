#!/usr/bin/env python3

"""
Ligue bois 1,
Si on peut produire une solution : on le fait
Sinon on lance un sort qui permet de diminuer le nombre d'ingredients d'écart avec
le sort le plus facile à lancer (qui requiert le moins d'ingredients supplémentaire)
"""

from time import time
from itertools import count
from copy import copy
from typing import Dict, Tuple, List, Optional, NamedTuple, Iterator, Iterable
from operator import itemgetter
from dataclasses import dataclass

from mcts import MCTreeSearch, IState
from user_state import Action, Witch, BrewAction, CastAction, LearnAction

BUILDERS = {
    "BREW": BrewAction,
    "CAST": CastAction,
    "OPPONENT_CAST": Action,
    "LEARN": LearnAction
}


def read_actions() -> Dict[str, List[Action]]:
    action_count = int(input())
    actions = {
        "CAST": [],
        # "OPPONENT_CAST": [],
        "LEARN": [],
        "BREW": []
    }
    for i in range(action_count):
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        if action_type in actions.keys():
            action = BUILDERS[action_type](
                (int(delta_0), int(delta_1), int(delta_2), int(delta_3)), int(price), int(action_id),
                int(tome_index), int(tax_count), castable != "0", int(repeatable != "0"),
            )
            actions[action_type].append(action)

    # pprint(
    #     pd.DataFrame(
    #         (a + (key, )
    #          for key, acts in actions.items()
    #          for a in acts), columns=[
    #         "delta_0", "delta_1", "delta_2", "delta_3", "price", "action_id",
    #         "tome_index", "tax_count", "castable", "repeatable", "type"
    #     ])[["delta_0", "delta_1", "delta_2", "delta_3", "price", "action_id", "type"]],
    #     sys.stderr
    # )
    return actions


def main():
    for i in count(0):
        start = time()
        all_actions = read_actions()

        me = Witch.read_input()
        other = Witch.read_input()

        best_action, score, brew_id = me.mcts_find_best_action(all_actions, 0)
        if best_action:
            best_action.do_it(round(time() - start, 2), brew_id)
        else:
            print("REST", time() - start)


if __name__ == '__main__':
    main()
