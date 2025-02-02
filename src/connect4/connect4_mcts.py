"""
Connect4 Game Module

This module provides the implementation of the Connect4 game, including functionalities 
for initializing the game, making moves, checking for a winner.
"""

from src.utils.players import Players
from src.utils.check_end import check_winner, check_full


class Connect4:
    """
    Connect4 game logic and functionalities.

    Attributes:
        row (int): Number of rows in the board.
        col (int): Number of columns in the board.
        win (int): Number of consecutive tokens needed to win.
        board (list): 2D list representing the game board.
        player (str): The symbol of player, who makes a move next.
    
    Methods:
        init_board: Resets the game board to its initial state.
        display_board: Displays the current state of the board.
        make_move: Makes a move on the board by placing the player's token in the specified column.
        get_valid_moves: Gets all valid moves (empty cells) on the board.
        get_row: Finds the lowest available row in a column.
        is_valid_move: Checks if a move is valid.
        is_winner: Checks if the specified player has won the game.
        is_draw: Checks if the board is full.
        is_game_over: Checks if the game has ended due to a win or a draw.
        check_row: Checks if a row index is valid.
        check_col: Checks if a column index is valid.
    """

    def __init__(self) -> None:
        """
        Initializes the Connect4 game with a default 6x7 board and win condition of 4 tokens.
        """
        self.row = 6
        self.col = 7
        self.win = 4
        self.board = None
        self.player = Players.P1.value
        self.init_board()

    def init_board(self) -> None:
        """
        Resets the game board to its initial state (empty cells).
        """
        self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]

    def display_board(self, turn: int = 0) -> None:
        """
        Displays the current state of the board, including the turn number.

        Args:
            turn (int): The current turn number.

        Exaple:
        |=============|
        |             |
        |             |
        |    X X      |
        |    O X X    |
        |  O X O O    |
        |  O O X X    |
        |=============|
        |0 1 2 3 4 5 6|
        """
        n = self.col * 2 - 1
        line_horizontal = "=" * (n)
        line_numbers = [str(x) for x in range(self.col)]
        print("|" + line_horizontal + "|")
        for row in self.board:
            print("|" + " ".join(row) + "|")
        print("|" + line_horizontal + "|")
        print("|" + " ".join(line_numbers) + "|")
        print(f"|{f'{turn:03}':=^{n}}|")
        print()

    def make_move(self, move: int) -> None:
        """
        Makes a move on the board by placing the player's token in the specified column.

        Args:
            move (int): The column index to place the token in.
        """
        row = self.get_row(col=move)
        self.board[row][move] = self.player
        self.player = Players.P2.value if self.player == Players.P1.value else Players.P1.value

    def get_valid_moves(self) -> list[int]:
        """
        Gets all valid moves (empty cells) on the board.

        Returns:
            list[int]: List of valid moves.
        """
        valid_moves = []
        for col in range(self.col):
            row = self.get_row(col=col)
            if self.check_row(row=row):
                valid_moves.append(col)
        return valid_moves

    def get_row(self, col: int) -> int:
        """
        Finds the lowest available row in a column.

        Args:
            col (int): The column index.

        Returns:
            int: The row index of the lowest available cell, or -1 if the column is full.
        """
        row_free = -1
        for row in range(self.row):
            if self.board[row][col] == " ":
                row_free = row
            else:
                break
        return row_free

    def is_valid_move(self, move: int) -> bool:
        """
        Checks if a move is valid by verifying that at least one cell is empty in the column.
        """
        if not self.check_col(col=move):
            return False

        row = self.get_row(col=move)
        if not self.check_row(row=row):
            return False

        return self.board[row][move] == " "

    def is_winner(self, player: str) -> bool:
        """
        Checks if the specified player has won the game.

        Args:
            player (str): The symbol of the player to check.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        return check_winner(board=self.board, player=player, win=self.win)

    def is_draw(self) -> bool:
        """
        Checks if the board is full, meaning no empty cells remain.

        Returns:
            bool: True if all cells are filled, False if there are any empty cells.
        """
        return check_full(board=self.board)

    def is_game_over(self) -> bool:
        """
        Checks if the game has ended due to a win or a draw.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.is_winner(Players.P1.value) or \
               self.is_winner(Players.P2.value) or \
               self.is_draw()

    def check_row(self, row: int) -> bool:
        """
        Checks if a row index is valid.

        Args:
            row (int): The row index to check.

        Returns:
            bool: True if the row is valid, False otherwise.
        """
        return 0 <= row < self.row

    def check_col(self, col: int) -> bool:
        """
        Checks if a column index is valid.

        Args:
            col (int): The column index to check.

        Returns:
            bool: True if the column is valid, False otherwise.
        """
        return 0 <= col < self.col
