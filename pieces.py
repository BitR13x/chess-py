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


    def can_take(self, x: int, y: int, board: list[list[str]]) -> bool:
        """ can take a piece?"""
        if is_piece(board, x, y) and board[x][y].color != self.color:
            return True

        return False

    #is_king_under_attack

    def is_king_attacked_with_move(self, x: int, y: int, board: list[list[str]], board_size: int, kings):
        # if attacking piece can now touch king
        if kings[self.color].attacked_by: #and not isinstance(self.attacked_by, King):
            if kings[self.color].attacked_by.position == (x, y):
                return False

            space = (board[x][y], (self.x, self.y))
            # pretend move piece
            board[self.x][self.y] = space[0]
            self.update_position(x, y)
            board[x][y] = self


            if kings[self.color].position in kings[self.color].attacked_by.get_moves(board, board_size, kings):
                board[x][y] = space[0]
                self.update_position(space[1][0], space[1][1])
                board[self.x][self.y] = self

                return True
            else:
                board[x][y] = space[0]
                self.update_position(space[1][0], space[1][1])
                board[self.x][self.y] = self

                return False
        else:
            return False

    def get_moves(self, board: list[list[str]], board_size: int, kings) -> list[tuple]:
        valid_moves = []
        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            while self.is_valid(x, y, board, board_size):
                if not self.is_king_attacked_with_move(x, y, board, board_size, kings):
                    valid_moves.append((x, y))

                if self.can_take(x, y, board):
                    break

                x += dx
                y += dy
        
        return valid_moves


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
    
    def get_moves(self, board: list[list[str]], board_size: int, kings) -> list[tuple]:
        valid_moves = []
        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            if self.is_valid(x, y, board, board_size):
                if not self.is_king_attacked_with_move(x, y, board, board_size, kings):
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


class Rook(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "R"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Queen(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "Q"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [(1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class King(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "K"
        super().__init__(color, piece_notation, image_id, x, y)
        self.init_position = True
        self.moves = [(1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.attacked_by = None


    def get_valid_moves(self, chessboard) -> bool:
        # oposite color
        moves = self.get_moves(chessboard.current_board, chessboard.height)
        pieces = chessboard.white_pieces if self.color == BLACK else chessboard.black_pieces

        for piece in pieces:
            if isinstance(piece, Pawn):
                protected = piece.get_taking_squares(chessboard.current_board, 
                                                     chessboard.height,
                                                     chessboard.kings)
            else:
                protected = piece.get_moves(chessboard.current_board,
                                            chessboard.height, 
                                            chessboard.kings)

            for move in moves:
                if move in protected:
                    moves.remove(move)

        return moves

    def castling_moves(self, board: list[list[str]]) -> list[tuple]:
        castling_moves = []
        if self.init_position:
            # ? need to check for valid if smaller table
            if isinstance(board[self.x][self.y + 3], Rook): # check for rook
                if board[self.x][self.y + 1] == "." and board[self.x][self.y + 2] == ".":
                    castling_moves.append((self.x, self.y + 2))
                
            if isinstance(board[self.x][self.y - 4], Rook):
                if board[self.x][self.y - 1] == "." and board[self.x][self.y - 2] == "." \
                    and board[self.x][self.y + 1] == ".":
                    castling_moves.append((self.x, self.y - 2))

        return castling_moves

    def is_valid(self, x: int, y: int, board: list[list[str]], board_size: int) -> bool:
        if not 0 <= x < board_size or not 0 <= y < board_size:
            return False

        if board[x][y] == ".":
            return True

        if self.can_take(x, y, board):
            return True

        return False

    def get_moves(self, board: list[list[str]], board_size: int, kings=None) -> list[tuple] | None:
        valid_moves = []
        valid_moves.extend(self.castling_moves(board))

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

    def get_taking_squares(self, board: list[list[str]], board_size: int, kings):
        valid_moves = []
        take_moves = [(1, -1), (1, 1)] if self.color == BLACK else [(-1, -1), (-1, 1)]
        for dx, dy in take_moves:
            if 0 <= self.x + dx < board_size and 0 <= self.y + dy < board_size:
                if self.can_take(self.x + dx, self.y + dy, board):
                    if not self.is_king_attacked_with_move(self.x + dx, self.y + dy, board, board_size, kings):
                        valid_moves.append((self.x + dx, self.y + dy))


        return valid_moves

    def get_moves(self, board: list[list[str]], board_size: int, kings) -> list[tuple]:
        valid_moves = []
        if self.is_valid(self.x + self.moves[0][0], self.y, board, board_size):
            if not self.is_king_attacked_with_move(self.x + self.moves[0][0], self.y, board, board_size, kings):
                valid_moves.append((self.x + self.moves[0][0], self.y))

        if self.init_position:
            if len(valid_moves) >= 1:
                x = self.x + self.moves[1][0]
                y = self.y + self.moves[1][1]
                if self.is_valid(x, y, board, board_size):
                    if not self.is_king_attacked_with_move(x, y, board, board_size, kings):
                        valid_moves.append((x, y))

        valid_moves.extend(self.get_taking_squares(board, board_size, kings))

        return valid_moves