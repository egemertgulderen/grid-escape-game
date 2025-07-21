"""
Board class for Grid Escape game.
"""
from typing import List, Tuple, Optional


class Board:
    """
    Represents the 5x5 grid board for the Grid Escape game.
    
    The board manages intersection positions, validates coordinates,
    and provides methods for determining starting positions, escape positions,
    and adjacent intersections for movement validation.
    """
    
    # Board dimensions
    GRID_SIZE = 7
    
    def __init__(self):
        """Initialize a new 5x5 game board."""
        # Grid coordinates range from (0,0) to (4,4)
        # (0,0) is top-left, (4,4) is bottom-right
        self._grid_size = self.GRID_SIZE
        
        # Track which intersections are occupied by pawns
        # Key: (x, y) tuple, Value: Pawn object or None
        self._intersections = {}
        
        # Initialize all intersections as empty
        for x in range(self._grid_size):
            for y in range(self._grid_size):
                self._intersections[(x, y)] = None
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Check if the given coordinates represent a valid position on the board.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            True if the position is valid (within board bounds), False otherwise
        """
        return 0 <= x < self._grid_size and 0 <= y < self._grid_size
    
    def is_intersection_empty(self, x: int, y: int) -> bool:
        """
        Check if the intersection at the given coordinates is empty.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            True if the intersection is empty, False if occupied or invalid
        """
        if not self.is_valid_position(x, y):
            return False
        return self._intersections[(x, y)] is None
    
    def get_pawn_at_intersection(self, x: int, y: int) -> Optional[object]:
        """
        Get the pawn at the specified intersection.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            The pawn at the intersection, or None if empty or invalid position
        """
        if not self.is_valid_position(x, y):
            return None
        return self._intersections[(x, y)]
    
    def place_pawn(self, pawn, x: int, y: int) -> bool:
        """
        Place a pawn at the specified intersection.
        
        Args:
            pawn: The pawn to place
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            True if the pawn was placed successfully, False otherwise
        """
        if not self.is_valid_position(x, y) or not self.is_intersection_empty(x, y):
            return False
        
        self._intersections[(x, y)] = pawn
        return True
    
    def remove_pawn(self, x: int, y: int) -> Optional[object]:
        """
        Remove a pawn from the specified intersection.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            The removed pawn, or None if no pawn was at the intersection
        """
        if not self.is_valid_position(x, y):
            return None
        
        pawn = self._intersections[(x, y)]
        self._intersections[(x, y)] = None
        return pawn
    
    def move_pawn(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        """
        Move a pawn from one intersection to another.
        
        Args:
            from_x: Source X-coordinate
            from_y: Source Y-coordinate
            to_x: Destination X-coordinate
            to_y: Destination Y-coordinate
            
        Returns:
            True if the move was successful, False otherwise
        """
        # Check if source position has a pawn and destination is empty
        if (not self.is_valid_position(from_x, from_y) or 
            not self.is_valid_position(to_x, to_y) or
            self._intersections[(from_x, from_y)] is None or
            not self.is_intersection_empty(to_x, to_y)):
            return False
        
        # Move the pawn
        pawn = self._intersections[(from_x, from_y)]
        self._intersections[(from_x, from_y)] = None
        self._intersections[(to_x, to_y)] = pawn
        return True
    
    def is_starting_position(self, x: int, y: int, player) -> bool:
        """
        Check if the given position is a valid starting position for the player.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            player: The player to check for
            
        Returns:
            True if the position is a valid starting position for the player
        """
        if not self.is_valid_position(x, y):
            return False
        
        # Player 1 (ID 1) starts on the bottom row (y = 6) in the center 5 points (x = 1-5)
        # Player 2 (ID 2) starts on the right column (x = 6) in the center 5 points (y = 1-5)
        if player.player_id == 1:
            return y == 6 and 1 <= x <= 5
        elif player.player_id == 2:
            return x == 6 and 1 <= y <= 5
        else:
            return False
    
    def is_escape_position(self, x: int, y: int, player) -> bool:
        """
        Check if the given position is an escape position for the player.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            player: The player to check for
            
        Returns:
            True if the position is an escape position for the player
        """
        if not self.is_valid_position(x, y):
            return False
        
        # Player 1 (ID 1) escapes from the top row (y = 0) in the center 5 points (x = 1-5)
        # Player 2 (ID 2) escapes from the left column (x = 0) in the center 5 points (y = 1-5)
        if player.player_id == 1:
            return y == 0 and 1 <= x <= 5
        elif player.player_id == 2:
            return x == 0 and 1 <= y <= 5
        else:
            return False
    
    def get_adjacent_intersections(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get all adjacent intersections to the given position.
        
        Adjacent intersections are those that are horizontally or vertically
        adjacent (not diagonally adjacent).
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            List of (x, y) tuples representing adjacent intersections
        """
        if not self.is_valid_position(x, y):
            return []
        
        adjacent = []
        
        # Check all four directions: up, down, left, right
        directions = [
            (0, -1),  # Up
            (0, 1),   # Down
            (-1, 0),  # Left
            (1, 0)    # Right
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position(new_x, new_y):
                adjacent.append((new_x, new_y))
        
        return adjacent
    
    def get_valid_moves_from_position(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get all valid move destinations from the given position.
        
        A valid move destination is an adjacent intersection that is empty.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            List of (x, y) tuples representing valid move destinations
        """
        adjacent_positions = self.get_adjacent_intersections(x, y)
        valid_moves = []
        
        for adj_x, adj_y in adjacent_positions:
            if self.is_intersection_empty(adj_x, adj_y):
                valid_moves.append((adj_x, adj_y))
        
        return valid_moves
    
    def get_all_starting_positions(self, player) -> List[Tuple[int, int]]:
        """
        Get all starting positions for the given player.
        
        Args:
            player: The player to get starting positions for
            
        Returns:
            List of (x, y) tuples representing starting positions
        """
        starting_positions = []
        
        for x in range(self._grid_size):
            for y in range(self._grid_size):
                if self.is_starting_position(x, y, player):
                    starting_positions.append((x, y))
        
        return starting_positions
    
    def get_all_escape_positions(self, player) -> List[Tuple[int, int]]:
        """
        Get all escape positions for the given player.
        
        Args:
            player: The player to get escape positions for
            
        Returns:
            List of (x, y) tuples representing escape positions
        """
        escape_positions = []
        
        for x in range(self._grid_size):
            for y in range(self._grid_size):
                if self.is_escape_position(x, y, player):
                    escape_positions.append((x, y))
        
        return escape_positions
    
    def clear_board(self) -> None:
        """Clear all pawns from the board."""
        for x in range(self._grid_size):
            for y in range(self._grid_size):
                self._intersections[(x, y)] = None
    
    def get_grid_size(self) -> int:
        """
        Get the size of the grid.
        
        Returns:
            The grid size (5 for a 5x5 grid)
        """
        return self._grid_size