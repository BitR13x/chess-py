"""Move execution and undo functionality"""

from constx import is_piece
from pieces import Pawn, King, Rook, Piece


class MoveExecutor:
    def __init__(self, board: list, chessboard_ui):
        self.board = board
        self.ui = chessboard_ui

    def execute_move(self, piece: Piece, x: int, y: int, last_move) -> dict:
        """Execute a move and return move data for history"""
        from_pos = (piece.x, piece.y)
        captured_piece = None
        captured_from = None
        is_en_passant = False
        is_castling = False
        is_promotion = False
        promoted_from = None

        # Check for en passant capture
        if isinstance(piece, Pawn) and last_move:
            last_piece, (lf_x, lf_y), (lt_x, lt_y) = last_move
            if isinstance(last_piece, Pawn) and abs(lf_x - lt_x) == 2:
                if (
                    lt_x == piece.x
                    and lt_y == y
                    and x == (lt_x + piece.x) // 2
                ):
                    captured_piece = self.board[lt_x][lt_y]
                    captured_from = (lt_x, lt_y)
                    is_en_passant = True
                    self.board[lt_x][lt_y] = "."

        # Handle castling
        if isinstance(piece, King):
            castling_moves = piece.castling_moves(self.board, len(self.board))
            if (x, y) in castling_moves:
                is_castling = True
                if y == piece.y - 2:  # Queenside
                    rook = self.board[x][piece.y - 4]
                    self._move_piece_internal(rook, x, y + 1)
                elif y == piece.y + 2:  # Kingside
                    rook = self.board[x][piece.y + 3]
                    self._move_piece_internal(rook, x, y - 1)

        # Normal capture
        if is_piece(self.board, x, y) and not is_en_passant:
            captured_piece = self.board[x][y]
            captured_from = (x, y)

        self._move_piece_internal(piece, x, y)
        piece.has_moved = True

        # Pawn promotion
        if isinstance(piece, Pawn):
            if (piece.color == "w" and x == 0) or (
                piece.color == "b" and x == len(self.board) - 1
            ):
                is_promotion = True
                promoted_from = piece

        return {
            "piece": piece,
            "from": from_pos,
            "to": (x, y),
            "captured": captured_piece,
            "captured_from": captured_from,
            "is_en_passant": is_en_passant,
            "is_castling": is_castling,
            "is_promotion": is_promotion,
            "promoted_from": promoted_from,
        }

    def _move_piece_internal(self, piece: Piece, x: int, y: int) -> None:
        """Internal method to move a piece without game logic"""
        self.board[piece.x][piece.y] = "."
        piece.update_position(x, y)
        self.board[piece.x][piece.y] = piece

    def undo_move(self, move_data: dict, pieces_notation: dict) -> None:
        """Undo a move given move data"""
        piece = move_data["piece"]
        from_pos = move_data["from"]
        to_pos = move_data["to"]
        captured = move_data["captured"]
        captured_from = move_data["captured_from"]

        # Handle promotion undo
        if move_data["is_promotion"]:
            promoted_piece = piece
            pawn = Pawn(promoted_piece.color, 0, to_pos[0], to_pos[1])
            pawn.has_moved = (
                False
                if from_pos[0] == (6 if pawn.color == "w" else 1)
                else True
            )
            self.board[to_pos[0]][to_pos[1]] = pawn
            piece = pawn

        self.board[to_pos[0]][to_pos[1]] = "."
        piece.update_position(from_pos[0], from_pos[1])
        self.board[from_pos[0]][from_pos[1]] = piece
        piece.has_moved = False

        if captured:
            self.board[captured_from[0]][captured_from[1]] = captured

        # Handle castling undo
        if move_data["is_castling"]:
            if to_pos[1] > from_pos[1]:  # Kingside
                rook = self.board[to_pos[0]][to_pos[1] - 1]
                self.board[to_pos[0]][to_pos[1] - 1] = "."
                rook.update_position(to_pos[0], from_pos[1] + 3)
                self.board[to_pos[0]][from_pos[1] + 3] = rook
                rook.has_moved = False
            else:  # Queenside
                rook = self.board[to_pos[0]][to_pos[1] + 1]
                self.board[to_pos[0]][to_pos[1] + 1] = "."
                rook.update_position(to_pos[0], from_pos[1] - 4)
                self.board[to_pos[0]][from_pos[1] - 4] = rook
                rook.has_moved = False
