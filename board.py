"""Main chess board management class"""

from pieces import Bishop, King, Knight, Pawn, Queen, Rook, Piece
from constx import is_piece, WHITE, BLACK
from utils.notation import NotationHelper
from utils.game_io import GameSerializer, export_pgn
from utils.image_manager import ImageManager
from game_logic.game_state import GameStateValidator
from game_logic.move_executor import MoveExecutor
from ui.info_panel import InfoPanel, ControlPanel
from ui.board_renderer import BoardRenderer
import tkinter as tk
from tkinter import messagebox, simpledialog
import os


class ChessBoard:
    def __init__(
        self, master: tk.Tk, board: list[list[str]], pixel_size: int
    ) -> None:
        self.height = 8
        self.master = master
        self.current_board = board

        self.canvas_size = pixel_size
        self.square_size = self.canvas_size // 8

        self.canvas = tk.Canvas(
            self.master, width=self.canvas_size, height=self.canvas_size
        )
        self.canvas.pack(side=tk.LEFT)

        self.notation_helper = NotationHelper()
        self.image_manager = ImageManager(__file__, self.square_size)

        self.pieces_notation = {
            "R": Rook,
            "N": Knight,
            "B": Bishop,
            "Q": Queen,
            "K": King,
            "P": Pawn,
        }

        # Game state
        self.black_pieces = []
        self.white_pieces = []
        self.kings = {WHITE: None, BLACK: None}
        self.white_score, self.black_score = 0, 0
        self.last_move = None
        self.move_history = []
        self.game_controller = None  # Will be set by GameController

        self.renderer = BoardRenderer(
            self.canvas, self.square_size, self.height, self.image_manager
        )

        # setup
        self.move_executor = MoveExecutor(self.current_board, self)
        self.game_serializer = GameSerializer(self.pieces_notation)

        self.info_panel = InfoPanel(self.master)
        self.control_panel = ControlPanel(
            self.info_panel.frame,
            {
                "undo": self.undo_move_ui,
                "flip": self.flip_board,
                "save": self.save_game,
                "load": self.load_game,
                "new_game": self.new_game,
            },
        )

        self.prepare_board()
        self.rerender()

    def prepare_board(self) -> None:
        """Initialize piece objects from board notation"""
        for x in range(len(self.current_board)):
            for y in range(len(self.current_board[0])):
                if self.current_board[x][y] != ".":
                    piece = self.current_board[x][y]
                    new_piece = self.pieces_notation[piece[1]](
                        piece[0], 0, x, y
                    )
                    self.current_board[x][y] = new_piece

                    if piece[0] == WHITE:
                        if isinstance(new_piece, King):
                            self.kings[WHITE] = new_piece
                        self.white_pieces.append(new_piece)
                    else:
                        if isinstance(new_piece, King):
                            self.kings[BLACK] = new_piece
                        self.black_pieces.append(new_piece)

    def rerender(self) -> None:
        """Redraw the entire board"""
        self.renderer.draw_board(
            self.current_board, self.kings, self.is_king_in_check
        )

    def move_piece(self, piece: Piece, x: int, y: int) -> tuple:
        """Execute a move"""
        move_data = self.move_executor.execute_move(
            piece, x, y, self.last_move
        )

        # Handle captured pieces
        if move_data["captured"] and not move_data["is_en_passant"]:
            self.remove_piece(move_data["captured"])
        elif move_data["is_en_passant"]:
            self.remove_piece(move_data["captured"])

        # Handle promotion
        if move_data["is_promotion"]:
            choice = self.show_promotion_dialog()
            new_piece = self.promote_pawn(piece, choice)
            move_data["piece"] = new_piece

        self.last_move = (
            move_data["piece"],
            move_data["from"],
            move_data["to"],
        )

        next_color = BLACK if piece.color == WHITE else WHITE
        is_check = self.is_king_in_check(next_color)
        pieces = (
            self.black_pieces if next_color == BLACK else self.white_pieces
        )
        game_state = GameStateValidator.check_game_state(
            self.current_board,
            self.height,
            self.kings,
            pieces,
            next_color,
            self.last_move,
        )
        is_checkmate = game_state == "checkmate"

        move_notation = self.notation_helper.move_to_notation(
            move_data["piece"],
            move_data["from"],
            move_data["to"],
            move_data["captured"],
            move_data["is_castling"],
            is_check,
            is_checkmate,
        )
        move_data["notation"] = move_notation

        self.move_history.append(move_data)
        self.info_panel.add_move(
            move_notation,
            len(self.move_history) // 2 + 1,
            piece.color == WHITE,
        )

        self.renderer.last_move_highlight = (
            move_data["from"],
            move_data["to"],
        )

        return move_data["captured"]

    def remove_piece(self, piece: Piece) -> None:
        """Remove a piece from the board"""
        if piece.color == WHITE:
            if piece in self.white_pieces:
                self.white_pieces.remove(piece)
            self.black_score += piece.weight
        else:
            if piece in self.black_pieces:
                self.black_pieces.remove(piece)
            self.white_score += piece.weight

    def is_king_in_check(self, color: str) -> bool:
        """Check if a king is in check"""
        return GameStateValidator.is_king_in_check(
            self.current_board, self.height, self.kings, color
        )

    def check_game_state(self, color: str) -> str:
        """Check game state for a given color"""
        pieces = self.white_pieces if color == WHITE else self.black_pieces
        return GameStateValidator.check_game_state(
            self.current_board,
            self.height,
            self.kings,
            pieces,
            color,
            self.last_move,
        )

    def update_score_display(self) -> None:
        """Update the score display in UI"""
        self.info_panel.update_score(self.white_score, self.black_score)

    @property
    def selected_square_highlight(self):
        """Get selected square highlight from renderer"""
        return self.renderer.selected_square_highlight

    @selected_square_highlight.setter
    def selected_square_highlight(self, value):
        """Set selected square highlight on renderer"""
        self.renderer.selected_square_highlight = value

    def show_promotion_dialog(self) -> str:
        """Show pawn promotion dialog"""
        choice = simpledialog.askstring(
            "Pawn Promotion", "Choose piece (Q/R/B/N):", initialvalue="Q"
        )
        if choice and choice.upper() in ["Q", "R", "B", "N"]:
            return choice.upper()
        return "Q"

    def promote_pawn(self, pawn: Pawn, choice: str) -> Piece:
        """Promote a pawn to the chosen piece"""
        piece_class = self.pieces_notation[choice]
        new_piece = piece_class(pawn.color, 0, pawn.x, pawn.y)
        new_piece.has_moved = True

        if pawn.color == WHITE:
            self.white_pieces.remove(pawn)
            self.white_pieces.append(new_piece)
        else:
            self.black_pieces.remove(pawn)
            self.black_pieces.append(new_piece)

        self.current_board[pawn.x][pawn.y] = new_piece

        return new_piece

    def undo_move_ui(self) -> None:
        """Undo the last move"""
        if len(self.move_history) == 0:
            messagebox.showinfo("Undo", "No moves to undo")
            return

        move_data = self.move_history.pop()

        if move_data["is_promotion"]:
            promoted_piece = move_data["piece"]
            if promoted_piece.color == WHITE:
                self.white_pieces.remove(promoted_piece)
            else:
                self.black_pieces.remove(promoted_piece)

        if move_data["captured"]:
            captured = move_data["captured"]
            if captured.color == WHITE:
                self.white_pieces.append(captured)
                self.black_score -= captured.weight
            else:
                self.black_pieces.append(captured)
                self.white_score -= captured.weight

        self.move_executor.undo_move(move_data, self.pieces_notation)
        if len(self.move_history) > 0:
            last = self.move_history[-1]
            self.last_move = (last["piece"], last["from"], last["to"])
            self.renderer.last_move_highlight = (last["from"], last["to"])
        else:
            self.last_move = None
            self.renderer.last_move_highlight = None

        self.info_panel.rebuild_history(self.move_history)
        self.info_panel.update_score(self.white_score, self.black_score)
        self.rerender()

        # Switch turn back in game controller
        if self.game_controller:
            self.game_controller.on_move = (
                WHITE if self.game_controller.on_move == BLACK else BLACK
            )

    def flip_board(self) -> None:
        """Flip the board view"""
        self.renderer.flip_board()
        self.rerender()

    def save_game(self) -> None:
        """Save the current game"""
        filename = simpledialog.askstring(
            "Save Game", "Enter filename:", initialvalue="game.json"
        )
        if not filename:
            return

        if not filename.endswith(".json"):
            filename += ".json"

        try:
            self.game_serializer.save_game(
                filename,
                self.current_board,
                self.move_history,
                self.white_score,
                self.black_score,
            )
            messagebox.showinfo("Save Game", f"Game saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Game", f"Error saving game: {e}")

    def load_game(self) -> None:
        """Load a game from file"""
        filename = simpledialog.askstring(
            "Load Game", "Enter filename:", initialvalue="game.json"
        )
        if not filename:
            return

        if not filename.endswith(".json"):
            filename += ".json"

        try:
            game_data = self.game_serializer.load_game(filename)

            self.white_pieces.clear()
            self.black_pieces.clear()
            self.move_history.clear()

            self.current_board = game_data["board"]
            self.white_pieces = game_data["white_pieces"]
            self.black_pieces = game_data["black_pieces"]
            self.kings = game_data["kings"]
            self.white_score = game_data["white_score"]
            self.black_score = game_data["black_score"]

            self.info_panel.clear_history()
            self.info_panel.update_score(self.white_score, self.black_score)
            self.rerender()

            messagebox.showinfo("Load Game", f"Game loaded from {filename}")
        except FileNotFoundError:
            messagebox.showerror("Load Game", f"File {filename} not found")
        except Exception as e:
            messagebox.showerror("Load Game", f"Error loading game: {e}")

    def new_game(self) -> None:
        """Start a new game"""
        if messagebox.askyesno(
            "New Game", "Start a new game? Current game will be lost."
        ):
            # Reset game state
            self.current_board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]

            self.white_pieces.clear()
            self.black_pieces.clear()
            self.move_history.clear()
            self.last_move = None
            self.white_score = 0
            self.black_score = 0
            self.renderer.last_move_highlight = None
            self.renderer.selected_square_highlight = None

            self.move_executor.board = self.current_board

            self.prepare_board()
            self.info_panel.clear_history()
            self.info_panel.update_score(0, 0)
            self.rerender()

            if self.game_controller:
                self.game_controller.reset_game_state()

    def create_image(self, x: int, y: int, piece: str) -> int:
        """Create an image on the board (for move indicators)"""
        return self.renderer.create_move_indicator(x, y, piece)

    def remove_img(self, image_id: int) -> None:
        """Remove an image from the board"""
        self.renderer.remove_image(image_id)

    def print_raw(self) -> None:
        """Debug print the board"""
        for row in self.current_board:
            print(" ".join(map(str, row)))
        print("----------------------")
