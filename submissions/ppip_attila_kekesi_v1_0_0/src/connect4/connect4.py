"""
Connect4 Game Module

This module provides the implementation of the Connect4 game, including functionalities 
for initializing the game, making moves, checking for a winner, and playing against 
an AI agent with different difficulty levels.

Run:
$ python -m src.connect4.connect4
"""

import os
import random
import logging
from src.utils.players import Players
from src.minimax.minimax import Minimax
from src.logger.logger_config import Logging
from src.utils.check_end import check_winner, check_full

# set logger up
logger = Logging().set_logger(
    name="Connect4",
    level=logging.NOTSET,
    # level=logging.INFO,
    # level=logging.DEBUG,
    path_dir=os.path.join(os.path.dirname(__file__), "..", "..", "logs")
)


class Connect4:
    """
    Connect4 game logic and functionalities.

    Attributes:
        row (int): Number of rows in the board.
        col (int): Number of columns in the board.
        win (int): Number of consecutive tokens needed to win.
        board (list): 2D list representing the game board.
        depth_max (int): Maximum depth for the minimax algorithm.
    """

    def __init__(self) -> None:
        """
        Initializes the Connect4 game with a default 6x7 board and win condition of 4 tokens.
        """
        logger.debug("called")
        self.row = 6
        self.col = 7
        self.win = 4
        self.board = None
        self.depth_max = 5
        self.init_board()
        logger.info("game is initialized")

    def init_board(self) -> None:
        """
        Resets the game board to its initial state (empty cells).
        """
        logger.debug("called")
        self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]
        logger.info("board is initialized")

    def move(self, move: tuple[int, int], player: str) -> None:
        """
        Places a player's token on the board.

        Args:
            move (tuple[int, int]): The row and column indices for the move.
            player (str): The token of the players.
        """
        logger.debug("called")
        self.board[move[0]][move[1]] = player
        logger.info("player-%s is moved into (%d, %d)", player, move[0], move[1])

    def remove(self, move: tuple[int, int]) -> None:
        """
        Removes a player's token from the board.

        Args:
            move (tuple[int, int]): The row and column indices to remove the token from.
        """
        logger.debug("called")
        player = self.board[move[0]][move[1]]
        self.board[move[0]][move[1]] = " "
        logger.info("player-%s is removed from (%d, %d)", player, move[0], move[1])

    def get_row(self, col: int) -> int:
        """
        Finds the lowest available row in a column.

        Args:
            col (int): The column index.

        Returns:
            int: The row index of the lowest available cell, or -1 if the column is full.
        """
        logger.debug("called")
        row_free = -1
        for row in range(self.row):
            if self.board[row][col] == " ":
                row_free = row
            else:
                break
        logger.info("col(%d) --> %d", col, row_free)
        return row_free

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """
        Gets all valid moves (empty cells) on the board.

        Returns:
            list[tuple[int, int]]: List of tuples representing valid moves.
        """
        logger.debug("called")
        valid_moves = []
        for col in range(self.col):
            row = self.get_row(col=col)
            if self.check_row(row=row):
                valid_moves.append((row, col))
        logger.info("%s: %s", row, valid_moves)
        return valid_moves

    def check_row(self, row: int) -> bool:
        """
        Checks if a row index is valid.

        Args:
            row (int): The row index to check.

        Returns:
            bool: True if the row is valid, False otherwise.
        """
        logger.debug("called")
        valid = 0 <= row < self.row
        logger.info("%s: %s", row, valid)
        return valid

    def check_col(self, col: int) -> bool:
        """
        Checks if a column index is valid.

        Args:
            col (int): The column index to check.

        Returns:
            bool: True if the column is valid, False otherwise.
        """
        logger.debug("called")
        valid = 0 <= col < self.col
        logger.info("%s, %s", col, valid)
        return valid

    def check_move(self, col: int) -> tuple[int, int] | None:
        """
        Validates a move by checking the column and row.

        Args:
            col (int): The column index of the move.

        Returns:
            tuple[int, int] | None: The valid move as a tuple, or None if invalid.
        """
        logger.debug("called")
        if not self.check_col(col=col):
            return None
        row = self.get_row(col=col)
        if not self.check_row(row=row):
            return None
        return (row, col)

    def check_input(self, input_: str) -> bool:
        """
        Validates if the input is an integer.

        Args:
            input_ (str): Input string to validate.

        Returns:
            bool: True if the input is an integer, False otherwise.
        """
        logger.debug("called")
        try:
            int(input_)
            result = True
            logger.info("%s: %s", input_, result)
            return result
        except ValueError:
            result = False
            logger.info("%s: %s", input_, result)
            return result

    def check_winner(self, player: str) -> bool:
        """
        Checks if the specified player has won the game.

        Args:
            player (str): The symbol of the player to check.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        logger.debug("called")
        return check_winner(board=self.board, player=player, win=self.win)

    def check_full(self) -> bool:
        """
        Checks if the board is full, meaning no empty cells remain.

        Returns:
            bool: True if all cells are filled, False if there are any empty cells.
        """
        logger.debug("called")
        return check_full(board=self.board)

    def evaluate(self) -> int:
        """
        Evaluates the board for game state.

        Returns:
            int: (row * col) if player-1 wins, -(row * col) if playe-2 wins, 0 for a draw.
        """
        logger.debug("called")
        n = self.row * self.col
        if check_winner(board=self.board, player=Players.P1.value, win=self.win):
            logger.info("%d", n)
            return n
        if check_winner(board=self.board, player=Players.P2.value, win=self.win):
            logger.info("%d", -n)
            return -n
        logger.info("%d", 0)
        return 0

    def make_move(self, player: str, col: int) -> bool:
        """
        Makes a move for the specified player at the given column.

        Args:
            player (str): The symbol of the player making the move.
            col (int): The column where the player wants to place their symbol.

        Returns:
            bool: True if the move was successful, False if the move was invalid.
        """
        logger.debug("called")
        move = self.check_move(col=col)
        if not isinstance(move, tuple):
            return False
        self.move(move=move, player=player)
        return True

    def display_board(self, turn: int) -> None:
        """
        Displays the current state of the board, including the turn number.

        Args:
            turn (int): The current turn number.

        Exaple:
        |=============|
        |             |
        |             |
        |    X X      |
        |    O X X    |
        |  O X O O    |
        |  O O X X    |
        |=============|
        |0 1 2 3 4 5 6|
        """
        logger.debug("called")
        n = self.col * 2 - 1
        line_horizontal = "=" * (n)
        line_numbers = [str(x) for x in range(self.col)]
        print("|" + line_horizontal + "|")
        for row in self.board:
            print("|" + " ".join(row) + "|")
        print("|" + line_horizontal + "|")
        print("|" + " ".join(line_numbers) + "|")
        print(f"|{f'{turn:03}':=^{n}}|")
        print()

    def turn_player(self, player: str) -> None:
        """
        Manages the turn for a human player, prompting them for input until a valid move is made.

        Args:
            player (str): The symbol of the current players.
        """
        logger.debug("called")
        while True:
            input_ = input(f"Enter column number to set '{player}' of player-{player}: ")
            if not self.check_input(input_=input_):
                continue
            col = int(input_)
            move_info = self.make_move(player=player, col=col)
            if not move_info:
                continue
            break

    def turn_agent_easy(self, player: str) -> None:
        """
        Manages the turn for an easy-level AI agent, selecting a random valid move.

        Args:
            player (str): The symbol of the AI players.
        """
        logger.debug("called")
        print(f"Enter column number to set '{player}' of player-{player}: ", end="")
        valid_moves = self.get_valid_moves()
        move = random.choice(valid_moves)
        print(f"{move[1]}")
        self.move(move=move, player=player)

    def turn_agent_hard(self, player: str) -> None:
        """
        Manages the turn for a hard-level AI agent, selecting the best move using the minimax algorithm.

        Args:
            player (str): The symbol of the AI players.
        """
        logger.debug("called")
        minimax = Minimax(
            func_evaluate=self.evaluate,
            func_check_full=self.check_full,
            func_move=self.move,
            func_remove=self.remove,
            func_get_valid_moves=self.get_valid_moves,
            depth_max=self.depth_max,
        )
        print(f"Enter column number to set '{player}' of player-{player}: ", end="")
        move = minimax.best_move(player=player)
        print(f"{move[1]}")
        self.move(move=move, player=player)

    def play_game(self, type_: str, first_move: str = "") -> None:
        """
        Starts and manages the game based on the selected game type and first move.

        Args:
            type_ (str): The game mode ('2' for 2-player, 'e' for 1-player easy, 'h' for 1-player hard).
            first_move (str): The player or agent that should make the first move ('p' for player, 'a' for agent).
        """
        logger.debug("called")
        self.init_board()
        turn = 0
        player = Players.P1
        self.display_board(turn=turn)
        while True:
            turn += 1
            # 2-Player
            if type_ == "2":
                self.turn_player(player=player.value)
            # 1-Player-Easy
            if type_ == "e":
                # First move: player
                if first_move == "p":
                    if player == Players.P1:
                        self.turn_player(player=player.value)
                    else:
                        self.turn_agent_easy(player=player.value)
                # First move: agent
                if first_move == "a":
                    if player == Players.P1:
                        self.turn_agent_easy(player=player.value)
                    else:
                        self.turn_player(player=player.value)
            # 1-Player-Hard
            if type_ == "h":
                # First move: player
                if first_move == "p":
                    if player == Players.P1:
                        self.turn_player(player=player.value)
                    else:
                        self.turn_agent_hard(player=player.value)
                # First move: agent
                if first_move == "a":
                    if player == Players.P1:
                        self.turn_agent_hard(player=player.value)
                    else:
                        self.turn_player(player=player.value)
            self.display_board(turn=turn)
            if check_winner(board=self.board, player=player.value, win=self.win):
                win_str = f"Player-{player.value} won."
                print(win_str)
                logger.info(win_str)
                break
            if check_full(board=self.board):
                win_str = "The board is full, resulting in a draw."
                print(win_str)
                logger.info(win_str)
                break
            player = Players.P2 if player == Players.P1 else Players.P1

    def get_input(self, message: str, answers: list[str], message_error: str = "Try again") -> str:
        """
        Prompts the user for input and ensures that the answer is one of the valid options.

        Args:
            message (str): The prompt message to display to the user.
            answers (list[str]): A list of valid answers that the user can input.
            message_error (str): The message to display if the user provides an invalid answer.

        Returns:
            str: The valid input provided by the user.
        """
        logger.debug("called")
        while True:
            answer = input(message)
            logger.info(answer)
            if answer in answers:
                print()
                return answer
            print(message_error)
            print()

    def run(self) -> None:
        """
        Runs the main game loop, allowing the user to choose game options, modes, and difficulty levels.

        The game continues until the user chooses to quit or a winner is determined.
        """
        logger.debug("called")
        message_game = "Start a new game (enter 'g')\nQuit the program (enter 'q')\nEnter your choice: "
        answers_game = ["g", "q"]
        message_player = "Play in 1-Player mode (enter '1')\nPlay in 2-Player mode (enter '2')\nSelect mode: "
        answers_player = ["1", "2"]
        message_difficulty = "Easy difficulty (enter 'e')\nHard difficulty (enter 'h')\nChoose difficulty: "
        answers_difficulty = ["e", "h"]
        message_first_move = "Agent moves first (enter 'a')\nPlayer moves first (enter 'p')\nWho does move first: "
        answers_first_move = ["p", "a"]
        while True:
            answer_game = self.get_input(
                message=message_game,
                answers=answers_game,
            )
            # Quit the game
            if answer_game == "q":
                return
            # Start the game
            if answer_game == "g":
                answer_player = self.get_input(
                    message=message_player,
                    answers=answers_player,
                )
                type_ = answer_player
                # 1-Player
                if answer_player == "1":
                    answer_difficulty = self.get_input(
                        message=message_difficulty,
                        answers=answers_difficulty,
                    )
                    answer_first_move = self.get_input(
                        message=message_first_move,
                        answers=answers_first_move,
                    )
                    type_ = answer_difficulty
                    # Easy
                    if answer_difficulty == "e":
                        self.play_game(type_=type_, first_move=answer_first_move)
                    # Hard
                    if answer_difficulty == "h":
                        self.play_game(type_=type_, first_move=answer_first_move)
                # 2-Player
                if answer_player == "2":
                    self.play_game(type_=type_)
                print()


if __name__ == "__main__":
    connect4 = Connect4()
    connect4.run()
