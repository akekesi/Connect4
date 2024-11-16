"""
Unit tests for the check_end module, which verifies the game logic
for checking a Connect4 winner and detecting a full board.

Run:
$ python -m tests.test_check_end
"""

import unittest

from src.utils.check_end import check_winner, check_full


class TestCheckEnd(unittest.TestCase):
    """
    Unit tests for the check_end module.
    The tests cover scenarios such as empty board, horizontal, vertical, diagonal wins, full board, 
    and random board states.
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
        Test case for an empty board.
        Verifies that no player wins and the board is not full on an empty board.
        """
        player = "X"
        self.assertFalse(check_winner(board=self.board, player=player, win=self.win))
        player = "O"
        self.assertFalse(check_winner(board=self.board, player=player, win=self.win))
        self.assertFalse(check_full(board=self.board))

    def test_horizontal_only(self):
        """
        Test case for horizontal win detection.
        Simulates horizontal wins for a given player in each row.
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
        Test case for vertical win detection.
        Simulates vertical wins for a given player in each column.
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
        Test case for positive diagonal win detection.
        Simulates positive diagonal wins for a given player.
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
        Test case for negative diagonal win detection.
        Simulates negative diagonal wins for a given player.
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
        Test case for a full board.
        Verifies that the board is correctly marked as full when there are no empty spaces.
        Also checks that the winner is identified correctly on a full board.
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

    def test_random_states(self):
        """
        Test case for various random board states.
        Verifies that the functions check_winner and check_full behave correctly 
        in different game states including both players potentially winning.
        """
        win = 3
        self.board = [
            [" ", " ", " ", " ",],
            [" ", " ", "O", " ",],
            [" ", "O", "X", " ",],
            ["O", "X", "X", "X",],
        ]
        self.assertTrue(check_winner(board=self.board, player="X", win=win))
        self.assertTrue(check_winner(board=self.board, player="O", win=win))
        self.assertFalse(check_full(board=self.board))

        self.board = [
            [" ", " ", " ", " ",],
            ["O", " ", "O", " ",],
            ["X", " ", "X", " ",],
            ["O", "X", "X", "X",],
        ]
        self.assertTrue(check_winner(board=self.board, player="X", win=win))
        self.assertFalse(check_winner(board=self.board, player="O", win=win))
        self.assertFalse(check_full(board=self.board))

        self.board = [
            [" ", " ", " ", " ",],
            [" ", " ", " ", " ",],
            [" ", "O", " ", " ",],
            ["O", "X", "X", "X",],
        ]
        self.assertTrue(check_winner(board=self.board, player="X", win=win))
        self.assertFalse(check_winner(board=self.board, player="O", win=win))
        self.assertFalse(check_full(board=self.board))

        self.board = [
            [" ", " ", " ", " ",],
            [" ", " ", " ", " ",],
            ["O", " ", " ", " ",],
            ["O", "X", "X", "X",],
        ]
        self.assertTrue(check_winner(board=self.board, player="X", win=win))
        self.assertFalse(check_winner(board=self.board, player="O", win=win))
        self.assertFalse(check_full(board=self.board))


if __name__ == "__main__":
    unittest.main()
