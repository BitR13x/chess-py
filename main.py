from board import ChessBoard
from constx import CHECKMATE, STALEMATE, IN_PROGRESS, is_piece, WHITE, BLACK
from pieces import Pawn
from game_logic.game_state import GameStateValidator
import tkinter as tk
from tkinter import messagebox


class GameController:
    def __init__(self, root: tk.Tk, board: list[list[str]], canvas_size: int):
        self.root = root
        self.on_move = WHITE
        self.chessboard = ChessBoard(root, board, canvas_size)
        self.current_piece = None
        self.possible_moves = []
        self.dots = set()

        self.chessboard.canvas.bind("<Button-1>", self.clicked)

        # Register reset callback with chessboard
        self.chessboard.game_controller = self

    def reset_game_state(self) -> None:
        """Reset the game controller state (called by new_game)"""
        self.on_move = WHITE
        self.current_piece = None
        self.possible_moves = []
        self.dots.clear()  # Clear the set without trying to delete already-deleted canvas items

    def clean_dots(self) -> None:
        """Remove move indicator dots from the board"""
        for image_id in self.dots:
            self.chessboard.remove_img(image_id)
        self.dots = set()

    def clicked(self, event: tk.Event) -> None:
        """Handle click events on the chess board"""
        # Convert click coordinates to board position
        if self.chessboard.renderer.view_from_white:
            x = int(event.y / self.chessboard.square_size)
            y = int(event.x / self.chessboard.square_size)
        else:
            # When viewing from black, flip both coordinates
            x = (
                self.chessboard.height
                - 1
                - int(event.y / self.chessboard.square_size)
            )
            y = (
                self.chessboard.height
                - 1
                - int(event.x / self.chessboard.square_size)
            )

        board = self.chessboard.current_board

        if self.current_piece == board[x][y]:
            self.current_piece = None
            self.possible_moves = []
            self.chessboard.renderer.selected_square_highlight = None
            self.clean_dots()
            self.chessboard.rerender()
            return

        if is_piece(board, x, y) and board[x][y].color == self.on_move:
            self.current_piece = board[x][y]
            self.chessboard.renderer.selected_square_highlight = (
                self.current_piece.x,
                self.current_piece.y,
            )

            self.clean_dots()

            if isinstance(self.current_piece, Pawn):
                self.possible_moves = self.current_piece.get_moves(
                    board,
                    self.chessboard.height,
                    self.chessboard.kings,
                    self.chessboard.last_move,
                )
            else:
                self.possible_moves = self.current_piece.get_moves(
                    board, self.chessboard.height, self.chessboard.kings
                )

            self.chessboard.rerender()

            # Draw move indicators after rerender
            for ax, ay in self.possible_moves:
                if self.chessboard.renderer.view_from_white:
                    display_x, display_y = ax, ay
                else:
                    # 180 degree rotation - flip both coordinates
                    display_x = self.chessboard.height - 1 - ax
                    display_y = self.chessboard.height - 1 - ay

                if is_piece(board, ax, ay):
                    image_id = self.chessboard.create_image(
                        display_x, display_y, "O"
                    )
                else:
                    image_id = self.chessboard.create_image(
                        display_x, display_y, "-"
                    )
                self.dots.add(image_id)

            return

        # Make a move
        if (
            (x, y) in self.possible_moves
            and self.current_piece
            and self.current_piece.color == self.on_move
        ):
            self.chessboard.move_piece(self.current_piece, x, y)
            self.clean_dots()
            self.chessboard.renderer.selected_square_highlight = None

            # Switch turns
            self.on_move = WHITE if self.on_move == BLACK else BLACK

            # Update score display
            self.chessboard.update_score_display()

            # Check for checkmate/stalemate
            game_state = self.chessboard.check_game_state(self.on_move)

            if game_state == CHECKMATE:
                winner = "White" if self.on_move == BLACK else "Black"
                messagebox.showinfo("Checkmate", f"Checkmate! {winner} wins!")
                self.chessboard.rerender()
            elif game_state == STALEMATE:
                messagebox.showinfo(
                    "Stalemate", "Stalemate! The game is a draw."
                )
                self.chessboard.rerender()
            else:
                # Check if king is in check (for visual indicator)
                if self.chessboard.is_king_in_check(self.on_move):
                    color_name = "White" if self.on_move == WHITE else "Black"
                    print(f"{color_name} is in check!")

                self.chessboard.rerender()

            self.current_piece = None
            self.possible_moves = []
            return


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess")

    myboard = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]

    game = GameController(root, myboard, 800)
    root.mainloop()
