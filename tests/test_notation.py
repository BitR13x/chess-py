"""Unit tests for notation utilities"""
import unittest
import sys
sys.path.insert(0, '..')

from utils.notation import NotationHelper
from pieces import Pawn, Rook, Knight, Queen, King
from constx import WHITE, BLACK


class TestNotationConversion(unittest.TestCase):
    def setUp(self):
        self.notation = NotationHelper()
    
    def test_position_to_notation(self):
        """Test converting board positions to algebraic notation"""
        self.assertEqual(self.notation.position_to_notation((7, 0)), "a1")
        self.assertEqual(self.notation.position_to_notation((7, 4)), "e1")
        self.assertEqual(self.notation.position_to_notation((0, 4)), "e8")
        self.assertEqual(self.notation.position_to_notation((0, 0)), "a8")
        self.assertEqual(self.notation.position_to_notation((0, 7)), "h8")
    
    def test_notation_to_position(self):
        """Test converting algebraic notation to board positions"""
        self.assertEqual(self.notation.notation_to_position("a1"), (7, 0))
        self.assertEqual(self.notation.notation_to_position("e1"), (7, 4))
        self.assertEqual(self.notation.notation_to_position("e8"), (0, 4))
        self.assertEqual(self.notation.notation_to_position("a8"), (0, 0))
        self.assertEqual(self.notation.notation_to_position("h8"), (0, 7))
    
    def test_pawn_move_notation(self):
        """Test pawn move notation"""
        pawn = Pawn(WHITE, 0, 6, 4)
        
        notation = self.notation.move_to_notation(
            pawn, (6, 4), (5, 4), None, False, False, False
        )
        
        self.assertEqual(notation, "e3", "Pawn move should be just the square")
    
    def test_pawn_capture_notation(self):
        """Test pawn capture notation"""
        pawn = Pawn(WHITE, 0, 5, 4)
        captured = Pawn(BLACK, 0, 4, 3)
        
        notation = self.notation.move_to_notation(
            pawn, (5, 4), (4, 3), captured, False, False, False
        )
        
        self.assertEqual(notation, "exd4", "Pawn capture should show file x square")
    
    def test_piece_move_notation(self):
        """Test piece move notation"""
        knight = Knight(WHITE, 0, 7, 1)
        
        notation = self.notation.move_to_notation(
            knight, (7, 1), (5, 2), None, False, False, False
        )
        
        self.assertEqual(notation, "Nc6", "Knight move should be N + square")
    
    def test_piece_capture_notation(self):
        """Test piece capture notation"""
        rook = Rook(WHITE, 0, 7, 0)
        captured = Pawn(BLACK, 0, 7, 7)
        
        notation = self.notation.move_to_notation(
            rook, (7, 0), (7, 7), captured, False, False, False
        )
        
        self.assertEqual(notation, "Rxh1", "Rook capture should be Rx + square")
    
    def test_castling_kingside_notation(self):
        """Test kingside castling notation"""
        king = King(WHITE, 0, 7, 4)
        
        notation = self.notation.move_to_notation(
            king, (7, 4), (7, 6), None, True, False, False
        )
        
        self.assertEqual(notation, "O-O", "Kingside castling should be O-O")
    
    def test_castling_queenside_notation(self):
        """Test queenside castling notation"""
        king = King(WHITE, 0, 7, 4)
        
        notation = self.notation.move_to_notation(
            king, (7, 4), (7, 2), None, True, False, False
        )
        
        self.assertEqual(notation, "O-O-O", "Queenside castling should be O-O-O")
    
    def test_check_notation(self):
        """Test check indicator in notation"""
        queen = Queen(WHITE, 0, 4, 4)
        
        notation = self.notation.move_to_notation(
            queen, (4, 4), (0, 4), None, False, True, False
        )
        
        self.assertEqual(notation, "Qe8+", "Check should add +")
    
    def test_checkmate_notation(self):
        """Test checkmate indicator in notation"""
        queen = Queen(WHITE, 0, 4, 4)
        
        notation = self.notation.move_to_notation(
            queen, (4, 4), (0, 4), None, False, False, True
        )
        
        self.assertEqual(notation, "Qe8#", "Checkmate should add #")


if __name__ == '__main__':
    unittest.main()
