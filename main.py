from Game import Game
from Agent import Agent

"""
This is the main script which runs the game with one player and one AI.

The human player starts.

Code used to run the game (excluding AI part) is taken from the following source:
https://github.com/simonmoesorensen/KalahaAI/tree/master


"""

# Function not changed from original
def print_game(game):
    state = game.get_state()
    slots = list(range(0, 6))

    # Access player fields and scores using the new keys
    player1_fields = state["p0_fields"]
    player2_fields = state["p1_fields"]
    player1_score = state["p0_score"]
    player2_score = state["p1_score"]

    player2_fields_display = player2_fields[::-1]  # Reverse for display

    print("Slots:   | ", end=""); print(*slots, sep=" | ", end=""); print(" |")
    print("=======================================")
    print("Player 2 | ", end="")
    print(*player2_fields_display, sep=" | ", end=""); print(" | Score: {0}".format(player2_score))
    print("---------------------------------------")
    print("Player 1 | ", end="")
    print(*player1_fields, sep=" | ", end=""); print(" | Score: {0}".format(player1_score))
    print("=======================================")


# Function not changed from original
def check_input(str):
    while 1:
        try:
            val = int(input(str))
            break
        except ValueError:
            print("Not a recognizable integer, please try again.")

    return val


if __name__ == "__main__":
    # Tree recursion limit
    print("Easy: 0")
    print("Medium: 1")
    print("Hard: 2")
    print("Very hard (and very slow): 3")
    rec_limit = 2 + check_input("Choose difficulty level: ") * 2

    ai_agent = Agent(algorithm = "minimax",
                     tree_depth = rec_limit)

    # Run game
    game = Game()
    should_end = game.is_terminal_state()

    print("Running game (anti-clockwise)")
    game_seq = []
    while not should_end:
        print_game(game)

        player_turn = game.get_player_turn()
        print("\nIt is player {0}'s turn".format(1 + player_turn))

        slot = None
        if player_turn == 0:
            # Player
            slot = check_input("Choose which slot to pick up (index at 0): ")
        else:
            # AI - This was written by us.
            print("AI computing best move:", end="")
            slot = ai_agent.get_best_move(game)
            print(f"AI moved stones from {5 - slot} slot")

        game_seq.append((player_turn, slot))
        # Reverse slot if player 2 is playing
        game.take_slot(slot)

        winner = 0
        if game.is_terminal_state():
            winner = game.end_game()
            should_end = True
            print_game(game)

    print("Game over, winner is Player {0}".format(winner))
    print("Game sequence:", game_seq)
    input("Press Enter to end...")
