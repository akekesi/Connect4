"""
Implements the Minimax algorithm for optimal move decision-making in turn-based games.
"""


from typing import Callable


class Minimax:
    """
    A Minimax class to implement the Minimax algorithm for decision-making in games.
    Utilizes evaluation and move functions provided during initialization to recursively
    simulate moves and return optimal decisions for maximizing or minimizing players.
    """

    def __init__(
            self,
            func_evaluate: Callable[[], int],
            func_check_full: Callable[[], bool],
            func_move: Callable[[tuple[int, int], str], None],
            func_remove: Callable[[tuple[int, int]], None],
            func_get_valid_moves: Callable[[], list[tuple[int, int]]],
        ) -> None:
        # pylint: disable=line-too-long
        # pylint: disable=too-many-arguments
        """
        Initializes the Minimax class with game functions.

        Args:
            func_evaluate (Callable[[], int]): Function to evaluate the board state and return a score.
            func_is_empty_cells (Callable[[], bool]): Function to check if there are empty cells available.
            func_move (Callable[[tuple[int, int], str], None]): Function to make a move on the board.
            func_remove (Callable[[tuple[int, int]], None]): Function to remove a move from the board.
            func_get_valid_moves (Callable[[], list[tuple[int, int]]]): Function to get a list of valid moves.
        """
        self.func_evaluate = func_evaluate
        self.func_check_full = func_check_full
        self.func_move = func_move
        self.func_remove = func_remove
        self.func_get_valid_moves = func_get_valid_moves

    def minimax(self, is_maximizing: bool) -> int:
        """
        Executes the Minimax algorithm to compute the best possible score for the 
        maximizing or minimizing player, depending on the current turn.

        Args:
            is_maximizing (bool): True if the current turn is for maximizing player,
            False otherwise.

        Returns:
            int: The optimal score for the current player.
        """
        score = self.func_evaluate()
        if score != 0 or self.func_check_full():
            return score

        moves = self.func_get_valid_moves()
        if is_maximizing:
            score = -999
            for move in moves:
                self.func_move(move=move, player="X")
                score = max(score, self.minimax(is_maximizing=False))
                self.func_remove(move=move)
        else:
            score = 999
            for move in moves:
                self.func_move(move=move, player="O")
                score = min(score, self.minimax(is_maximizing=True))
                self.func_remove(move=move)
        return score

    def best_move(self, player: str) -> tuple[int, int]:
        """
        Determines the best move for the given player using the Minimax algorithm.

        Args:
            player (str): The player for whom to determine the best move ("X" or "O").

        Returns:
            tuple[int, int]: The best move (row, col) for the given player.
        """
        move_best = None
        moves = self.func_get_valid_moves()
        if player == "X":
            score_best = -999
            for move in moves:
                self.func_move(move=move, player=player)
                score = self.minimax(is_maximizing=False)
                self.func_remove(move=move)
                if score > score_best:
                    score_best = score
                    move_best = move
        if player == "O":
            score_best = 999
            for move in moves:
                self.func_move(move=move, player=player)
                score = self.minimax(is_maximizing=True)
                self.func_remove(move=move)
                if score < score_best:
                    score_best = score
                    move_best = move
        return move_best
