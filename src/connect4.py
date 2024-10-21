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

import os
import logging
import numpy as np

from src.logger_config import Logging
from src.check_finish import check_finish


# set logger up
logger = Logging().set_logger(
    name="Connect4",
    level=logging.DEBUG,
    path_dir=os.path.join(os.path.dirname(__file__), "..", "logs")
)


class Connect4:
    """A class to represent the Connect4 game board and logic."""

    def __init__(self) -> None:
        """
        Initializes the Connect4 board with 6 rows and 7 columns, 
        and sets the board to be empty (represented by zeros).
        Disc of player-1: (int) 1
        Disc of player-2: (int) 2
        """
        logger.debug("0")
        self.row = 6
        self.col = 7
        self.discs = [1, 2]
        self.board = np.zeros((self.row, self.col))
        logger.info("board is initialized")
        logger.debug("1")

    def set_disc(self, disc: int, row: int, col: int) -> None:
        """
        Places a disc on the board at the specified row and column.

        Args:
            disc (int): The player's disc (1 or 2).
            row (int): The row to place the disc in.
            col (int): The column to place the disc in.
        """
        logger.debug("0")
        self.board[row, col] = disc
        logger.info("disc is set")
        logger.debug("1")

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
        logger.debug("0")
        nonzero_list = np.nonzero(self.board[:, col])[0]
        if np.size(nonzero_list) == 0:
            row = self.row - 1
        else:
            row = int(nonzero_list[0]) - 1
        logger.info("%d", row)
        logger.debug("1")
        return row

    def check_valid_col(self, col: int) -> bool:
        """
        Checks if the given column index is valid (within board bounds).

        Args:
            col (int): The column index to check.

        Returns:
            bool: True if the column index is valid, False otherwise.
        """
        logger.debug("0")
        valid = (0 <= col < self.col)
        logger.info("%s", valid)
        logger.debug("1")
        return valid

    def check_valid_row(self, row: int) -> bool:
        """
        Checks if the given row index is valid (within board bounds).

        Args:
            row (int): The row index to check.

        Returns:
            bool: True if the row index is valid, False otherwise.
        """
        logger.debug("0")
        valid = (0 <= row < self.row)
        logger.info("%s", valid)
        logger.debug("1")
        return valid

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
        logger.debug("0")
        if not self.check_valid_col(col=col):
            logger.info("invalid col = %d", col)
            logger.debug("1")
            return False

        row = self.get_row(col=col)
        if not self.check_valid_row(row=row):
            logger.info("invalid row = %d", row)
            logger.debug("2")
            return False

        self.set_disc(disc=disc, row=row, col=col)
        logger.info("move is done")
        logger.debug("3")
        return True

    def game(self) -> None:
        # TODO: init board ???
        logger.debug("0")
        while True:
            disc = int(input("Enter your disc value: "))
            col = int(input("Enter column number: "))
            # TODO: check input
            move_info = self.move(disc=disc, col=col)
            if not move_info:
                logger.info("Invalid move.")
                continue
            print(connect4.board)
            if disc == check_finish(board=self.board, disc=disc):
                logger.info("Player-%d won.", disc)
                break
            if 0 == check_finish(board=self.board, disc=disc):
                logger.info("The board is full, resulting in a draw.")
                break
        logger.debug("1")


if __name__ == "__main__":
    connect4 = Connect4()

    connect4.move(disc=1, col=2)  # Player 1 places a disc in column 2
    connect4.move(disc=2, col=3)  # Player 2 places a disc in column 3
    connect4.move(disc=1, col=3)  # Player 1 places a disc in column 3

    print(connect4.board)

    connect4.game()
