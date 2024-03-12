# sources:
# https://www.youtube.com/watch?v=l-hh51ncgDI (excellent explanantion recursive approach to minimax)
#

from Game import Game
import copy
import random


class Agent:
    def __init__(self, algorithm, tree_depth, player_number=1):
        self.algorithm = algorithm
        self.tree_depth = tree_depth
        self.player_number = player_number  # AI agent by default is player 1, however we should be able to change this in order to test the AI agents against itself
        self.number_of_investigated_states = 0

    def get_best_move(self, game: Game) -> int:
        """
        Return the best move for the AI agent as the slot number (0-5).

        This function just calls the appropriate algorithm based on the input.
        Possible algorithms are:
        - minimax - just minimimax
        - alphabeta - minimax with alpha beta pruning, implemented as a separate function for the sake of the report
        - random - algorithm to return a random valid move
        - montecarlo TODO
        """
        if self.algorithm == "minimax":
            best_move, eval = self.minimax(game=game, depth=self.tree_depth)
            return best_move
        elif self.algorithm == "alphabeta":
            best_move, eval = self.minimax_alpha_beta(
                game=game, depth=self.tree_depth, alpha=float("-inf"), beta=float("inf")
            )
            return best_move
        elif self.algorithm == "random":
            return self.random_move(game)
        elif self.algorithm == "montecarlo":
            return self.monte_carlo(game)
        else:
            raise ValueError("Algorithm not supported")

    def minimax(self, game: Game, depth: int) -> list[int, float]:
        """
        Recursive implementation of minimax algorithm without alpha-beta pruning

        output:
        list[best_move (int), best_score (float)]
        """
        if depth == 0 or game.is_terminal_state():
            return [None, self.evaluation_function(game=game)]

        if game.get_state()["player_turn"] == self.player_number:
            # Maximie own turn
            maxEval = float("-inf")
            best_move = None
            child_dict = self.generate_children(game_copy=copy.deepcopy(game))
            for move, child in child_dict.items():
                _, eval = self.minimax(game=child, depth=depth - 1)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
            return [best_move, maxEval]
        else:
            # Minimize opponents turn
            minEval = float("inf")
            best_move = None
            child_dict = self.generate_children(game_copy=copy.deepcopy(game))
            for move, child in child_dict.items():
                _, eval = self.minimax(game=child, depth=depth - 1)
                if eval < minEval:
                    minEval = eval
                    best_move = move
            return [best_move, minEval]

    def minimax_alpha_beta(self, game: Game, depth: int, alpha: float, beta: float):
        """
        Recursive implementation of minimax algorithm with alpha beta pruning.

        Note: minimax_alpha_beta() and minimax() can be compined into one function,
              to minimize the amout of code, however to make it more explicit for
              the report sake we decided to make them as separate functions.
        """
        if depth == 0 or game.is_terminal_state():
            return [None, self.evaluation_function(game=game)]

        if game.get_state()["player_turn"] == self.player_number:
            # Maximie own turn
            maxEval = float("-inf")
            best_move = None
            child_dict = self.generate_children(game_copy=copy.deepcopy(game))
            for move, child in child_dict.items():
                _, eval = self.minimax_alpha_beta(game=child, depth=depth - 1, alpha=alpha, beta=beta)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return [best_move, maxEval]
        else:
            # Minimize opponents turn
            minEval = float("inf")
            best_move = None
            child_dict = self.generate_children(game_copy=copy.deepcopy(game))
            for move, child in child_dict.items():
                _, eval = self.minimax_alpha_beta(game=child, depth=depth - 1, alpha=alpha, beta=beta)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return [best_move, minEval]

    def monte_carlo(self, game: Game):
        pass

    def random_move(self, game: Game):
        """
        Function to return a random valid move.
        """
        valid_moves = []
        for move in range(6):
            if (
                game.get_state()["player_turn"] == 0
                and game.get_state()["p0_fields"][move] != 0
                or game.get_state()["player_turn"] == 1
                and game.get_state()["p1_fields"][move] != 0
            ):
                valid_moves.append(move)
        return valid_moves[random.randint(0, len(valid_moves) - 1)]

    def evaluation_function(self, game: Game) -> float:
        """
        Function to evaluate the game state.
        It returns a score for the game state

        This function supports evaluation when two AI agents play against each others.
        """
        if self.player_number == 0:
            eval = float(game.get_state()["p0_score"] - game.get_state()["p1_score"])
        else:
            eval = float(game.get_state()["p1_score"] - game.get_state()["p0_score"])
        return eval

    def generate_children(self, game_copy: Game) -> dict[int, int]:
        """
        Function to generate children for the game state
        Evaluate every possible move and append to the list if it is valid

        input:
        game: Game object

        output:
        dict: Dictionary, where key is the move and value is the game state
        """
        moves_dict = {}
        for move in range(6):
            if (
                game_copy.get_state()["player_turn"] == 0
                and game_copy.get_state()["p0_fields"][move] != 0
                or game_copy.get_state()["player_turn"] == 1
                and game_copy.get_state()["p1_fields"][move] != 0
            ):
                game_to_check = copy.deepcopy(
                    game_copy
                )  # Create a new instance of the game for every possible next move.
                game_to_check.take_slot(move)
                moves_dict[move] = game_to_check
                self.number_of_investigated_states += 1

        return moves_dict
