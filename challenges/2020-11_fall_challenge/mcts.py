#!/usr/bin/env python3

from abc import ABCMeta
from time import time
import math
import random
from typing import List, Optional


def randomPolicy(state: "IState"):
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()


class IState(metaclass=ABCMeta):
    def getCurrentPlayer(self) -> int:
        raise NotImplementedError

    def getPossibleActions(self) -> List:
        raise NotImplementedError

    def takeAction(self, action) -> "IState":
        raise NotImplementedError

    def isTerminal(self) -> bool:
        raise NotImplementedError

    def getReward(self) -> float:
        raise NotImplementedError


class TreeNode:
    def __init__(self, state: IState, parent: Optional["TreeNode"]):
        self.state: IState = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}


class MCTreeSearch:
    def __init__(self, time_limit_ms=None, iteration_limit=None,
                 cste_exploration=1 / math.sqrt(2), policy=randomPolicy):

        self.cste_exploration = cste_exploration
        self.policy = policy
        self.root: Optional[TreeNode] = None
        if time_limit_ms is None:
            if iteration_limit is None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iteration_limit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iteration_limit
            self.limitType = 'iterations'
        else:
            if iteration_limit is not None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = time_limit_ms
            self.limitType = 'time'

    def search(self, initial_state: IState):
        self.root = TreeNode(initial_state, None)
        # print("Searching from node", initial_state.witch)

        if self.limitType == 'time':
            time_limit = time() + self.timeLimit / 1000
            while time() < time_limit:
                self.execute_round()
        else:
            for i in range(self.searchLimit):
                self.execute_round()

        best_child = self.getBestChild(self.root, 0)
        return self.getAction(self.root, best_child)

    def execute_round(self):
        # print("New training round")
        node = self.select_node(self.root)
        reward = self.policy(node.state)
        self.backpropogate(node, reward)

    def select_node(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.cste_exploration)
            else:
                return self.expand(node)
        return node

    def expand(self, node: TreeNode):
        # print("Expanding node from", node.state)
        actions = list(node.state.getPossibleActions())
        # print("Got actions", actions)
        for action in actions:
            # print(" Trying action", action)
            if action not in node.children:
                new_node = TreeNode(node.state.takeAction(action), node)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return new_node

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node: TreeNode, exploration_value: float):
        # print("Get best child from", node.state)
        best_value = float("-inf")
        best_nodes = []
        for child in node.children.values():
            node_value = node.state.getCurrentPlayer() * child.totalReward / child.numVisits
            node_value += exploration_value * math.sqrt(2 * math.log(node.numVisits) / child.numVisits)
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def getAction(self, root, best_child):
        for action, node in root.children.items():
            if node is best_child:
                return action
