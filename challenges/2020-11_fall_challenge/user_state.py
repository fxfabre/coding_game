#!/usr/bin/env python3

from copy import copy
from typing import Dict, Tuple, List, Optional, NamedTuple, Iterator, Iterable
from operator import itemgetter
from dataclasses import dataclass
from mcts import MCTreeSearch, IState
from itertools import count

MAX_DEEP = 6
DEBUG = True


def dataclass_wrapper(*a, **b):
    if DEBUG:
        b["frozen"] = True  # add a performance penalty
        return dataclass(*a, **b)
    else:
        return dataclass(*a, **b)


@dataclass_wrapper()
class Action:
    delta: Tuple[int, int, int, int] = (0, 0, 0, 0)
    price: int = 0

    action_id: int = 0      # CAST, OPPONENT_CAST, LEARN, BREW
    tome_index: int = 0     # the index in the tome if this is a tome spell, equal to the read-ahead tax
    tax_count: int = 0      # the amount of taxed tier-0 ingredients you gain from learning this spell
    is_castable: bool = True   # True if this is a castable player spell
    repeatable: int = 1     # 1 if this is a repeatable player spell

    def is_cast(self) -> bool:
        return False

    def is_brew(self) -> bool:
        return False

    def is_learn(self) -> bool:
        return False

    def do_it(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self) -> str:
        return str(list(self.delta) + [self.price])

    def update(self, **kwargs):
        return Action(**dict(self.__dict__, **kwargs))

    def update_all_actions(self, all_actions: Dict[str, List["Action"]]) -> Dict[str, List["Action"]]:
        raise NotImplementedError

    def __hash__(self):
        return hash(self.action_id)


class CastAction(Action):
    def is_cast(self):
        return True

    def do_it(self, *args, **kwargs):
        print("CAST", self.action_id, *args, **kwargs)

    def update_all_actions(self, all_actions: Dict[str, List["Action"]]) -> Dict[str, List["Action"]]:
        new_actions = copy(all_actions)
        new_actions["CAST"] = [
            action.update(is_castable=False) if action.action_id == self.action_id else action
            for action in new_actions["CAST"]
        ]
        return new_actions


class MultiCastAction(CastAction):
    def do_it(self, *args, **kwargs):
        print("BREW", self.action_id, self.repeatable, *args, **kwargs)


class BrewAction(Action):
    def is_brew(self):
        return True

    def do_it(self, *args, **kwargs):
        print("BREW", self.action_id, *args, **kwargs)

    def update_all_actions(self, all_actions: Dict[str, List["Action"]]) -> Dict[str, List["Action"]]:
        return copy(all_actions)


class LearnAction(Action):
    def do_it(self, *args, **kwargs):
        print("LEARN", self.action_id, *args, **kwargs)

    def update_all_actions(self, all_actions: Dict[str, List["Action"]]) -> Dict[str, List["Action"]]:
        new_actions = copy(all_actions)
        new_actions["LEARN"] = [
            action
            for action in new_actions["LEARN"]
            if action.action_id != self.action_id
        ]
        new_actions["CAST"] = new_actions["CAST"] + [CastAction(self.delta, 0, self.action_id)]
        return new_actions

    def is_learn(self) -> bool:
        return True


class RestAction(Action):
    def do_it(self, *args, **kwargs):
        print("REST", *args, **kwargs)

    def update_all_actions(self, all_actions: Dict[str, List["Action"]]) -> Dict[str, List["Action"]]:
        new_actions = copy(all_actions)
        new_actions["CAST"] = [
            action.update(is_castable=True) if not action.is_castable else action
            for action in new_actions["CAST"]
        ]
        return new_actions


