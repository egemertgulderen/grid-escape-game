"""
Player class for Grid Escape game.
"""
from typing import List, Tuple
from .pawn import Pawn

class Player:
    """
    Represents a player in the Grid Escape game.
    
    Each player has 7 pawns and is responsible for tracking their state,
    including which pawns are on the board and which have escaped.
    """
    
    def __init__(self, player_id: int, color: Tuple[int, int, int]):
        """
        Initialize a new player.
        
        Args:
            player_id: Unique identifier for this player (1 or 2)
            color: RGB color tuple for this player's pawns
        """
        self._player_id = player_id
        self._color = color
        self._pawns = [Pawn(self, i) for i in range(7)]  # Each player has 7 pawns
        
    @property
    def player_id(self) -> int:
        """Get the player's unique identifier."""
        return self._player_id
    
    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the player's color."""
        return self._color
    
    def get_pawns(self) -> List[Pawn]:
        """
        Get all pawns belonging to this player.
        
        Returns:
            List of all pawns owned by this player
        """
        return self._pawns
    
    def get_pawns_on_board(self) -> List[Pawn]:
        """
        Get all pawns that are currently on the board.
        
        Returns:
            List of pawns that are on the board
        """
        return [pawn for pawn in self._pawns if pawn.is_on_board()]
    
    def get_escaped_pawns(self) -> List[Pawn]:
        """
        Get all pawns that have escaped from the board.
        
        Returns:
            List of pawns that have escaped
        """
        return [pawn for pawn in self._pawns if pawn.is_escaped()]
    
    def get_unplaced_pawns(self) -> List[Pawn]:
        """
        Get all pawns that have not yet been placed on the board.
        
        Returns:
            List of pawns that have not been placed
        """
        return [pawn for pawn in self._pawns 
                if not pawn.is_on_board() and not pawn.is_escaped()]
    
    def has_won(self) -> bool:
        """
        Check if this player has won the game.
        
        A player wins when all 7 pawns have escaped.
        
        Returns:
            True if the player has won, False otherwise
        """
        return len(self.get_escaped_pawns()) == 7
    
    def can_move_any_pawn(self, board) -> bool:
        """
        Check if any of the player's pawns can make a valid move.
        
        Args:
            board: The game board
            
        Returns:
            True if at least one pawn can move, False otherwise
        """
        for pawn in self.get_pawns_on_board():
            if pawn.get_valid_moves(board):
                return True
        return False
    
    def get_pawn_at_position(self, x: int, y: int) -> Pawn:
        """
        Get the pawn at the specified position, if any.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            The pawn at the position, or None if no pawn is there
        """
        for pawn in self.get_pawns_on_board():
            pos = pawn.get_position()
            if pos and pos[0] == x and pos[1] == y:
                return pawn
        return None