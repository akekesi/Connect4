# TODO: mark the winning discs
"""
"""


import os
import random
import logging

from enum import Enum
from src.minimax import Minimax
from src.logger_config import Logging
from src.check_end import check_winner, check_full


# set logger up
logger = Logging().set_logger(
    name="Connect4",
    level=logging.NOTSET,
    # level=logging.INFO,
    # level=logging.DEBUG,
    path_dir=os.path.join(os.path.dirname(__file__), "..", "logs")
)


class Player(Enum):
    P1 = "X"
    P2 = "O"


class Connect4:
    """
    """

    def __init__(self) -> None:
        """
        """
        logger.debug("0")
        self.row = 6
        self.col = 7
        self.win = 4
        self.board = None
        self.depth_max = 5
        self.init_board()
        logger.info("board is initialized")
        logger.debug("1")

    def init_board(self) -> None:
        """
        """
        logger.debug("0")
        self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]
        logger.debug("1")

    def move(self, move: tuple[int, int], player: str) -> None:
        """
        """
        logger.debug("0")
        self.board[move[0]][move[1]] = player
        logger.info("player-%s is moved into (%d, %d)", player, move[0], move[1])
        logger.debug("1")

    def remove(self, move: tuple[int, int]) -> None:
        """
        """
        logger.debug("0")
        player = self.board[move[0]][move[1]]
        self.board[move[0]][move[1]] = " "
        logger.info("player-%s is removed from (%d, %d)", player, move[0], move[1])
        logger.debug("1")

    def get_row(self, col: int) -> int:
        """
        """
        logger.debug("0")
        row_free = -1
        for row in range(self.row):
            if self.board[row][col] == " ":
                row_free = row
            else:
                break
        logger.info("%d", row_free)
        logger.debug("1")
        return row_free

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """
        """
        logger.debug("0")
        valid_moves = []
        for col in range(self.col):
            row = self.get_row(col=col)
            if self.check_row(row=row):
                valid_moves.append((row, col))
        logger.debug("1")
        return valid_moves

    def check_row(self, row: int) -> bool:
        """
        """
        logger.debug("0")
        valid = 0 <= row < self.row
        logger.info("%s", valid)
        logger.debug("1")
        return valid

    def check_col(self, col: int) -> bool:
        """
        """
        logger.debug("0")
        valid = 0 <= col < self.col
        logger.info("%s", valid)
        logger.debug("1")
        return valid

    def check_move(self, col: int) -> tuple[int, int] | None:
        """
        """
        logger.debug("0")
        if not self.check_col(col=col):
            logger.info("invalid col = %d", col)
            logger.debug("1")
            return None
        row = self.get_row(col=col)
        if not self.check_row(row=row):
            logger.info("invalid row = %d", row)
            logger.debug("2")
            return None
        return (row, col)

    def check_input(self, input_: str) -> bool:
        """
        """
        logger.debug("0")
        try:
            int(input_)
            logger.info("True")
            logger.debug("1")
            return True
        except ValueError:
            logger.info("False")
            logger.debug("2")
            return False

    def check_winner(self, player: str) -> bool:
        """
        Checks if the specified player has won the game.

        Args:
            player (str): The symbol of the player to check ('X' or 'O').

        Returns:
            bool: True if the player has won, False otherwise.
        """
        return check_winner(board=self.board, player=player, win=self.win)

    def check_full(self) -> bool:
        """
        Checks if the board is full, meaning no empty cells remain.

        Returns:
            bool: True if all cells are filled, False if there are any empty cells.
        """
        return check_full(board=self.board)

    def evaluate(self) -> int:
        """
        Evaluates the board for game state.

        Returns:
            int: 1 if 'X' wins, -1 if 'O' wins, 0 for a draw.
        """
        if check_winner(board=self.board, player=Player.P1.value, win=self.win):
            return self.row * self.col
        if check_winner(board=self.board, player=Player.P2.value, win=self.win):
            return -self.row * self.col
        return 0

    def make_move(self, player: str, col: int) -> bool:
        """
        """
        logger.debug("0")
        move = self.check_move(col=col)
        if not isinstance(move, tuple):
            logger.debug("1")
            return False
        self.move(move=move, player=player)
        logger.info("move(%d, %d) is done", move[0], move[1])
        logger.debug("2")
        return True

    def display_board(self, turn: int) -> None:
        """
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
        logger.debug("0")
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
        logger.debug("1")

    def turn_player(self, player: str) -> None:
        """
        """
        logger.debug("0")
        while True:
            input_ = input(f"Enter column number to set '{player}' of player-{player}: ")
            if not self.check_input(input_=input_):
                continue
            col = int(input_)
            move_info = self.make_move(player=player, col=col)
            if not move_info:
                logger.info("invalid move.")
                continue
            break
        logger.debug("1")

    def turn_agent_easy(self, player: str) -> None:
        """
        """
        logger.debug("0")
        print(f"Enter column number to set '{player}' of player-{player}: ", end="")
        valid_moves = self.get_valid_moves()
        move = random.choice(valid_moves)
        print(f"{move[1]}")
        self.move(move=move, player=player)
        logger.info("move(%d, %d) is done", move[0], move[1])
        logger.debug("1")

    def turn_agent_hard(self, player: str) -> None:
        """
        """
        logger.debug("0")
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
        logger.info("move(%d, %d) is done", move[0], move[1])
        logger.debug("1")

    def play_game(self, type_: str, first_move: str = "") -> None:
        """
        """
        logger.debug("0")
        self.init_board()
        turn = 0
        player = Player.P1
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
                    if player == Player.P1:
                        self.turn_player(player=player.value)
                    else:
                        self.turn_agent_easy(player=player.value)
                # First move: agent
                if first_move == "a":
                    if player == Player.P1:
                        self.turn_agent_easy(player=player.value)
                    else:
                        self.turn_player(player=player.value)
            # 1-Player-Hard
            if type_ == "h":
                # First move: player
                if first_move == "p":
                    if player == Player.P1:
                        self.turn_player(player=player.value)
                    else:
                        self.turn_agent_hard(player=player.value)
                # First move: agent
                if first_move == "a":
                    if player == Player.P1:
                        self.turn_agent_hard(player=player.value)
                    else:
                        self.turn_player(player=player.value)
            self.display_board(turn=turn)
            if check_winner(board=self.board, player=player.value, win=self.win):
                win_str = f"Player-{player.value} won."
                print(win_str)
                logger.info(win_str)
                logger.debug("1")
                break
            if check_full(board=self.board):
                win_str = "The board is full, resulting in a draw."
                print(win_str)
                logger.info(win_str)
                logger.debug("2")
                break
            player = Player.P2 if player == Player.P1 else Player.P1

    def get_input(self, message: str, answers: list[str], message_error: str = "Try again") -> str:
        """
        """
        logger.debug("0")
        while True:
            answer = input(message)
            logger.info(answer)
            if answer in answers:
                print()
                logger.debug("1")
                return answer
            print(message_error)
            print()

    def run(self) -> None:
        """
        """
        logger.debug("0")
        while True:
            message_game = "Start a new game (enter 'g')\nQuit the program (enter 'q')\nEnter your choice: "
            answers_game = ["g", "q"]
            message_player = "Play in 1-Player mode (enter '1')\nPlay in 2-Player mode (enter '2')\nSelect mode: "
            answers_player = ["1", "2"]
            message_difficulty = "Easy difficulty (enter 'e')\nHard difficulty (enter 'h')\nChoose difficulty: "
            answers_difficulty = ["e", "h"]
            message_first_move = "Agent moves first (enter 'a')\nPlayer moves first (enter 'p')\nWho does move first: "
            answers_first_move = ["p", "a"]

            answer_game = self.get_input(
                message=message_game,
                answers=answers_game,
            )
            # Quit the game
            if answer_game == "q":
                logger.debug("1")
                return
            # Start the game
            if answer_game == "g":
                answers_player = self.get_input(
                    message=message_player,
                    answers=answers_player,
                )
                type_ = answers_player
                # 1-Player
                if answers_player == "1":
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
                if answers_player == "2":
                    self.play_game(type_=type_)
                print()


if __name__ == "__main__":
    connect4 = Connect4()
    connect4.run()
