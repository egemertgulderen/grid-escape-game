"""
Unit tests for the Pawn class.
"""
import unittest
import sys
import os
from unittest.mock import Mock

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_logic.pawn import Pawn


class TestPawn(unittest.TestCase):
    """Test cases for the Pawn class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_player = Mock()
        self.mock_player.player_id = 1
        self.pawn = Pawn(self.mock_player, 0)
    
    def test_pawn_initialization(self):
        """Test that a pawn is properly initialized."""
        self.assertEqual(self.pawn.player, self.mock_player)
        self.assertEqual(self.pawn.pawn_id, 0)
        self.assertIsNone(self.pawn.get_position())
        self.assertFalse(self.pawn.is_on_board())
        self.assertFalse(self.pawn.is_escaped())
    
    def test_set_and_get_position(self):
        """Test setting and getting pawn position."""
        # Initially no position
        self.assertIsNone(self.pawn.get_position())
        
        # Set position
        self.pawn.set_position(2, 3)
        self.assertEqual(self.pawn.get_position(), (2, 3))
        self.assertTrue(self.pawn.is_on_board())
        self.assertFalse(self.pawn.is_escaped())
    
    def test_is_on_board(self):
        """Test the is_on_board method."""
        # Initially not on board
        self.assertFalse(self.pawn.is_on_board())
        
        # Place on board
        self.pawn.set_position(1, 1)
        self.assertTrue(self.pawn.is_on_board())
        
        # Escape from board
        self.pawn.escape()
        self.assertFalse(self.pawn.is_on_board())
    
    def test_escape(self):
        """Test the escape functionality."""
        # Place pawn on board first
        self.pawn.set_position(2, 2)
        self.assertTrue(self.pawn.is_on_board())
        self.assertFalse(self.pawn.is_escaped())
        
        # Escape the pawn
        self.pawn.escape()
        self.assertFalse(self.pawn.is_on_board())
        self.assertTrue(self.pawn.is_escaped())
        self.assertIsNone(self.pawn.get_position())
    
    def test_set_position_resets_escaped_state(self):
        """Test that setting position resets escaped state."""
        # Escape the pawn first
        self.pawn.set_position(1, 1)
        self.pawn.escape()
        self.assertTrue(self.pawn.is_escaped())
        
        # Set new position should reset escaped state
        self.pawn.set_position(3, 3)
        self.assertFalse(self.pawn.is_escaped())
        self.assertTrue(self.pawn.is_on_board())
        self.assertEqual(self.pawn.get_position(), (3, 3))
    
    def test_get_valid_moves_empty_when_not_on_board(self):
        """Test that get_valid_moves returns empty list when pawn not on board."""
        mock_board = Mock()
        
        # Pawn not on board
        self.assertEqual(self.pawn.get_valid_moves(mock_board), [])
        
        # Escaped pawn
        self.pawn.set_position(1, 1)
        self.pawn.escape()
        self.assertEqual(self.pawn.get_valid_moves(mock_board), [])
    
    def test_get_valid_moves_with_board(self):
        """Test that get_valid_moves uses board's get_valid_moves_from_position method."""
        mock_board = Mock()
        mock_board.get_valid_moves_from_position.return_value = [(1, 2), (3, 2)]
        
        self.pawn.set_position(2, 2)
        valid_moves = self.pawn.get_valid_moves(mock_board)
        
        # Should call board's method with pawn's position
        mock_board.get_valid_moves_from_position.assert_called_once_with(2, 2)
        self.assertEqual(valid_moves, [(1, 2), (3, 2)])
    
    def test_can_move_to_valid_position(self):
        """Test can_move_to method with valid positions."""
        mock_board = Mock()
        mock_board.get_valid_moves_from_position.return_value = [(1, 2), (3, 2), (2, 1), (2, 3)]
        
        self.pawn.set_position(2, 2)
        
        # Test valid moves
        self.assertTrue(self.pawn.can_move_to(mock_board, 1, 2))
        self.assertTrue(self.pawn.can_move_to(mock_board, 3, 2))
        self.assertTrue(self.pawn.can_move_to(mock_board, 2, 1))
        self.assertTrue(self.pawn.can_move_to(mock_board, 2, 3))
        
        # Test invalid move
        self.assertFalse(self.pawn.can_move_to(mock_board, 1, 1))  # Diagonal move
        self.assertFalse(self.pawn.can_move_to(mock_board, 4, 4))  # Far away
    
    def test_can_move_to_when_not_on_board(self):
        """Test can_move_to returns False when pawn not on board."""
        mock_board = Mock()
        
        # Pawn not on board
        self.assertFalse(self.pawn.can_move_to(mock_board, 1, 1))
        
        # Escaped pawn
        self.pawn.set_position(1, 1)
        self.pawn.escape()
        self.assertFalse(self.pawn.can_move_to(mock_board, 2, 2))
    
    def test_move_to_valid_position(self):
        """Test move_to method with valid move."""
        mock_board = Mock()
        mock_board.get_valid_moves_from_position.return_value = [(1, 2), (3, 2)]
        mock_board.move_pawn.return_value = True
        mock_board.is_escape_position.return_value = False
        
        self.pawn.set_position(2, 2)
        
        # Test successful move
        result = self.pawn.move_to(mock_board, 1, 2)
        self.assertTrue(result)
        
        # Verify board methods were called correctly
        mock_board.move_pawn.assert_called_once_with(2, 2, 1, 2)
        mock_board.is_escape_position.assert_called_once_with(1, 2, self.mock_player)
        
        # Verify pawn position was updated
        self.assertEqual(self.pawn.get_position(), (1, 2))
        self.assertTrue(self.pawn.is_on_board())
        self.assertFalse(self.pawn.is_escaped())
    
    def test_move_to_invalid_position(self):
        """Test move_to method with invalid move."""
        mock_board = Mock()
        mock_board.get_valid_moves_from_position.return_value = [(1, 2), (3, 2)]
        
        self.pawn.set_position(2, 2)
        original_position = self.pawn.get_position()
        
        # Test invalid move (not in valid moves list)
        result = self.pawn.move_to(mock_board, 4, 4)
        self.assertFalse(result)
        
        # Verify position didn't change
        self.assertEqual(self.pawn.get_position(), original_position)
        
        # Verify board.move_pawn was not called
        mock_board.move_pawn.assert_not_called()
    
    def test_move_to_board_move_fails(self):
        """Test move_to when board.move_pawn fails."""
        mock_board = Mock()
        mock_board.get_valid_moves_from_position.return_value = [(1, 2), (3, 2)]
        mock_board.move_pawn.return_value = False  # Board move fails
        
        self.pawn.set_position(2, 2)
        original_position = self.pawn.get_position()
        
        # Test move that fails at board level
        result = self.pawn.move_to(mock_board, 1, 2)
        self.assertFalse(result)
        
        # Verify position didn't change
        self.assertEqual(self.pawn.get_position(), original_position)
        
        # Verify board.move_pawn was called but failed
        mock_board.move_pawn.assert_called_once_with(2, 2, 1, 2)
    
    def test_move_to_escape_position(self):
        """Test move_to method when moving to escape position."""
        mock_board = Mock()
        mock_board.get_valid_moves_from_position.return_value = [(2, 0)]  # Escape position
        mock_board.move_pawn.return_value = True
        mock_board.is_escape_position.return_value = True  # This is an escape position
        
        self.pawn.set_position(2, 1)
        
        # Test move to escape position
        result = self.pawn.move_to(mock_board, 2, 0)
        self.assertTrue(result)
        
        # Verify board methods were called correctly
        mock_board.move_pawn.assert_called_once_with(2, 1, 2, 0)
        mock_board.is_escape_position.assert_called_once_with(2, 0, self.mock_player)
        mock_board.remove_pawn.assert_called_once_with(2, 0)
        
        # Verify pawn escaped
        self.assertFalse(self.pawn.is_on_board())
        self.assertTrue(self.pawn.is_escaped())
        self.assertIsNone(self.pawn.get_position())
    
    def test_move_to_when_not_on_board(self):
        """Test move_to returns False when pawn not on board."""
        mock_board = Mock()
        
        # Pawn not on board
        result = self.pawn.move_to(mock_board, 1, 1)
        self.assertFalse(result)
        
        # Escaped pawn
        self.pawn.set_position(1, 1)
        self.pawn.escape()
        result = self.pawn.move_to(mock_board, 2, 2)
        self.assertFalse(result)
    
    def test_get_adjacent_positions(self):
        """Test get_adjacent_positions method."""
        mock_board = Mock()
        mock_board.get_adjacent_intersections.return_value = [(1, 2), (3, 2), (2, 1), (2, 3)]
        
        self.pawn.set_position(2, 2)
        adjacent_positions = self.pawn.get_adjacent_positions(mock_board)
        
        # Should call board's method with pawn's position
        mock_board.get_adjacent_intersections.assert_called_once_with(2, 2)
        self.assertEqual(adjacent_positions, [(1, 2), (3, 2), (2, 1), (2, 3)])
    
    def test_get_adjacent_positions_when_not_on_board(self):
        """Test get_adjacent_positions returns empty list when pawn not on board."""
        mock_board = Mock()
        
        # Pawn not on board
        self.assertEqual(self.pawn.get_adjacent_positions(mock_board), [])
        
        # Escaped pawn
        self.pawn.set_position(1, 1)
        self.pawn.escape()
        self.assertEqual(self.pawn.get_adjacent_positions(mock_board), [])
    
    def test_is_blocked(self):
        """Test is_blocked method."""
        mock_board = Mock()
        
        # Pawn with valid moves is not blocked
        mock_board.get_valid_moves_from_position.return_value = [(1, 2), (3, 2)]
        self.pawn.set_position(2, 2)
        self.assertFalse(self.pawn.is_blocked(mock_board))
        
        # Pawn with no valid moves is blocked
        mock_board.get_valid_moves_from_position.return_value = []
        self.assertTrue(self.pawn.is_blocked(mock_board))
    
    def test_is_adjacent_to(self):
        """Test is_adjacent_to method."""
        self.pawn.set_position(2, 2)
        
        # Test adjacent positions
        self.assertTrue(self.pawn.is_adjacent_to(1, 2))  # Left
        self.assertTrue(self.pawn.is_adjacent_to(3, 2))  # Right
        self.assertTrue(self.pawn.is_adjacent_to(2, 1))  # Up
        self.assertTrue(self.pawn.is_adjacent_to(2, 3))  # Down
        
        # Test non-adjacent positions
        self.assertFalse(self.pawn.is_adjacent_to(1, 1))  # Diagonal
        self.assertFalse(self.pawn.is_adjacent_to(3, 3))  # Diagonal
        self.assertFalse(self.pawn.is_adjacent_to(4, 2))  # Too far
        self.assertFalse(self.pawn.is_adjacent_to(2, 4))  # Too far
    
    def test_is_adjacent_to_when_not_on_board(self):
        """Test is_adjacent_to returns False when pawn not on board."""
        # Pawn not on board
        self.assertFalse(self.pawn.is_adjacent_to(1, 1))
        
        # Escaped pawn
        self.pawn.set_position(1, 1)
        self.pawn.escape()
        self.assertFalse(self.pawn.is_adjacent_to(1, 2))
    
    def test_would_escape_at(self):
        """Test would_escape_at method."""
        mock_board = Mock()
        
        # Position is an escape position
        mock_board.is_escape_position.return_value = True
        self.pawn.set_position(2, 1)
        self.assertTrue(self.pawn.would_escape_at(mock_board, 2, 0))
        mock_board.is_escape_position.assert_called_with(2, 0, self.mock_player)
        
        # Position is not an escape position
        mock_board.is_escape_position.return_value = False
        self.assertFalse(self.pawn.would_escape_at(mock_board, 2, 2))
        mock_board.is_escape_position.assert_called_with(2, 2, self.mock_player)


if __name__ == '__main__':
    unittest.main()