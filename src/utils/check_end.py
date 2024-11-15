"""
"""


# pylint: disable=too-many-return-statements
def check_winner(board: list[list[int]], player: str, win: int) -> bool:
    """
    """
    if check_winner_horizontal(board=board, player=player, win=win):
        return True
    if check_winner_vertical(board=board, player=player, win=win):
        return True
    if check_winner_diagonal_left_pos(board=board, player=player, win=win):
        return True
    if check_winner_diagonal_right_neg(board=board, player=player, win=win):
        return True
    if check_winner_diagonal_top_pos(board=board, player=player, win=win):
        return True
    if check_winner_diagonal_top_neg(board=board, player=player, win=win):
        return True
    return False

def check_winner_horizontal(board: list[list[int]], player: str, win: int) -> bool:
    """
    """
    row = len(board)
    col = len(board[0])
    for r in range(row):
        win_ = 0
        for c in range(col):
            if board[r][c] == player:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return True
    return False


def check_winner_vertical(board: list[list[int]], player: str, win: int) -> bool:
    """
    """
    row = len(board)
    col = len(board[0])
    for c in range(col):
        win_ = 0
        for r in range(row):
            if board[r][c] == player:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return True
    return False


def check_winner_diagonal_left_pos(board: list[list[int]], player: str, win: int) -> bool:
    """
    """
    row = len(board)
    col = len(board[0])
    for r in range(row):
        win_ = 0
        for c in range(col):
            if row <= r + c:
                break
            if board[r + c][c] == player:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return True
    return False


def check_winner_diagonal_right_neg(board: list[list[int]], player: str, win: int) -> bool:
    """
    """
    row = len(board)
    col = len(board[0])
    for r in range(row):
        win_ = 0
        for c in range(col):
            if row <= r + c:
                break
            if board[r + c][col - 1 - c] == player:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return True
    return False


def check_winner_diagonal_top_pos(board: list[list[int]], player: str, win: int) -> bool:
    """
    """
    row = len(board)
    col = len(board[0])
    for c in range(col):
        win_ = 0
        for r in range(row):
            if col <= r + c:
                break
            if board[r][c + r] == player:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return True
    return False


def check_winner_diagonal_top_neg(board: list[list[int]], player: str, win: int) -> bool:
    """
    """
    row = len(board)
    col = len(board[0])
    for c in range(col):
        win_ = 0
        for r in range(row):
            if col <= r + c:
                break
            if board[r][col - 1 - c - r] == player:
                win_ += 1
            else:
                win_ = 0
            if win_ == win:
                return True
    return False


def check_full(board) -> bool:
    """
    Checks if the board is full, meaning no empty cells remain.

    Returns:
        bool: True if all cells are filled, False if there are any empty cells.
    """
    return not any(cell == " " for row in board for cell in row)
