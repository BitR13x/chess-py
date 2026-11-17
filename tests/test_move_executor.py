"""Unit tests for move execution and undo functionality"""
import unittest
import sys
sys.path.insert(0, '..')

from pieces import Pawn, Rook, Knight, King
from constx import WHITE, BLACK
from game_logic.move_executor import MoveExecutor


class MockUI:
    """Mock UI for testing"""
    pass


class TestMoveExecution(unittest.TestCase):
    def setUp(self):
        """Set up a clean board for each test"""
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
        self.executor = MoveExecutor(self.board, MockUI())
    
    def test_simple_move(self):
        """Test basic piece movement"""
        pawn = Pawn(WHITE, 0, 6, 4)
        self.board[6][4] = pawn
        
        move_data = self.executor.execute_move(pawn, 5, 4, None)
        
        self.assertEqual(self.board[5][4], pawn, "Pawn should be at new position")
        self.assertEqual(self.board[6][4], '.', "Old position should be empty")
        self.assertEqual(pawn.position, (5, 4), "Pawn position should be updated")
        self.assertTrue(pawn.has_moved, "Pawn should be marked as moved")
    
    def test_capture_move(self):
        """Test capturing an enemy piece"""
        white_pawn = Pawn(WHITE, 0, 4, 4)
        black_pawn = Pawn(BLACK, 0, 3, 5)
        self.board[4][4] = white_pawn
        self.board[3][5] = black_pawn
        
        move_data = self.executor.execute_move(white_pawn, 3, 5, None)
        
        self.assertEqual(self.board[3][5], white_pawn, "White pawn should capture")
        self.assertEqual(move_data['captured'], black_pawn, "Should record captured piece")
        self.assertFalse(move_data['is_en_passant'], "Should not be en passant")
    
    def test_en_passant_capture(self):
        """Test en passant capture execution"""
        white_pawn = Pawn(WHITE, 0, 3, 4)
        black_pawn = Pawn(BLACK, 0, 3, 5)
        white_pawn.has_moved = True
        black_pawn.has_moved = True
        
        self.board[3][4] = white_pawn
        self.board[3][5] = black_pawn
        
        # Simulate black pawn just moved two squares
        last_move = (black_pawn, (1, 5), (3, 5))
        
        move_data = self.executor.execute_move(white_pawn, 2, 5, last_move)
        
        self.assertTrue(move_data['is_en_passant'], "Should be en passant")
        self.assertEqual(move_data['captured'], black_pawn, "Should capture black pawn")
        self.assertEqual(self.board[3][5], '.', "Captured pawn square should be empty")
    
    def test_castling_kingside(self):
        """Test kingside castling execution"""
        king = King(WHITE, 0, 7, 4)
        rook = Rook(WHITE, 0, 7, 7)
        self.board[7][4] = king
        self.board[7][7] = rook
        self.kings[WHITE] = king
        
        move_data = self.executor.execute_move(king, 7, 6, None)
        
        self.assertTrue(move_data['is_castling'], "Should be castling")
        self.assertEqual(self.board[7][6], king, "King should be at g1")
        self.assertEqual(self.board[7][5], rook, "Rook should be at f1")
        self.assertEqual(self.board[7][4], '.', "King's old square should be empty")
        self.assertEqual(self.board[7][7], '.', "Rook's old square should be empty")
    
    def test_castling_queenside(self):
        """Test queenside castling execution"""
        king = King(WHITE, 0, 7, 4)
        rook = Rook(WHITE, 0, 7, 0)
        self.board[7][4] = king
        self.board[7][0] = rook
        self.kings[WHITE] = king
        
        move_data = self.executor.execute_move(king, 7, 2, None)
        
        self.assertTrue(move_data['is_castling'], "Should be castling")
        self.assertEqual(self.board[7][2], king, "King should be at c1")
        self.assertEqual(self.board[7][3], rook, "Rook should be at d1")


class TestMoveUndo(unittest.TestCase):
    def setUp(self):
        """Set up a clean board for each test"""
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
        self.executor = MoveExecutor(self.board, MockUI())
        self.pieces_notation = {
            "R": Rook,
            "N": Knight,
            "P": Pawn,
            "K": King
        }
    
    def test_undo_simple_move(self):
        """Test undoing a basic move"""
        pawn = Pawn(WHITE, 0, 6, 4)
        self.board[6][4] = pawn
        
        # Execute move
        move_data = self.executor.execute_move(pawn, 5, 4, None)
        
        # Undo move
        self.executor.undo_move(move_data, self.pieces_notation)
        
        self.assertEqual(self.board[6][4], pawn, "Pawn should be back at start")
        self.assertEqual(self.board[5][4], '.', "Target square should be empty")
        self.assertEqual(pawn.position, (6, 4), "Pawn position should be restored")
        self.assertFalse(pawn.has_moved, "Pawn should be marked as not moved")
    
    def test_undo_capture(self):
        """Test undoing a capture"""
        white_pawn = Pawn(WHITE, 0, 4, 4)
        black_pawn = Pawn(BLACK, 0, 3, 5)
        self.board[4][4] = white_pawn
        self.board[3][5] = black_pawn
        
        # Execute capture
        move_data = self.executor.execute_move(white_pawn, 3, 5, None)
        
        # Undo capture
        self.executor.undo_move(move_data, self.pieces_notation)
        
        self.assertEqual(self.board[4][4], white_pawn, "White pawn should be restored")
        self.assertEqual(self.board[3][5], black_pawn, "Black pawn should be restored")
        self.assertFalse(white_pawn.has_moved, "White pawn should not be marked as moved")
    
    def test_undo_castling(self):
        """Test undoing castling"""
        king = King(WHITE, 0, 7, 4)
        rook = Rook(WHITE, 0, 7, 7)
        self.board[7][4] = king
        self.board[7][7] = rook
        self.kings[WHITE] = king
        
        # Execute castling
        move_data = self.executor.execute_move(king, 7, 6, None)
        
        # Undo castling
        self.executor.undo_move(move_data, self.pieces_notation)
        
        self.assertEqual(self.board[7][4], king, "King should be back at e1")
        self.assertEqual(self.board[7][7], rook, "Rook should be back at h1")
        self.assertEqual(self.board[7][6], '.', "g1 should be empty")
        self.assertEqual(self.board[7][5], '.', "f1 should be empty")
        self.assertFalse(king.has_moved, "King should not be marked as moved")
        self.assertFalse(rook.has_moved, "Rook should not be marked as moved")


if __name__ == '__main__':
    unittest.main()
