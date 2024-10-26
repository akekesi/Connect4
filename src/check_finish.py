"""
Module for checking the game status in a Connect4 board.

This module provides functions to check for a winning condition (horizontal, vertical, diagonal)
or a full board in a Connect4 game. It evaluates if a player has won by placing a certain number
of their discs (based on the win condition) in a row in different orientations or if the board 
is completely filled, resulting in a draw.
"""

import numpy as np


# pylint: disable=too-many-return-statements
def check_finish(board: np.ndarray, disc: int, win: int) -> int:
    """
    Check if the game has reached a winning or full condition.

    This function checks the board for any winning condition (horizontal, vertical, or diagonal)
    based on the specified number of discs required to win (win argument).
    It also checks if the board is full, resulting in a draw.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.
        disc (int): The disc value representing the current player's disc.
        win (int): The number of discs in a row required to win.

    Returns:
        int: Returns the disc value if the player has won, 0 if the board is full (draw), 
             or -1 if the game is still ongoing.
    """
    if disc == check_finish_horizontal(board=board, disc=disc, win=win):
        return disc
    if disc == check_finish_vertical(board=board, disc=disc, win=win):
        return disc
    if disc == check_finish_diagonal_left_pos(board=board, disc=disc, win=win):
        return disc
    if disc == check_finish_diagonal_right_neg(board=board, disc=disc, win=win):
        return disc
    if disc == check_finish_diagonal_top_pos(board=board, disc=disc, win=win):
        return disc
    if disc == check_finish_diagonal_top_neg(board=board, disc=disc, win=win):
        return disc
    return check_finish_full(board=board)


def check_finish_horizontal(board: np.ndarray, disc: int, win: int) -> int:
    """
    Check for a horizontal win condition.

    This function scans the board for a sequence of discs in a row horizontally
    based on the win argument.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.
        disc (int): The disc value representing the current player's disc.
        win (int): The number of discs in a row required to win.

    Returns:
        int: The disc value if a horizontal win is found, or -1 if no win is found.
    """
    (row, col) = board.shape
    for r in range(row):
        win_ = 0
        for c in range(col):
            if board[r, c] == disc:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return disc
    return -1


def check_finish_vertical(board: np.ndarray, disc: int, win: int) -> int:
    """
    Check for a vertical win condition.

    This function scans the board for a sequence of discs in a row vertically
    based on the win argument.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.
        disc (int): The disc value representing the current player's disc.
        win (int): The number of discs in a row required to win.

    Returns:
        int: The disc value if a vertical win is found, or -1 if no win is found.
    """
    (row, col) = board.shape
    for c in range(col):
        win_ = 0
        for r in range(row):
            if board[r, c] == disc:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return disc
    return -1


def check_finish_diagonal_left_pos(board: np.ndarray, disc: int, win: int) -> int:
    """
    Check for a diagonal win condition (from top-left to bottom-right in the left section).

    This function scans the board for a sequence of discs in a row in the top-left to
    bottom-right diagonal direction in the left section, based on the win argument.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.
        disc (int): The disc value representing the current player's disc.
        win (int): The number of discs in a row required to win.

    Returns:
        int: The disc value if a diagonal win is found, or -1 if no win is found.
    """
    (row, col) = board.shape
    for r in range(row):
        win_ = 0
        for c in range(col):
            if row <= r + c:
                break
            if board[r + c, c] == disc:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return disc
    return -1


def check_finish_diagonal_right_neg(board: np.ndarray, disc: int, win: int) -> int:
    """
    Check for a diagonal win condition (from top-right to bottom-left in the right section).

    This function scans the board for a sequence of discs in a row in the top-right to
    bottom-left diagonal direction in the right section, based on the win argument.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.
        disc (int): The disc value representing the current player's disc.
        win (int): The number of discs in a row required to win.

    Returns:
        int: The disc value if a diagonal win is found, or -1 if no win is found.
    """
    (row, col) = board.shape
    for r in range(row):
        win_ = 0
        for c in range(col):
            if row <= r + c:
                break
            if board[r + c, col - 1 - c] == disc:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return disc
    return -1


def check_finish_diagonal_top_pos(board: np.ndarray, disc: int, win: int) -> int:
    """
    Check for a diagonal win condition (from top-left to bottom-right in the top section).

    This function scans the board for a sequence of discs in a row in the top-left to
    bottom-right diagonal direction in the top section, based on the win argument.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.
        disc (int): The disc value representing the current player's disc.
        win (int): The number of discs in a row required to win.

    Returns:
        int: The disc value if a diagonal win is found, or -1 if no win is found.
    """
    (row, col) = board.shape
    for c in range(col):
        win_ = 0
        for r in range(row):
            if col <= r + c:
                break
            if board[r, c + r] == disc:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return disc
    return -1


def check_finish_diagonal_top_neg(board: np.ndarray, disc: int, win: int) -> int:
    """
    Check for a diagonal win condition (from top-right to bottom-left in the top section).

    This function scans the board for a sequence of discs in a row in the top-right to
    bottom-left diagonal direction in the top section, based on the win argument.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.
        disc (int): The disc value representing the current player's disc.
        win (int): The number of discs in a row required to win.

    Returns:
        int: The disc value if a diagonal win is found, or -1 if no win is found.
    """
    (row, col) = board.shape
    for c in range(col):
        win_ = 0
        for r in range(row):
            if col <= r + c:
                break
            if board[r, col - 1 - c - r] == disc:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return disc
    return -1


def check_finish_full(board) -> int:
    """
    Check if the board is full, indicating a draw.

    This function checks if there are any empty spaces left on the board. If the board is full,
    the game ends in a draw.

    Args:
        board (np.ndarray): The game board represented as a NumPy array.

    Returns:
        int: Returns 0 if the board is full (draw), or -1 if the game is still ongoing.
    """
    (row, col) = board.shape
    nonzero_list = np.nonzero(board)[0]
    if np.size(nonzero_list) == row * col:
        return 0
    return -1
