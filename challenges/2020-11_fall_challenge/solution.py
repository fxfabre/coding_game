#!/usr/bin/env python3

"""
Ligue bois 1,
Trop lent : 77 ms par loop
"""

import sys
import math
from collections import namedtuple
from itertools import count
import pandas as pd
from pprint import pprint
from typing import Dict, Tuple

User = namedtuple("User", ["inv_0", "inv_1", "inv_2", "inv_3", "score"])


def read_actions() -> Dict[str, pd.DataFrame]:
    action_count = int(input())
    actions = []
    for i in range(action_count):
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()

        actions.append((
            delta_0, delta_1, delta_2, delta_3, price,
            action_id, action_type,     # CAST, OPPONENT_CAST, LEARN, BREW
            tome_index,         # the index in the tome if this is a tome spell, equal to the read-ahead tax
            tax_count,          # the amount of taxed tier-0 ingredients you gain from learning this spell
            castable != "0",    # 1 if this is a castable player spell
            repeatable != "0",  # 1 if this is a repeatable player spell
        ))

    columns = [
        "delta_0", "delta_1", "delta_2", "delta_3", "price",
        "action_id", "action_type",
        "tome_index", "tax_count",
        "castable", "repeatable"
    ]
    df_actions = pd.DataFrame(actions, columns=columns)

    df_actions["delta_0"] = df_actions["delta_0"].astype(int)
    df_actions["delta_1"] = df_actions["delta_1"].astype(int)
    df_actions["delta_2"] = df_actions["delta_2"].astype(int)
    df_actions["delta_3"] = df_actions["delta_3"].astype(int)
    df_actions["price"]   = df_actions["price"].astype(int)

    df_actions["action_id"] = df_actions["action_id"].astype(int)
    df_actions["tome_index"] = df_actions["tome_index"].astype(int)
    df_actions["tax_count"] = df_actions["tax_count"].astype(int)
    df_actions["castable"] = df_actions["castable"].astype(bool)
    df_actions["repeatable"] = df_actions["repeatable"].astype(bool)

    return {action: df for action, df in df_actions.groupby("action_type")}


def read_user_infos():
    inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
    return (inv_0, inv_1, inv_2, inv_3, score)


def filter_possible_action(df: pd.DataFrame, user_data:Tuple) -> pd.DataFrame:
    query = " and ".join(f"delta_{n} >= -{user_data[n]}" for n in range(4))
    return df.query(query).sort_values("price", ascending=False).head(1)


def main():
    actions = read_actions()

    me = read_user_infos()
    other = read_user_infos()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    df_brew = filter_possible_action(actions["BREW"], me)
    if df_brew.shape[0] > 0:
        action_id = df_brew["action_id"].iloc[0]
        print("BREW", df_brew["action_id"].iloc[0])
        pprint((action_id, df_brew), sys.stderr)
        return

    df_casts = actions["CAST"]
    df_casts = filter_possible_action(df_casts[df_casts["castable"]], me)
    if df_casts.shape[0] > 0:
        action_id = df_casts["action_id"].sample().iloc[0]
        print("CAST", action_id)
        pprint((action_id, df_casts), sys.stderr)
        return

    print("REST")
    return

    df_opponent = actions["OPPONENT_CAST"]
    df_opponent = filter_possible_action(df_opponent[df_opponent["castable"]], me)
    if df_opponent.shape[0] > 0:
        action_id = df_opponent["action_id"].sample().iloc[0]
        print("CAST", action_id)
        pprint((action_id, df_opponent), sys.stderr)
        return

    print("WAIT")


while True:
    main()
