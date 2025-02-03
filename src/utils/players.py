"""
This module defines an enumeration for player tokens used in a game.
"""

from enum import Enum


class Players(Enum):
    """
    Enumeration for player tokens.

    Attributes:
        P1 (str): Token for Player 1 ('X').
        P2 (str): Token for Player 2 ('O').
        EMPTY (str): Token for an empty cell (' ').
    """
    P1 = "X"
    P2 = "O"
    EMPTY = " "
