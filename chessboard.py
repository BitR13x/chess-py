from pieces import Bishop, King, Knight, Pawn, Queen, Rook, Piece
from constx import is_piece, WHITE, BLACK
import tkinter as tk
import os


#pieces_images = {
#    "bR": full_path("pieces/black/bR.svg"),
#    "bN": full_path("pieces/black/bN.svg"),
#    "bB": full_path("pieces/black/bB.svg"),
#    "bQ": full_path("pieces/black/bQ.svg"),
#    "bK": full_path("pieces/black/bK.svg"),
#    "bP": full_path("pieces/black/bP.svg"),
#
#    "wR": full_path("pieces/white/wR.svg"),
#    "wN": full_path("pieces/white/wN.svg"),
#    "wB": full_path("pieces/white/wB.svg"),
#    "wQ": full_path("pieces/white/wQ.svg"),
#    "wK": full_path("pieces/white/wK.svg"),
#    "wP": full_path("pieces/white/wP.svg")
#}


class ChessBoard:
    def __init__(self, master: tk.Tk, board: list[list[str]], pixel_size: int) -> None:
        self.letters = "abcdefgh"
        self.height = 8
        
        # tk.root
        self.master = master
        self.current_board = board

        self.canvas_size = pixel_size
        self.square_size = self.canvas_size // 8

        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.pieces_notation = {
            "R": Rook,
            "N": Knight,
            "B": Bishop,
            "Q": Queen,
            "K": King,
            "P": Pawn
        }
        self.piece_images = {
            "bR": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/black/bR.png"))),
            "bN": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/black/bN.png"))),
            "bB": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/black/bB.png"))),
            "bQ": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/black/bQ.png"))),
            "bK": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/black/bK.png"))),
            "bP": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/black/bP.png"))),

            "wR": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/white/wR.png"))),
            "wN": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/white/wN.png"))),
            "wB": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/white/wB.png"))),
            "wQ": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/white/wQ.png"))),
            "wK": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/white/wK.png"))),
            "wP": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/white/wP.png"))),

            "O": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/greycircle.png"))),
            "-": self.scale_img(tk.PhotoImage(file=self.full_path("pieces/greydot.png")))
        }

        self.prepare_board()
        self.draw_chessboard(WHITE)
        self.draw_pieces(WHITE)

    def scale_img(self, image: tk.PhotoImage, x=2, y=2) -> tk.PhotoImage:
        #image = image.zoom(2, 2)
        image = image.subsample(x, y)
        return image

    def rerender(self, color: str) -> None:
        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.draw_chessboard(color)
        self.draw_pieces(color)

    def draw_chessboard(self, def_color: str) -> None:
        for row in range(self.height):
            for col in range(self.height):
                x0, y0 = col * self.square_size, row * self.square_size
                x1, y1 = x0 + self.square_size, y0 + self.square_size

                if def_color == WHITE:
                    color = "white" if (row + col) % 2 == 0 else "lightgray"
                else:
                    color = "lightgray" if (row + col) % 2 == 0 else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def full_path(self, relative_path: str) -> str:
        absolute_path = os.path.dirname(__file__)
        return os.path.join(absolute_path, relative_path)


    def create_image(self, x: int, y: int, piece: str) -> int:
        x, y = x * self.square_size, y * self.square_size
        return self.canvas.create_image(y + self.square_size // 2, x + self.square_size // 2,
                                             image=self.piece_images[piece], anchor=tk.CENTER)

    def draw_pieces(self, color: str) -> None:
        for row in range(self.height):
            for col in range(self.height):
                if is_piece(self.current_board, row, col):
                    
                    piece = self.current_board[row][col]
                    if color == WHITE:
                        image_id = self.create_image(row, col, piece.name)
                    else:
                        image_id = self.create_image(self.height - row, col, piece.name)
                    piece.image_id = image_id

                        #.move(image_id, change_in_x, change_in_y)
                        #.delete(image_id)

    def move_piece(self, piece: Piece, x: int, y: int) -> None:
        ax = (x * self.square_size)
        ay = (y * self.square_size)

        self.current_board[piece.x][piece.y] = "."
        self.canvas.moveto(piece.image_id, ay, ax)

        piece.update_position(x, y)
        self.current_board[piece.x][piece.y] = piece

        if isinstance(piece, Pawn):
            piece.init_position = False



    def remove_img(self, image_id: int) -> None:
        self.canvas.delete(image_id)


    def prepare_board(self) -> None:
        """init objects"""
        for x in range(len(self.current_board)):
            for y in range(len(self.current_board[0])):
                if self.current_board[x][y] != ".":
                    piece = self.current_board[x][y]
                    self.current_board[x][y] = self.pieces_notation[piece[1]](piece[0], 0, x, y)
        self.print_raw()

    def notation(self, piece: str, position: tuple) -> str:
        x = self.height - position[0]
        y = self.letters[position[1]]
        return piece + y + str(x)


    def print_raw(self) -> None:
        for row in self.current_board:
            print(" ".join(map(str, row)))
        print("----------------------")
