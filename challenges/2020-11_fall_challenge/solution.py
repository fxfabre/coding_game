#!/usr/bin/env python3

"""
Ligue bois 2
"""

import sys
import math
import pandas as pd


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def read_actions():
    action_count = int(input())  # the number of spells and recipes in play
    actions = []
    for i in range(action_count):
        # action_id: the unique ID of this spell or recipe
        # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
        # delta_0: tier-0 ingredient change
        # delta_1: tier-1 ingredient change
        # delta_2: tier-2 ingredient change
        # delta_3: tier-3 ingredient change
        # price: the price in rupees if this is a potion
        # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax
        # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell
        # castable: in the first league: always 0; later: 1 if this is a castable player spell
        # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        tome_index = int(tome_index)
        tax_count = int(tax_count)
        castable = castable != "0"
        repeatable = repeatable != "0"

        actions.append({
            "action_id" : int(action_id),
            "action_type": action_type,
            "delta_0": int(delta_0),
            "delta_1": int(delta_1),
            "delta_2": int(delta_2),
            "delta_3": int(delta_3),
            "price": int(price),
        })
    df_actions = pd.DataFrame(actions)
    df_actions["action_id"] = df_actions["action_id"].astype(int)
    df_actions["delta_0"] = df_actions["delta_0"].astype(int)
    df_actions["delta_1"] = df_actions["delta_1"].astype(int)
    df_actions["delta_2"] = df_actions["delta_2"].astype(int)
    df_actions["delta_3"] = df_actions["delta_3"].astype(int)
    df_actions["price"]   = df_actions["price"].astype(int)
    return df_actions


def read_user_infos():
    inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
    return inv_0, inv_1, inv_2, inv_3, score


# game loop
while True:
    df_actions = read_actions()

    me = read_user_infos()
    other = read_user_infos()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT
    query = " and ".join(f"delta_{n} >= -{me[n]}" for n in range(4))
    df_solution = df_actions.query(query).sort_values("price", ascending=False).head(1)

    if df_solution.shape[0] == 0:
        print("WAIT")
    else:
        print("BREW", df_solution["action_id"].iloc[0])
