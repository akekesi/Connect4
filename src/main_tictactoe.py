from src.mcts.mcts import MCTS, Node
from src.utils.players import Players
from src.tictactoe.tictactoe_mcts import TicTacToe


if __name__ == "__main__":
    game = TicTacToe()
    mcts = MCTS(
        game_constructor=TicTacToe,
        player_1=Players.P1.value,
        player_2=Players.P2.value,
        iterations=1000
    )

    answer = input("Do you want to start the game? (y/n): ")
    if answer.lower() == "y":
        game.player = Players.P1.value
    else:
        game.player = Players.P2.value
    while not game.is_game_over():
        game.display_board()
        if game.player == Players.P1.value:
            move = tuple(map(int, input("Enter move (row, col): ").split()))
            while not game.is_valid_move(move=move):
                move = int(input("Invalid move. Try again."))
            game.make_move(move=move)
        else:
            print("AI is thinking...")
            root = Node(game)
            board_best_move = mcts.search(root=root).state
            best_move = mcts.get_changed_position(
                list1=game.board,
                list2=board_best_move.board,
            )
            game.make_move(move=best_move)

    game.display_board()
    if game.is_winner(player=Players.P1.value):
        print(f"{Players.P1.value} win!")
    elif game.is_winner(player=Players.P2.value):
        print(f"{Players.P2.value} wins!")
    else:
        print("It's a draw!")
