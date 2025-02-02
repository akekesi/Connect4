"""
Unit tests for the Connect4 game.
This module tests the core functionality of the Connect4 game implementation,
including the board initialization, valid moves, game rules, and winner detection.

Run:
$ python -m tests.test_connect4_mcts
"""

import unittest
from src.connect4.connect4_mcts import Connect4


class TestConnect4(unittest.TestCase):
    """
    Unit tests for the Connect4 class.
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
        Test if the Connect4 board is correctly initialized to an empty state.
        """
        expected_board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertEqual(self.connect4.board, expected_board)

    def test_make_move(self):
        """
        Test the functionality of making a move on the board.
        Ensures moves are applied correctly for alternating players.
        """
        expected_board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        player = "X"
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                move = col
                self.connect4.make_move(move=move)
                expected_board[row][col] = player
                self.assertEqual(self.connect4.board, expected_board)
                player = "O" if player == "X" else "X"
                self.assertEqual(self.connect4.player, player)

    def test_get_valid_moves(self):
        """
        Test retrieving valid moves from the current board state.
        """
        valid_moves = self.connect4.get_valid_moves()
        expected_valid_moves = []
        for col in range(self.connect4.col):
            expected_valid_moves.append(col)
        self.assertEqual(valid_moves, expected_valid_moves)

        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                move = col
                self.connect4.make_move(move=move)
                expected_valid_moves = []
                for c in range(self.connect4.col):
                    row_ = row
                    if c <= col:
                        row_ = row - 1
                    if 0 <= row_:
                        expected_valid_moves.append(c)
                valid_moves = self.connect4.get_valid_moves()

                self.assertEqual(valid_moves, expected_valid_moves)

    def test_get_row(self):
        """
        Test retrieving the correct row index for a given column.
        """
        # Test empty column:
        for col in range(self.connect4.col):
            self.assertEqual(self.connect4.get_row(col=col), self.connect4.row - 1)

        # Test not empty column:
        player = "X"
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                move = col
                self.connect4.make_move(move=move)
                self.assertEqual(self.connect4.get_row(col=col), row - 1)
                player = "O" if player == "X" else "X"

    def test_is_valid_move(self):
        """
        Test the validity of a move on the board.
        """
        for col in range(self.connect4.col):
            self.assertTrue(self.connect4.is_valid_move(move=col))
        self.connect4.board = [["X" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        for col in range(-self.connect4.col, self.connect4.col + 3):
            self.assertFalse(self.connect4.is_valid_move(move=col))

    def test_is_winner(self):
        """
        Test the detection of a winning condition in the board.
        """
        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "O", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "O", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertTrue(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "X", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "O", "X", " ", " ", " "],
            [" ", "O", "X", "O", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "O", " ", " "],
            [" ", " ", " ", "O", "X", " ", " "],
            [" ", " ", "O", "X", "X", " ", " "],
            [" ", "O", "X", "O", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertTrue(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())

    def test_is_draw(self):
        """
        Test the detection of a draw condition in the board.
        """
        self.connect4.board = [["X" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertTrue(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertTrue(self.connect4.is_draw())

        self.connect4.board = [["O" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertTrue(self.connect4.is_winner(player="O"))
        self.assertTrue(self.connect4.is_draw())

    def test_is_game_over(self):
        """
        Test the detection of the game over condition in the board.
        """
        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "O", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())
        self.assertTrue(self.connect4.is_game_over())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "O", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertTrue(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())
        self.assertTrue(self.connect4.is_game_over())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "X", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "O", "X", " ", " ", " "],
            [" ", "O", "X", "O", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())
        self.assertTrue(self.connect4.is_game_over())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "O", " ", " "],
            [" ", " ", " ", "O", "X", " ", " "],
            [" ", " ", "O", "X", "X", " ", " "],
            [" ", "O", "X", "O", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertTrue(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())
        self.assertTrue(self.connect4.is_game_over())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "O", " ", " "],
            [" ", " ", " ", " ", "X", " ", " "],
            [" ", " ", "O", "X", "X", " ", " "],
            [" ", "O", "X", "O", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())
        self.assertFalse(self.connect4.is_game_over())

        self.connect4.board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertFalse(self.connect4.is_draw())
        self.assertFalse(self.connect4.is_game_over())

        self.connect4.board = [
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
        ]
        self.assertFalse(self.connect4.is_winner(player="X"))
        self.assertFalse(self.connect4.is_winner(player="O"))
        self.assertTrue(self.connect4.is_draw())
        self.assertTrue(self.connect4.is_game_over())

    def test_check_row(self):
        """
        Test the validity of row indices.
        """
        rows_invalid = [
            -3, -2, -1,
            self.connect4.row,
            self.connect4.row + 1,
            self.connect4.row + 2,
            self.connect4.row + 3,
        ]
        for row_invalid in rows_invalid:
            self.assertFalse(self.connect4.check_row(row=row_invalid))
        for row_valid in range(self.connect4.row):
            self.assertTrue(self.connect4.check_col(col=row_valid))

    def test_check_col(self):
        """
        Test the validity of column indices.
        """
        cols_invalid = [
            -3, -2, -1,
            self.connect4.col,
            self.connect4.col + 1,
            self.connect4.col + 2,
            self.connect4.col + 3,
        ]
        for col_invalid in cols_invalid:
            self.assertFalse(self.connect4.check_col(col=col_invalid))
        for col_valid in range(self.connect4.col):
            self.assertTrue(self.connect4.check_col(col=col_valid))


if __name__ == "__main__":
    unittest.main()
