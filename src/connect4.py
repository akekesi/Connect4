# TODO: agent minimax / alpha-beta
# TODO: put agents in folders like isis example
# TODO: option for selection of beginner player
# TODO: mark the winning discs
"""
"""

import os
import random
import logging

from src.logger_config import Logging
from src.check_end import check_winner, check_full


# set logger up
logger = Logging().set_logger(
    name="Connect4",
    # level=logging.NOTSET,
    level=logging.INFO,
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
                return row_free
        logger.info("%d", row)
        logger.debug("1")
        return row

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

    def make_move(self, player: str, col: int) -> bool:
        """
        """
        logger.debug("0")

        move = self.check_move(col=col)
        if not isinstance(move, tuple):
            logger.debug("1")
            return False
        self.move(player=player, move=move)
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
        print("|=============|")
        for row in self.board:
            print("|" + " ".join(row) + "|")
        print("|=============|")
        print("|0 1 2 3 4 5 6|")
        print(f"|{f'Turn:{turn:02}':=^13}|")
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
        print(f"Enter column number to set '{player}' of player-{player}: ")
        valid_moves = self.get_valid_moves()
        move = random.choice(valid_moves)
        self.move(player=player, move=move)
        logger.info("move(%d, %d) is done", move[0], move[1])
        logger.debug("1")

    def turn_hard(self, player: str) -> None:
        """
        """
        raise NotImplementedError
        # logger.debug("0")
        # print(f"Enter column number to set '{self.tiles[disc]}' of player-{disc}: ")
        # row, col = ???
        # self.set_disc(player=player, row=row, col=col)
        # logger.info("move(%d, %d) is done", row, col)
        # logger.debug("1")

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
                    self.turn_player(player=player)
                else:
                    self.turn_hard(player=player)
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
            msg_game = "Game: g"
            msg_quit = "Quit: q"
            msg_game_1_player = "1-Player: 1"
            msg_game_2_player = "2-Player: 2"
            msg_game_easy = "Easy: e"
            msg_game_hard = "Hard: h"

            print(msg_game)
            print(msg_quit)

            answer = input()
            if answer == "q":
                logger.debug("1")
                return
            if answer == "g":
                print(msg_game_1_player)
                print(msg_game_2_player)
                answer = input()
                if answer == "1":
                    print(msg_game_easy)
                    print(msg_game_hard)
                    answer = input()
                    if answer == "e":
                        self.play_game(type_=answer)
                    if answer == "h":
                        self.play_game(type_=answer)
                if answer == "2":
                    self.play_game(type_=answer)


if __name__ == "__main__":
    connect4 = Connect4()
    connect4.run()
