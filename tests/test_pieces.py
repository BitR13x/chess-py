"""Unit tests for chess pieces"""
import unittest
import sys
sys.path.insert(0, '..')

from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from constx import WHITE, BLACK


class TestPawnMovement(unittest.TestCase):
    def setUp(self):
        """Set up a clean board for each test"""
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
    
    def test_white_pawn_initial_double_move(self):
        """White pawn should be able to move 1 or 2 squares from starting position"""
        pawn = Pawn(WHITE, 0, 6, 4)
        self.board[6][4] = pawn
        
        moves = pawn.get_moves(self.board, 8, self.kings)
        
        self.assertIn((5, 4), moves, "Pawn should move one square forward")
        self.assertIn((4, 4), moves, "Pawn should move two squares forward from start")
    
    def test_black_pawn_initial_double_move(self):
        """Black pawn should be able to move 1 or 2 squares from starting position"""
        pawn = Pawn(BLACK, 0, 1, 4)
        self.board[1][4] = pawn
        
        moves = pawn.get_moves(self.board, 8, self.kings)
        
        self.assertIn((2, 4), moves, "Pawn should move one square forward")
        self.assertIn((3, 4), moves, "Pawn should move two squares forward from start")
    
    def test_pawn_blocked(self):
        """Pawn should not move if blocked"""
        pawn = Pawn(WHITE, 0, 6, 4)
        blocker = Pawn(WHITE, 0, 5, 4)
        self.board[6][4] = pawn
        self.board[5][4] = blocker
        
        moves = pawn.get_moves(self.board, 8, self.kings)
        
        self.assertEqual(len(moves), 0, "Blocked pawn should have no moves")
    
    def test_pawn_capture(self):
        """Pawn should capture diagonally"""
        pawn = Pawn(WHITE, 0, 5, 4)
        enemy = Pawn(BLACK, 0, 4, 3)
        self.board[5][4] = pawn
        self.board[4][3] = enemy
        
        moves = pawn.get_moves(self.board, 8, self.kings)
        
        self.assertIn((4, 3), moves, "Pawn should capture diagonally")
        self.assertIn((4, 4), moves, "Pawn should also move forward")
    
    def test_pawn_en_passant(self):
        """Test en passant capture"""
        white_pawn = Pawn(WHITE, 0, 3, 4)
        black_pawn = Pawn(BLACK, 0, 3, 5)
        white_pawn.has_moved = True
        black_pawn.has_moved = True
        
        self.board[3][4] = white_pawn
        self.board[3][5] = black_pawn
        
        # Simulate black pawn just moved from (1, 5) to (3, 5)
        last_move = (black_pawn, (1, 5), (3, 5))
        
        moves = white_pawn.get_moves(self.board, 8, self.kings, last_move)
        
        self.assertIn((2, 5), moves, "White pawn should be able to capture en passant")


