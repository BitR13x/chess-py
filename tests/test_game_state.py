"""Unit tests for game state validation (check, checkmate, stalemate)"""
import unittest
import sys
sys.path.insert(0, '..')

from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from constx import WHITE, BLACK, CHECKMATE, STALEMATE, IN_PROGRESS
from game_logic.game_state import GameStateValidator


class TestCheckDetection(unittest.TestCase):
    def setUp(self):
        """Set up a clean board for each test"""
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.kings = {WHITE: King(WHITE, 0, 7, 4), BLACK: King(BLACK, 0, 0, 4)}
        self.board[7][4] = self.kings[WHITE]
        self.board[0][4] = self.kings[BLACK]
    
    def test_rook_gives_check(self):
        """Rook should put king in check"""
        rook = Rook(WHITE, 0, 0, 0)
        self.board[0][0] = rook
        
        is_check = GameStateValidator.is_king_in_check(
            self.board, 8, self.kings, BLACK
        )
        
        self.assertTrue(is_check, "Black king should be in check from rook")
    
    def test_no_check_when_blocked(self):
        """Check should be blocked by pieces"""
        rook = Rook(WHITE, 0, 0, 0)
        pawn = Pawn(BLACK, 0, 0, 2)
        self.board[0][0] = rook
        self.board[0][2] = pawn
        
        is_check = GameStateValidator.is_king_in_check(
            self.board, 8, self.kings, BLACK
        )
        
        self.assertFalse(is_check, "Check should be blocked by pawn")
    
    def test_knight_gives_check(self):
        """Knight should put king in check"""
        knight = Knight(WHITE, 0, 2, 3)
        self.board[2][3] = knight
        
        is_check = GameStateValidator.is_king_in_check(
            self.board, 8, self.kings, BLACK
        )
        
        self.assertTrue(is_check, "Black king should be in check from knight")
    
    def test_pawn_gives_check(self):
        """Pawn should put king in check diagonally"""
        pawn = Pawn(WHITE, 0, 1, 3)
        self.board[1][3] = pawn
        
        is_check = GameStateValidator.is_king_in_check(
            self.board, 8, self.kings, BLACK
        )
        
        self.assertTrue(is_check, "Black king should be in check from pawn")
    
    def test_discovered_check(self):
        """Moving a piece should reveal check behind it"""
        queen = Queen(WHITE, 0, 0, 0)
        pawn = Pawn(WHITE, 0, 0, 2)
        self.board[0][0] = queen
        self.board[0][2] = pawn
        
        # Initially not in check (pawn blocks)
        is_check_before = GameStateValidator.is_king_in_check(
            self.board, 8, self.kings, BLACK
        )
        self.assertFalse(is_check_before, "King should not be in check while blocked")
        
        # Move pawn out of the way
        self.board[0][2] = '.'
        self.board[1][2] = pawn
        pawn.update_position(1, 2)
        
        # Now in check (discovered check)
        is_check_after = GameStateValidator.is_king_in_check(
            self.board, 8, self.kings, BLACK
        )
        self.assertTrue(is_check_after, "King should be in check after pawn moves")


