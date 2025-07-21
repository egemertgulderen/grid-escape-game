"""
Pawn class for Grid Escape game.
"""
from typing import Optional, Tuple, List, Set

class Pawn:
    """
    Represents a pawn in the Grid Escape game.
    
    Each pawn belongs to a player and can be placed on the board,
    moved between intersections, and eventually escaped from the board.
    """
    
    def __init__(self, player, pawn_id: int):
        """
        Initialize a new pawn.
        
        Args:
            player: The player that owns this pawn
            pawn_id: Unique identifier for this pawn within the player's collection
        """
        self._player = player
        self._pawn_id = pawn_id
        self._position: Optional[Tuple[int, int]] = None
        self._escaped = False
    
    @property
    def player(self):
        """Get the player that owns this pawn."""
        return self._player
    
    @property
    def pawn_id(self) -> int:
        """Get the pawn's unique identifier."""
        return self._pawn_id
    
    def get_position(self) -> Optional[Tuple[int, int]]:
        """
        Get the current position of the pawn on the board.
        
        Returns:
            A tuple (x, y) representing the grid coordinates, or None if not on board
        """
        return self._position
    
    def set_position(self, x: int, y: int) -> None:
        """
        Set the position of the pawn on the board.
        
        Args:
            x: X-coordinate (0-4)
            y: Y-coordinate (0-4)
        """
        self._position = (x, y)
        self._escaped = False
    
    def is_on_board(self) -> bool:
        """
        Check if the pawn is currently on the board.
        
        Returns:
            True if the pawn is on the board, False otherwise
        """
        return self._position is not None and not self._escaped
    
    def escape(self) -> None:
        """
        Mark the pawn as escaped from the board.
        
        This removes the pawn from the board and marks it as escaped.
        """
        self._escaped = True
        self._position = None
    
    def is_escaped(self) -> bool:
        """
        Check if the pawn has escaped from the board.
        
        Returns:
            True if the pawn has escaped, False otherwise
        """
        return self._escaped
    
    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        """
        Get all valid moves for this pawn based on the current board state.
        
        A valid move is to an adjacent intersection that is not occupied by any pawn.
        For Player 1, only upward movement is allowed (bottom to top).
        For Player 2, only leftward movement is allowed (right to left).
        
        Args:
            board: The game board
            
        Returns:
            List of (x, y) coordinates representing valid move destinations
        """
        if not self.is_on_board() or self._position is None:
            return []
        
        x, y = self._position
        
        # Get all adjacent empty positions
        adjacent_empty = board.get_valid_moves_from_position(x, y)
        valid_moves = []
        
        # Filter based on player's allowed direction
        for adj_x, adj_y in adjacent_empty:
            # Player 1 can only move upward (decreasing y)
            if self._player.player_id == 1 and adj_y < y:
                valid_moves.append((adj_x, adj_y))
            # Player 2 can only move leftward (decreasing x)
            elif self._player.player_id == 2 and adj_x < x:
                valid_moves.append((adj_x, adj_y))
        
        return valid_moves
    
    def get_adjacent_positions(self, board) -> List[Tuple[int, int]]:
        """
        Get all adjacent positions regardless of whether they are occupied.
        
        This is useful for determining if a pawn is blocked by other pawns.
        
        Args:
            board: The game board
            
        Returns:
            List of (x, y) coordinates representing adjacent positions
        """
        if not self.is_on_board() or self._position is None:
            return []
        
        x, y = self._position
        return board.get_adjacent_intersections(x, y)
    
    def is_blocked(self, board) -> bool:
        """
        Check if this pawn is completely blocked by other pawns.
        
        A pawn is blocked if all adjacent intersections are occupied.
        
        Args:
            board: The game board
            
        Returns:
            True if the pawn is blocked, False otherwise
        """
        return len(self.get_valid_moves(board)) == 0
    
    def can_move_to(self, board, to_x: int, to_y: int) -> bool:
        """
        Check if this pawn can move to the specified position.
        
        A move is valid if:
        1. The pawn is on the board
        2. The destination is adjacent (horizontally or vertically)
        3. The destination is not occupied by any pawn
        
        Args:
            board: The game board
            to_x: Destination X-coordinate
            to_y: Destination Y-coordinate
            
        Returns:
            True if the move is valid, False otherwise
        """
        if not self.is_on_board() or self._position is None:
            return False
        
        # Check if destination is in valid moves list
        valid_moves = self.get_valid_moves(board)
        return (to_x, to_y) in valid_moves
    
    def is_adjacent_to(self, x: int, y: int) -> bool:
        """
        Check if the given position is adjacent to this pawn.
        
        Adjacent means horizontally or vertically adjacent, not diagonally.
        
        Args:
            x: X-coordinate to check
            y: Y-coordinate to check
            
        Returns:
            True if the position is adjacent, False otherwise
        """
        if not self.is_on_board() or self._position is None:
            return False
        
        current_x, current_y = self._position
        
        # Check if horizontally or vertically adjacent (not diagonal)
        # Adjacent means exactly one coordinate differs by exactly 1
        x_diff = abs(current_x - x)
        y_diff = abs(current_y - y)
        
        return (x_diff == 1 and y_diff == 0) or (x_diff == 0 and y_diff == 1)
    
    def would_escape_at(self, board, x: int, y: int) -> bool:
        """
        Check if moving to the given position would cause this pawn to escape.
        
        Args:
            board: The game board
            x: X-coordinate to check
            y: Y-coordinate to check
            
        Returns:
            True if the pawn would escape at this position, False otherwise
        """
        return board.is_escape_position(x, y, self._player)
    
    def move_to(self, board, to_x: int, to_y: int) -> bool:
        """
        Move this pawn to the specified position if the move is valid.
        
        This method handles the complete move logic including:
        - Validating the move is legal
        - Updating the board state
        - Updating the pawn's position
        - Handling escape conditions
        
        Args:
            board: The game board
            to_x: Destination X-coordinate
            to_y: Destination Y-coordinate
            
        Returns:
            True if the move was successful, False otherwise
        """
        # Validate the move
        if not self.can_move_to(board, to_x, to_y):
            return False
        
        current_x, current_y = self._position
        
        # Execute the move on the board
        if board.move_pawn(current_x, current_y, to_x, to_y):
            # Update pawn's position
            self.set_position(to_x, to_y)
            
            # Check if pawn reached an escape position
            if board.is_escape_position(to_x, to_y, self._player):
                # Remove pawn from board and mark as escaped
                board.remove_pawn(to_x, to_y)
                self.escape()
            
            return True
        
        return False