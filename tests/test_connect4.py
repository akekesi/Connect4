"""
Unit tests for the Connect4 game.
This module tests the core functionality of the Connect4 game implementation,
including the board initialization, valid moves, game rules, and winner detection.

Run:
$ python -m tests.test_connect4
"""

import unittest
from unittest.mock import patch
from src.connect4.connect4 import Connect4


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

    def test_move(self):
        """
        Test the functionality of making a move on the board.
        Ensures moves are applied correctly for alternating players.
        """
        expected_board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        player = "X"
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                move = (row, col)
                self.connect4.move(move=move, player=player)
                expected_board[row][col] = player
                self.assertEqual(self.connect4.board, expected_board)
                player = "O" if player == "X" else "X"

    def test_remove(self):
        """
        Test removing a move from the board.
        Ensures that the board reverts to the state before the move was made.
        """
        expected_board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        player = "X"
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                move = (row, col)
                self.connect4.move(move=move, player=player)
                expected_board[row][col] = player
                self.assertEqual(self.connect4.board, expected_board)
                self.connect4.remove(move=move)
                expected_board[row][col] = " "
                self.assertEqual(self.connect4.board, expected_board)
                player = "O" if player == "X" else "X"

    def test_get_valid_moves(self):
        """
        Test retrieving valid moves from the current board state.
        """
        valid_moves = self.connect4.get_valid_moves()
        expected_valid_moves = []
        for col in range(self.connect4.col):
            row = self.connect4.row - 1
            expected_valid_moves.append((row, col))
        self.assertEqual(valid_moves, expected_valid_moves)

        player = "X"
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                move = (row, col)
                self.connect4.move(move=move, player=player)
                expected_valid_moves = []
                for c in range(self.connect4.col):
                    row_ = row
                    if c <= col:
                        row_ = row - 1
                    if 0 <= row_:
                        expected_valid_moves.append((row_, c))
                valid_moves = self.connect4.get_valid_moves()

                self.assertEqual(valid_moves, expected_valid_moves)

    def test_check_input(self):
        """
        Test the validation of player input for move columns.
        """
        inputs_invalid = [
            "",
            " ",
            "one",
            "X",
            "x",
            "O",
            "o",
            str(-1.),
            str(-1.0),
            str(-1.1),
            str(-1.23),
            str(0.),
            str(0.0),
            str(0.1),
            str(1.23),
        ]
        for input_ in inputs_invalid:
            self.assertFalse(self.connect4.check_input(input_=input_))

        inputs_valid = [
            str(-1),
            str(-11),
            str(0),
            str(self.connect4.col),
            str(self.connect4.col + 1),
        ]
        for input_ in inputs_valid:
            self.assertTrue(self.connect4.check_input(input_=input_))

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
                move = (row, col)
                self.connect4.move(move=move, player=player)
                self.assertEqual(self.connect4.get_row(col=col), row - 1)
                player = "O" if player == "X" else "X"

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

    def test_make_move_valid(self):
        """
        Test making valid moves on the board.
        """
        expected_board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        player = "X"
        for row in range(self.connect4.row - 1, -1, -1):
            for col in range(self.connect4.col):
                expected_board[row][col] = player
                result = self.connect4.make_move(player=player, col=col)
                self.assertEqual(self.connect4.board, expected_board)
                self.assertEqual(result, True)
                player = "O" if player == "X" else "X"

    def test_make_move_invalid(self):
        """
        Test making invalid moves on the board.
        """
        invalid_cols = [
            -3, -2, -1,
            self.connect4.col,
            self.connect4.col + 1,
            self.connect4.col + 2,
            self.connect4.col + 3,
        ]
        expected_board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        player = "X"

        # Test for invalid column:
        for invalid_col in invalid_cols:
            result = self.connect4.make_move(player=player, col=invalid_col)
            self.assertEqual(self.connect4.board, expected_board)
            self.assertEqual(result, False)

        # Test for invalid row (column is fully filled):
        expected_board = [["X" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.connect4.board = [["X" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        for col in range(self.connect4.col):
            result = self.connect4.make_move(player=player, col=col)
            self.assertEqual(self.connect4.board, expected_board)
            self.assertEqual(result, False)

    def test_check_winner(self):
        """
        Test detecting a winning condition in the board.
        """
        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "O", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "O", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertTrue(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "X", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "O", "X", " ", " ", " "],
            [" ", "O", "X", "O", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "O", " ", " "],
            [" ", " ", " ", "O", "X", " ", " "],
            [" ", " ", "O", "X", "X", " ", " "],
            [" ", "O", "X", "O", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertTrue(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())

    def test_check_full(self):
        """
        Test detecting a full board condition.
        """
        self.connect4.board = [["X" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertTrue(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertTrue(self.connect4.check_full())

        self.connect4.board = [["O" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertTrue(self.connect4.check_winner(player="O"))
        self.assertTrue(self.connect4.check_full())

    def test_evaluate(self):
        """
        Test the evaluation functionality.
        """
        n = 6 * 7
        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "O", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())
        self.assertEqual(self.connect4.evaluate(), n)

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "O", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            ["O", "O", "X", "X", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertTrue(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())
        self.assertEqual(self.connect4.evaluate(), -n)

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "X", " ", " ", " ", " ", " "],
            [" ", "O", "X", " ", " ", " ", " "],
            [" ", "O", "O", "X", " ", " ", " "],
            [" ", "O", "X", "O", "X", "X", " "],
        ]
        self.assertTrue(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())
        self.assertEqual(self.connect4.evaluate(), n)

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "O", " ", " "],
            [" ", " ", " ", "O", "X", " ", " "],
            [" ", " ", "O", "X", "X", " ", " "],
            [" ", "O", "X", "O", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertTrue(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())
        self.assertEqual(self.connect4.evaluate(), -n)

        self.connect4.board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "O", " ", " "],
            [" ", " ", " ", " ", "X", " ", " "],
            [" ", " ", "O", "X", "X", " ", " "],
            [" ", "O", "X", "O", "X", " ", " "],
        ]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())
        self.assertEqual(self.connect4.evaluate(), 0)

        self.connect4.board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertFalse(self.connect4.check_full())
        self.assertEqual(self.connect4.evaluate(), 0)

        self.connect4.board = [
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
        ]
        self.assertFalse(self.connect4.check_winner(player="X"))
        self.assertFalse(self.connect4.check_winner(player="O"))
        self.assertTrue(self.connect4.check_full())
        self.assertEqual(self.connect4.evaluate(), 0)

    @patch("builtins.input", side_effect=["x", "", "a"])
    def test_get_input(self, mock_input):
        """
        Test the input validation logic.
        """
        message = "test_message"
        answers = ["a", "b"]
        message_error = "test_message_error"
        answer = self.connect4.get_input(
            message=message,
            answers=answers,
            message_error=message_error,
        )
        self.assertEqual(answer, "a")
        self.assertEqual(mock_input.call_count, 3)


if __name__ == "__main__":
    unittest.main()
