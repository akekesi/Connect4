"""
Two-Player Tic-Tac-Toe Game with Minimax Move Recommendations

This module provides a command-line Tic-Tac-Toe game for two players, with real-time
move recommendations based on the Minimax algorithm. Both players, receive
suggested moves for optimal gameplay, though they can choose their own moves as well.

Run:
$ python -m src.tictactoe.tictactoe
"""

from src.utils.players import Players
from src.minimax.minimax import Minimax


class TicTacToe:
    """
    A Tic-Tac-Toe game with two-player functionality and Minimax-based move recommendations.

    This class represents a Tic-Tac-Toe game board and includes methods for playing the game
    interactively between two players. The class offers move validation, win detection,
    and real-time optimal move suggestions using the Minimax algorithm.

    Attributes:
    n (int): The size of the Tic-Tac-Toe board (3x3).
    board (list[list[int]]): A 2D list representing the Tic-Tac-Toe board, 
                             initially empty with each cell set to a space (" ").
    """

    def __init__(self) -> None:
        """
        Initializes a new Tic-Tac-Toe game with a 3x3 board.
        """
        self.n = 3
        self.board = [[" " for _ in range(self.n)] for _ in range(self.n)]

    def move(self, move: tuple[int, int], player: str) -> None:
        """
        Places the player's symbol at the specified position on the board.

        Args:
            move (tuple[int, int]): The (row, col) position on the board.
            player (str): The symbol of the player.
        """
        self.board[move[0]][move[1]] = player

    def remove(self, move: tuple[int, int]) -> None:
        """
        Removes a symbol from the specified position on the board, setting it to empty.

        Args:
            move (tuple[int, int]): The (row, col) position to be cleared.
        """
        self.board[move[0]][move[1]] = " "

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """
        Gets all valid moves on the board (empty cells).

        Returns:
            list[tuple[int, int]]: List of coordinates for all empty cells.
        """
        return [(x, y) for x in range(self.n) for y in range(self.n) if self.board[x][y] == " "]

    def check_move(self, move: tuple[int, int]) -> bool:
        """
        Checks if the move is valid (within bounds and cell is empty).

        Args:
            move (tuple[int, int]): The (row, col) position to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= move[0] < self.n and \
               0 <= move[1] < self.n and \
               self.board[move[0]][move[1]] == " "

    def check_input(self, input_: str) -> bool:
        """
        Validates if the input string represents a valid move format 
        (two integers separated by space).

        Args:
            input_ (str): The input string from the user.

        Returns:
            bool: True if input is valid, False otherwise.
        """
        try:
            _, _ = map(int, input_.split())
            return True
        except ValueError:
            return False

    def check_winner(self, player: str) -> bool:
        """
        Checks if the specified player has won the game.

        Args:
            player (str): The symbol of the player to check.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        for i in range(self.n):
            if all(self.board[i][j] == player for j in range(self.n)) or \
               all(self.board[j][i] == player for j in range(self.n)):
                return True
        return all(self.board[i][i] == player for i in range(self.n)) or \
               all(self.board[i][self.n - 1 - i] == player for i in range(self.n))

    def check_full(self) -> bool:
        """
        Checks if the board is full, meaning no empty cells remain.

        Returns:
            bool: True if all cells are filled, False if there are any empty cells.
        """
        return not any(cell == " " for row in self.board for cell in row)

    def evaluate(self) -> int:
        """
        Evaluates the board for game state.

        Returns:
            int: 1 if player-1 wins, -1 if player-2 wins, 0 for a draw.
        """
        if self.check_winner(player=Players.P1.value):
            return self.n ** 2
        if self.check_winner(player=Players.P2.value):
            return -self.n ** 2
        return 0

    def make_move(self, move: tuple[int, int], player: str) -> bool:
        """
        Attempts to place the player's symbol on the board at (x, y).

        Args:
            move (tuple[int, int]): The (row, col) position on the board.
            player (str): The symbol of the player.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.check_move(move=move):
            self.move(move=move, player=player)
            return True
        return False

    def display_board(self) -> None:
        """
        Prints the current state of the board with lines separating cells.
        """
        line_horizontal = " ---" * self.n + " "
        print(line_horizontal)
        for row in self.board:
            print("| " + " | ".join(row) + " |")
            print(line_horizontal)

    def play_game(self) -> None:
        """
        Runs the game loop where player-1 and player-2 take turns
        to play until there is a winner or draw.
        """
        player = Players.P1
        minimax = Minimax(
            func_evaluate=self.evaluate,
            func_check_full=self.check_full,
            func_move=self.move,
            func_remove=self.remove,
            func_get_valid_moves=self.get_valid_moves,
        )
        while True:
            print()
            print(f"{player.value}'s turn:")
            self.display_board()
            print("Best move: ", end="")
            print(minimax.best_move(player=player.value))

            input_ = input("Enter move (row, col): ")
            if not self.check_input(input_=input_):
                print("Invalid input. Try again.")
                continue
            x, y = map(int, input_.split())
            move = (x, y)

            if not self.make_move(move=move, player=player.value):
                print("Invalid move. Try again.")
                continue

            if self.check_winner(player=player.value):
                print()
                print(f"Player-{player.value} won.")
                break

            if self.check_full():
                print()
                print("The board is full, resulting in a draw.")
                break

            player = Players.P2 if player == Players.P1 else Players.P1
        self.display_board()


if __name__ == "__main__":
    tictactoe = TicTacToe()
    tictactoe.play_game()
