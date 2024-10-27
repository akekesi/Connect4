# TODO: agent minimax / alpha-beta
# TODO: game selection of start
# TODO: mark the winning discs

"""
Connect4 Game Module

This module provides an implementation of the Connect4 game. It allows players
to place discs into a grid, following the rules of the game. The module uses
NumPy to manage the board and contains functions to check valid moves, place discs,
and manage the game state.

Classes:
    Connect4: Represents the Connect4 game board and logic for making moves.

Example usage:
    connect4 = Connect4()
    connect4.run()
"""

import os
import random
import logging
import numpy as np

from typing import List
from src.logger_config import Logging
from src.check_finish import check_finish


# set logger up
logger = Logging().set_logger(
    name="Connect4",
    # level=logging.NOTSET,
    level=logging.INFO,
    # level=logging.DEBUG,
    path_dir=os.path.join(os.path.dirname(__file__), "..", "logs")
)


class Connect4:
    """A class to represent the Connect4 game board and logic."""

    def __init__(self) -> None:
        """
        Initializes the Connect4 board with 6 rows and 7 columns, 
        and sets the board to be empty (represented by zeros).
        Disc of player-1: (int) 1
        Disc of player-2: (int) 2
        """
        logger.debug("0")
        self.row = 6
        self.col = 7
        self.win = 4
        self.discs = [1, 2]
        self.tiles = {
            0: " ",
            1: "x",
            2: "o",
        }
        self.init_board()
        logger.info("board is initialized")
        logger.debug("1")

    def init_board(self) -> None:
        """
        Initializes an empty Connect4 board represented by a 2D NumPy array 
        with dimensions defined by the number of rows and columns. Each cell 
        is initialized to zero, indicating an empty space.
        """
        logger.debug("0")
        self.board = np.zeros((self.row, self.col))
        logger.debug("1")

    def set_disc(self, disc: int, row: int, col: int) -> None:
        """
        Places a disc on the board at the specified row and column.

        Args:
            disc (int): The player's disc (1 or 2).
            row (int): The row to place the disc in.
            col (int): The column to place the disc in.
        """
        logger.debug("0")
        self.board[row, col] = disc
        logger.info("disc-%s is set into (%d, %d)", self.tiles[disc], row, col)
        logger.debug("1")

    def get_row(self, col: int) -> int:
        """
        Returns the lowest available row in the specified column 
        where a disc can be placed.

        Args:
            col (int): The column to check.

        Returns:
            int: The index of the lowest available row. If the column 
            is empty, returns the last row. If not, returns the row 
            just above the first occupied row.
        """
        logger.debug("0")
        nonzero_list = np.nonzero(self.board[:, col])[0]
        if np.size(nonzero_list) == 0:
            row = self.row - 1
        else:
            row = int(nonzero_list[0]) - 1
        logger.info("%d", row)
        logger.debug("1")
        return row

    def get_valid_moves(self) -> List:
        """
        Returns a list of valid moves, where a move is represented as a 
        list containing the row and column index.

        Returns:
            List: A list of lists, each containing the row and column 
                index for a valid move.
        """
        logger.debug("0")
        valid_moves = []
        for col in range(self.col):
            row = self.get_row(col=col)
            if self.check_valid_row(row=row):
                valid_moves.append([row, col])
        logger.debug("1")
        return valid_moves

    def check_valid_row(self, row: int) -> bool:
        """
        Checks if the given row index is valid (within board bounds).

        Args:
            row (int): The row index to check.

        Returns:
            bool: True if the row index is valid, False otherwise.
        """
        logger.debug("0")
        valid = 0 <= row < self.row
        logger.info("%s", valid)
        logger.debug("1")
        return valid

    def check_valid_col(self, col: int) -> bool:
        """
        Checks if the given column index is valid (within board bounds).

        Args:
            col (int): The column index to check.

        Returns:
            bool: True if the column index is valid, False otherwise.
        """
        logger.debug("0")
        valid = 0 <= col < self.col
        logger.info("%s", valid)
        logger.debug("1")
        return valid

    def check_valid_input(self, input_: str) -> bool:
        """
        Checks if the input string can be converted to an integer, 
        representing a valid column input.

        Args:
            input_ (str): The input string to validate.

        Returns:
            bool: True if the input is valid, False otherwise.
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

    def move(self, disc: int, col: int) -> bool:
        """
        Makes a move by placing a disc in the specified column 
        if the column and row are valid.

        Args:
            disc (int): The player's disc (1 or 2).
            col (int): The column to place the disc in.

        Returns:
            bool: True if the move is valid and successful, False otherwise.
        """
        logger.debug("0")
        if not self.check_valid_col(col=col):
            logger.info("invalid col = %d", col)
            logger.debug("1")
            return False

        row = self.get_row(col=col)
        if not self.check_valid_row(row=row):
            logger.info("invalid row = %d", row)
            logger.debug("2")
            return False

        self.set_disc(disc=disc, row=row, col=col)
        logger.info("move(%d, %d) is done", row, col)
        logger.debug("3")
        return True

    def turn_player(self, disc: int) -> None:
        """
        Handles the player's turn by prompting for a column input and 
        making the move if valid.

        Args:
            disc (int): The player's disc (1 or 2).
        """
        logger.debug("0")
        while True:
            input_ = input(f"Enter column number to set '{self.tiles[disc]}' of player-{disc}: ")
            if not self.check_valid_input(input_=input_):
                continue
            col = int(input_)
            move_info = self.move(disc=disc, col=col)
            if not move_info:
                logger.info("invalid move.")
                continue
            break
        logger.debug("1")

    def turn_easy(self, disc: int) -> None:
        """
        Executes a turn for the computer player in "easy" mode, where 
        a random valid move is selected.

        Args:
            disc (int): The player's disc (1 or 2).
        """
        logger.debug("0")
        print(f"Enter column number to set '{self.tiles[disc]}' of player-{disc}: ")
        valid_moves = self.get_valid_moves()
        row, col = random.choice(valid_moves)
        self.set_disc(disc=disc, row=row, col=col)
        logger.info("move(%d, %d) is done", row, col)
        logger.debug("1")

    def turn_hard(self, disc: int) -> None:
        """
        Executes a turn for the computer player in "hard" mode.
        # TODO: update this after implementation

        Args:
            disc (int): The player's disc (1 or 2).
        """
        raise NotImplementedError
        # logger.debug("0")
        # print(f"Enter column number to set '{self.tiles[disc]}' of player-{disc}: ")
        # row, col = ???
        # self.set_disc(disc=disc, row=row, col=col)
        # logger.info("move(%d, %d) is done", row, col)
        # logger.debug("1")

    def game(self, type_: str) -> None:
        """
        Manages the flow of the game, allowing for different player 
        configurations such as single-player, two-player, and AI modes.

        Args:
            type_ (str): Type of game mode:
                            "2" for two-player 
                            "e" for single-player easy
                            "h" for single-player hard
        """
        logger.debug("0")
        self.init_board()
        turn = 0
        self.print_pritty(turn=turn)
        while True:
            disc = self.discs[turn % 2]
            turn += 1
            if type_ == "2":
                self.turn_player(disc=disc)
            if type_ == "e":
                if disc == self.discs[0]:
                    self.turn_player(disc=disc)
                else:
                    self.turn_easy(disc=disc)
            if type_ == "h":
                if disc == self.discs[0]:
                    self.turn_player(disc=disc)
                else:
                    self.turn_hard(disc=disc)
            self.print_pritty(turn=turn)
            win = check_finish(board=self.board, disc=disc, win=self.win)
            if win == disc:
                win_str = f"Player-{disc} won."
                print(win_str)
                logger.info(win_str)
                logger.debug("1")
                break
            if win == 0:
                win_str = "The board is full, resulting in a draw."
                print(win_str)
                logger.info(win_str)
                logger.debug("2")
                break

    def run(self) -> None:
        """
        Initiates the Connect4 game with menu prompts for selecting 
        game mode or quitting.
        """
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
                        self.game(type_=answer)
                    if answer == "h":
                        self.game(type_=answer)
                if answer == "2":
                    self.game(type_=answer)

    def print_pritty(self, turn: int) -> None:
        """
        Prints the current state of the game board in a formatted grid, 
        showing the current turn number and positions of player discs.

        Args:
            turn (int): The current turn number.

        Exaple:
        |==============|
        |              |
        |              |
        |    X X       |
        |    O X X     |
        |  O X O O     |
        |  O O X X     |
        |==============|
        |0 1 2 3 4 5 6 |
        """
        print("|=============|")
        for row in range(self.row):
            row_str = "|"
            for col in range(self.col):
                row_str += self.tiles[self.board[row, col]]
                if col < self.col - 1:
                    row_str += " "
                else:
                    row_str += "|"
            print(row_str)
        print("|=============|")
        print("|0 1 2 3 4 5 6|")
        print(f"|{f'Turn:{turn:02}':=^13}|")
        print()


if __name__ == "__main__":
    connect4 = Connect4()

    connect4.run()
