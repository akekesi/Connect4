"""
"""

import unittest

from src.connect4 import Connect4


class TestConnect4(unittest.TestCase):
    """
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
        """
        expected_board = self.board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.assertEqual(self.connect4.board, expected_board)

    def test_move(self):
        """
        """
        expected_board = self.board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
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
        """
        expected_board = self.board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
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
        """
        expected_board = self.board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
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
        """
        invalid_cols = [
            -3, -2, -1,
            self.connect4.col,
            self.connect4.col + 1,
            self.connect4.col + 2,
            self.connect4.col + 3,
        ]
        expected_board = self.board = [[" " for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        player = "X"

        # Test for invalid column:
        for invalid_col in invalid_cols:
            result = self.connect4.make_move(player=player, col=invalid_col)
            self.assertEqual(self.connect4.board, expected_board)
            self.assertEqual(result, False)

        # Test for invalid row (column is fully filled):
        expected_board = self.board = [["X" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        self.connect4.board = self.board = [["X" for _ in range(self.connect4.col)] for _ in range(self.connect4.row)]
        for col in range(self.connect4.col):
            result = self.connect4.make_move(player=player, col=col)
            self.assertEqual(self.connect4.board, expected_board)
            self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
