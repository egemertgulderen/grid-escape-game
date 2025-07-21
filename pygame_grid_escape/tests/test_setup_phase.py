"""
Integration tests for the setup phase of the Grid Escape game.

These tests verify the complete setup phase workflow including pawn placement,
player turn switching, and transition to the movement phase.
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Mock pygame module
sys.modules['pygame'] = Mock()

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_logic.game_state import GameState
from game_logic.board import Board
from game_logic.player import Player
from input.input_handler import InputHandler


class TestSetupPhase(unittest.TestCase):
    """Test cases for the setup phase workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game_state = GameState()
        self.renderer = Mock()
        self.input_handler = InputHandler(self.renderer)
        
        # Ensure game is in setup phase
        self.game_state.phase = GameState.SETUP
        
        # Mock renderer's pixel_to_grid_position method
        self.renderer.pixel_to_grid_position = lambda pos: pos
    
    def test_initial_setup_state(self):
        """Test the initial state of the game during setup phase."""
        # Game should start in setup phase
        self.assertTrue(self.game_state.is_setup_phase())
        self.assertFalse(self.game_state.is_movement_phase())
        self.assertFalse(self.game_state.is_game_over())
        
        # Player 1 should go first
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
        
        # Each player should have 7 unplaced pawns
        player1 = self.game_state.players[0]
        player2 = self.game_state.players[1]
        self.assertEqual(len(player1.get_unplaced_pawns()), 7)
        self.assertEqual(len(player2.get_unplaced_pawns()), 7)
        
        # No pawns should be on the board
        self.assertEqual(len(player1.get_pawns_on_board()), 0)
        self.assertEqual(len(player2.get_pawns_on_board()), 0)
        
        # Setup should not be complete
        self.assertFalse(self.game_state.is_setup_complete())
    
    def test_place_pawn_valid_position(self):
        """Test placing a pawn at a valid starting position."""
        # Player 1's starting positions are on the bottom row (y=4)
        result = self.input_handler._handle_setup_phase_click(2, 4, self.game_state)
        
        # Pawn should be placed successfully
        self.assertTrue(result)
        
        # Player 1 should have one less unplaced pawn
        player1 = self.game_state.players[0]
        self.assertEqual(len(player1.get_unplaced_pawns()), 6)
        self.assertEqual(len(player1.get_pawns_on_board()), 1)
        
        # The pawn should be at the specified position
        pawn = player1.get_pawns_on_board()[0]
        self.assertEqual(pawn.get_position(), (2, 4))
        
        # Current player should still be player 1
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
    
    def test_place_pawn_invalid_position(self):
        """Test placing a pawn at an invalid starting position."""
        # Player 1's starting positions are on the bottom row (y=4), not middle row (y=2)
        result = self.input_handler._handle_setup_phase_click(2, 2, self.game_state)
        
        # Pawn placement should fail
        self.assertFalse(result)
        
        # Player 1 should still have all unplaced pawns
        player1 = self.game_state.players[0]
        self.assertEqual(len(player1.get_unplaced_pawns()), 7)
        self.assertEqual(len(player1.get_pawns_on_board()), 0)
    
    def test_place_pawn_occupied_position(self):
        """Test placing a pawn at an already occupied position."""
        # Place first pawn
        self.input_handler._handle_setup_phase_click(2, 4, self.game_state)
        
        # Try to place another pawn at the same position
        result = self.input_handler._handle_setup_phase_click(2, 4, self.game_state)
        
        # Pawn placement should fail
        self.assertFalse(result)
        
        # Player 1 should still have 6 unplaced pawns (one was placed successfully)
        player1 = self.game_state.players[0]
        self.assertEqual(len(player1.get_unplaced_pawns()), 6)
        self.assertEqual(len(player1.get_pawns_on_board()), 1)
    
    def test_player_switch_after_placing_all_pawns(self):
        """Test that turn switches to player 2 after player 1 places all pawns."""
        player1 = self.game_state.players[0]
        
        # Temporarily modify the is_starting_position method to allow more positions
        original_is_starting_position = self.game_state.board.is_starting_position
        
        def modified_is_starting_position(x, y, player):
            if player.player_id == 1:
                return y == 4 or y == 3  # Allow both bottom rows
            else:
                return original_is_starting_position(x, y, player)
        
        # Apply the monkey patch
        self.game_state.board.is_starting_position = modified_is_starting_position
        
        # Create a list of unique positions for all 7 pawns
        positions = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (0, 3), (1, 3)]
        
        # Place all 7 pawns for player 1
        for i in range(7):
            pawn = player1.get_unplaced_pawns()[0]
            x, y = positions[i]
            self.game_state.place_pawn(pawn, x, y)
        
        # Player 1 should have placed all pawns
        self.assertEqual(len(player1.get_unplaced_pawns()), 0)
        
        # Current player should now be player 2
        self.assertEqual(self.game_state.get_current_player().player_id, 2)
        
        # Game should still be in setup phase
        self.assertTrue(self.game_state.is_setup_phase())
    
    def test_transition_to_movement_phase(self):
        """Test transition from setup to movement phase after all pawns are placed."""
        player1 = self.game_state.players[0]
        player2 = self.game_state.players[1]
        
        # Temporarily modify the is_starting_position method to allow more positions
        original_is_starting_position = self.game_state.board.is_starting_position
        
        def modified_is_starting_position(x, y, player):
            if player.player_id == 1:
                return y == 4 or y == 3  # Allow both bottom rows for player 1
            elif player.player_id == 2:
                return y == 0 or y == 1  # Allow both top rows for player 2
            else:
                return original_is_starting_position(x, y, player)
        
        # Apply the monkey patch
        self.game_state.board.is_starting_position = modified_is_starting_position
        
        # Create lists of unique positions for all 7 pawns for each player
        positions_player1 = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (0, 3), (1, 3)]
        positions_player2 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1)]
        
        # Place all 7 pawns for player 1
        for i in range(7):
            pawn = player1.get_unplaced_pawns()[0]
            x, y = positions_player1[i]
            self.game_state.place_pawn(pawn, x, y)
        
        # Place all 7 pawns for player 2
        for i in range(7):
            pawn = player2.get_unplaced_pawns()[0]
            x, y = positions_player2[i]
            self.game_state.place_pawn(pawn, x, y)
        
        # All pawns should be placed
        self.assertEqual(len(player1.get_unplaced_pawns()), 0)
        self.assertEqual(len(player2.get_unplaced_pawns()), 0)
        
        # Setup should be complete
        self.assertTrue(self.game_state.is_setup_complete())
        
        # Game should be in movement phase
        self.assertTrue(self.game_state.is_movement_phase())
        self.assertFalse(self.game_state.is_setup_phase())
        
        # Player 1 should be the current player in movement phase
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
    
    def test_handle_click_setup_phase(self):
        """Test the handle_click method during setup phase."""
        # Create a proper mock for renderer
        self.renderer.pixel_to_grid_position = Mock(return_value=(2, 4))
        
        # Handle click
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        # Click should be processed successfully
        self.assertTrue(result)
        
        # A pawn should be placed
        player1 = self.game_state.players[0]
        self.assertEqual(len(player1.get_unplaced_pawns()), 6)
        self.assertEqual(len(player1.get_pawns_on_board()), 1)
    
    def test_handle_click_outside_grid(self):
        """Test handling click outside the grid during setup phase."""
        # Mock renderer to return None for pixel_to_grid_position
        self.renderer.pixel_to_grid_position.return_value = None
        
        # Handle click
        result = self.input_handler.handle_click((100, 100), self.game_state, self.renderer)
        
        # Click should not be processed
        self.assertFalse(result)
        
        # No pawns should be placed
        player1 = self.game_state.players[0]
        self.assertEqual(len(player1.get_unplaced_pawns()), 7)
        self.assertEqual(len(player1.get_pawns_on_board()), 0)


if __name__ == '__main__':
    unittest.main()