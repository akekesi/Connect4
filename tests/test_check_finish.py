"""
Unit tests for the Connect4 game to check 
if the game correctly identifies win, draw, or ongoing game states.
"""

import unittest
import numpy as np

from src.check_finish import check_finish


class TestCheckFinish(unittest.TestCase):
    """
    Test suite for the check_finish function in the Connect4 game.
    """
    row = 6
    col = 7
    win = 4
    disc = 1

    def setUp(self) -> None:
        """
        This method is called before each test.
        Set up a blank Connect4 board before each test case.
        """
        self.board = np.zeros((self.row, self.col))

    def tearDown(self) -> None:
        """
        This method is called after each test.
        Clean up the board instance after each test case.
        """
        del self.board

    def test_empty(self):
        """
        Test that an empty board returns -1, indicating the game is ongoing with no winner.
        """
        self.assertEqual(check_finish(board=self.board, disc=self.disc, win=self.win), -1)

    def test_horizontal_only(self):
        """
        Test horizontal win conditions 
        by placing four consecutive discs of the same type across each row.
        """
        self.assertEqual(check_finish(board=self.board, disc=self.disc, win=self.win), -1)

        for row in range(self.row):
            self.board[row, :] = [self.disc, self.disc, self.disc, self.disc, 0, 0, 0]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

            self.board[row, :] = [0, self.disc, self.disc, self.disc, self.disc, 0, 0]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

            self.board[row, :] = [0, 0, self.disc, self.disc, self.disc, self.disc, 0]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

            self.board[row, :] = [0, 0, 0, self.disc, self.disc, self.disc, self.disc]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

    def test_vertical_only(self):
        """
        Test vertical win conditions 
        by placing four consecutive discs of the same type down each column.
        """
        self.assertEqual(check_finish(board=self.board, disc=self.disc, win=self.win), -self.disc)

        for col in range(self.col):
            self.board[:, col] = [self.disc, self.disc, self.disc, self.disc, 0, 0]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

            self.board[:, col] = [0, self.disc, self.disc, self.disc, self.disc, 0]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

            self.board[:, col] = [0, self.disc, self.disc, self.disc, self.disc, 0]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

            self.board[:, col] = [0, 0, self.disc, self.disc, self.disc, self.disc]
            self.assertEqual(
                first=check_finish(board=self.board, disc=self.disc, win=self.win),
                second=self.disc
            )

    def test_diagonal_pos_only(self):
        """
        Test positive-slope diagonal win conditions 
        by placing four consecutive discs in positive diagonals.
        """
        rows = np.arange(self.row)
        cols = np.arange(self.col)
        row_steps = self.row - self.win + 1
        col_steps = self.col - self.win + 1

        for row_step in range(row_steps):
            for col_step in range(col_steps):
                self.board = np.zeros((self.row, self.col))
                self.board[rows[0+row_step:4+row_step], cols[0+col_step:4+col_step]] = self.disc
                self.assertEqual(
                    first=check_finish(board=self.board, disc=self.disc, win=self.win),
                    second=self.disc
                )

    def test_diagonal_neg_only(self):
        """
        Test negative-slope diagonal win conditions 
        by placing four consecutive discs in negative diagonals.
        """
        rows = np.arange(self.row)
        cols = np.arange(-1, -self.col - 1, -1)
        row_steps = self.row - self.win + 1
        col_steps = self.col - self.win + 1

        for row_step in range(row_steps):
            for col_step in range(col_steps):
                self.board = np.zeros((self.row, self.col))
                self.board[rows[0+row_step:4+row_step], cols[0+col_step:4+col_step]] = self.disc
                self.assertEqual(
                    first=check_finish(board=self.board, disc=self.disc, win=self.win),
                    second=self.disc
                )

    def test_full(self):
        """
        Test a full board scenario where no more moves are possible, 
        checking for a draw or invalid outcome.
        """
        self.board = np.ones((self.row, self.col))
        self.assertEqual(check_finish(board=self.board, disc=self.disc, win=self.win), self.disc)

        self.board *= 2
        self.assertEqual(check_finish(board=self.board, disc=self.disc, win=self.win), 0)

        self.board = np.array([
            [1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2, 1],
        ])
        self.assertEqual(check_finish(board=self.board, disc=self.disc, win=self.win), 0)


if __name__ == "__main__":
    unittest.main()
