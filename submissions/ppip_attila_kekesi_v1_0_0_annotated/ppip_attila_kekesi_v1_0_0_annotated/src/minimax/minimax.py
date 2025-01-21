"""
This module implements the Minimax algorithm for decision-making in two-player games. 
It provides a `Minimax` class to calculate the optimal move based on an evaluation function 
and simulates future game states using recursive search.
"""

from typing import Callable
from src.utils.players import Players


class Minimax:
    """
    A class implementing the Minimax algorithm for decision-making in two-player games. The algorithm computes the optimal move
    for a player by simulating all possible moves and evaluating the resulting game states using a heuristic evaluation function.

    Attributes:
        func_evaluate (Callable[[], int]): A function to evaluate the current game state and return a score.
        func_check_full (Callable[[], bool]): A function to check if the game board is full, indicating a draw.
        func_move (Callable[[tuple[int, int], str], None]): A function to make a move on the game board.
        func_remove (Callable[[tuple[int, int]], None]): A function to undo a move on the game board.
        func_get_valid_moves (Callable[[], list[tuple[int, int]]]): A function to get a list of valid moves for the current player.
        depth_max (int): The maximum depth to search during the minimax algorithm. Defaults to infinity for unlimited depth.
    """

    def __init__(
            self,
            func_evaluate: Callable[[], int],
            func_check_full: Callable[[], bool],
            func_move: Callable[[tuple[int, int], str], None],
            func_remove: Callable[[tuple[int, int]], None],
            func_get_valid_moves: Callable[[], list[tuple[int, int]]],
            depth_max: int = float("inf")
        ) -> None:
        """
        Initializes the Minimax object with the required functions and maximum search depth.

        Args:
            func_evaluate (Callable[[], int]): A function to evaluate the current game state and return a score.
            func_check_full (Callable[[], bool]): A function to check if the game board is full, indicating a draw.
            func_move (Callable[[tuple[int, int], str], None]): A function to make a move on the game board.
            func_remove (Callable[[tuple[int, int]], None]): A function to undo a move on the game board.
            func_get_valid_moves (Callable[[], list[tuple[int, int]]]): A function to get a list of valid moves for the current player.
            depth_max (int, optional): The maximum depth for the Minimax algorithm to search. Defaults to infinity for unlimited depth.
        """
        self.func_evaluate = func_evaluate
        self.func_check_full = func_check_full
        self.func_move = func_move
        self.func_remove = func_remove
        self.func_get_valid_moves = func_get_valid_moves
        self.depth_max = depth_max

    def minimax(self, is_maximizing: bool, depth: int) -> int:
        """
        Recursively calculates the minimax score for the current game state.

        This method evaluates all possible moves for the current player, simulates them, and returns the best score based on
        whether the current player is maximizing or minimizing their score.

        Args:
            is_maximizing (bool): Whether the current player is trying to maximize their score (True) or minimize it (False).
            depth (int): The current depth of the recursion.

        Returns:
            int: The best score for the current game state.
        """
        score = self.func_evaluate()
        if score != 0 or self.func_check_full() or depth == self.depth_max:
            return score - depth if score > 0 else score + depth

        moves = self.func_get_valid_moves()
        if is_maximizing:
            max_score = -float("inf")
            for move in moves:
                self.func_move(move=move, player=Players.P1.value)
                max_score = max(max_score, self.minimax(is_maximizing=False, depth=depth + 1))
                self.func_remove(move=move)
            return max_score
        else:
            min_score = float("inf")
            for move in moves:
                self.func_move(move=move, player=Players.P2.value)
                min_score = min(min_score, self.minimax(is_maximizing=True, depth=depth + 1))
                self.func_remove(move=move)
            return min_score

    def best_move(self, player: str) -> tuple[int, int]:
        """
        Calculates the best move for the given player using the Minimax algorithm.

        This method evaluates all valid moves for the player and returns the move with the best score based on the
        Minimax evaluation.

        Args:
            player (str): The player for whom to calculate the best move.

        Returns:
            tuple[int, int]: The coordinates of the best move for the given player.
        """
        move_best = None
        moves = self.func_get_valid_moves()
        if player == Players.P1.value:
            score_best = -float("inf")
            for move in moves:
                self.func_move(move=move, player=player)
                score = self.minimax(is_maximizing=False, depth=1)
                self.func_remove(move=move)
                if score > score_best:
                    score_best = score
                    move_best = move
        if player == Players.P2.value:
            score_best = float("inf")
            for move in moves:
                self.func_move(move=move, player=player)
                score = self.minimax(is_maximizing=True, depth=1)
                self.func_remove(move=move)
                if score < score_best:
                    score_best = score
                    move_best = move
        return move_best
