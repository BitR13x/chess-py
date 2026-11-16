from constx import is_piece, WHITE, BLACK


class Piece:
    def __init__(
        self, color: chr, piece_notation: chr, image_id: int, x: int, y: int
    ) -> None:
        weights = {
            "Q": 9.75,
            "R": 5,
            "N": 3.25,
            "B": 3.25,
            "P": 1,
            "K": float("inf"),
        }
        self.color = color
        self.name = color + piece_notation
        self.weight = weights[piece_notation]
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.moves = []
        self.image_id = image_id
        self.has_moved = False  # castling, en passant

    def __repr__(self) -> str:
        return f"{self.name}"  # - {self.position}"

    def is_valid(
        self, x: int, y: int, board: list[list[str]], board_size: int
    ) -> bool:
        if not 0 <= x < board_size or not 0 <= y < board_size:
            return False

        if board[x][y] == ".":
            return True

        if self.can_take(x, y, board):
            return True

        return False

    def can_take(self, x: int, y: int, board: list[list[str]]) -> bool:
        """can take a piece?"""
        if is_piece(board, x, y) and board[x][y].color != self.color:
            return True

        return False

    def would_leave_king_in_check(
        self, x: int, y: int, board: list[list[str]], board_size: int, kings
    ) -> bool:
        """Simulate the move and check if our king would be in check"""
        # Save the current state
        original_pos = (self.x, self.y)
        captured_piece = board[x][y]

        # Make the move temporarily
        board[self.x][self.y] = "."
        original_x, original_y = self.x, self.y
        self.update_position(x, y)
        board[x][y] = self

        my_king = kings[self.color]
        king_in_check = False
        opponent_color = BLACK if self.color == WHITE else WHITE

        # Check all opponent pieces to see if they can attack our king
        for row in board:
            for square in row:
                if (
                    isinstance(square, Piece)
                    and square.color == opponent_color
                    and square != self
                ):
                    if isinstance(square, Pawn):
                        attack_squares = square.get_attack_squares(
                            board, board_size
                        )
                    else:
                        attack_squares = (
                            square.get_moves_without_check_validation(
                                board, board_size
                            )
                        )

                    if my_king.position in attack_squares:
                        king_in_check = True
                        break
            if king_in_check:
                break

        # Restore the board
        board[x][y] = captured_piece
        self.update_position(original_x, original_y)
        board[self.x][self.y] = self

        return king_in_check

    def get_moves_without_check_validation(
        self, board: list[list[str]], board_size: int
    ) -> list[tuple]:
        """Get moves without checking if they leave king in check (to avoid infinite recursion)"""
        valid_moves = []
        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            while self.is_valid(x, y, board, board_size):
                valid_moves.append((x, y))

                if self.can_take(x, y, board):
                    break

                x += dx
                y += dy

        return valid_moves

    def get_moves(
        self, board: list[list[str]], board_size: int, kings
    ) -> list[tuple]:
        """Get all legal moves for this piece"""
        candidate_moves = self.get_moves_without_check_validation(
            board, board_size
        )

        # Filter out moves that would leave our king in check
        valid_moves = []
        for move in candidate_moves:
            if not self.would_leave_king_in_check(
                move[0], move[1], board, board_size, kings
            ):
                valid_moves.append(move)

        return valid_moves

    def update_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.position = (x, y)


