"""
Unit tests for the Board class.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_logic.board import Board
from game_logic.player import Player
from game_logic.pawn import Pawn


class TestBoard(unittest.TestCase):
    """Test cases for the Board class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.board = Board()
        self.player1 = Player(1, (0, 102, 204))  # Blue
        self.player2 = Player(2, (204, 0, 0))    # Red
        self.pawn1 = self.player1.get_pawns()[0]
        self.pawn2 = self.player2.get_pawns()[0]
    
    def test_board_initialization(self):
        """Test that the board initializes correctly."""
        self.assertEqual(self.board.get_grid_size(), 5)
        
        # Check that all intersections are initially empty
        for x in range(5):
            for y in range(5):
                self.assertTrue(self.board.is_intersection_empty(x, y))
                self.assertIsNone(self.board.get_pawn_at_intersection(x, y))
    
    def test_is_valid_position(self):
        """Test position validation."""
        # Valid positions
        self.assertTrue(self.board.is_valid_position(0, 0))
        self.assertTrue(self.board.is_valid_position(4, 4))
        self.assertTrue(self.board.is_valid_position(2, 3))
        
        # Invalid positions
        self.assertFalse(self.board.is_valid_position(-1, 0))
        self.assertFalse(self.board.is_valid_position(0, -1))
        self.assertFalse(self.board.is_valid_position(5, 0))
        self.assertFalse(self.board.is_valid_position(0, 5))
        self.assertFalse(self.board.is_valid_position(-1, -1))
        self.assertFalse(self.board.is_valid_position(5, 5))
    
    def test_pawn_placement_and_removal(self):
        """Test placing and removing pawns."""
        # Place a pawn
        self.assertTrue(self.board.place_pawn(self.pawn1, 2, 2))
        self.assertFalse(self.board.is_intersection_empty(2, 2))
        self.assertEqual(self.board.get_pawn_at_intersection(2, 2), self.pawn1)
        
        # Try to place another pawn at the same position
        self.assertFalse(self.board.place_pawn(self.pawn2, 2, 2))
        
        # Remove the pawn
        removed_pawn = self.board.remove_pawn(2, 2)
        self.assertEqual(removed_pawn, self.pawn1)
        self.assertTrue(self.board.is_intersection_empty(2, 2))
        self.assertIsNone(self.board.get_pawn_at_intersection(2, 2))
        
        # Try to remove from empty intersection
        self.assertIsNone(self.board.remove_pawn(2, 2))
    
    def test_pawn_placement_invalid_positions(self):
        """Test placing pawns at invalid positions."""
        # Try to place at invalid coordinates
        self.assertFalse(self.board.place_pawn(self.pawn1, -1, 0))
        self.assertFalse(self.board.place_pawn(self.pawn1, 0, -1))
        self.assertFalse(self.board.place_pawn(self.pawn1, 5, 0))
        self.assertFalse(self.board.place_pawn(self.pawn1, 0, 5))
    
    def test_move_pawn(self):
        """Test moving pawns between intersections."""
        # Place a pawn
        self.assertTrue(self.board.place_pawn(self.pawn1, 1, 1))
        
        # Move the pawn to an adjacent position
        self.assertTrue(self.board.move_pawn(1, 1, 1, 2))
        self.assertTrue(self.board.is_intersection_empty(1, 1))
        self.assertEqual(self.board.get_pawn_at_intersection(1, 2), self.pawn1)
        
        # Try to move to an occupied position
        self.assertTrue(self.board.place_pawn(self.pawn2, 2, 2))
        self.assertFalse(self.board.move_pawn(1, 2, 2, 2))
        
        # Try to move from an empty position
        self.assertFalse(self.board.move_pawn(3, 3, 3, 4))
        
        # Try to move to invalid positions
        self.assertFalse(self.board.move_pawn(1, 2, -1, 2))
        self.assertFalse(self.board.move_pawn(1, 2, 5, 2))
    
    def test_starting_positions_player1(self):
        """Test starting position identification for Player 1."""
        # Player 1 starts on bottom row (y = 4)
        for x in range(5):
            self.assertTrue(self.board.is_starting_position(x, 4, self.player1))
        
        # Other positions should not be starting positions for Player 1
        for y in range(4):  # y = 0, 1, 2, 3
            for x in range(5):
                self.assertFalse(self.board.is_starting_position(x, y, self.player1))
        
        # Test get_all_starting_positions
        starting_positions = self.board.get_all_starting_positions(self.player1)
        expected_positions = [(x, 4) for x in range(5)]
        self.assertEqual(set(starting_positions), set(expected_positions))
    
    def test_starting_positions_player2(self):
        """Test starting position identification for Player 2."""
        # Player 2 starts on top row (y = 0)
        for x in range(5):
            self.assertTrue(self.board.is_starting_position(x, 0, self.player2))
        
        # Other positions should not be starting positions for Player 2
        for y in range(1, 5):  # y = 1, 2, 3, 4
            for x in range(5):
                self.assertFalse(self.board.is_starting_position(x, y, self.player2))
        
        # Test get_all_starting_positions
        starting_positions = self.board.get_all_starting_positions(self.player2)
        expected_positions = [(x, 0) for x in range(5)]
        self.assertEqual(set(starting_positions), set(expected_positions))
    
    def test_escape_positions_player1(self):
        """Test escape position identification for Player 1."""
        # Player 1 escapes from top row (y = 0)
        for x in range(5):
            self.assertTrue(self.board.is_escape_position(x, 0, self.player1))
        
        # Other positions should not be escape positions for Player 1
        for y in range(1, 5):  # y = 1, 2, 3, 4
            for x in range(5):
                self.assertFalse(self.board.is_escape_position(x, y, self.player1))
        
        # Test get_all_escape_positions
        escape_positions = self.board.get_all_escape_positions(self.player1)
        expected_positions = [(x, 0) for x in range(5)]
        self.assertEqual(set(escape_positions), set(expected_positions))
    
    def test_escape_positions_player2(self):
        """Test escape position identification for Player 2."""
        # Player 2 escapes from bottom row (y = 4)
        for x in range(5):
            self.assertTrue(self.board.is_escape_position(x, 4, self.player2))
        
        # Other positions should not be escape positions for Player 2
        for y in range(4):  # y = 0, 1, 2, 3
            for x in range(5):
                self.assertFalse(self.board.is_escape_position(x, y, self.player2))
        
        # Test get_all_escape_positions
        escape_positions = self.board.get_all_escape_positions(self.player2)
        expected_positions = [(x, 4) for x in range(5)]
        self.assertEqual(set(escape_positions), set(expected_positions))
    
    def test_starting_escape_positions_invalid_positions(self):
        """Test starting and escape position checks with invalid coordinates."""
        # Invalid positions should return False
        self.assertFalse(self.board.is_starting_position(-1, 0, self.player1))
        self.assertFalse(self.board.is_starting_position(0, -1, self.player1))
        self.assertFalse(self.board.is_starting_position(5, 0, self.player1))
        self.assertFalse(self.board.is_starting_position(0, 5, self.player1))
        
        self.assertFalse(self.board.is_escape_position(-1, 0, self.player1))
        self.assertFalse(self.board.is_escape_position(0, -1, self.player1))
        self.assertFalse(self.board.is_escape_position(5, 0, self.player1))
        self.assertFalse(self.board.is_escape_position(0, 5, self.player1))
    
    def test_adjacent_intersections_center(self):
        """Test adjacency calculation for center positions."""
        # Test center position (2, 2)
        adjacent = self.board.get_adjacent_intersections(2, 2)
        expected = [(2, 1), (2, 3), (1, 2), (3, 2)]  # Up, Down, Left, Right
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 4)
    
    def test_adjacent_intersections_corner(self):
        """Test adjacency calculation for corner positions."""
        # Test top-left corner (0, 0)
        adjacent = self.board.get_adjacent_intersections(0, 0)
        expected = [(0, 1), (1, 0)]  # Down, Right
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 2)
        
        # Test bottom-right corner (4, 4)
        adjacent = self.board.get_adjacent_intersections(4, 4)
        expected = [(4, 3), (3, 4)]  # Up, Left
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 2)
        
        # Test top-right corner (4, 0)
        adjacent = self.board.get_adjacent_intersections(4, 0)
        expected = [(4, 1), (3, 0)]  # Down, Left
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 2)
        
        # Test bottom-left corner (0, 4)
        adjacent = self.board.get_adjacent_intersections(0, 4)
        expected = [(0, 3), (1, 4)]  # Up, Right
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 2)
    
    def test_adjacent_intersections_edge(self):
        """Test adjacency calculation for edge positions."""
        # Test top edge (2, 0)
        adjacent = self.board.get_adjacent_intersections(2, 0)
        expected = [(2, 1), (1, 0), (3, 0)]  # Down, Left, Right
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 3)
        
        # Test bottom edge (2, 4)
        adjacent = self.board.get_adjacent_intersections(2, 4)
        expected = [(2, 3), (1, 4), (3, 4)]  # Up, Left, Right
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 3)
        
        # Test left edge (0, 2)
        adjacent = self.board.get_adjacent_intersections(0, 2)
        expected = [(0, 1), (0, 3), (1, 2)]  # Up, Down, Right
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 3)
        
        # Test right edge (4, 2)
        adjacent = self.board.get_adjacent_intersections(4, 2)
        expected = [(4, 1), (4, 3), (3, 2)]  # Up, Down, Left
        self.assertEqual(set(adjacent), set(expected))
        self.assertEqual(len(adjacent), 3)
    
    def test_adjacent_intersections_invalid_position(self):
        """Test adjacency calculation for invalid positions."""
        # Invalid positions should return empty list
        self.assertEqual(self.board.get_adjacent_intersections(-1, 0), [])
        self.assertEqual(self.board.get_adjacent_intersections(0, -1), [])
        self.assertEqual(self.board.get_adjacent_intersections(5, 0), [])
        self.assertEqual(self.board.get_adjacent_intersections(0, 5), [])
    
    def test_valid_moves_from_position(self):
        """Test getting valid moves from a position."""
        # Test with empty board - all adjacent positions should be valid
        valid_moves = self.board.get_valid_moves_from_position(2, 2)
        expected = [(2, 1), (2, 3), (1, 2), (3, 2)]
        self.assertEqual(set(valid_moves), set(expected))
        
        # Place pawns to block some moves
        self.assertTrue(self.board.place_pawn(self.pawn1, 2, 1))  # Block up
        self.assertTrue(self.board.place_pawn(self.pawn2, 1, 2))  # Block left
        
        valid_moves = self.board.get_valid_moves_from_position(2, 2)
        expected = [(2, 3), (3, 2)]  # Only down and right should be available
        self.assertEqual(set(valid_moves), set(expected))
        
        # Block all adjacent positions
        self.assertTrue(self.board.place_pawn(self.player1.get_pawns()[1], 2, 3))  # Block down
        self.assertTrue(self.board.place_pawn(self.player2.get_pawns()[1], 3, 2))  # Block right
        
        valid_moves = self.board.get_valid_moves_from_position(2, 2)
        self.assertEqual(valid_moves, [])  # No valid moves
    
    def test_valid_moves_corner_position(self):
        """Test getting valid moves from corner positions."""
        # Test corner position with empty board
        valid_moves = self.board.get_valid_moves_from_position(0, 0)
        expected = [(0, 1), (1, 0)]
        self.assertEqual(set(valid_moves), set(expected))
        
        # Block one adjacent position
        self.assertTrue(self.board.place_pawn(self.pawn1, 0, 1))
        valid_moves = self.board.get_valid_moves_from_position(0, 0)
        expected = [(1, 0)]
        self.assertEqual(valid_moves, expected)
    
    def test_clear_board(self):
        """Test clearing the board."""
        # Place some pawns
        self.assertTrue(self.board.place_pawn(self.pawn1, 1, 1))
        self.assertTrue(self.board.place_pawn(self.pawn2, 2, 2))
        
        # Verify pawns are placed
        self.assertFalse(self.board.is_intersection_empty(1, 1))
        self.assertFalse(self.board.is_intersection_empty(2, 2))
        
        # Clear the board
        self.board.clear_board()
        
        # Verify all intersections are empty
        for x in range(5):
            for y in range(5):
                self.assertTrue(self.board.is_intersection_empty(x, y))
                self.assertIsNone(self.board.get_pawn_at_intersection(x, y))


if __name__ == '__main__':
    unittest.main()