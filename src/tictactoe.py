"""
Two-Player Tic-Tac-Toe Game with Minimax Move Recommendations

This module provides a command-line Tic-Tac-Toe game for two players, with real-time
move recommendations based on the Minimax algorithm. Both players, 'X' and 'O', receive
suggested moves for optimal gameplay, though they can choose their own moves as well.

Classes
-------
TicTacToe
    A class that represents the Tic-Tac-Toe game, including methods for displaying
    the board, validating moves, making moves, checking for a winner, and using the
    Minimax algorithm to recommend the best moves for both players.

Usage
-----
Run this module to start a two-player game. Each turn, the current player receives
a recommended move based on the Minimax algorithm. Players can input their own moves
or follow the recommended moves.

Example
-------
$ python tictactoe.py
X's turn:
 --- --- --- 
|   |   |   |
 --- --- --- 
|   |   |   |
 --- --- --- 
|   |   |   |
 --- --- --- 
Best move: (1, 1)
Enter move (row, col): 

The game continues until either player wins or the board is full.

"""


class TicTacToe:
    """
    A class to represent a Tic-Tac-Toe game, including display, move validation,
    checking for winners, and implementing the Minimax algorithm for optimal moves.

    Attributes
    ----------
    n : int
        The size of the Tic-Tac-Toe board (3x3).
    board : list
        The current state of the Tic-Tac-Toe board as a 2D list of strings.

    Methods
    -------
    display_board() -> None:
        Prints the current state of the board to the console.

    empty_cells() -> bool:
        Checks if there are any empty cells on the board.

    valid_move(x: int, y: int) -> bool:
        Checks if a move is within bounds and if the target cell is empty.

    make_move(x: int, y: int, player: str) -> bool:
        Places the player's symbol on the board if the move is valid and returns True;
        otherwise, returns False.

    check_winner(player: str) -> bool:
        Checks if the specified player has won by having three in a row.

    evaluate() -> int:
        Evaluates the board state to determine if 'X' has won (1), 'O' has won (-1),
        or if it's a draw (0).

    minimax(is_maximizing: bool) -> int:
        The Minimax algorithm to determine the optimal score for the maximizing
        or minimizing player.

    best_move(player: str) -> tuple[int, int]:
        Finds and returns the best move for the specified player using the Minimax algorithm.

    play_game() -> None:
        Runs the game loop where two players, "X" and "O", take turns to play,
        displaying the board after each move and announcing the winner or a draw.
    """

    def __init__(self) -> None:
        self.n = 3
        self.board = [[" " for _ in range(self.n)] for _ in range(self.n)]

    def display_board(self) -> None:
        """Prints the current state of the board with lines separating cells."""
        line_horizontal = " ---" * self.n + " "
        print(line_horizontal)
        for row in self.board:
            print("| " + " | ".join(row) + " |")
            print(line_horizontal)

    def empty_cells(self) -> bool:
        """Returns True if there are any empty cells on the board; otherwise, False."""
        return any(cell == " " for row in self.board for cell in row)

    def valid_move(self, x: int, y: int) -> bool:
        """Checks if the move is valid (within bounds and cell is empty).

        Args:
            x (int): Row index.
            y (int): Column index.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == " "

    def make_move(self, x: int, y: int, player: str) -> bool:
        """Attempts to place the player's symbol on the board at (x, y).

        Args:
            x (int): Row index.
            y (int): Column index.
            player (str): The symbol of the player ('X' or 'O').

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.valid_move(x, y):
            self.board[x][y] = player
            return True
        return False

    def check_winner(self, player: str) -> bool:
        """Checks if the specified player has won the game.

        Args:
            player (str): The symbol of the player to check ('X' or 'O').

        Returns:
            bool: True if the player has won, False otherwise.
        """
        for i in range(self.n):
            if all(self.board[i][j] == player for j in range(self.n)) or \
               all(self.board[j][i] == player for j in range(self.n)):
                return True
        return all(self.board[i][i] == player for i in range(self.n)) or \
               all(self.board[i][self.n - 1 - i] == player for i in range(self.n))

    def evaluate(self) -> int:
        """Evaluates the board for game state.

        Returns:
            int: 1 if 'X' wins, -1 if 'O' wins, 0 for a draw.
        """
        if self.check_winner("X"):
            return 1
        if self.check_winner("O"):
            return -1
        return 0

    def minimax(self, is_maximizing: bool) -> int:
        """The Minimax algorithm to calculate optimal score for the current player.

        Args:
            is_maximizing (bool): True if 'X' is playing (maximizing), False if 'O' (minimizing).

        Returns:
            int: The optimal score for the given player state.
        """
        score = self.evaluate()
        if score != 0 or not self.empty_cells():
            return score

        if is_maximizing:
            score = -999
            for x in range(self.n):
                for y in range(self.n):
                    if self.board[x][y] == " ":
                        self.board[x][y] = "X"
                        score = max(score, self.minimax(is_maximizing=False))
                        self.board[x][y] = " "
        else:
            score = 999
            for x in range(self.n):
                for y in range(self.n):
                    if self.board[x][y] == " ":
                        self.board[x][y] = "O"
                        score = min(score, self.minimax(is_maximizing=True))
                        self.board[x][y] = " "
        return score

    def best_move(self, player: str) -> tuple[int, int]:
        """Finds the best move for the specified player using Minimax.

        Args:
            player (str): The player symbol ('X' or 'O').

        Returns:
            tuple[int, int]: The coordinates of the best move as (row, column).
        """
        move = None
        if player == "X":
            score_best = -999
            for x in range(self.n):
                for y in range(self.n):
                    if self.board[x][y] == " ":
                        self.board[x][y] = player
                        score = self.minimax(is_maximizing=False)
                        self.board[x][y] = " "
                        if score > score_best:
                            score_best = score
                            move = (x, y)
        if player == "O":
            score_best = 999
            for x in range(self.n):
                for y in range(self.n):
                    if self.board[x][y] == " ":
                        self.board[x][y] = player
                        score = self.minimax(is_maximizing=True)
                        self.board[x][y] = " "
                        if score < score_best:
                            score_best = score
                            move = (x, y)
        return move

    def play_game(self) -> None:
        """Runs the game loop where 'X' and 'O' take turns
        to play until there is a winner or draw."""
        player = "X"
        while True:
            print()
            print(f"{player}'s turn:")
            self.display_board()
            print("Best move: ", end="")
            print(self.best_move(player=player))

            x, y = map(int, input("Enter move (row, col): ").split())

            if not self.make_move(x=x, y=y, player=player):
                print("Invalid move. Try again.")
                continue

            if self.check_winner(player=player):
                msg_finish =f"{player} wins!"
                break

            if not self.empty_cells():
                msg_finish = "It's a draw!"
                break

            player = "O" if player == "X" else "X"

        print()
        print(msg_finish)
        self.display_board()


if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
