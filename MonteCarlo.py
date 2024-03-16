# from Agent import Agent
# from Game import Game
import copy
import math
import random


class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game_state.get_legal_moves()

    

    def UCB1(self, total_visits, c_param=1.41):
        if self.visits == 0:
            return float('inf')  # to ensure unvisited nodes are prioritized
        return self.wins / self.visits + c_param * (math.log(total_visits) / self.visits) ** 0.5

    def select_child(self):
        # Select a child node with highest UCB1 score
        return max(self.children, key=lambda child: child.UCB1(self.visits))

    def add_child(self, move, game_state):
        # Add a new child node for the given move
        child_node = MCTSNode(game_state=game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        # Update this node - increment visit count and add result to wins
        self.visits += 1
        self.wins += result
