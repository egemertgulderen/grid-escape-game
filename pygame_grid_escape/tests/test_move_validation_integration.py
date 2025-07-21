"""
Integration tests for move validation and pawn movement logic.

These tests use real Board, Player, and Pawn objects to test the complete
move validation system including blocking scenarios and escape conditions.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_logic.board import Board
from game_logic.player import Player
from game_logic.pawn import Pawn
from game_logic.game_state import GameState


class TestMoveValidationIntegration(unittest.TestCase):
    """Integration test cases for move validation and pawn movement."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.board = Board()
        self.player1 = Player(1, (0, 102, 204))  # Blue
        self.player2 = Player(2, (204, 0, 0))    # Red
        self.pawn1 = self.player1.get_pawns()[0]
        self.pawn2 = self.player2.get_pawns()[0]
    
    def test_pawn_valid_moves_empty_board(self):
        """Test pawn valid moves on empty board."""
        # Place pawn in center of board
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        
        valid_moves = self.pawn1.get_valid_moves(self.board)
        expected_moves = [(2, 1), (2, 3), (1, 2), (3, 2)]  # Up, Down, Left, Right
        
        self.assertEqual(set(valid_moves), set(expected_moves))
        self.assertEqual(len(valid_moves), 4)
    
    def test_pawn_valid_moves_corner_position(self):
        """Test pawn valid moves from corner position."""
        # Place pawn in top-left corner
        self.board.place_pawn(self.pawn1, 0, 0)
        self.pawn1.set_position(0, 0)
        
        valid_moves = self.pawn1.get_valid_moves(self.board)
        expected_moves = [(0, 1), (1, 0)]  # Down, Right
        
        self.assertEqual(set(valid_moves), set(expected_moves))
        self.assertEqual(len(valid_moves), 2)
    
    def test_pawn_valid_moves_edge_position(self):
        """Test pawn valid moves from edge position."""
        # Place pawn on left edge
        self.board.place_pawn(self.pawn1, 0, 2)
        self.pawn1.set_position(0, 2)
        
        valid_moves = self.pawn1.get_valid_moves(self.board)
        expected_moves = [(0, 1), (0, 3), (1, 2)]  # Up, Down, Right
        
        self.assertEqual(set(valid_moves), set(expected_moves))
        self.assertEqual(len(valid_moves), 3)
    
    def test_pawn_blocked_by_opponent_pawn(self):
        """Test that opponent pawns block movement."""
        # Place player 1 pawn in center
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        
        # Place player 2 pawn to block upward movement
        self.board.place_pawn(self.pawn2, 2, 1)
        self.pawn2.set_position(2, 1)
        
        valid_moves = self.pawn1.get_valid_moves(self.board)
        expected_moves = [(2, 3), (1, 2), (3, 2)]  # Down, Left, Right (Up blocked)
        
        self.assertEqual(set(valid_moves), set(expected_moves))
        self.assertEqual(len(valid_moves), 3)
    
    def test_pawn_blocked_by_own_pawn(self):
        """Test that own pawns also block movement."""
        pawn1a = self.player1.get_pawns()[0]
        pawn1b = self.player1.get_pawns()[1]
        
        # Place first pawn in center
        self.board.place_pawn(pawn1a, 2, 2)
        pawn1a.set_position(2, 2)
        
        # Place second pawn of same player to block movement
        self.board.place_pawn(pawn1b, 2, 1)
        pawn1b.set_position(2, 1)
        
        valid_moves = pawn1a.get_valid_moves(self.board)
        expected_moves = [(2, 3), (1, 2), (3, 2)]  # Down, Left, Right (Up blocked)
        
        self.assertEqual(set(valid_moves), set(expected_moves))
        self.assertEqual(len(valid_moves), 3)
    
    def test_pawn_completely_blocked(self):
        """Test pawn with no valid moves (completely blocked)."""
        pawn1a = self.player1.get_pawns()[0]
        pawn1b = self.player1.get_pawns()[1]
        pawn2a = self.player2.get_pawns()[0]
        pawn2b = self.player2.get_pawns()[1]
        
        # Place target pawn in center
        self.board.place_pawn(pawn1a, 2, 2)
        pawn1a.set_position(2, 2)
        
        # Block all four adjacent positions
        self.board.place_pawn(pawn1b, 2, 1)  # Up
        pawn1b.set_position(2, 1)
        self.board.place_pawn(pawn2a, 2, 3)  # Down
        pawn2a.set_position(2, 3)
        self.board.place_pawn(pawn2b, 1, 2)  # Left
        pawn2b.set_position(1, 2)
        self.board.place_pawn(self.player1.get_pawns()[2], 3, 2)  # Right
        self.player1.get_pawns()[2].set_position(3, 2)
        
        valid_moves = pawn1a.get_valid_moves(self.board)
        self.assertEqual(valid_moves, [])
        
        # Test is_blocked method
        self.assertTrue(pawn1a.is_blocked(self.board))
        self.assertFalse(pawn1b.is_blocked(self.board))  # This pawn can still move
    
    def test_can_move_to_method(self):
        """Test can_move_to method with various scenarios."""
        # Place pawn in center
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        
        # Test valid adjacent moves
        self.assertTrue(self.pawn1.can_move_to(self.board, 2, 1))  # Up
        self.assertTrue(self.pawn1.can_move_to(self.board, 2, 3))  # Down
        self.assertTrue(self.pawn1.can_move_to(self.board, 1, 2))  # Left
        self.assertTrue(self.pawn1.can_move_to(self.board, 3, 2))  # Right
        
        # Test invalid moves
        self.assertFalse(self.pawn1.can_move_to(self.board, 1, 1))  # Diagonal
        self.assertFalse(self.pawn1.can_move_to(self.board, 4, 4))  # Far away
        self.assertFalse(self.pawn1.can_move_to(self.board, 2, 4))  # Two steps
        
        # Block a position and test
        self.board.place_pawn(self.pawn2, 2, 1)
        self.pawn2.set_position(2, 1)
        self.assertFalse(self.pawn1.can_move_to(self.board, 2, 1))  # Now blocked
    
    def test_move_to_successful_move(self):
        """Test successful pawn movement."""
        # Place pawn
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        
        # Move pawn to adjacent position
        result = self.pawn1.move_to(self.board, 2, 1)
        self.assertTrue(result)
        
        # Verify pawn position updated
        self.assertEqual(self.pawn1.get_position(), (2, 1))
        self.assertTrue(self.pawn1.is_on_board())
        
        # Verify board state updated
        self.assertIsNone(self.board.get_pawn_at_intersection(2, 2))  # Old position empty
        self.assertEqual(self.board.get_pawn_at_intersection(2, 1), self.pawn1)  # New position occupied
    
    def test_move_to_blocked_position(self):
        """Test move to blocked position fails."""
        # Place pawns
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        self.board.place_pawn(self.pawn2, 2, 1)  # Block destination
        self.pawn2.set_position(2, 1)
        
        original_position = self.pawn1.get_position()
        
        # Try to move to blocked position
        result = self.pawn1.move_to(self.board, 2, 1)
        self.assertFalse(result)
        
        # Verify pawn didn't move
        self.assertEqual(self.pawn1.get_position(), original_position)
        self.assertEqual(self.board.get_pawn_at_intersection(2, 2), self.pawn1)
        self.assertEqual(self.board.get_pawn_at_intersection(2, 1), self.pawn2)
    
    def test_move_to_invalid_position(self):
        """Test move to invalid position fails."""
        # Place pawn
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        
        original_position = self.pawn1.get_position()
        
        # Try diagonal move (invalid)
        result = self.pawn1.move_to(self.board, 1, 1)
        self.assertFalse(result)
        
        # Try move too far (invalid)
        result = self.pawn1.move_to(self.board, 4, 4)
        self.assertFalse(result)
        
        # Verify pawn didn't move
        self.assertEqual(self.pawn1.get_position(), original_position)
        self.assertEqual(self.board.get_pawn_at_intersection(2, 2), self.pawn1)
    
    def test_move_to_escape_position_player1(self):
        """Test Player 1 pawn escaping from top row."""
        # Place Player 1 pawn near escape position (top row is escape for Player 1)
        self.board.place_pawn(self.pawn1, 2, 1)
        self.pawn1.set_position(2, 1)
        
        # Move to escape position (top row, y=0)
        result = self.pawn1.move_to(self.board, 2, 0)
        self.assertTrue(result)
        
        # Verify pawn escaped
        self.assertTrue(self.pawn1.is_escaped())
        self.assertFalse(self.pawn1.is_on_board())
        self.assertIsNone(self.pawn1.get_position())
        
        # Verify board position is empty
        self.assertIsNone(self.board.get_pawn_at_intersection(2, 0))
    
    def test_move_to_escape_position_player2(self):
        """Test Player 2 pawn escaping from bottom row."""
        # Place Player 2 pawn near escape position (bottom row is escape for Player 2)
        self.board.place_pawn(self.pawn2, 2, 3)
        self.pawn2.set_position(2, 3)
        
        # Move to escape position (bottom row, y=4)
        result = self.pawn2.move_to(self.board, 2, 4)
        self.assertTrue(result)
        
        # Verify pawn escaped
        self.assertTrue(self.pawn2.is_escaped())
        self.assertFalse(self.pawn2.is_on_board())
        self.assertIsNone(self.pawn2.get_position())
        
        # Verify board position is empty
        self.assertIsNone(self.board.get_pawn_at_intersection(2, 4))
    
    def test_move_to_non_escape_position(self):
        """Test moving to non-escape position doesn't trigger escape."""
        # Place Player 1 pawn and move to middle row (not escape position)
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        
        # Move to non-escape position
        result = self.pawn1.move_to(self.board, 2, 3)
        self.assertTrue(result)
        
        # Verify pawn didn't escape
        self.assertFalse(self.pawn1.is_escaped())
        self.assertTrue(self.pawn1.is_on_board())
        self.assertEqual(self.pawn1.get_position(), (2, 3))
        
        # Verify board position is occupied
        self.assertEqual(self.board.get_pawn_at_intersection(2, 3), self.pawn1)
    
    def test_player_can_move_any_pawn(self):
        """Test Player.can_move_any_pawn method with various scenarios."""
        # Initially no pawns on board
        self.assertFalse(self.player1.can_move_any_pawn(self.board))
        
        # Place one pawn with valid moves
        self.board.place_pawn(self.pawn1, 2, 2)
        self.pawn1.set_position(2, 2)
        self.assertTrue(self.player1.can_move_any_pawn(self.board))
        
        # Block all moves for the pawn
        pawns = self.player2.get_pawns()
        self.board.place_pawn(pawns[0], 2, 1)  # Up
        pawns[0].set_position(2, 1)
        self.board.place_pawn(pawns[1], 2, 3)  # Down
        pawns[1].set_position(2, 3)
        self.board.place_pawn(pawns[2], 1, 2)  # Left
        pawns[2].set_position(1, 2)
        self.board.place_pawn(pawns[3], 3, 2)  # Right
        pawns[3].set_position(3, 2)
        
        # Now player 1 cannot move
        self.assertFalse(self.player1.can_move_any_pawn(self.board))
        
        # But player 2 can move (their pawns are not blocked)
        self.assertTrue(self.player2.can_move_any_pawn(self.board))
    
    def test_complex_blocking_scenario(self):
        """Test complex scenario with multiple pawns and blocking."""
        # Set up a scenario where some pawns can move and others cannot
        player1_pawns = self.player1.get_pawns()
        player2_pawns = self.player2.get_pawns()
        
        # Place Player 1 pawns
        self.board.place_pawn(player1_pawns[0], 1, 1)  # Can move
        player1_pawns[0].set_position(1, 1)
        self.board.place_pawn(player1_pawns[1], 3, 3)  # Will be blocked
        player1_pawns[1].set_position(3, 3)
        
        # Place Player 2 pawns to block some moves
        self.board.place_pawn(player2_pawns[0], 3, 2)  # Block up from (3,3)
        player2_pawns[0].set_position(3, 2)
        self.board.place_pawn(player2_pawns[1], 3, 4)  # Block down from (3,3)
        player2_pawns[1].set_position(3, 4)
        self.board.place_pawn(player2_pawns[2], 2, 3)  # Block left from (3,3)
        player2_pawns[2].set_position(2, 3)
        self.board.place_pawn(player2_pawns[3], 4, 3)  # Block right from (3,3)
        player2_pawns[3].set_position(4, 3)
        
        # Player 1 should still be able to move (pawn at 1,1 can move)
        self.assertTrue(self.player1.can_move_any_pawn(self.board))
        
        # Pawn at (1,1) should have valid moves
        valid_moves_1_1 = player1_pawns[0].get_valid_moves(self.board)
        self.assertGreater(len(valid_moves_1_1), 0)
        
        # Pawn at (3,3) should have no valid moves
        valid_moves_3_3 = player1_pawns[1].get_valid_moves(self.board)
        self.assertEqual(len(valid_moves_3_3), 0)
        
        # Test is_blocked method
        self.assertTrue(player1_pawns[1].is_blocked(self.board))
        self.assertFalse(player1_pawns[0].is_blocked(self.board))
    
    def test_is_adjacent_to(self):
        """Test is_adjacent_to method."""
        self.pawn1.set_position(2, 2)
        
        # Test adjacent positions
        self.assertTrue(self.pawn1.is_adjacent_to(1, 2))  # Left
        self.assertTrue(self.pawn1.is_adjacent_to(3, 2))  # Right
        self.assertTrue(self.pawn1.is_adjacent_to(2, 1))  # Up
        self.assertTrue(self.pawn1.is_adjacent_to(2, 3))  # Down
        
        # Test non-adjacent positions
        self.assertFalse(self.pawn1.is_adjacent_to(1, 1))  # Diagonal
        self.assertFalse(self.pawn1.is_adjacent_to(3, 3))  # Diagonal
        self.assertFalse(self.pawn1.is_adjacent_to(4, 2))  # Too far
        self.assertFalse(self.pawn1.is_adjacent_to(2, 4))  # Too far
    
    def test_would_escape_at(self):
        """Test would_escape_at method."""
        # Player 1 escapes at top row (y=0)
        self.pawn1.set_position(2, 1)
        self.assertTrue(self.pawn1.would_escape_at(self.board, 2, 0))
        self.assertFalse(self.pawn1.would_escape_at(self.board, 2, 2))
        
        # Player 2 escapes at bottom row (y=4)
        self.pawn2.set_position(2, 3)
        self.assertTrue(self.pawn2.would_escape_at(self.board, 2, 4))
        self.assertFalse(self.pawn2.would_escape_at(self.board, 2, 2))
    
    def test_multiple_pawns_escaping(self):
        """Test multiple pawns escaping scenario."""
        # Place multiple pawns for Player 1 near escape positions
        pawns = self.player1.get_pawns()
        
        # Place pawns near escape row
        self.board.place_pawn(pawns[0], 1, 1)
        pawns[0].set_position(1, 1)
        self.board.place_pawn(pawns[1], 3, 1)
        pawns[1].set_position(3, 1)
        
        # Move first pawn to escape
        result = pawns[0].move_to(self.board, 1, 0)
        self.assertTrue(result)
        self.assertTrue(pawns[0].is_escaped())
        
        # Move second pawn to escape
        result = pawns[1].move_to(self.board, 3, 0)
        self.assertTrue(result)
        self.assertTrue(pawns[1].is_escaped())
        
        # Check escaped pawns count
        escaped_pawns = self.player1.get_escaped_pawns()
        self.assertEqual(len(escaped_pawns), 2)
        self.assertIn(pawns[0], escaped_pawns)
        self.assertIn(pawns[1], escaped_pawns)
    
    def test_game_state_move_validation(self):
        """Test move validation through GameState."""
        game_state = GameState()
        game_state.phase = GameState.PLAYING  # Skip setup phase
        
        # Get players and pawns
        player1 = game_state.players[0]
        player2 = game_state.players[1]
        pawn1 = player1.get_pawns()[0]
        pawn2 = player2.get_pawns()[0]
        
        # Place pawns on board
        game_state.board.place_pawn(pawn1, 2, 2)
        pawn1.set_position(2, 2)
        game_state.board.place_pawn(pawn2, 2, 1)
        pawn2.set_position(2, 1)
        
        # Set current player to player 1
        game_state.current_player_index = 0
        
        # Test valid move for current player
        result = game_state.move_pawn(pawn1, 3, 2)
        self.assertTrue(result)
        self.assertEqual(pawn1.get_position(), (3, 2))
        
        # Current player should now be player 2
        self.assertEqual(game_state.get_current_player(), player2)
        
        # Player 2 should not be able to move to occupied position
        result = game_state.move_pawn(pawn2, 3, 2)
        self.assertFalse(result)
        self.assertEqual(pawn2.get_position(), (2, 1))
        
        # Player 2 should be able to make valid move
        result = game_state.move_pawn(pawn2, 1, 1)
        self.assertTrue(result)
        self.assertEqual(pawn2.get_position(), (1, 1))
        
        # Current player should now be player 1 again
        self.assertEqual(game_state.get_current_player(), player1)
    
    def test_turn_skipping_when_blocked(self):
        """Test turn skipping when a player has no valid moves."""
        game_state = GameState()
        game_state.phase = GameState.PLAYING  # Skip setup phase
        
        # Get players and pawns
        player1 = game_state.players[0]
        player2 = game_state.players[1]
        pawn1 = player1.get_pawns()[0]
        
        # Place player 1 pawn in a position where it will be completely blocked
        game_state.board.place_pawn(pawn1, 2, 2)
        pawn1.set_position(2, 2)
        
        # Block all four directions with player 2 pawns
        for i, pos in enumerate([(2, 1), (2, 3), (1, 2), (3, 2)]):
            pawn2 = player2.get_pawns()[i]
            game_state.board.place_pawn(pawn2, pos[0], pos[1])
            pawn2.set_position(pos[0], pos[1])
        
        # Set current player to player 1
        game_state.current_player_index = 0
        
        # Player 1 should not be able to move any pawn
        self.assertFalse(player1.can_move_any_pawn(game_state.board))
        
        # Switch turn should skip player 1 and go to player 2
        game_state.switch_turn()
        self.assertEqual(game_state.get_current_player(), player2)
        
        # Player 2 should be able to move
        self.assertTrue(player2.can_move_any_pawn(game_state.board))


if __name__ == '__main__':
    unittest.main()