from constx import is_piece, WHITE, BLACK

class Piece:
    def __init__(self, color: chr, piece_notation: chr, image_id: int, x: int, y: int) -> None:
        weights = {"Q": 9.75, "R": 5, "N": 3.25, "B": 3.25, "P": 1, "K": float("inf")}
        self.color = color
        self.name = color + piece_notation
        self.weight = weights[piece_notation]
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.moves = []
        self.image_id = image_id

    def __repr__(self) -> str:
        return f"{self.name}" #- {self.position}"

    def is_valid(self, x: int, y: int, board: list[list[str]], board_size: int) -> bool:
        if not 0 <= x < board_size or not 0 <= y < board_size:
            return False

        if board[x][y] == ".":
            return True

        if self.can_take(x, y, board):
            return True

        return False


    def can_take(self, x: int, y: int, board: list[list[str]]):
        """ can take a piece?"""
        if is_piece(board, x, y) and board[x][y].color != self.color:
            return True

        return False

    def make_move(self, x: int, y: int, board: list[list[str]]):
        board[x][y] = self.name

    def get_moves(self, board: list[list[str]], board_size: int) -> list[tuple] | None:
        return None

    def update_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.position = (x, y)

    def undo_move(self):
        pass


class Knight(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "N"
        super().__init__(color, piece_notation, image_id, x ,y)
        self.moves = [
            (+1, +2),
            (+1, -2),
            (-1, +2),
            (-1, -2),
            (+2, +1),
            (+2, -1),
            (-2, +1),
            (-2, -1)
        ]
    
    def get_moves(self, board: list[list[str]], board_size: int) -> list[tuple]:
        valid_moves = []
        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            if self.is_valid(x, y, board, board_size):
                valid_moves.append((x, y))

        return valid_moves

class Bishop(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "B"
        super().__init__(color, piece_notation, image_id, x, y)
        # possible implementation
        self.moves = [
            (+1, +1),
            (+1, -1),
            (-1, -1),
            (-1, +1)
        ]

    def get_moves(self, board: list[list[str]], board_size: int) -> list[tuple]:
        valid_moves = []
        row, col = self.x - 1, self.y + 1
        while row >= 0 and col < board_size:
            if board[row][col] != ".":
                if self.can_take(row, col, board):
                    valid_moves.append((row, col))
                break

            valid_moves.append((row, col))
            row -= 1
            col += 1

        # Check diagonal moves to the top-left
        row, col = self.x - 1, self.y - 1
        while row >= 0 and col >= 0:
            if board[row][col] != ".":
                if self.can_take(row, col, board):
                    valid_moves.append((row, col))
                break

            valid_moves.append((row, col))
            row -= 1
            col -= 1

        # Check diagonal moves to the bottom-right
        row, col = self.x + 1, self.y + 1
        while row < board_size and col < board_size:
            if board[row][col] != ".":
                if self.can_take(row, col, board):
                    valid_moves.append((row, col))
                break

            valid_moves.append((row, col))
            row += 1
            col += 1

        # Check diagonal moves to the bottom-left
        row, col = self.x + 1, self.y - 1
        while row < board_size and col >= 0:
            if board[row][col] != ".":
                if self.can_take(row, col, board):
                    valid_moves.append((row, col))
                break

            valid_moves.append((row, col))
            row += 1
            col -= 1

        return valid_moves


class Rook(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "R"
        super().__init__(color, piece_notation, image_id, x, y)


class Queen(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "Q"
        super().__init__(color, piece_notation, image_id, x, y)


class King(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "K"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [(1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def can_take(self, x: int, y: int, board: list[list[str]]):
        # if protected false
        return super().can_take(x, y, board)

    def get_moves(self, board: list[list[str]], board_size: int) -> list[tuple] | None:
        valid_moves = []
        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            if self.is_valid(x, y, board, board_size):
                valid_moves.append((x, y))

        return valid_moves

class Pawn(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "P"
        super().__init__(color, piece_notation, image_id, x, y)
        self.init_position = True
        self.moves = [(1, 0), (2, 0)] if color == BLACK else [(-1, 0), (-2, 0)]

    def is_valid(self, x: int, y: int, board: list[list[str]], board_size: int) -> bool:
        if not 0 <= x < board_size or not 0 <= y < board_size:
            return False

        if board[x][y] == ".":
            return True

        return False

    def get_moves(self, board: list[list[str]], board_size: int) -> list[tuple]:
        valid_moves = []
        if self.is_valid(self.x + self.moves[0][0], self.y, board, board_size):
            valid_moves.append((self.x + self.moves[0][0], self.y))

        if self.init_position:
            if len(valid_moves) >= 1:
                x = self.x + self.moves[1][0]
                y = self.y + self.moves[1][1]
                if self.is_valid(x, y, board, board_size):
                    valid_moves.append((x, y))

        take_moves = [(1, -1), (1, 1)] if self.color == BLACK else [(-1, -1), (-1, 1)]
        for dx, dy in take_moves:
            if self.can_take(self.x + dx, self.y + dy, board):
                valid_moves.append((self.x + dx, self.y + dy))

        return valid_moves