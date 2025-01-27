"""
Two-Player Tic-Tac-Toe Game with MCTS Move Recommendations

This module provides a command-line Tic-Tac-Toe game for two players, with real-time
move recommendations based on the MCTS algorithm. Both players, receive
suggested moves for optimal gameplay, though they can choose their own moves as well.

Run:
$ python -m src.tictactoe.tictactoe
"""

from src.utils.players import Players
from src.mcts.mcts_tictactoe_test_00 import MCTS, Node


class TicTacToe:
    """
    A Tic-Tac-Toe game with two-player functionality and MCTS-based move recommendations.

    This class represents a Tic-Tac-Toe game board and includes methods for playing the game
    interactively between two players. The class offers move validation, win detection,
    and real-time optimal move suggestions using the MCTS algorithm.

    Attributes:
    n (int): The size of the Tic-Tac-Toe board (3x3).
    board (list[list[int]]): A 2D list representing the Tic-Tac-Toe board, 
                             initially empty with each cell set to a space (" ").
    """

    def __init__(self) -> None:
        """
        Initializes a new Tic-Tac-Toe game with a 3x3 board.
        """
        self.n = 3
        self.board = [[" " for _ in range(self.n)] for _ in range(self.n)]
        self.current_player = Players.P1.value

    def display_board(self) -> None:
        """
        Prints the current state of the board with lines separating cells.
        """
        line_horizontal = " ---" * self.n + " "
        print(line_horizontal)
        for row in self.board:
            print("| " + " | ".join(row) + " |")
            print(line_horizontal)

    def is_valid_move(self, move: tuple[int, int]) -> bool:
        """
        Checks if the move is valid (within bounds and cell is empty).

        Args:
            move (tuple[int, int]): The (row, col) position to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= move[0] < self.n and \
               0 <= move[1] < self.n and \
               self.board[move[0]][move[1]] == " "

    def make_move(self, move: tuple[int, int]) -> None:
        """
        Places the player's symbol at the specified position on the board.

        Args:
            move (tuple[int, int]): The (row, col) position on the board.
        """
        self.board[move[0]][move[1]] = self.current_player
        self.current_player = Players.P2.value if self.current_player == Players.P1.value else Players.P1.value

    def undo_move(self, move: tuple[int, int]) -> None:
        """
        Removes a symbol from the specified position on the board, setting it to empty.

        Args:
            move (tuple[int, int]): The (row, col) position to be cleared.
        """
        self.board[move[0]][move[1]] = " "
        self.current_player = Players.P2.value if self.current_player == Players.P1.value else Players.P1.value

    def is_winner(self, player: str) -> bool:
        """
        Checks if the specified player has won the game.

        Args:
            player (str): The symbol of the player to check.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        for i in range(self.n):
            if all(self.board[i][j] == player for j in range(self.n)) or \
               all(self.board[j][i] == player for j in range(self.n)):
                return True
        return all(self.board[i][i] == player for i in range(self.n)) or \
               all(self.board[i][self.n - 1 - i] == player for i in range(self.n))

    def is_draw(self) -> bool:
        """
        Checks if the board is full, meaning no empty cells remain.

        Returns:
            bool: True if all cells are filled, False if there are any empty cells.
        """
        return not any(cell == " " for row in self.board for cell in row)

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """
        Gets all valid moves on the board (empty cells).

        Returns:
            list[tuple[int, int]]: List of coordinates for all empty cells.
        """
        return [(x, y) for x in range(self.n) for y in range(self.n) if self.board[x][y] == " "]

    def is_game_over(self) -> bool:
        """
        Checks if the game has ended due to a win or a draw.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.is_winner(Players.P1.value) or self.is_winner(Players.P2.value) or self.is_draw()

if __name__ == "__main__":
    game = TicTacToe()
    mcts = MCTS(game_constructor=TicTacToe, iterations=1000)

    # initial state
    # game.board = [
    #     [" ", "X", "X",],
    #     ["O", "O", " ",],
    #     [" ", " ", " ",],
    # ]
    # game.board = [
    #     ["X", " ", "X",],
    #     [" ", " ", " ",],
    #     ["O", "O", " ",],
    # ]

    while not game.is_game_over():
        game.display_board()
        if game.current_player == Players.P1.value: # User will start the game
        # if game.current_player == Players.P2.value: # AI will start the game
            input_ = input("Enter move (row, col): ")
            x, y = map(int, input_.split())
            move = (x, y)
            while not game.is_valid_move(move=move):
                move = int(input("Invalid move. Try again."))
            game.make_move(move=move)
        else:
            print("AI is thinking...")
            root = Node(game)
            board_best_move = mcts.search(root=root).state
            list1 = game.board
            list2 = board_best_move.board
            best_move_y = [index for index, (element1, element2) in enumerate(zip(list1, list2)) if element1 != element2][0]
            best_move_x = [index for index, (element1, element2) in enumerate(zip(list1[best_move_y], list2[best_move_y])) if element1 != element2][0]
            game.make_move(move=(best_move_y, best_move_x))

    game.display_board()
    if game.is_winner(player=Players.P1.value):
        print(f"{Players.P1.value} win!")
    elif game.is_winner(player=Players.P2.value):
        print(f"{Players.P2.value} wins!")
    else:
        print("It's a draw!")
