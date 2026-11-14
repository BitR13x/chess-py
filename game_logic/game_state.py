"""Game state validation: check, checkmate, stalemate detection"""

from constx import is_piece, WHITE, BLACK, CHECKMATE, STALEMATE, IN_PROGRESS
from pieces import Piece, Pawn


class GameStateValidator:
    @staticmethod
    def is_king_in_check(
        board: list, board_size: int, kings: dict, color: str
    ) -> bool:
        """Check if the king of the given color is in check"""
        king = kings[color]
        if not king:
            return False

        opponent_color = BLACK if color == WHITE else WHITE

        for row in board:
            for square in row:
                if (
                    isinstance(square, Piece)
                    and square.color == opponent_color
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

                    if king.position in attack_squares:
                        return True
        return False

    @staticmethod
    def get_all_legal_moves(
        board: list,
        board_size: int,
        kings: dict,
        pieces: list,
        color: str,
        last_move=None,
    ) -> list:
        """Get all legal moves for a color"""
        legal_moves = []

        for piece in pieces:
            if isinstance(piece, Pawn):
                moves = piece.get_moves(board, board_size, kings, last_move)
            else:
                moves = piece.get_moves(board, board_size, kings)

            for move in moves:
                legal_moves.append((piece, move))

        return legal_moves

    @staticmethod
    def check_game_state(
        board: list,
        board_size: int,
        kings: dict,
        pieces: list,
        color: str,
        last_move=None,
    ) -> str:
        """Check if the game is in checkmate, stalemate, or in progress"""
        legal_moves = GameStateValidator.get_all_legal_moves(
            board, board_size, kings, pieces, color, last_move
        )

        if len(legal_moves) == 0:
            if GameStateValidator.is_king_in_check(
                board, board_size, kings, color
            ):
                return CHECKMATE
            else:
                return STALEMATE

        return IN_PROGRESS
