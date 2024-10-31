"""
"""

import unittest

from src.check_end import check_winner, check_full


class TestCheckEnd(unittest.TestCase):
    """
    """
    row = 6
    col = 7
    win = 4
    player = "X"

    def setUp(self) -> None:
        """
        This method is called before each test.
        Set up a blank Connect4 board before each test case.
        """
        self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]

    def tearDown(self) -> None:
        """
        This method is called after each test.
        Clean up the board instance after each test case.
        """
        del self.board

    def test_empty(self):
        """
        """
        player = "X"
        self.assertFalse(check_winner(board=self.board, player=player, win=self.win))
        player = "O"
        self.assertFalse(check_winner(board=self.board, player=player, win=self.win))
        self.assertFalse(check_full(board=self.board))

    def test_horizontal_only(self):
        """
        """
        self.assertFalse(check_winner(board=self.board, player=self.player, win=self.win))

        for row in range(self.row):
            self.board[row][:] = [self.player, self.player, self.player, self.player, " ", " ", " "]
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            self.board[row][:] = [" ", self.player, self.player, self.player, self.player, " ", " "]
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            self.board[row][:] = [" ", " ", self.player, self.player, self.player, self.player, " "]
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            self.board[row][:] = [" ", " ", " ", self.player, self.player, self.player, self.player]
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            self.board[row][:] = [" ", " ", " ", " ", " ", " ", " "]

    def test_vertical_only(self):
        """
        """
        self.assertFalse(check_winner(board=self.board, player=self.player, win=self.win))

        for col in range(self.col):
            values = [self.player, self.player, self.player, self.player, " ", " "]
            for row, value in enumerate(values):
                self.board[row][col] = value
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            values = [" ", self.player, self.player, self.player, self.player, " "]
            for row, value in enumerate(values):
                self.board[row][col] = value
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            values = [" ", self.player, self.player, self.player, self.player, " "]
            for row, value in enumerate(values):
                self.board[row][col] = value
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            values = [" ", " ", self.player, self.player, self.player, self.player]
            for row, value in enumerate(values):
                self.board[row][col] = value
            self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

            values = [" ", " ", " ", " ", " ", " "]
            for row, value in enumerate(values):
                self.board[row][col] = value

    def test_diagonal_pos_only(self):
        """
        """
        row_steps = self.row - self.win + 1
        col_steps = self.col - self.win + 1

        for row_step in range(row_steps):
            for col_step in range(col_steps):
                self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]
                for n in range(self.win):
                    self.board[n + row_step][n + col_step] = self.player
                self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

    def test_diagonal_neg_only(self):
        """
        """
        row_steps = self.row - self.win + 1
        col_steps = self.col - self.win + 1

        for row_step in range(row_steps):
            for col_step in range(col_steps):
                self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]
                for n in range(self.win):
                    self.board[n + row_step][-1 - n - col_step] = self.player
                self.assertTrue(check_winner(board=self.board, player=self.player, win=self.win))

    def test_full(self):
        """
        """
        player = "X"
        self.board = [[player for _ in range(self.col)] for _ in range(self.row)]
        self.assertTrue(check_winner(board=self.board, player=player, win=self.win))
        self.assertTrue(check_full(board=self.board))

        player = "O"
        self.board = [[player for _ in range(self.col)] for _ in range(self.row)]
        self.assertTrue(check_winner(board=self.board, player=player, win=self.win))
        self.assertTrue(check_full(board=self.board))

        self.board = [
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
        ]
        self.assertTrue(check_full(board=self.board))
        for row in range(self.row):
            for col in range(self.col):
                player = self.board[row][col]
                self.board[row][col] = " "
                self.assertFalse(check_full(board=self.board))
                self.board[row][col] = player


if __name__ == "__main__":
    unittest.main()