class Knight(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "N"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [
            (+1, +2),
            (+1, -2),
            (-1, +2),
            (-1, -2),
            (+2, +1),
            (+2, -1),
            (-2, +1),
            (-2, -1),
        ]

    def get_moves_without_check_validation(
        self, board: list[list[str]], board_size: int
    ) -> list[tuple]:
        """Knight doesn't slide, so override the base method"""
        valid_moves = []
        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            if self.is_valid(x, y, board, board_size):
                valid_moves.append((x, y))
        return valid_moves

    def get_moves(
        self, board: list[list[str]], board_size: int, kings
    ) -> list[tuple]:
        candidate_moves = self.get_moves_without_check_validation(
            board, board_size
        )

        # Filter out moves that would leave our king in check
        valid_moves = []
        for move in candidate_moves:
            if not self.would_leave_king_in_check(
                move[0], move[1], board, board_size, kings
            ):
                valid_moves.append(move)

        return valid_moves


class Bishop(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "B"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [(+1, +1), (+1, -1), (-1, -1), (-1, +1)]


class Rook(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "R"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Queen(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "Q"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [
            (1, 1),
            (1, -1),
            (1, 0),
            (0, 1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]


class King(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "K"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [
            (1, 1),
            (1, -1),
            (1, 0),
            (0, 1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]

    def is_square_attacked(
        self,
        x: int,
        y: int,
        board: list[list[str]],
        board_size: int,
        opponent_color: str,
    ) -> bool:
        """Check if a square is attacked by any opponent piece"""
        for row in board:
            for square in row:
                if (
                    isinstance(square, Piece)
                    and square.color == opponent_color
                ):
                    # check attack squares
                    if isinstance(square, Pawn):
                        attack_squares = square.get_attack_squares(
                            board, board_size
                        )
                    elif isinstance(square, King):
                        attack_squares = []
                        for dx, dy in square.moves:
                            nx, ny = square.x + dx, square.y + dy
                            if 0 <= nx < board_size and 0 <= ny < board_size:
                                attack_squares.append((nx, ny))
                    else:
                        attack_squares = (
                            square.get_moves_without_check_validation(
                                board, board_size
                            )
                        )

                    if (x, y) in attack_squares:
                        return True
        return False

    def castling_moves(
        self, board: list[list[str]], board_size: int
    ) -> list[tuple]:
        """Get valid castling moves"""
        castling_moves = []

        if self.has_moved:
            return castling_moves

        opponent_color = BLACK if self.color == WHITE else WHITE

        if board_size >= 8 and self.y + 3 < board_size:
            rook = board[self.x][self.y + 3]
            if (
                isinstance(rook, Rook)
                and not rook.has_moved
                and rook.color == self.color
            ):
                if (
                    board[self.x][self.y + 1] == "."
                    and board[self.x][self.y + 2] == "."
                ):
                    if (
                        not self.is_square_attacked(
                            self.x, self.y, board, board_size, opponent_color
                        )
                        and not self.is_square_attacked(
                            self.x,
                            self.y + 1,
                            board,
                            board_size,
                            opponent_color,
                        )
                        and not self.is_square_attacked(
                            self.x,
                            self.y + 2,
                            board,
                            board_size,
                            opponent_color,
                        )
                    ):
                        castling_moves.append((self.x, self.y + 2))

        if board_size >= 8 and self.y - 4 >= 0:
            rook = board[self.x][self.y - 4]
            if (
                isinstance(rook, Rook)
                and not rook.has_moved
                and rook.color == self.color
            ):
                if (
                    board[self.x][self.y - 1] == "."
                    and board[self.x][self.y - 2] == "."
                    and board[self.x][self.y - 3] == "."
                ):
                    if (
                        not self.is_square_attacked(
                            self.x, self.y, board, board_size, opponent_color
                        )
                        and not self.is_square_attacked(
                            self.x,
                            self.y - 1,
                            board,
                            board_size,
                            opponent_color,
                        )
                        and not self.is_square_attacked(
                            self.x,
                            self.y - 2,
                            board,
                            board_size,
                            opponent_color,
                        )
                    ):
                        castling_moves.append((self.x, self.y - 2))

        return castling_moves

    def is_valid(
        self, x: int, y: int, board: list[list[str]], board_size: int
    ) -> bool:
        if not 0 <= x < board_size or not 0 <= y < board_size:
            return False

        if board[x][y] == ".":
            return True

        if self.can_take(x, y, board):
            return True

        return False

    def get_moves_without_check_validation(
        self, board: list[list[str]], board_size: int
    ) -> list[tuple]:
        """King moves without checking if squares are attacked"""
        valid_moves = []
        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            if self.is_valid(x, y, board, board_size):
                valid_moves.append((x, y))
        return valid_moves

    def get_moves(
        self, board: list[list[str]], board_size: int, kings=None
    ) -> list[tuple]:
        """Get all legal king moves including castling"""
        valid_moves = []
        opponent_color = BLACK if self.color == WHITE else WHITE

        for dx, dy in self.moves:
            x = self.x + dx
            y = self.y + dy
            if self.is_valid(x, y, board, board_size):
                if not self.is_square_attacked(
                    x, y, board, board_size, opponent_color
                ):
                    valid_moves.append((x, y))

        valid_moves.extend(self.castling_moves(board, board_size))

        return valid_moves


class Pawn(Piece):
    def __init__(self, color: chr, image_id: int, x: int, y: int) -> None:
        piece_notation = "P"
        super().__init__(color, piece_notation, image_id, x, y)
        self.moves = [(1, 0), (2, 0)] if color == BLACK else [(-1, 0), (-2, 0)]

    def is_valid(
        self, x: int, y: int, board: list[list[str]], board_size: int
    ) -> bool:
        if not 0 <= x < board_size or not 0 <= y < board_size:
            return False

        if board[x][y] == ".":
            return True

        return False

    def get_attack_squares(
        self, board: list[list[str]], board_size: int
    ) -> list[tuple]:
        """Get all squares this pawn attacks (not necessarily with pieces on them)"""
        attack_squares = []
        take_moves = (
            [(1, -1), (1, 1)] if self.color == BLACK else [(-1, -1), (-1, 1)]
        )
        for dx, dy in take_moves:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < board_size and 0 <= y < board_size:
                attack_squares.append((x, y))
        return attack_squares

    def get_taking_squares(
        self, board: list[list[str]], board_size: int, kings, last_move=None
    ) -> list[tuple]:
        """Get actual capture moves including en passant"""
        valid_moves = []
        take_moves = (
            [(1, -1), (1, 1)] if self.color == BLACK else [(-1, -1), (-1, 1)]
        )

        for dx, dy in take_moves:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < board_size and 0 <= y < board_size:
                if self.can_take(x, y, board):
                    if not self.would_leave_king_in_check(
                        x, y, board, board_size, kings
                    ):
                        valid_moves.append((x, y))

                # En passant
                elif last_move:
                    last_piece, (from_x, from_y), (to_x, to_y) = last_move
                    if isinstance(last_piece, Pawn):
                        if (
                            abs(from_x - to_x) == 2
                            and to_x == self.x
                            and to_y == y
                        ):
                            if not self.would_leave_king_in_check(
                                x, y, board, board_size, kings
                            ):
                                valid_moves.append((x, y))

        return valid_moves

    def get_moves_without_check_validation(
        self, board: list[list[str]], board_size: int
    ) -> list[tuple]:
        """Get pawn moves without check validation (for attack detection)"""
        # For attack detection, we only care about diagonal attacks
        return self.get_attack_squares(board, board_size)

    def get_moves(
        self, board: list[list[str]], board_size: int, kings, last_move=None
    ) -> list[tuple]:
        """Get all legal pawn moves including en passant"""
        valid_moves = []

        # Moves
        if self.is_valid(self.x + self.moves[0][0], self.y, board, board_size):
            if not self.would_leave_king_in_check(
                self.x + self.moves[0][0], self.y, board, board_size, kings
            ):
                valid_moves.append((self.x + self.moves[0][0], self.y))

        if not self.has_moved and len(valid_moves) >= 1:
            x = self.x + self.moves[1][0]
            y = self.y + self.moves[1][1]
            if self.is_valid(x, y, board, board_size):
                if not self.would_leave_king_in_check(
                    x, y, board, board_size, kings
                ):
                    valid_moves.append((x, y))

        # Captures (including en passant)
        valid_moves.extend(
            self.get_taking_squares(board, board_size, kings, last_move)
        )

        return valid_moves
