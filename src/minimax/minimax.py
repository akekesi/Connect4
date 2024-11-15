"""
Implements the Minimax algorithm for optimal move decision-making in turn-based games.
"""


from typing import Callable


class Minimax:
    """
    A Minimax class to implement the Minimax algorithm for decision-making in turn-based games.
    The algorithm utilizes evaluation and move functions provided during initialization to recursively
    simulate moves and return optimal decisions for maximizing or minimizing players, with an optional
    depth limit to improve performance in complex games.

    Attributes:
        func_evaluate (Callable[[], int]): A function to evaluate the current board state and return a score.
        func_check_full (Callable[[], bool]): A function to check if the game board is full (no more moves).
        func_move (Callable[[tuple[int, int], str], None]): A function to make a move on the board.
        func_remove (Callable[[tuple[int, int]], None]): A function to remove a move from the board.
        func_get_valid_moves (Callable[[], list[tuple[int, int]]]): A function to retrieve a list of valid moves.
        depth_max (int): Maximum depth for recursion in the minimax algorithm. Limits the search to improve
                         performance by stopping after reaching this depth.

    Methods:
        minimax(is_maximizing: bool, depth: int) -> int:
            Recursively calculates the optimal score for the maximizing or minimizing player
            up to a specified maximum depth. Stops if a win/loss, full board, or max depth is reached.
        
        best_move(player: str) -> tuple[int, int]:
            Determines the best move for the specified player using the Minimax algorithm.
            Iterates through all valid moves and calculates scores to select the optimal move.
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
        # pylint: disable=line-too-long
        # pylint: disable=too-many-arguments
        """
        Initializes the Minimax class with game-specific functions and a depth limit.

        Args:
            func_evaluate (Callable[[], int]): Function to evaluate the board state and return a score.
            func_check_full (Callable[[], bool]): Function to check if the board is fully occupied.
            func_move (Callable[[tuple[int, int], str], None]): Function to make a move on the board.
            func_remove (Callable[[tuple[int, int]], None]): Function to remove a move from the board.
            func_get_valid_moves (Callable[[], list[tuple[int, int]]]): Function to get a list of valid moves.
            depth_max (int): Optional; maximum depth for the minimax search (default is inf).
        """
        self.func_evaluate = func_evaluate
        self.func_check_full = func_check_full
        self.func_move = func_move
        self.func_remove = func_remove
        self.func_get_valid_moves = func_get_valid_moves
        self.depth_max = depth_max

    def minimax(self, is_maximizing: bool, depth: int) -> int:
        """
        Executes the Minimax algorithm to compute the optimal score for the current player
        up to a maximum depth. Adjusts scores based on the depth to prioritize faster wins
        or delayed losses.

        Args:
            is_maximizing (bool): True if the current player is maximizing, False otherwise.
            depth (int): Current depth of the recursive search, incremented with each call.

        Returns:
            int: The optimal score for the player at the current board state, considering
                 the specified max depth.
        """
        score = self.func_evaluate()
        if score != 0 or self.func_check_full() or depth == self.depth_max:
            return score - depth if score > 0 else score + depth

        moves = self.func_get_valid_moves()
        if is_maximizing:
            max_score = -float("inf")
            for move in moves:
                self.func_move(move=move, player="X")
                max_score = max(max_score, self.minimax(is_maximizing=False, depth=depth + 1))
                self.func_remove(move=move)
            return max_score
        else:
            min_score = float("inf")
            for move in moves:
                self.func_move(move=move, player="O")
                min_score = min(min_score, self.minimax(is_maximizing=True, depth=depth + 1))
                self.func_remove(move=move)
            return min_score

    def best_move(self, player: str) -> tuple[int, int]:
        """
        Determines the best possible move for the specified player using the Minimax algorithm.
        Considers all valid moves, applies the Minimax function to each, and selects the move
        with the highest or lowest score based on player type.

        Args:
            player (str): The player making the move, typically "X" (maximizing) or "O" (minimizing).

        Returns:
            tuple[int, int]: The coordinates of the best move for the player on the game board.
        """
        move_best = None
        moves = self.func_get_valid_moves()
        if player == "X":
            score_best = -float("inf")
            for move in moves:
                self.func_move(move=move, player=player)
                score = self.minimax(is_maximizing=False, depth=1)
                self.func_remove(move=move)
                if score > score_best:
                    score_best = score
                    move_best = move
        if player == "O":
            score_best = float("inf")
            for move in moves:
                self.func_move(move=move, player=player)
                score = self.minimax(is_maximizing=True, depth=1)
                self.func_remove(move=move)
                if score < score_best:
                    score_best = score
                    move_best = move
        return move_best