class Witch(NamedTuple):
    inv: Tuple[int, int, int, int]
    score: int

    @classmethod
    def read_input(cls) -> "Witch":
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        return Witch((inv_0, inv_1, inv_2, inv_3), score)

    def find_best_action(self, all_actions: Dict[str, List[Action]], player_turn):
        return self.mcts_find_best_action(all_actions, player_turn)

    def heuristique_find_best_action(self, actions: Dict[str, List[Action]]) -> Optional[Action]:
        brew_action = self.find_best_brew(actions["BREW"])
        if brew_action is not None:
            return brew_action

        cast_action = self.find_best_cast(actions["CAST"], actions["BREW"])
        if cast_action is not None:
            return cast_action

        return RestAction()

    def find_best_brew(self, list_potions: List[Action]) -> Optional[Action]:
        """Renvoie la solution faisable qui rapporte le plus de rubis"""
        max_price = -1
        best_potion = None
        for witch, potion in self.apply_all_possible_actions(list_potions):
            if potion.price > max_price:
                max_price = potion.price
                best_potion = potion
        return best_potion

    def find_best_cast(self, list_sorts: List[Action], list_potions: List[Action]) -> Optional[Action]:
        """
        Minimise la distance avec la solution la plus proche
        return : le sort qui permet de minimiser le nombre d'ingrédients manquants pour une potion (quelconque)
        Mais aucune garantie que les nouveaux ingrédients facilitent la possibilité de faire une potion
        """
        interet_sorts = {}
        for witch, sort in self.apply_all_possible_actions(s for s in list_sorts if s.is_castable):
            interet_sorts[sort.action_id] = 0
            for potion in list_potions:
                """combien il me manque d'ingredients pour faire la potion ?"""
                distance_potion = -sum(
                    min(0, witch.inv[i] - potion.delta[i])
                    for i in range(4)
                )
                interet_sorts[sort.action_id] += distance_potion

        if len(interet_sorts) == 0:
            return None

        best_action_id = min(interet_sorts.items(), key=itemgetter(1))[0]
        return next(sort for sort in list_sorts if sort.action_id == best_action_id)

    def __add__(self, other: Action) -> "Witch":
        return Witch(tuple(self.inv[i] + other.delta[i] for i in range(4)), self.score + other.price)

    def apply_all_possible_actions(self, actions: Iterable[Action]) -> Iterator[Tuple["Witch", Action]]:
        for action in actions:
            if action.is_cast() and (not action.is_castable):
                continue

            new_witch = self + action
            if (sum(new_witch.inv) <= 10) and (min(new_witch.inv) >= 0):
                # print(self.inv, "can apply", action.action_id, new_witch.inv)
                yield new_witch, action

    def recursive_find_best_action(self, all_actions: Dict[str, List[Action]], deep=MAX_DEEP) -> Tuple[Action, int, int]:
        """
        Does not handle is_castable or not castable
        Bug because cast cannot be done twice -> Need to add action "Rest"
        + Update possible actions each time
        returns Best action to do now, score, target brew_id I would like to do
        """
        best_action = RestAction()

        if deep <= 0:
            return best_action, 0, 0

        best_score = 0
        target_brew_id = 0
        for action_type, actions in all_actions.items():
            if (deep == 1) and (action_type != "BREW"):
                continue

            # print(" " * (2 - deep) + action_type)
            for witch, action in self.apply_all_possible_actions(actions):
                # print(" " * (3 - deep) + "Eval", action, "->", witch.inv)
                if action_type == "BREW":
                    score = action.price
                    brew_id = action.action_id
                else:
                    sub_act, sub_score, brew_id = witch.recursive_find_best_action(all_actions, deep - 1)
                    score = action.price + sub_score

                if score >= best_score:
                    best_action = action
                    best_score = score
                    target_brew_id = brew_id if brew_id != 0 else target_brew_id
                    # print(" " * (3 - deep) + "Keep", action, "=>", witch.inv, best_score)

        return best_action, best_score, target_brew_id

    def mcts_find_best_action(self, all_actions: Dict[str, List[Action]], player_turn) -> Tuple[Action, int, int]:
        """
        Does not handle is_castable or not castable
        Bug because cast cannot be done twice -> Need to add action "Rest"
        + Update possible actions each time
        returns Best action to do now, score, target brew_id I would like to do
        """
        initial_state = WitchState(self, all_actions, None, player_turn, 0)
        mcts = MCTreeSearch(time_limit_ms=50)
        # mcts = MCTreeSearch(iteration_limit=10)
        best_action = mcts.search(initial_state)
        return best_action, 0, 0

    def can_do(self, action: Action, repeat=1):
        new_inventaire = tuple(self.inv[i] + repeat * action.delta[i] for i in range(4))
        return (sum(new_inventaire) <= 10) and (min(new_inventaire) >= 0)


@dataclass()
class WitchState(IState):
    witch: Witch
    all_actions: Dict[str, List[Action]]
    last_action: Optional[Action]
    player_turn: int = 0
    nb_actions: int = 0

    def getPossibleActions(self) -> List:
        if any(not action.is_castable for action in self.all_actions.get("CAST", [])):
            yield RestAction()
        for action in self.all_actions["BREW"]:
            if self.witch.can_do(action):
                yield action
        for action in self.all_actions["CAST"]:
            if action.is_castable:
                if self.witch.can_do(action):
                    yield action
                if action.repeatable:
                    n = 2
                    while self.witch.can_do(action, repeat=n):
                        n += 1
                        yield MultiCastAction(
                            tuple(n * action.delta[i] for i in range(4)), action.price, action.action_id,
                            action.tome_index, action.tax_count, action.is_castable, n
                        )

        if self.nb_actions <= 1:
            # Only the first action can be a learn in the MCTS simulation
            for action in self.all_actions["LEARN"]:
                if self.witch.can_do(action):
                    yield action

    def takeAction(self, action: Action) -> "IState":
        new_actions = action.update_all_actions(self.all_actions)
        return WitchState(self.witch + action, new_actions, action, self.player_turn + 1, self.nb_actions + 1)

    def isTerminal(self) -> bool:
        return self.player_turn > 0
        if self.last_action is None:
            return False
        if self.player_turn >= 100:
            return True
        if self.nb_actions > 7:
            return True
        return self.last_action.is_brew()

    def getReward(self) -> float:
        return self.witch.score

    def getCurrentPlayer(self) -> int:
        return 1

    def __str__(self):
        return str(self.witch.inv) + ", " + str(self.last_action)
