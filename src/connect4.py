# TODO: use enum for players' discs
# TODO: agent minimax / alpha-beta
# TODO: put agents in folders like isis example
# TODO: option for selection of beginner player
# TODO: mark the winning discs
"""
"""


import os
import random
import logging

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
        if check_winner(board=self.board, player="X", win=self.win):
            return self.row * self.col
        if check_winner(board=self.board, player="O", win=self.win):
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

    def turn_easy(self, player: str) -> None:
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

    def turn_hard(self, player: str) -> None:
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

    def play_game(self, type_: str) -> None:
        """
        """
        logger.debug("0")
        self.init_board()
        turn = 0
        player = "X"
        self.display_board(turn=turn)
        while True:
            turn += 1
            if type_ == "2":
                self.turn_player(player=player)
            if type_ == "e":
                if player == "X":
                    self.turn_player(player=player)
                else:
                    self.turn_easy(player=player)
            if type_ == "h":
                if player == "X":
                    self.turn_hard(player=player)
                else:
                    self.turn_player(player=player)
            self.display_board(turn=turn)
            if check_winner(board=self.board, player=player, win=self.win):
                win_str = f"Player-{player} won."
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
            player = "O" if player == "X" else "X"

    def run(self) -> None:
        """
        """
        logger.debug("0")
        while True:
            msg_game = "Start a new game (enter 'g')"
            msg_quit = "Quit the program (enter 'q')"
            msg_game_1_player = "Play in 1-Player mode (enter '1')"
            msg_game_2_player = "Play in 2-Player mode (enter '2')"
            msg_game_easy = "Choose Easy difficulty (enter 'e')"
            msg_game_hard = "Choose Hard difficulty (enter 'h')"

            print(msg_game)
            print(msg_quit)

            answer = input("Enter your choice: ")
            print()
            if answer == "q":
                logger.debug("1")
                return
            if answer == "g":
                print(msg_game_1_player)
                print(msg_game_2_player)
                answer = input("Select mode: ")
                print()
                if answer == "1":
                    print(msg_game_easy)
                    print(msg_game_hard)
                    answer = input("Choose difficulty: ")
                    print()
                    if answer == "e":
                        self.play_game(type_=answer)
                    if answer == "h":
                        self.play_game(type_=answer)
                if answer == "2":
                    self.play_game(type_=answer)
                print()


if __name__ == "__main__":
    connect4 = Connect4()
    connect4.run()
