from src.mcts.mcts import MCTS, Node
from src.utils.players import Players
from src.connect4.connect4_mcts import Connect4


if __name__ == "__main__":
    connect4 = Connect4()
    mcts = MCTS(
        game_constructor=Connect4,
        player1=Players.P1.value,
        player2=Players.P2.value,
        iterations=1000,
    )

    while not connect4.is_game_over():
        connect4.display_board()
        if connect4.current_player == Players.P1.value:
            print("AI-X is thinking...")
            root = Node(connect4)
            board_best_move = mcts.search(root=root).state
            best_move = mcts.get_changed_position(
                list1=connect4.board,
                list2=board_best_move.board,
            )
            connect4.make_move(move=best_move[1])
        else:
            print("AI-O is thinking...")
            root = Node(connect4)
            board_best_move = mcts.search(root=root).state
            best_move = mcts.get_changed_position(
                list1=connect4.board,
                list2=board_best_move.board,
            )
            connect4.make_move(move=best_move[1])

    connect4.display_board()
    if connect4.is_winner(player=Players.P1.value):
        print(f"{Players.P1.value} win!")
    elif connect4.is_winner(player=Players.P2.value):
        print(f"{Players.P2.value} wins!")
    else:
        print("It's a draw!")
