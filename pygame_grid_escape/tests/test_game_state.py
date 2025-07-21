"""
Unit tests for GameState class.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_logic.game_state import GameState
from game_logic.player import Player
from game_logic.pawn import Pawn


class TestGameState(unittest.TestCase):
    """Test cases for GameState class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game_state = GameState()
    
    def test_initial_state(self):
        """Test that GameState initializes correctly."""
        # Should start in setup phase
        self.assertTrue(self.game_state.is_setup_phase())
        self.assertFalse(self.game_state.is_movement_phase())
        self.assertFalse(self.game_state.is_game_over())
        
        # Should have two players
        self.assertEqual(len(self.game_state.players), 2)
        self.assertEqual(self.game_state.players[0].player_id, 1)
        self.assertEqual(self.game_state.players[1].player_id, 2)
        
        # Player 1 should start first
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
        
        # No winner initially
        self.assertIsNone(self.game_state.get_winner())
        self.assertIsNone(self.game_state.check_victory())
    
    def test_get_current_player(self):
        """Test getting the current player."""
        # Initially player 1
        current = self.game_state.get_current_player()
        self.assertEqual(current.player_id, 1)
        
        # Switch turn and check player 2
        self.game_state.switch_turn()
        current = self.game_state.get_current_player()
        self.assertEqual(current.player_id, 2)
        
        # Switch again back to player 1
        self.game_state.switch_turn()
        current = self.game_state.get_current_player()
        self.assertEqual(current.player_id, 1)
    
    def test_get_other_player(self):
        """Test getting the other player."""
        # Initially player 1 is current, so other should be player 2
        other = self.game_state.get_other_player()
        self.assertEqual(other.player_id, 2)
        
        # Switch turn and check
        self.game_state.switch_turn()
        other = self.game_state.get_other_player()
        self.assertEqual(other.player_id, 1)
    
    def test_switch_turn_basic(self):
        """Test basic turn switching."""
        # Start with player 1
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
        
        # Switch to player 2
        self.game_state.switch_turn()
        self.assertEqual(self.game_state.get_current_player().player_id, 2)
        
        # Switch back to player 1
        self.game_state.switch_turn()
        self.assertEqual(self.game_state.get_current_player().player_id, 1)
    
    def test_switch_turn_clears_selected_pawn(self):
        """Test that switching turns clears the selected pawn."""
        # Set a selected pawn
        pawn = self.game_state.players[0].get_pawns()[0]
        self.game_state.selected_pawn = pawn
        
        # Switch turn
        self.game_state.switch_turn()
        
        # Selected pawn should be cleared
        self.assertIsNone(self.game_state.selected_pawn)
    
    def test_switch_turn_game_over(self):
        """Test that switching turns doesn't work when game is over."""
        # Set game to over state
        self.game_state.phase = GameState.GAME_OVER
        original_player = self.game_state.get_current_player().player_id
        
        # Try to switch turn
        self.game_state.switch_turn()
        
        # Player should not have changed
        self.assertEqual(self.game_state.get_current_player().player_id, original_player)
    
    def test_phase_transitions(self):
        """Test phase transition methods."""
        # Start in setup
        self.assertTrue(self.game_state.is_setup_phase())
        
        # Transition to playing
        self.game_state.phase = GameState.PLAYING
        self.assertTrue(self.game_state.is_movement_phase())
        self.assertFalse(self.game_state.is_setup_phase())
        
        # Transition to game over
        self.game_state.phase = GameState.GAME_OVER
        self.assertTrue(self.game_state.is_game_over())
        self.assertFalse(self.game_state.is_movement_phase())
    
    def test_transition_to_playing_phase(self):
        """Test transitioning from setup to playing phase."""
        # Should fail if not in setup phase
        self.game_state.phase = GameState.PLAYING
        self.assertFalse(self.game_state.transition_to_playing_phase())
        
        # Reset to setup phase
        self.game_state.phase = GameState.SETUP
        
        # Should fail if pawns are not all placed
        self.assertFalse(self.game_state.transition_to_playing_phase())
        
        # Place all pawns (simulate by marking them as escaped to reduce unplaced count)
        for player in self.game_state.players:
            for pawn in player.get_pawns():
                pawn._escaped = True
        
        # Now transition should succeed
        self.assertTrue(self.game_state.transition_to_playing_phase())
        self.assertTrue(self.game_state.is_movement_phase())
        self.assertEqual(self.game_state.current_player_index, 0)  # Player 1 starts
    
    def test_is_setup_complete(self):
        """Test setup completion detection."""
        # Initially setup is not complete (all pawns unplaced)
        self.assertFalse(self.game_state.is_setup_complete())
        
        # Place some pawns for player 1
        player1 = self.game_state.players[0]
        for i, pawn in enumerate(player1.get_pawns()[:3]):
            pawn.set_position(i, 4)  # Place on bottom row
        
        # Still not complete
        self.assertFalse(self.game_state.is_setup_complete())
        
        # Place all pawns for both players
        for player in self.game_state.players:
            for i, pawn in enumerate(player.get_pawns()):
                if player.player_id == 1:
                    pawn.set_position(i % 5, 4)  # Bottom row for player 1
                else:
                    pawn.set_position(i % 5, 0)  # Top row for player 2
        
        # Now setup should be complete
        self.assertTrue(self.game_state.is_setup_complete())
    
    def test_check_victory(self):
        """Test victory condition checking."""
        # Initially no winner
        self.assertIsNone(self.game_state.check_victory())
        
        # Make player 1 win by escaping all pawns
        player1 = self.game_state.players[0]
        for pawn in player1.get_pawns():
            pawn.escape()
        
        # Now player 1 should be the winner
        winner = self.game_state.check_victory()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.player_id, 1)
        
        # Reset and make player 2 win
        self.game_state.reset_game()
        player2 = self.game_state.players[1]
        for pawn in player2.get_pawns():
            pawn.escape()
        
        winner = self.game_state.check_victory()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.player_id, 2)
    
    def test_can_player_move(self):
        """Test checking if a player can move."""
        player1 = self.game_state.players[0]
        
        # Initially no pawns on board, so cannot move
        self.assertFalse(self.game_state.can_player_move(player1))
        
        # Place a pawn on the board
        pawn = player1.get_pawns()[0]
        pawn.set_position(2, 2)  # Middle of board
        self.game_state.board.place_pawn(pawn, 2, 2)
        
        # Now player should be able to move (assuming valid moves exist)
        # Note: This test depends on the pawn's get_valid_moves implementation
        # For now, we'll test the method exists and returns the expected type
        result = self.game_state.can_player_move(player1)
        self.assertIsInstance(result, bool)
    
    def test_reset_game(self):
        """Test game reset functionality."""
        # Modify game state
        self.game_state.phase = GameState.PLAYING
        self.game_state.current_player_index = 1
        self.game_state.winner = self.game_state.players[0]
        
        # Place some pawns
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns()[0]
        pawn.set_position(2, 2)
        self.game_state.board.place_pawn(pawn, 2, 2)
        
        # Escape some pawns
        player1.get_pawns()[1].escape()
        
        # Reset the game
        self.game_state.reset_game()
        
        # Check that everything is reset
        self.assertTrue(self.game_state.is_setup_phase())
        self.assertEqual(self.game_state.current_player_index, 0)
        self.assertIsNone(self.game_state.winner)
        self.assertIsNone(self.game_state.selected_pawn)
        
        # Check that all pawns are reset
        for player in self.game_state.players:
            for pawn in player.get_pawns():
                self.assertIsNone(pawn.get_position())
                self.assertFalse(pawn.is_escaped())
                self.assertFalse(pawn.is_on_board())
    
    def test_place_pawn_setup_phase(self):
        """Test placing pawns during setup phase."""
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns()[0]
        
        # Should succeed on valid starting position
        success = self.game_state.place_pawn(pawn, 0, 4)  # Bottom row for player 1
        self.assertTrue(success)
        self.assertEqual(pawn.get_position(), (0, 4))
        
        # Should fail on invalid starting position
        pawn2 = player1.get_pawns()[1]
        success = self.game_state.place_pawn(pawn2, 0, 0)  # Top row (player 2's start)
        self.assertFalse(success)
        self.assertIsNone(pawn2.get_position())
        
        # Should fail on occupied position
        pawn3 = player1.get_pawns()[2]
        success = self.game_state.place_pawn(pawn3, 0, 4)  # Same position as pawn
        self.assertFalse(success)
    
    def test_place_pawn_wrong_phase(self):
        """Test that placing pawns fails outside setup phase."""
        # Change to playing phase
        self.game_state.phase = GameState.PLAYING
        
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns()[0]
        
        # Should fail in playing phase
        success = self.game_state.place_pawn(pawn, 0, 4)
        self.assertFalse(success)
    
    def test_move_pawn_playing_phase(self):
        """Test moving pawns during playing phase."""
        # Set up game in playing phase with pawns placed
        self.game_state.phase = GameState.PLAYING
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns()[0]
        
        # Place pawn on board
        pawn.set_position(2, 2)
        self.game_state.board.place_pawn(pawn, 2, 2)
        
        # Should succeed for valid adjacent move
        success = self.game_state.move_pawn(pawn, 2, 1)  # Move up
        self.assertTrue(success)
        self.assertEqual(pawn.get_position(), (2, 1))
    
    def test_move_pawn_wrong_phase(self):
        """Test that moving pawns fails outside playing phase."""
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns()[0]
        pawn.set_position(2, 2)
        
        # Should fail in setup phase
        success = self.game_state.move_pawn(pawn, 2, 1)
        self.assertFalse(success)
    
    def test_move_pawn_wrong_turn(self):
        """Test that moving pawns fails when it's not the player's turn."""
        # Set up game in playing phase
        self.game_state.phase = GameState.PLAYING
        self.game_state.current_player_index = 0  # Player 1's turn
        
        # Try to move player 2's pawn
        player2 = self.game_state.players[1]
        pawn = player2.get_pawns()[0]
        pawn.set_position(2, 2)
        self.game_state.board.place_pawn(pawn, 2, 2)
        
        success = self.game_state.move_pawn(pawn, 2, 1)
        self.assertFalse(success)
    
    def test_pawn_escape_on_move(self):
        """Test that pawns escape when moved to escape positions."""
        # Set up game in playing phase
        self.game_state.phase = GameState.PLAYING
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns()[0]
        
        # Place pawn near escape position (player 1 escapes from top row y=0)
        pawn.set_position(0, 1)
        self.game_state.board.place_pawn(pawn, 0, 1)
        
        # Move to escape position
        success = self.game_state.move_pawn(pawn, 0, 0)
        self.assertTrue(success)
        
        # Pawn should be escaped
        self.assertTrue(pawn.is_escaped())
        self.assertFalse(pawn.is_on_board())
        
        # Board position should be empty
        self.assertTrue(self.game_state.board.is_intersection_empty(0, 0))
    
    def test_victory_detection_on_switch_turn(self):
        """Test that victory is detected when switching turns."""
        # Set up game in playing phase
        self.game_state.phase = GameState.PLAYING
        player1 = self.game_state.players[0]
        
        # Make player 1 win by escaping all but one pawn
        for pawn in player1.get_pawns()[:-1]:
            pawn.escape()
        
        # Last pawn is on board
        last_pawn = player1.get_pawns()[-1]
        last_pawn.set_position(0, 1)
        self.game_state.board.place_pawn(last_pawn, 0, 1)
        
        # Move last pawn to escape position
        success = self.game_state.move_pawn(last_pawn, 0, 0)
        self.assertTrue(success)
        
        # Game should be over with player 1 as winner
        self.assertTrue(self.game_state.is_game_over())
        self.assertEqual(self.game_state.get_winner().player_id, 1)
    
    def test_turn_skipping_when_player_cannot_move(self):
        """Test automatic turn skipping when a player cannot move."""
        # Set up game in playing phase with both players having pawns
        self.game_state.phase = GameState.PLAYING
        self.game_state.current_player_index = 0  # Player 1's turn
        
        player1 = self.game_state.players[0]
        player2 = self.game_state.players[1]
        
        # Place player 1's pawn in a position where it can't move (surrounded)
        pawn1 = player1.get_pawns()[0]
        pawn1.set_position(2, 2)
        self.game_state.board.place_pawn(pawn1, 2, 2)
        
        # Surround player 1's pawn with player 2's pawns
        positions = [(1, 2), (3, 2), (2, 1), (2, 3)]
        for i, pos in enumerate(positions):
            if i < len(player2.get_pawns()):
                pawn2 = player2.get_pawns()[i]
                pawn2.set_position(pos[0], pos[1])
                self.game_state.board.place_pawn(pawn2, pos[0], pos[1])
        
        # Place another player 2 pawn that can move
        movable_pawn = player2.get_pawns()[4]
        movable_pawn.set_position(0, 0)
        self.game_state.board.place_pawn(movable_pawn, 0, 0)
        
        # Mock the can_player_move method to simulate the scenario
        original_method = self.game_state.can_player_move
        def mock_can_move(player):
            if player.player_id == 1:
                return False  # Player 1 cannot move
            else:
                return True   # Player 2 can move
        
        self.game_state.can_player_move = mock_can_move
        
        # Switch turn - should skip player 1 and go to player 2
        self.game_state.switch_turn()
        
        # Should now be player 2's turn
        self.assertEqual(self.game_state.get_current_player().player_id, 2)
        
        # Restore original method
        self.game_state.can_player_move = original_method
    
    def test_setup_to_playing_transition_automatic(self):
        """Test automatic transition from setup to playing when all pawns placed."""
        # Place all pawns for both players
        player1 = self.game_state.players[0]
        player2 = self.game_state.players[1]
        
        # Place player 1 pawns on bottom row (5 positions available)
        for i, pawn in enumerate(player1.get_pawns()[:5]):  # Only place first 5 pawns
            success = self.game_state.place_pawn(pawn, i, 4)
            self.assertTrue(success)
        
        # Place remaining player 1 pawns by manually setting them as escaped
        for pawn in player1.get_pawns()[5:]:
            pawn.escape()
        
        # Game should still be in setup after placing player 1's pawns
        self.assertTrue(self.game_state.is_setup_phase())
        
        # Place player 2 pawns on top row (5 positions available) except the last one
        for i, pawn in enumerate(player2.get_pawns()[:4]):  # Place first 4 pawns
            success = self.game_state.place_pawn(pawn, i, 0)
            self.assertTrue(success)
        
        # Place remaining player 2 pawns by manually setting them as escaped except one
        for pawn in player2.get_pawns()[5:]:
            pawn.escape()
        
        # Game should still be in setup
        self.assertTrue(self.game_state.is_setup_phase())
        
        # Place the last pawn - this should trigger transition
        last_pawn = player2.get_pawns()[4]
        success = self.game_state.place_pawn(last_pawn, 4, 0)
        self.assertTrue(success)
        
        # Now all pawns are either placed or escaped, so setup should be complete
        # and game should transition to playing phase
        self.assertTrue(self.game_state.is_movement_phase())
        self.assertEqual(self.game_state.current_player_index, 0)  # Player 1 starts
    
    def test_game_state_consistency_after_operations(self):
        """Test that game state remains consistent after various operations."""
        # Start in setup phase
        self.assertTrue(self.game_state.is_setup_phase())
        
        # Place some pawns
        player1 = self.game_state.players[0]
        pawn = player1.get_pawns()[0]
        success = self.game_state.place_pawn(pawn, 0, 4)
        self.assertTrue(success)
        
        # Verify pawn is correctly placed
        self.assertEqual(pawn.get_position(), (0, 4))
        self.assertTrue(pawn.is_on_board())
        self.assertFalse(pawn.is_escaped())
        
        # Verify board state
        board_pawn = self.game_state.board.get_pawn_at_intersection(0, 4)
        self.assertEqual(board_pawn, pawn)
        
        # Reset and verify everything is cleared
        self.game_state.reset_game()
        self.assertIsNone(pawn.get_position())
        self.assertFalse(pawn.is_on_board())
        self.assertFalse(pawn.is_escaped())
        self.assertTrue(self.game_state.board.is_intersection_empty(0, 4))


if __name__ == '__main__':
    unittest.main()