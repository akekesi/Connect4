"""
Module to run a Connect4 game.
"""

from src.connect4.connect4 import Connect4


def run_connect4() -> None:
    """
    Initializes a Connect4 game and runs the main game loop.

    This function creates an instance of the Connect4 class and calls its
    `run` method to start and manage the game. It is designed to be called
    as the main function for the game application.
    """
    connect4 = Connect4()
    connect4.run()


if __name__ == "__main__":
    # Run the Connect4 game when the script is executed
    run_connect4()
