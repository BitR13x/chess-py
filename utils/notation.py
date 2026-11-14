"""Chess notation utilities for algebraic notation and move formatting"""


class NotationHelper:
    def __init__(self):
        self.letters = "abcdefgh"
        self.height = 8

    def position_to_notation(self, position: tuple) -> str:
        """Convert (x, y) position to algebraic notation like 'e4'"""
        x, y = position
        file = self.letters[y]
        rank = str(self.height - x)
        return f"{file}{rank}"

    def notation_to_position(self, notation: str) -> tuple:
        """Convert algebraic notation like 'e4' to (x, y) position"""
        file = notation[0]
        rank = notation[1]
        y = self.letters.index(file)
        x = self.height - int(rank)
        return (x, y)

    def move_to_notation(
        self,
        piece,
        from_pos: tuple,
        to_pos: tuple,
        captured=None,
        is_castling: bool = False,
        is_check: bool = False,
        is_checkmate: bool = False,
    ) -> str:
        """Generate algebraic notation for a move"""
        if is_castling:
            notation = "O-O" if to_pos[1] > from_pos[1] else "O-O-O"
        else:
            piece_symbol = piece.name[1] if piece.name[1] != "P" else ""
            from_file = self.letters[from_pos[1]]
            to_square = self.position_to_notation(to_pos)

            if captured:
                if piece.name[1] == "P":
                    notation = f"{from_file}x{to_square}"
                else:
                    notation = f"{piece_symbol}x{to_square}"
            else:
                notation = f"{piece_symbol}{to_square}"

        # check/checkmate indicators
        if is_checkmate:
            notation += "#"
        elif is_check:
            notation += "+"

        return notation
