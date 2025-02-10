"""Generate test data for the Connect4 game."""


import os
import csv
import numpy as np
import pandas as pd

from src.mcts.mcts import MCTS
from src.utils.players import Players
from src.connect4.connect4_mcts import Connect4
from sklearn.model_selection import train_test_split
from itertools import combinations_with_replacement, permutations


ROWS = 6
COLS = 7
N_SAMPLES = 7 # Number of samples to generate
SIZE_TEST = 0.2
RANDOM_STATE = 42
TURNS = ["X", "X", "X", "O", "O", "O"]
PATH_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PATH_CONNECT4_BOARDS_ALL = os.path.join(PATH_DATA_DIR, "boards", f"connect4_boards_t{len(TURNS)}_all.csv")
PATH_CONNECT4_BOARDS_N_SAMPLES = os.path.join(PATH_DATA_DIR, "boards", f"connect4_boards_t{len(TURNS)}_{N_SAMPLES}.csv")


def valid_board(placements: list[tuple[str, int]]) -> tuple:
    """Check if the board is valid (tokens must obey gravity) and pad columns to 6 elements."""
    board = [[] for _ in range(COLS)]  # Each column is a stack (list)
    
    for ball, col in placements:
        if len(board[col]) >= ROWS:  # If column is full, discard this case
            return None
        board[col].append(ball)  # Add the ball to the column
    
    # Convert columns to tuples and pad them to 6 elements with " "
    return tuple(tuple(col + [Players.EMPTY.value] * (ROWS - len(col))) for col in board)


def generate_boards(turns: list) -> set:
    """Generate all valid board states for distributing 6 balls into 7 columns."""
    all_col_choices = combinations_with_replacement(range(COLS), len(turns))  # Choose columns (ignoring order)
    unique_boards = set()
    
    for col_choice in all_col_choices:
        for ball_permutation in set(permutations(turns)):  # Generate distinct ball orders
            placements = list(zip(ball_permutation, col_choice))  # Pair balls with column choices
            board = valid_board(placements)  # Validate stacking
            if board:
                unique_boards.add(board)
    return unique_boards


def random_sample(
    boards: tuple,
    n_samples: int,
    random_state: int,
) -> tuple:
    """Randomly sample n rows from a 3D tuple."""
    np.random.seed(random_state)
    boards = tuple(boards)
    indices = np.random.choice(len(boards), size=n_samples, replace=False)
    return tuple(boards[i] for i in indices)


def save_boards_to_csv(
    boards: set,
    path_csv: str,
) -> None:
    """Save the generated board states to a CSV file."""
    with open(path_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Write header (optional, but helpful)
        header = [f"R{r}C{c}" for r in range(ROWS) for c in range(COLS)]
        writer.writerow(header)
        
        # Write board states as flattened rows
        for board in boards:
            flattened_board = [board[c][r] for r in range(ROWS) for c in range(COLS)]  # Row-major flattening
            writer.writerow(flattened_board)


def split_csv(
    path_csv: str,
    test_size: float,
    random_state: int,
) -> tuple:
    """Splits a CSV file into training and testing datasets and saves them as separate CSV files."""
    # Load the dataset
    df = pd.read_csv(path_csv)

    # Split into train and test sets
    train, test = train_test_split(df, test_size=test_size, random_state=random_state)

    # Generate output file names
    path_csv_train = path_csv.replace(".csv", "_train.csv")
    path_csv_test = path_csv.replace(".csv", "_test.csv")

    # Save to CSV files
    train.to_csv(path_csv_train, index=False)
    test.to_csv(path_csv_test, index=False)

    return path_csv_train, path_csv_test


def add_best_move_to_board(path_boards: str) -> None:
    """Add the best move to the board."""
    df = pd.read_csv(path_boards)
    best_moves = []
    for data in df.values:
        game = Connect4()
        mcts = MCTS(
            game_constructor=Connect4,
            player_1=Players.P1.value,
            player_2=Players.P2.value,
            iterations=1000,
        )

        matrix = [data[::-1][i:i+7][::-1] for i in range(0, len(data), 7)]
        game.board = [list(row) for row in matrix]
        best_move = mcts.get_best_move(game=game)
        best_moves.append(best_move[1])

    df["best_move"] = best_moves
    df.to_csv(path_boards, index=False)


if __name__ == "__main__":
    # Generate and save boards
    boards = generate_boards(turns=TURNS)

    # Print some examples
    for board in list(boards)[:5]:
        print(board)

    # Save the boards to a CSV file
    save_boards_to_csv(
        boards=boards,
        path_csv=PATH_CONNECT4_BOARDS_ALL,
    )

    # Randomly sample 1000 boards
    boards_small = random_sample(
        boards=boards,
        n_samples=N_SAMPLES,
        random_state=RANDOM_STATE,
    )

    # Save the boards to a CSV file
    save_boards_to_csv(
        boards=boards_small,
        path_csv=PATH_CONNECT4_BOARDS_N_SAMPLES,
    )

    # Load the CSV file
    df = pd.read_csv(PATH_CONNECT4_BOARDS_N_SAMPLES)

    # Display the first few rows
    print(df.head())

    # Add the best move to the board
    add_best_move_to_board(path_boards=PATH_CONNECT4_BOARDS_N_SAMPLES)

    # Split the CSV file into training and testing datasets
    path_csv_train, path_csv_test = split_csv(
        path_csv=PATH_CONNECT4_BOARDS_N_SAMPLES,
        test_size=SIZE_TEST,
        random_state=RANDOM_STATE,
    )

    # Display the paths to the training and testing datasets
    print(f"{path_csv_train =}")
    print(f"{path_csv_test = }")

    # Load the training and testing datasets
    df_train = pd.read_csv(path_csv_train)
    df_test = pd.read_csv(path_csv_test)

    # Display the first few rows of the training and testing dataset
    print(df_train.head())
    print(df_test.head())