class TestRookMovement(unittest.TestCase):
    def setUp(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
    
    def test_rook_horizontal_movement(self):
        """Rook should move horizontally"""
        rook = Rook(WHITE, 0, 4, 4)
        self.board[4][4] = rook
        
        moves = rook.get_moves(self.board, 8, self.kings)
        
        # Should be able to move to all horizontal squares
        for col in range(8):
            if col != 4:
                self.assertIn((4, col), moves, f"Rook should move to (4, {col})")
    
    def test_rook_vertical_movement(self):
        """Rook should move vertically"""
        rook = Rook(WHITE, 0, 4, 4)
        self.board[4][4] = rook
        
        moves = rook.get_moves(self.board, 8, self.kings)
        
        # Should be able to move to all vertical squares (except king squares)
        for row in range(8):
            if row != 4 and row != 0 and row != 7:
                self.assertIn((row, 4), moves, f"Rook should move to ({row}, 4)")
    
    def test_rook_blocked_by_own_piece(self):
        """Rook should not jump over own pieces"""
        rook = Rook(WHITE, 0, 4, 4)
        blocker = Pawn(WHITE, 0, 4, 6)
        self.board[4][4] = rook
        self.board[4][6] = blocker
        
        moves = rook.get_moves(self.board, 8, self.kings)
        
        self.assertIn((4, 5), moves, "Rook should move to square before blocker")
        self.assertNotIn((4, 6), moves, "Rook should not capture own piece")
        self.assertNotIn((4, 7), moves, "Rook should not jump over own piece")
    
    def test_rook_captures_enemy(self):
        """Rook should capture enemy pieces"""
        rook = Rook(WHITE, 0, 4, 4)
        enemy = Pawn(BLACK, 0, 4, 6)
        self.board[4][4] = rook
        self.board[4][6] = enemy
        
        moves = rook.get_moves(self.board, 8, self.kings)
        
        self.assertIn((4, 6), moves, "Rook should capture enemy piece")
        self.assertNotIn((4, 7), moves, "Rook should not move past captured piece")


class TestKnightMovement(unittest.TestCase):
    def setUp(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
    
    def test_knight_l_shape_moves(self):
        """Knight should move in L-shape"""
        knight = Knight(WHITE, 0, 4, 4)
        self.board[4][4] = knight
        
        moves = knight.get_moves(self.board, 8, self.kings)
        
        expected_moves = [
            (5, 6), (5, 2),  # Down-right, down-left
            (3, 6), (3, 2),  # Up-right, up-left
            (6, 5), (6, 3),  # Right-down, left-down
            (2, 5), (2, 3)   # Right-up, left-up
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"Knight should move to {move}")
    
    def test_knight_jumps_over_pieces(self):
        """Knight should jump over pieces"""
        knight = Knight(WHITE, 0, 4, 4)
        # Surround knight with pieces
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = 4 + dx, 4 + dy
                if 0 <= x < 8 and 0 <= y < 8:
                    self.board[x][y] = Pawn(WHITE, 0, x, y)
        
        self.board[4][4] = knight
        
        moves = knight.get_moves(self.board, 8, self.kings)
        
        # Knight should still be able to move to its L-shaped positions
        self.assertGreater(len(moves), 0, "Knight should jump over pieces")
    
    def test_knight_edge_movement(self):
        """Knight on edge should have fewer moves"""
        knight = Knight(WHITE, 0, 7, 0)
        self.board[7][0] = knight
        
        moves = knight.get_moves(self.board, 8, self.kings)
        
        # From corner, knight should only have 2 possible moves
        self.assertEqual(len(moves), 2, "Knight in corner should have 2 moves")


class TestBishopMovement(unittest.TestCase):
    def setUp(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
    
    def test_bishop_diagonal_movement(self):
        """Bishop should move diagonally"""
        bishop = Bishop(WHITE, 0, 4, 4)
        self.board[4][4] = bishop
        
        moves = bishop.get_moves(self.board, 8, self.kings)
        
        # Check all four diagonals
        diagonals = [
            [(3, 5), (2, 6), (1, 7)],  # Up-right
            [(3, 3), (2, 2), (1, 1)],  # Up-left (skip king at 0,4)
            [(5, 5), (6, 6), (7, 7)],  # Down-right
            [(5, 3), (6, 2), (7, 1)]   # Down-left
        ]
        
        for diagonal in diagonals:
            for move in diagonal:
                if move[0] != 0:  # Skip black king row
                    self.assertIn(move, moves, f"Bishop should move to {move}")


class TestQueenMovement(unittest.TestCase):
    def setUp(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
    
    def test_queen_moves_like_rook_and_bishop(self):
        """Queen should move like both rook and bishop"""
        queen = Queen(WHITE, 0, 4, 4)
        self.board[4][4] = queen
        
        moves = queen.get_moves(self.board, 8, self.kings)
        
        # Should have moves in all 8 directions
        self.assertGreater(len(moves), 20, "Queen should have many moves")
        
        # Check a few specific moves
        self.assertIn((4, 0), moves, "Queen should move horizontally like rook")
        self.assertIn((0, 4), moves, "Queen should move vertically like rook")
        self.assertIn((2, 2), moves, "Queen should move diagonally like bishop")


class TestKingMovement(unittest.TestCase):
    def setUp(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
    
    def test_king_one_square_movement(self):
        """King should move one square in any direction"""
        king = King(WHITE, 0, 4, 4)
        self.board[4][4] = king
        self.kings[WHITE] = king
        
        moves = king.get_moves(self.board, 8, self.kings)
        
        expected_moves = [
            (3, 3), (3, 4), (3, 5),
            (4, 3),         (4, 5),
            (5, 3), (5, 4), (5, 5)
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"King should move to {move}")
    
    def test_king_cannot_move_into_check(self):
        """King should not move into attacked squares"""
        king = King(WHITE, 0, 7, 4)
        enemy_rook = Rook(BLACK, 0, 0, 5)
        self.board[7][4] = king
        self.board[0][5] = enemy_rook
        
        moves = king.get_moves(self.board, 8, self.kings)
        
        # King should not move to column 5 (attacked by rook)
        self.assertNotIn((7, 5), moves, "King should not move into check")
        self.assertNotIn((6, 5), moves, "King should not move into check")
    
    def test_castling_kingside(self):
        """Test kingside castling"""
        king = King(WHITE, 0, 7, 4)
        rook = Rook(WHITE, 0, 7, 7)
        self.board[7][4] = king
        self.board[7][7] = rook
        self.kings[WHITE] = king
        
        moves = king.get_moves(self.board, 8, self.kings)
        
        self.assertIn((7, 6), moves, "King should be able to castle kingside")
    
    def test_castling_blocked(self):
        """Castling should be blocked by pieces in between"""
        king = King(WHITE, 0, 7, 4)
        rook = Rook(WHITE, 0, 7, 7)
        knight = Knight(WHITE, 0, 7, 6)
        self.board[7][4] = king
        self.board[7][7] = rook
        self.board[7][6] = knight
        self.kings[WHITE] = king
        
        moves = king.get_moves(self.board, 8, self.kings)
        
        self.assertNotIn((7, 6), moves, "Castling should be blocked by pieces")
    
    def test_castling_through_check(self):
        """King cannot castle through check"""
        king = King(WHITE, 0, 7, 4)
        rook = Rook(WHITE, 0, 7, 7)
        enemy_rook = Rook(BLACK, 0, 0, 5)
        self.board[7][4] = king
        self.board[7][7] = rook
        self.board[0][5] = enemy_rook
        self.kings[WHITE] = king
        
        moves = king.get_moves(self.board, 8, self.kings)
        
        self.assertNotIn((7, 6), moves, "King cannot castle through check")


if __name__ == '__main__':
    unittest.main()