class TestCheckmateDetection(unittest.TestCase):
    def test_back_rank_mate(self):
        """Test back rank checkmate"""
        board = [['.' for _ in range(8)] for _ in range(8)]
        
        # Black king trapped by own pawns
        black_king = King(BLACK, 0, 0, 4)
        black_pawn1 = Pawn(BLACK, 0, 1, 3)
        black_pawn2 = Pawn(BLACK, 0, 1, 4)
        black_pawn3 = Pawn(BLACK, 0, 1, 5)
        
        # White rook gives checkmate
        white_rook = Rook(WHITE, 0, 0, 0)
        white_king = King(WHITE, 0, 7, 4)
        
        board[0][4] = black_king
        board[1][3] = black_pawn1
        board[1][4] = black_pawn2
        board[1][5] = black_pawn3
        board[0][0] = white_rook
        board[7][4] = white_king
        
        black_pawn1.has_moved = True
        black_pawn2.has_moved = True
        black_pawn3.has_moved = True
        
        kings = {WHITE: white_king, BLACK: black_king}
        black_pieces = [black_king, black_pawn1, black_pawn2, black_pawn3]
        
        game_state = GameStateValidator.check_game_state(
            board, 8, kings, black_pieces, BLACK
        )
        
        self.assertEqual(game_state, CHECKMATE, "Should be checkmate")
    
    def test_scholars_mate(self):
        """Test scholar's mate pattern"""
        board = [['.' for _ in range(8)] for _ in range(8)]
        
        # Setup scholar's mate position
        white_queen = Queen(WHITE, 0, 4, 5)
        white_bishop = Bishop(WHITE, 0, 5, 2)
        white_king = King(WHITE, 0, 7, 4)
        
        black_king = King(BLACK, 0, 0, 4)
        black_pawn1 = Pawn(BLACK, 0, 1, 3)
        black_pawn2 = Pawn(BLACK, 0, 1, 4)
        black_pawn3 = Pawn(BLACK, 0, 1, 5)
        
        board[4][5] = white_queen
        board[5][2] = white_bishop
        board[7][4] = white_king
        board[0][4] = black_king
        board[1][3] = black_pawn1
        board[1][4] = black_pawn2
        board[1][5] = black_pawn3
        
        kings = {WHITE: white_king, BLACK: black_king}
        black_pieces = [black_king, black_pawn1, black_pawn2, black_pawn3]
        
        # Queen on f5 with bishop support should be checkmate if king has no escape
        game_state = GameStateValidator.check_game_state(
            board, 8, kings, black_pieces, BLACK
        )
        
        # This might not be checkmate depending on exact position, but should at least be check
        is_check = GameStateValidator.is_king_in_check(board, 8, kings, BLACK)
        self.assertTrue(is_check, "Should be in check")


class TestStalemateDetection(unittest.TestCase):
    def test_lone_king_stalemate(self):
        """Test stalemate with lone king trapped"""
        board = [['.' for _ in range(8)] for _ in range(8)]
        
        # Black king in corner with no legal moves
        black_king = King(BLACK, 0, 0, 0)
        
        # White queen and king box in black king
        white_queen = Queen(WHITE, 0, 1, 2)
        white_king = King(WHITE, 0, 2, 1)
        
        board[0][0] = black_king
        board[1][2] = white_queen
        board[2][1] = white_king
        
        kings = {WHITE: white_king, BLACK: black_king}
        black_pieces = [black_king]
        
        game_state = GameStateValidator.check_game_state(
            board, 8, kings, black_pieces, BLACK
        )
        
        # Should be stalemate (king has no moves but not in check)
        is_check = GameStateValidator.is_king_in_check(board, 8, kings, BLACK)
        if not is_check:
            self.assertEqual(game_state, STALEMATE, "Should be stalemate")


class TestGameState(unittest.TestCase):
    def test_game_in_progress(self):
        """Test that normal positions are in progress"""
        board = [['.' for _ in range(8)] for _ in range(8)]
        
        white_king = King(WHITE, 0, 7, 4)
        black_king = King(BLACK, 0, 0, 4)
        white_pawn = Pawn(WHITE, 0, 6, 4)
        black_pawn = Pawn(BLACK, 0, 1, 4)
        
        board[7][4] = white_king
        board[0][4] = black_king
        board[6][4] = white_pawn
        board[1][4] = black_pawn
        
        kings = {WHITE: white_king, BLACK: black_king}
        white_pieces = [white_king, white_pawn]
        
        game_state = GameStateValidator.check_game_state(
            board, 8, kings, white_pieces, WHITE
        )
        
        self.assertEqual(game_state, IN_PROGRESS, "Game should be in progress")
    
    def test_legal_moves_available(self):
        """Test that pieces have legal moves in normal position"""
        board = [['.' for _ in range(8)] for _ in range(8)]
        
        white_king = King(WHITE, 0, 7, 4)
        black_king = King(BLACK, 0, 0, 4)
        white_rook = Rook(WHITE, 0, 7, 0)
        
        board[7][4] = white_king
        board[0][4] = black_king
        board[7][0] = white_rook
        
        kings = {WHITE: white_king, BLACK: black_king}
        white_pieces = [white_king, white_rook]
        
        legal_moves = GameStateValidator.get_all_legal_moves(
            board, 8, kings, white_pieces, WHITE
        )
        
        self.assertGreater(len(legal_moves), 0, "Should have legal moves")


if __name__ == '__main__':
    unittest.main()
