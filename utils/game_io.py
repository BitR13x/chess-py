"""Game save/load functionality for chess games"""

import json
from constx import is_piece


class GameSerializer:
    def __init__(self, pieces_notation: dict):
        self.pieces_notation = pieces_notation

    def save_game(
        self,
        filename: str,
        board: list,
        move_history: list,
        white_score: int,
        black_score: int,
    ) -> None:
        """Save the current game state to a JSON file"""
        # Convert board to serializable format
        board_data = []
        for row in board:
            row_data = []
            for square in row:
                if is_piece(
                    board,
                    square.x if hasattr(square, "x") else -1,
                    square.y if hasattr(square, "y") else -1,
                ):
                    row_data.append(
                        {
                            "name": square.name,
                            "has_moved": square.has_moved,
                            "position": (square.x, square.y),
                        }
                    )
                else:
                    row_data.append(".")
            board_data.append(row_data)

        game_data = {
            "board": board_data,
            "move_history": [m["notation"] for m in move_history],
            "white_score": white_score,
            "black_score": black_score,
        }

        with open(filename, "w") as f:
            json.dump(game_data, f, indent=2)

    def load_game(self, filename: str) -> dict:
        """Load a game from a JSON file"""
        with open(filename, "r") as f:
            game_data = json.load(f)

        # Reconstruct board with piece objects
        board = [["." for _ in range(8)] for _ in range(8)]
        white_pieces = []
        black_pieces = []
        kings = {"w": None, "b": None}

        for x in range(len(game_data["board"])):
            for y in range(len(game_data["board"][0])):
                square_data = game_data["board"][x][y]
                if square_data != ".":
                    piece_name = square_data["name"]
                    color = piece_name[0]
                    piece_type = piece_name[1]

                    from pieces import King

                    piece = self.pieces_notation[piece_type](color, 0, x, y)
                    piece.has_moved = square_data["has_moved"]
                    board[x][y] = piece

                    if color == "w":
                        if isinstance(piece, King):
                            kings["w"] = piece
                        white_pieces.append(piece)
                    else:
                        if isinstance(piece, King):
                            kings["b"] = piece
                        black_pieces.append(piece)

        return {
            "board": board,
            "white_pieces": white_pieces,
            "black_pieces": black_pieces,
            "kings": kings,
            "white_score": game_data["white_score"],
            "black_score": game_data["black_score"],
            "move_history": game_data.get("move_history", []),
        }


def export_pgn(
    move_history: list,
    white_player: str = "White",
    black_player: str = "Black",
    result: str = "*",
) -> str:
    """Export game to PGN format"""
    pgn = f'[White "{white_player}"]\n'
    pgn += f'[Black "{black_player}"]\n'
    pgn += f'[Result "{result}"]\n\n'

    move_num = 1
    for i, move in enumerate(move_history):
        if i % 2 == 0:
            pgn += f"{move_num}. {move['notation']} "
        else:
            pgn += f"{move['notation']} "
            move_num += 1

    pgn += result
    return pgn
