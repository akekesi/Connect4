"""
Connect4 Game Module

This module provides an implementation of the Connect4 game. It allows players
to place discs into a grid, following the rules of the game. The module uses
NumPy to manage the board and contains functions to check valid moves, place discs,
and manage the game state.

Classes:
    Connect4: Represents the Connect4 game board and logic for making moves.

Example usage:
    connect4 = Connect4()
    connect4.move(1, 3)  # Player 1 places a disc in column 3
    connect4.move(2, 4)  # Player 2 places a disc in column 4
"""

import numpy as np


class Connect4:
    """A class to represent the Connect4 game board and logic."""

    def __init__(self) -> None:
        """
        Initializes the Connect4 board with 6 rows and 7 columns, 
        and sets the board to be empty (represented by zeros).
        Disc of player-1: (int) 1
        Disc of player-2: (int) 2
        """
        self.row = 6
        self.col = 7
        self.discs = [1, 2]
        self.board = np.zeros((self.row, self.col))

    def set_disc(self, disc: int, row: int, col: int) -> None:
        """
        Places a disc on the board at the specified row and column.

        Args:
            disc (int): The player's disc (1 or 2).
            row (int): The row to place the disc in.
            col (int): The column to place the disc in.
        """
        self.board[row, col] = disc

    def get_row(self, col: int) -> int:
        """
        Returns the lowest available row in the specified column 
        where a disc can be placed.

        Args:
            col (int): The column to check.

        Returns:
            int: The index of the lowest available row. If the column 
            is empty, returns the last row. If not, returns the row 
            just above the first occupied row.
        """
        row = np.nonzero(self.board[:, col])[0]
        if np.size(row) == 0:
            return self.row - 1
        return int(row[0]) - 1

    def check_valid_col(self, col: int) -> bool:
        """
        Checks if the given column index is valid (within board bounds).

        Args:
            col (int): The column index to check.

        Returns:
            bool: True if the column index is valid, False otherwise.
        """
        return 0 <= col < self.col

    def check_valid_row(self, row: int) -> bool:
        """
        Checks if the given row index is valid (within board bounds).

        Args:
            row (int): The row index to check.

        Returns:
            bool: True if the row index is valid, False otherwise.
        """
        return 0 <= row < self.row

    def move(self, disc: int, col: int) -> bool:
        """
        Makes a move by placing a disc in the specified column 
        if the column and row are valid.

        Args:
            disc (int): The player's disc (1 or 2).
            col (int): The column to place the disc in.

        Returns:
            bool: True if the move is valid and successful, False otherwise.
        """
        if not self.check_valid_col(col=col):
            print(f"invalid {col = }")
            return False

        row = self.get_row(col=col)
        if not self.check_valid_row(row=row):
            print(f"invalid {row = }")
            return False

        self.set_disc(disc=disc, row=row, col=col)
        return True


if __name__ == "__main__":
    connect4 = Connect4()

    connect4.move(disc=1, col=2)  # Player 1 places a disc in column 2
    connect4.move(disc=2, col=3)  # Player 2 places a disc in column 3
    connect4.move(disc=1, col=3)  # Player 1 places a disc in column 3

    print(connect4.board)
