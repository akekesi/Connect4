"""
Unit tests for Connect4 Game Module.

This script contains unit tests for the Connect4 class, which tests the board initialization, 
disc placement, move validation, and other core functionalities of the game logic.

Tested functionalities include:
    - Initialization of the game board.
    - Placing a disc in a valid column.
    - Returning the correct row for a move.
    - Checking if columns and rows are valid.
    - Handling invalid moves, such as out-of-bounds columns or full columns.

The unittest framework is used for testing.
"""

import unittest
import numpy as np
from src.connect4 import Connect4


class TestConnect4(unittest.TestCase):
    """
    Test suite for the Connect4 game class.
    """

    def setUp(self) -> None:
        """
        This method is called before each test. It sets up the Connect4 instance.
        """
        self.connect4 = Connect4()

    def tearDown(self) -> None:
        """
        This method is called after each test. It cleans up the Connect4 instance.
        """
        del self.connect4

    def test_initial_board(self):
        """
        Test if the board is initialized correctly as an empty grid (filled with zeros).
        """
        expected_board = np.zeros((self.connect4.row, self.connect4.col))
        np.testing.assert_array_equal(self.connect4.board, expected_board)

    def test_set_disc(self):
        """
        Test if a disc is correctly placed on the board in the specified row and column.
        """
        expected_board = np.zeros((self.connect4.row, self.connect4.col))
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                disc = self.connect4.discs[(row + col) % 2]
                self.connect4.set_disc(disc=disc, row=row, col=col)
                expected_board[row, col] = disc
                np.testing.assert_array_equal(self.connect4.board, expected_board)

    def test_get_row(self):
        """
        Test if the correct lowest available row is returned for disc placement.
        """
        # Test empty column:
        for col in range(self.connect4.col):
            self.assertEqual(self.connect4.get_row(col=col), 5)

        # Test not empty column:
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                disc = self.connect4.discs[(row + col) % 2]
            self.connect4.set_disc(disc=disc, row=row, col=col)
            self.assertEqual(self.connect4.get_row(col=col), row - 1)

    def test_check_valid_col(self):
        """
        Test if a column index is valid (within the board's range).
        """
        invalid_cols = [
            -3, -2, -1,
            self.connect4.col,
            self.connect4.col + 1,
            self.connect4.col + 2,
            self.connect4.col + 3,
        ]
        for invalid_col in invalid_cols:
            self.assertEqual(
                self.connect4.check_valid_col(col=invalid_col),
                False
            )

    def test_check_valid_row(self):
        """
        Test if a row index is valid (within the board's range).
        """
        invalid_rows = [
            -3, -2, -1,
            self.connect4.row,
            self.connect4.row + 1,
            self.connect4.row + 2,
            self.connect4.row + 3,
        ]
        for invalid_row in invalid_rows:
            self.assertEqual(
                self.connect4.check_valid_row(row=invalid_row),
                False
            )

    def test_move_valid(self):
        """
        Test if discs are placed correctly in valid columns.
        """
        expected_board = np.zeros((self.connect4.row, self.connect4.col))
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                disc = self.connect4.discs[(row + col) % 2]
                expected_board[row, col] = disc
                result = self.connect4.move(disc=disc, col=col)
                np.testing.assert_array_equal(self.connect4.board, expected_board)
                self.assertEqual(result, True)

    def test_move_invalid(self):
        """
        Test handling of invalid moves, including out-of-bounds columns and full columns.
        """
        invalid_cols = [
            -3, -2, -1,
            self.connect4.col,
            self.connect4.col + 1,
            self.connect4.col + 2,
            self.connect4.col + 3,
        ]
        expected_board = np.zeros((self.connect4.row, self.connect4.col))

        # Test for invalid column:
        for invalid_col in invalid_cols:
            result = self.connect4.move(disc=1, col=invalid_col)
            np.testing.assert_array_equal(self.connect4.board, expected_board)
            self.assertEqual(result, False)

        # Test for invalid row (column is fully filled):
        expected_board = np.ones((self.connect4.row, self.connect4.col))
        self.connect4.board = np.ones((self.connect4.row, self.connect4.col))
        for col in range(self.connect4.col):
            result = self.connect4.move(disc=1, col=col)
            np.testing.assert_array_equal(self.connect4.board, expected_board)
            self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
