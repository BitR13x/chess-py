BLACK = "b"
WHITE = "w"

CHECKMATE = "checkmate"
STALEMATE = "stalemate"
IN_PROGRESS = "in_progress"


def is_piece(board: list[list[str]], x: int, y: int) -> bool:
    if hasattr(board[x][y], "name"):
        return True
    else:
        return False
