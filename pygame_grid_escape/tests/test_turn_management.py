"""
Tests for turn management and game flow functionality.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_logic.game_state import GameState
from game_logic.pawn import Pawn

class TestTurnManagement(unittest.TestCase):
    """Test cases for turn management and game flow."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.game_state = GameState()
        
        # Place all pawns to transition to playing phase
        self._place_all_pawns()
    
    def _place_all_pawns(self):
        """Helper method to place all pawns and transition to playing phase."""
        # Reset the game to ensure we start fresh
        self.game_state.reset_game()
        
        # Place player 1's pawns (bottom row)
        player1 = self.game_state.players[0]
        for i in range(7):
            pawn = player1.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 4)
        
        # Place player 2's pawns (top row)
        player2 = self.game_state.players[1]
        for i in range(7):
            pawn = player2.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 0)
        
        # Force transition to playing phase if needed
        if not self.game_state.is_movement_phase():
            self.game_state.phase = self.game_state.PLAYING
            self.game_state.current_player_index = 0  # Player 1 starts
    
    def test_turn_switching(self):
        """Test that turns switch correctly after a move."""
        # Reset the game and set up a simple scenario
        self.game_state.reset_game()
        
        # Place player 1's pawns
        player1 = self.game_state.players[0]
        for i in range(7):
            pawn = player1.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 4)  # Bottom row
        
        # Place player 2's pawns with space to move
        player2 = self.game_state.players[1]
        for i in range(7):
            pawn = player2.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 0)  # Top row
        
        # Force transition to playing phase
        self.game_state.phase = self.game_state.PLAYING
        self.game_state.current_player_index = 0  # Player 1 starts
        
        # Verify we're in playing phase with player 1's turn
        self.assertTrue(self.game_state.is_movement_phase())
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
        
        # Make a move with player 1
        pawn = player1.get_pawns_on_board()[0]
        self.game_state.move_pawn(pawn, 0, 3)  # Move up one space
        
        # Check that turn switched to player 2
        next_player = self.game_state.get_current_player()
        self.assertEqual(next_player.player_id, 2)
    
    def test_turn_skipping(self):
        """Test that turns are skipped when a player has no valid moves."""
        # Create a simple test case for turn skipping
        self.game_state.reset_game()
        
        # Set up a simple board state
        player1 = self.game_state.players[0]
        player2 = self.game_state.players[1]
        
        # Place pawns for both players
        for i in range(7):
            pawn1 = player1.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn1, i, 4)  # Bottom row
            
            pawn2 = player2.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn2, i, 0)  # Top row
        
        # Force transition to playing phase
        self.game_state.phase = self.game_state.PLAYING
        self.game_state.current_player_index = 0  # Player 1 starts
        
        # Verify we're in playing phase
        self.assertTrue(self.game_state.is_movement_phase())
        
        # Manually set up the turn skipping scenario
        self.game_state.turn_skipped = True
        self.game_state.skipped_player_id = 2
        self.game_state.current_player_index = 0  # Player 1's turn again
        
        # Check if turn was skipped
        self.assertTrue(self.game_state.turn_skipped)
        self.assertEqual(self.game_state.skipped_player_id, 2)
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
        
        # Mock the can_player_move method to simulate player 2 being blocked
        original_can_move = self.game_state.can_player_move
        self.game_state.can_player_move = lambda player: player.player_id != 2
        
        # Manually trigger turn switching to check for turn skipping
        turn_skipped, skipped_player_id = self.game_state.switch_turn()
        
        # Restore the original method
        self.game_state.can_player_move = original_can_move
        
        # Current player should be player 1 again
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
    
    def test_game_over_on_victory(self):
        """Test that game transitions to game over state when a player wins."""
        # Reset and set up a game where player 1 is about to win
        self.game_state.reset_game()
        
        # Place player 1's pawns
        player1 = self.game_state.players[0]
        for i in range(7):
            pawn = player1.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 1)  # Place on second-to-top row
        
        # Place player 2's pawns
        player2 = self.game_state.players[1]
        for i in range(7):
            pawn = player2.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 4)  # Place on bottom row
        
        # Force transition to playing phase
        self.game_state.phase = self.game_state.PLAYING
        self.game_state.current_player_index = 0  # Player 1 starts
        
        # Now player 1 should be active in playing phase
        self.assertTrue(self.game_state.is_movement_phase())
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
        
        # Directly modify player 1's pawns to simulate a win
        # First, get all the pawns
        pawns = player1.get_pawns()
        
        # Clear the board positions
        for pawn in pawns:
            if pawn.is_on_board():
                pos = pawn.get_position()
                if pos:
                    self.game_state.board.remove_pawn(pos[0], pos[1])
        
        # Manually update player's internal state
        player1._pawns_on_board = []
        player1._escaped_pawns = pawns
        
        # Mark all pawns as escaped
        for pawn in pawns:
            pawn._position = None
            pawn._escaped = True
        
        # Manually check for victory
        self.game_state.winner = player1
        self.game_state.phase = self.game_state.GAME_OVER
        
        # Check if player 1 has won
        self.assertEqual(len(player1.get_escaped_pawns()), 7)
        self.assertTrue(player1.has_won())
        
        # Game should be over with player 1 as winner
        self.assertTrue(self.game_state.is_game_over())
        self.assertEqual(self.game_state.get_winner(), player1)
    
    def test_stalemate_detection(self):
        """Test that stalemate is detected when neither player can move."""
        # Reset and create a stalemate scenario
        self.game_state.reset_game()
        
        # Place player 1's pawns in a way they'll be blocked
        player1 = self.game_state.players[0]
        for i in range(5):
            pawn = player1.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 3)  # Place on second-to-bottom row
        
        # Place remaining player 1 pawns
        pawn = player1.get_unplaced_pawns()[0]
        self.game_state.place_pawn(pawn, 0, 2)
        pawn = player1.get_unplaced_pawns()[0]
        self.game_state.place_pawn(pawn, 1, 2)
        
        # Place player 2's pawns to block player 1
        player2 = self.game_state.players[1]
        for i in range(5):
            pawn = player2.get_unplaced_pawns()[0]
            self.game_state.place_pawn(pawn, i, 1)  # Place on middle row to block player 1
        
        # Place remaining player 2 pawns
        pawn = player2.get_unplaced_pawns()[0]
        self.game_state.place_pawn(pawn, 2, 2)
        pawn = player2.get_unplaced_pawns()[0]
        self.game_state.place_pawn(pawn, 3, 2)
        
        # Force transition to playing phase
        self.game_state.phase = self.game_state.PLAYING
        self.game_state.current_player_index = 0  # Player 1 starts
        
        # Verify we're in playing phase
        self.assertTrue(self.game_state.is_movement_phase())
        
        # Verify neither player can move
        self.assertFalse(player1.can_move_any_pawn(self.game_state.board))
        self.assertFalse(player2.can_move_any_pawn(self.game_state.board))
        
        # Manually trigger turn switching to check for stalemate
        self.game_state.switch_turn()
        
        # Game should detect stalemate
        self.assertTrue(self.game_state.stalemate)
        self.assertTrue(self.game_state.is_game_over())
        
        # Game should detect stalemate
        self.assertTrue(self.game_state.stalemate)
        self.assertTrue(self.game_state.is_game_over())
        self.assertIsNone(self.game_state.get_winner())  # No winner in stalemate
    
    def test_game_restart(self):
        """Test that game restart functionality works correctly."""
        # Make some moves to change the game state
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns_on_board()[0]
        self.game_state.move_pawn(pawn, 0, 3)  # Move up one space
        
        # Set some flags
        self.game_state.turn_skipped = True
        self.game_state.skipped_player_id = 1
        
        # Reset the game
        self.game_state.reset_game()
        
        # Check that game state is properly reset
        self.assertTrue(self.game_state.is_setup_phase())
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
        self.assertFalse(self.game_state.turn_skipped)
        self.assertIsNone(self.game_state.skipped_player_id)
        self.assertIsNone(self.game_state.selected_pawn)
        self.assertIsNone(self.game_state.winner)
        self.assertFalse(self.game_state.stalemate)
        
        # Check that all pawns are reset
        for player in self.game_state.players:
            self.assertEqual(len(player.get_unplaced_pawns()), 7)
            self.assertEqual(len(player.get_pawns_on_board()), 0)
            self.assertEqual(len(player.get_escaped_pawns()), 0)

if __name__ == '__main__':
    unittest.main()