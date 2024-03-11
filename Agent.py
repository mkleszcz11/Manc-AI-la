# sources:
# https://www.youtube.com/watch?v=l-hh51ncgDI (excellent explanantion recursive approach to minimax)
# 

from Game import Game
import copy

class Agent:
    def __init__(self, algorithm, tree_depth):
        self.algorithm = algorithm
        self.tree_depth = tree_depth

    def get_best_move(self, game: Game) -> int:
        '''
        return the best move for the AI agent as the slot number 0-5
        '''
        if self.algorithm == "minimax":
            best_move, eval = self.minimax(game = game, depth = self.tree_depth)
            return best_move
        elif self.algorithm == "alphabeta":
            return self.alpha_beta(game)
        elif self.algorithm == "montecarlo":
            return self.monte_carlo(game)
        else:
            raise ValueError("Algorithm not supported")
    
    def minimax(self, game: Game, depth: int) -> list[int, float]:
        '''
        Recursive implementation of minimax algorithm

        output:
        list[best_move (int), best_score (float)]
        '''
        if depth == 0 or game.is_terminal_state():
            # TODO add function to get all of the accumulated points
            # self.last_move(game)
            return [None, self.evaluation_function(game = game)]

        # print(f"##### depth: {depth} #####")
        # print(f"current state: {game.get_state()}")

        if game.get_state()["player_turn"] == 1:
            # AI agent turn -> maximize
            maxEval = float("-inf")
            best_move = None
            child_dict = self.generate_children(game_copy = copy.deepcopy(game))
            for move, child in child_dict.items():
                _, eval = self.minimax(game = child, depth = depth - 1)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
            return [best_move, maxEval]
        else:
            # Player turn -> minimize
            minEval = float("inf")
            best_move = None
            child_dict = self.generate_children(game_copy = copy.deepcopy(game))
            for move, child in child_dict.items():
                _, eval = self.minimax(game = child, depth = depth - 1)
                if eval < minEval:
                    minEval = eval
                    best_move = move
            return [best_move, minEval]

    def alpha_beta(self, game: Game):
        pass
    
    def monte_carlo(self, game: Game):
        pass
    
    def evaluation_function(self, game: Game) -> float:
        '''
        Function to evaluate the game state.
        It returns a score for the game state
        
        This is function for AI agent, which we are treating as player 1
        TODO -> take into accout finishing on the empty pocket
        '''
        eval = float(game.get_state()["p1_score"] - game.get_state()["p0_score"])
        return eval

    def generate_children(self, game_copy: Game) -> dict[int, int]:
        '''
        Function to generate children for the game state
        Evaluate every possible move and append to the list if it is valid
        
        input:
        game: Game object
        
        output:
        dict: Dictionary, where key is the move and value is the game state
        '''
        moves_dict = {}
        for move in range(6):
            # Create a new instance of the game for every move.
            game_to_check = copy.deepcopy(game_copy)
            # print("trying move: ", move)
            # if game_to_check.take_slot(move):
            #     moves_dict[move] = game_to_check 
            if game_copy.get_state()["player_turn"] == 0 and game_copy.get_state()["p0_fields"][move] != 0 or\
               game_copy.get_state()["player_turn"] == 1 and game_copy.get_state()["p1_fields"][move] != 0:
                #print(f"trying move: {move} for player {game_copy.get_state()['player_turn']}")
                game_to_check.take_slot(move)
                moves_dict[move] = game_to_check

        return moves_dict
