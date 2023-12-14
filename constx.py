BLACK = "b"
WHITE = "w"

def is_piece(board: list[list[str]], x: int, y: int) -> bool:
    if hasattr(board[x][y], "name"):
        return True
    else:
        return False