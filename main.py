from chessboard import *
import tkinter as tk



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
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

    mychessboard = ChessBoard(root, myboard, 800)
    myboard = mychessboard.current_board
    dots = set()

    def clean_dots(chessboard: ChessBoard) -> None:
        global dots
        for image_id in dots:
            chessboard.remove_img(image_id)
        
        dots = set()

    current_piece = None
    possible_moves = []
    def clicked(event: tk.Event) -> None:
        x = int(event.y / mychessboard.square_size)
        y = int(event.x / mychessboard.square_size)

        if is_piece(myboard, x, y):
            global current_piece, possible_moves
            current_piece = myboard[x][y]

            clean_dots(mychessboard)
            possible_moves = myboard[x][y].get_moves(myboard, mychessboard.height)

            for ax, ay in possible_moves:
                # ! will overwrite enemy piece
                image_id = mychessboard.create_image(ax, ay, "-")
                dots.add(image_id)


        if (x, y) in possible_moves:
            mychessboard.move_piece(current_piece, x, y)
            clean_dots(mychessboard)

        mychessboard.print_raw()

    mychessboard.canvas.bind('<Button-1>', clicked)

    root.mainloop()
