"""
Unit tests for the Player class.
"""
import unittest
import sys
import os
from unittest.mock import Mock

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_logic.player import Player


class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(1, (0, 0, 255))  # Blue player
    
    def test_player_initialization(self):
        """Test that a player is properly initialized."""
        self.assertEqual(self.player.player_id, 1)
        self.assertEqual(self.player.color, (0, 0, 255))
        
        # Should have 7 pawns
        pawns = self.player.get_pawns()
        self.assertEqual(len(pawns), 7)
        
        # All pawns should belong to this player
        for i, pawn in enumerate(pawns):
            self.assertEqual(pawn.player, self.player)
            self.assertEqual(pawn.pawn_id, i)
    
    def test_get_pawns_on_board_initially_empty(self):
        """Test that initially no pawns are on board."""
        self.assertEqual(len(self.player.get_pawns_on_board()), 0)
    
    def test_get_escaped_pawns_initially_empty(self):
        """Test that initially no pawns have escaped."""
        self.assertEqual(len(self.player.get_escaped_pawns()), 0)
    
    def test_get_unplaced_pawns_initially_all(self):
        """Test that initially all pawns are unplaced."""
        unplaced = self.player.get_unplaced_pawns()
        self.assertEqual(len(unplaced), 7)
    
    def test_pawns_on_board_tracking(self):
        """Test tracking of pawns on board."""
        pawns = self.player.get_pawns()
        
        # Place some pawns on board
        pawns[0].set_position(0, 0)
        pawns[1].set_position(1, 0)
        pawns[2].set_position(2, 0)
        
        on_board = self.player.get_pawns_on_board()
        self.assertEqual(len(on_board), 3)
        self.assertIn(pawns[0], on_board)
        self.assertIn(pawns[1], on_board)
        self.assertIn(pawns[2], on_board)
        
        # Check unplaced pawns
        unplaced = self.player.get_unplaced_pawns()
        self.assertEqual(len(unplaced), 4)
    
    def test_escaped_pawns_tracking(self):
        """Test tracking of escaped pawns."""
        pawns = self.player.get_pawns()
        
        # Place and escape some pawns
        pawns[0].set_position(0, 0)
        pawns[0].escape()
        pawns[1].set_position(1, 0)
        pawns[1].escape()
        
        escaped = self.player.get_escaped_pawns()
        self.assertEqual(len(escaped), 2)
        self.assertIn(pawns[0], escaped)
        self.assertIn(pawns[1], escaped)
        
        # Should not be on board
        on_board = self.player.get_pawns_on_board()
        self.assertEqual(len(on_board), 0)
        
        # Should not be unplaced
        unplaced = self.player.get_unplaced_pawns()
        self.assertEqual(len(unplaced), 5)
    
    def test_has_won_false_initially(self):
        """Test that player hasn't won initially."""
        self.assertFalse(self.player.has_won())
    
    def test_has_won_false_with_some_escaped(self):
        """Test that player hasn't won with only some pawns escaped."""
        pawns = self.player.get_pawns()
        
        # Escape 6 pawns
        for i in range(6):
            pawns[i].set_position(i, 0)
            pawns[i].escape()
        
        self.assertFalse(self.player.has_won())
    
    def test_has_won_true_with_all_escaped(self):
        """Test that player wins when all 7 pawns escape."""
        pawns = self.player.get_pawns()
        
        # Escape all 7 pawns
        for i in range(7):
            pawns[i].set_position(i % 5, 0)
            pawns[i].escape()
        
        self.assertTrue(self.player.has_won())
    
    def test_can_move_any_pawn_false_when_no_pawns_on_board(self):
        """Test that can_move_any_pawn returns False when no pawns on board."""
        mock_board = Mock()
        self.assertFalse(self.player.can_move_any_pawn(mock_board))
    
    def test_can_move_any_pawn_false_when_no_valid_moves(self):
        """Test that can_move_any_pawn returns False when no pawns can move."""
        mock_board = Mock()
        pawns = self.player.get_pawns()
        
        # Place pawns on board but mock no valid moves
        pawns[0].set_position(0, 0)
        pawns[1].set_position(1, 0)
        
        # Mock get_valid_moves to return empty list
        for pawn in pawns:
            pawn.get_valid_moves = Mock(return_value=[])
        
        self.assertFalse(self.player.can_move_any_pawn(mock_board))
    
    def test_can_move_any_pawn_true_when_pawn_can_move(self):
        """Test that can_move_any_pawn returns True when at least one pawn can move."""
        mock_board = Mock()
        pawns = self.player.get_pawns()
        
        # Place pawns on board
        pawns[0].set_position(0, 0)
        pawns[1].set_position(1, 0)
        
        # Mock first pawn to have no moves, second to have moves
        pawns[0].get_valid_moves = Mock(return_value=[])
        pawns[1].get_valid_moves = Mock(return_value=[(2, 0)])
        
        self.assertTrue(self.player.can_move_any_pawn(mock_board))
    
    def test_get_pawn_at_position_none_when_no_pawn(self):
        """Test that get_pawn_at_position returns None when no pawn at position."""
        self.assertIsNone(self.player.get_pawn_at_position(0, 0))
    
    def test_get_pawn_at_position_returns_pawn_when_present(self):
        """Test that get_pawn_at_position returns pawn when present."""
        pawns = self.player.get_pawns()
        pawns[0].set_position(2, 3)
        
        found_pawn = self.player.get_pawn_at_position(2, 3)
        self.assertEqual(found_pawn, pawns[0])
        
        # Should return None for different position
        self.assertIsNone(self.player.get_pawn_at_position(1, 1))
    
    def test_get_pawn_at_position_multiple_pawns(self):
        """Test get_pawn_at_position with multiple pawns on board."""
        pawns = self.player.get_pawns()
        pawns[0].set_position(0, 0)
        pawns[1].set_position(1, 1)
        pawns[2].set_position(2, 2)
        
        self.assertEqual(self.player.get_pawn_at_position(0, 0), pawns[0])
        self.assertEqual(self.player.get_pawn_at_position(1, 1), pawns[1])
        self.assertEqual(self.player.get_pawn_at_position(2, 2), pawns[2])
        self.assertIsNone(self.player.get_pawn_at_position(3, 3))


if __name__ == '__main__':
    unittest.main()