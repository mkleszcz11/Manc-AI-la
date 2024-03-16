# This file contains the game logic for the game Kalaha
# It is based on the following source:
# https://github.com/simonmoesorensen/KalahaAI/tree/master
# However, it has been modified to for the different state description.


import copy


class Game:
    def __init__(self):
        self.state = {"p0_fields": [4] * 6, "p1_fields": [4] * 6, "p0_score": 0, "p1_score": 0, "player_turn": 0}

    def get_state(self):
        return copy.deepcopy(self.state)

    def get_player_turn(self):
        return self.state["player_turn"]

    def take_slot(self, pocket):
        """
        Function to take a slot from the game board
        It updates the game state based on the move
        If move is not valid, it returns False
        """
        if pocket > 5 or pocket < 0:
            print("Invalid pocket")
            return False

        player = "p0" if self.state["player_turn"] == 0 else "p1"
        opponent = "p1" if player == "p0" else "p0"

        if self.state[f"{player}_fields"][pocket] == 0:
            print("No pieces in pocket")
            return False

        pocket_pieces = self.state[f"{player}_fields"][pocket]
        self.state[f"{player}_fields"][pocket] = 0

        current_pocket = pocket
        player_changed = False

        while pocket_pieces > 0:
            current_pocket += 1
            if current_pocket == 6:  # When reaching the player's score slot
                if (
                    player == "p0"
                    and self.state["player_turn"] == 0
                    or player == "p1"
                    and self.state["player_turn"] == 1
                ):
                    self.state[f"{player}_score"] += 1
                    pocket_pieces -= 1
                    if pocket_pieces == 0:  # End in own store
                        return True
                current_pocket = 0
                player, opponent = opponent, player  # Switch sides
                player_changed = not player_changed
                continue

            self.state[f"{player}_fields"][current_pocket] += 1
            pocket_pieces -= 1

        # Check if last piece ends in own empty pocket - possible capture
        if (
            self.state[f"{player}_fields"][current_pocket] == 1
            and not player_changed
            and self.state[f"{opponent}_fields"][5 - current_pocket] > 0
        ):
            self.capture(current_pocket, player, opponent)

        # Switch player turn if last piece did not end in own store
        if current_pocket != 0:
            self.state["player_turn"] = 1 - self.state["player_turn"]

        return True

    def capture(self, pocket, player, opponent):
        opposite_pocket = 5 - pocket
        captured_pieces = self.state[f"{player}_fields"][pocket] + self.state[f"{opponent}_fields"][opposite_pocket]
        self.state[f"{player}_fields"][pocket] = 0
        self.state[f"{opponent}_fields"][opposite_pocket] = 0
        self.state[f"{player}_score"] += captured_pieces

    def is_terminal_state(self):
        if sum(self.state["p0_fields"]) == 0 or sum(self.state["p1_fields"]) == 0:
            return True
        return False

    def end_game(self):
        self.state["p0_score"] += sum(self.state["p0_fields"])
        self.state["p1_score"] += sum(self.state["p1_fields"])
        self.state["p0_fields"] = [0] * 6
        self.state["p1_fields"] = [0] * 6

        if self.state["p0_score"] > self.state["p1_score"]:
            winner = 0
        elif self.state["p1_score"] > self.state["p0_score"]:
            winner = 1
        else:
            winner = -1  # Draw
        return winner
    def get_legal_moves(self):
        legal_moves = []
        current_player_pits = self.state['p0_fields'] if self.state['player_turn'] == 0 else self.state['p1_fields']
        for i, seeds in enumerate(current_player_pits):
            if seeds > 0:  # A move is legal if the pit contains one or more seeds
                legal_moves.append(i)
        return legal_moves

