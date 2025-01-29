"""
Two-Player Tic-Tac-Toe Game

This module provides a command-line Tic-Tac-Toe game for two players.
"""

from src.utils.players import Players


class TicTacToe:
    """
    A Tic-Tac-Toe game with two-player functionality.

    This class represents a Tic-Tac-Toe game board.
    The class offers move validation, win detection.

    Attributes:
    n (int): The size of the Tic-Tac-Toe board (3x3).
    board (list[list[int]]): A 2D list representing the Tic-Tac-Toe board, 
                             initially empty with each cell set to a space (" ").
    player (str): The symbol of player who makes a move next.
    """

    def __init__(self) -> None:
        """
        Initializes a new Tic-Tac-Toe game with a 3x3 board.
        """
        self.n = 3
        self.board = [[" " for _ in range(self.n)] for _ in range(self.n)]
        self.player = Players.P1.value

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
        self.board[move[0]][move[1]] = self.player
        self.player = Players.P2.value if self.player == Players.P1.value else Players.P1.value

    def undo_move(self, move: tuple[int, int]) -> None:
        """
        Removes a symbol from the specified position on the board, setting it to empty.

        Args:
            move (tuple[int, int]): The (row, col) position to be cleared.
        """
        self.board[move[0]][move[1]] = " "
        self.player = Players.P2.value if self.player == Players.P1.value else Players.P1.value

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
