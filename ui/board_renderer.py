"""Board rendering and visual management"""

import tkinter as tk
from constx import is_piece, WHITE, BLACK
from pieces import Piece


class BoardRenderer:
    def __init__(
        self, canvas: tk.Canvas, square_size: int, height: int, image_manager
    ):
        self.canvas = canvas
        self.square_size = square_size
        self.height = height
        self.image_manager = image_manager

        self.view_from_white = True
        self.selected_square_highlight = None
        self.last_move_highlight = None
        self.check_square = None

    def draw_board(
        self, board: list, kings: dict, is_king_in_check_fn
    ) -> None:
        """Draw the complete chess board with all highlights"""
        self.canvas.delete("all")

        for row in range(self.height):
            for col in range(self.height):
                self._draw_square(row, col, kings, is_king_in_check_fn)

        self._draw_pieces(board)

    def _draw_square(
        self, row: int, col: int, kings: dict, is_king_in_check_fn
    ) -> None:
        """Draw a single square with appropriate coloring"""
        # Transform coordinates based on view
        if self.view_from_white:
            display_row, display_col = row, col
        else:
            # 180 degree rotation
            display_row = self.height - row - 1
            display_col = self.height - col - 1
        
        x0, y0 = display_col * self.square_size, display_row * self.square_size
        x1, y1 = x0 + self.square_size, y0 + self.square_size

        # Color pattern based on board position, not display position
        color = "white" if (row + col) % 2 == 0 else "lightgray"

        if self.selected_square_highlight == (row, col):
            color = "#baca44"

        if self.last_move_highlight:
            from_sq, to_sq = self.last_move_highlight
            if (row, col) == from_sq or (row, col) == to_sq:
                color = "#cdd26a"

        for king_color in [WHITE, BLACK]:
            king = kings[king_color]
            if king and is_king_in_check_fn(king_color):
                # Check indicator is based on board position, not display
                if (row, col) == (king.x, king.y):
                    color = "#ff6b6b"

        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def _draw_pieces(self, board: list) -> None:
        """Draw all pieces on the board"""
        for row in range(self.height):
            for col in range(self.height):
                if isinstance(board[row][col], Piece):
                    piece = board[row][col]
                    if self.view_from_white:
                        image_id = self._create_piece_image(
                            row, col, piece.name
                        )
                    else:
                        # When viewing from black, flip both row and column
                        image_id = self._create_piece_image(
                            self.height - row - 1, 
                            self.height - col - 1, 
                            piece.name
                        )
                    piece.image_id = image_id

    def _create_piece_image(self, x: int, y: int, piece_name: str) -> int:
        """Create an image on the canvas"""
        x_pos = y * self.square_size + self.square_size // 2
        y_pos = x * self.square_size + self.square_size // 2
        return self.canvas.create_image(
            x_pos,
            y_pos,
            image=self.image_manager.get_image(piece_name),
            anchor=tk.CENTER,
        )

    def create_move_indicator(
        self, x: int, y: int, indicator_type: str
    ) -> int:
        """Create a move indicator dot or circle"""
        return self._create_piece_image(x, y, indicator_type)

    def remove_image(self, image_id: int) -> None:
        """Remove an image from the canvas"""
        self.canvas.delete(image_id)

    def move_piece_image(self, piece: Piece, x: int, y: int) -> None:
        """Move a piece's image to a new position"""
        ax = y * self.square_size
        ay = x * self.square_size
        self.canvas.moveto(piece.image_id, ax, ay)

    def flip_board(self) -> None:
        """Flip the board view"""
        self.view_from_white = not self.view_from_white
