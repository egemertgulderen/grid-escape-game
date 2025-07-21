"""
Unit tests for the InputHandler class.
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Mock pygame module
sys.modules['pygame'] = Mock()

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from input.input_handler import InputHandler


class TestInputHandler(unittest.TestCase):
    """Test cases for the InputHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.input_handler = InputHandler()
        self.game_state = Mock()
        self.renderer = Mock()
        
        # Add missing attributes to renderer mock
        self.renderer.WINDOW_WIDTH = 800
        self.renderer.WINDOW_HEIGHT = 600
        
        # Mock players and pawns
        self.mock_player = Mock()
        self.mock_pawn = Mock()
        
        # Set up game state mock
        self.game_state.get_current_player.return_value = self.mock_player
        self.game_state.board = Mock()
        self.game_state.selected_pawn = None
    
    def test_handle_click_outside_grid(self):
        """Test handling click outside the grid."""
        # Mock renderer to return None for pixel_to_grid_position
        self.renderer.pixel_to_grid_position.return_value = None
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertFalse(result)
        self.renderer.pixel_to_grid_position.assert_called_once_with((100, 100))
        self.assertIsNone(self.game_state.selected_pawn)
    
    def test_handle_click_setup_phase(self):
        """Test handling click during setup phase."""
        # Mock renderer to return grid position
        self.renderer.pixel_to_grid_position.return_value = (2, 4)
        
        # Mock game state to be in setup phase
        self.game_state.is_setup_phase.return_value = True
        self.game_state.is_movement_phase.return_value = False
        self.game_state.is_game_over.return_value = False
        
        # Mock board to validate starting position
        self.game_state.board.is_starting_position.return_value = True
        self.game_state.board.is_intersection_empty.return_value = True
        
        # Mock player to have unplaced pawns
        unplaced_pawns = [self.mock_pawn]
        self.mock_player.get_unplaced_pawns.return_value = unplaced_pawns
        
        # Mock successful pawn placement
        self.game_state.place_pawn.return_value = True
        
        # After placement, player has no more unplaced pawns
        self.mock_player.get_unplaced_pawns.side_effect = [unplaced_pawns, []]
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertTrue(result)
        self.game_state.board.is_starting_position.assert_called_once_with(2, 4, self.mock_player)
        self.game_state.board.is_intersection_empty.assert_called_once_with(2, 4)
        self.game_state.place_pawn.assert_called_once_with(self.mock_pawn, 2, 4)
        self.game_state.switch_turn.assert_called_once()
    
    def test_handle_click_setup_phase_invalid_position(self):
        """Test handling click on invalid starting position during setup phase."""
        # Mock renderer to return grid position
        self.renderer.pixel_to_grid_position.return_value = (2, 2)
        
        # Mock game state to be in setup phase
        self.game_state.is_setup_phase.return_value = True
        self.game_state.is_movement_phase.return_value = False
        self.game_state.is_game_over.return_value = False
        
        # Mock board to invalidate starting position
        self.game_state.board.is_starting_position.return_value = False
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertFalse(result)
        self.game_state.board.is_starting_position.assert_called_once_with(2, 2, self.mock_player)
        self.game_state.place_pawn.assert_not_called()
    
    def test_handle_click_movement_phase_select_pawn(self):
        """Test selecting a pawn during movement phase."""
        # Mock renderer to return grid position
        self.renderer.pixel_to_grid_position.return_value = (2, 2)
        
        # Mock game state to be in movement phase
        self.game_state.is_setup_phase.return_value = False
        self.game_state.is_movement_phase.return_value = True
        self.game_state.is_game_over.return_value = False
        
        # No pawn is currently selected
        self.game_state.selected_pawn = None
        
        # Mock player to have a pawn at the clicked position
        self.mock_player.get_pawn_at_position.return_value = self.mock_pawn
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertTrue(result)
        self.mock_player.get_pawn_at_position.assert_called_once_with(2, 2)
        self.assertEqual(self.game_state.selected_pawn, self.mock_pawn)
    
    def test_handle_click_movement_phase_move_pawn(self):
        """Test moving a selected pawn during movement phase."""
        # Mock renderer to return grid position
        self.renderer.pixel_to_grid_position.return_value = (3, 2)
        
        # Mock game state to be in movement phase
        self.game_state.is_setup_phase.return_value = False
        self.game_state.is_movement_phase.return_value = True
        self.game_state.is_game_over.return_value = False
        
        # A pawn is currently selected
        self.game_state.selected_pawn = self.mock_pawn
        
        # Mock valid moves for the selected pawn
        self.mock_pawn.get_valid_moves.return_value = [(3, 2), (2, 3)]
        
        # Mock successful pawn movement
        self.game_state.move_pawn.return_value = True
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertTrue(result)
        self.mock_pawn.get_valid_moves.assert_called_once_with(self.game_state.board)
        self.game_state.move_pawn.assert_called_once_with(self.mock_pawn, 3, 2)
    
    def test_handle_click_movement_phase_deselect_pawn(self):
        """Test deselecting a pawn during movement phase."""
        # Mock renderer to return grid position outside valid moves
        self.renderer.pixel_to_grid_position.return_value = (4, 4)
        
        # Mock game state to be in movement phase
        self.game_state.is_setup_phase.return_value = False
        self.game_state.is_movement_phase.return_value = True
        self.game_state.is_game_over.return_value = False
        
        # A pawn is currently selected
        self.game_state.selected_pawn = self.mock_pawn
        
        # Mock valid moves for the selected pawn (not including clicked position)
        self.mock_pawn.get_valid_moves.return_value = [(3, 2), (2, 3)]
        self.mock_pawn.get_position.return_value = (2, 2)
        
        # Mock that there's no pawn at the clicked position for current player
        self.mock_player.get_pawn_at_position.return_value = None
        
        # Mock the other player and its get_pawn_at_position method
        mock_other_player = Mock()
        mock_other_player.get_pawn_at_position.return_value = None
        self.game_state.get_other_player.return_value = mock_other_player
        
        # Mock board methods
        self.game_state.board.is_valid_position.return_value = True
        self.game_state.board.get_adjacent_positions.return_value = [(1, 2), (3, 2), (2, 1), (2, 3)]
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertTrue(result)
        # Verify that the input handler processed the click correctly
        self.mock_pawn.get_valid_moves.assert_called_once_with(self.game_state.board)
    
    def test_handle_click_movement_phase_select_different_pawn(self):
        """Test selecting a different pawn during movement phase."""
        # Mock renderer to return grid position
        self.renderer.pixel_to_grid_position.return_value = (4, 4)
        
        # Mock game state to be in movement phase
        self.game_state.is_setup_phase.return_value = False
        self.game_state.is_movement_phase.return_value = True
        self.game_state.is_game_over.return_value = False
        
        # A pawn is currently selected
        self.game_state.selected_pawn = self.mock_pawn
        
        # Mock valid moves for the selected pawn (not including clicked position)
        self.mock_pawn.get_valid_moves.return_value = [(3, 2), (2, 3)]
        
        # Mock that there's another pawn at the clicked position
        another_pawn = Mock()
        self.mock_player.get_pawn_at_position.return_value = another_pawn
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertTrue(result)
        self.mock_pawn.get_valid_moves.assert_called_once_with(self.game_state.board)
        self.mock_player.get_pawn_at_position.assert_called_once_with(4, 4)
        self.assertEqual(self.game_state.selected_pawn, another_pawn)
    
    def test_handle_click_game_over(self):
        """Test handling click during game over state."""
        # Mock renderer to return grid position
        self.renderer.pixel_to_grid_position.return_value = (2, 2)
        
        # Mock game state to be in game over state
        self.game_state.is_setup_phase.return_value = False
        self.game_state.is_movement_phase.return_value = False
        self.game_state.is_game_over.return_value = True
        
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        self.assertFalse(result)
    
    def test_get_intersection_from_pixel(self):
        """Test get_intersection_from_pixel method."""
        # Mock renderer to return grid position
        self.renderer.pixel_to_grid_position.return_value = (2, 3)
        
        result = self.input_handler.get_intersection_from_pixel((100, 100), self.renderer)
        
        self.assertEqual(result, (2, 3))
        self.renderer.pixel_to_grid_position.assert_called_once_with((100, 100))


if __name__ == '__main__':
    unittest.main()