"""
GameState class for Grid Escape game.
"""
from typing import List, Optional, Tuple
from .player import Player
from .board import Board

class GameState:
    """
    Manages the overall state of the Grid Escape game.
    
    This includes tracking the current phase (setup or movement),
    the current player's turn, victory conditions, and automatic
    turn management when players cannot move.
    """
    
    # Game phases
    PLAYING = 0
    GAME_OVER = 1
    
    def __init__(self):
        """Initialize a new game state."""
        # Create players with their colors
        self.players = [
            Player(1, (0, 102, 204)),  # Player 1: Blue
            Player(2, (204, 0, 0))     # Player 2: Red
        ]
        
        # Create the game board
        self.board = Board()
        
        # Set initial game state
        self.phase = self.PLAYING
        self.current_player_index = 0
        self.selected_pawn = None
        self.winner = None
        
        # Turn management flags
        self.turn_skipped = False
        self.skipped_player_id = None
        self.stalemate = False
    
    def get_current_player(self) -> Player:
        """
        Get the player whose turn it currently is.
        
        Returns:
            The current player
        """
        return self.players[self.current_player_index]
    
    def get_other_player(self) -> Player:
        """
        Get the player who is not currently taking their turn.
        
        Returns:
            The other player
        """
        other_index = (self.current_player_index + 1) % len(self.players)
        return self.players[other_index]
    
    def switch_turn(self) -> Tuple[bool, Optional[int]]:
        """
        Switch to the next player's turn.
        
        Automatically handles turn skipping if the next player cannot move.
        Updates game state to GAME_OVER if a victory condition is met.
        
        Returns:
            Tuple containing:
            - Boolean indicating if a turn was skipped
            - Player ID of the skipped player (or None if no skip)
        """
        if self.phase == self.GAME_OVER:
            return False, None
        
        # Reset turn skipped flags
        self.turn_skipped = False
        self.skipped_player_id = None
        
        # Clear any selected pawn when switching turns
        self.selected_pawn = None
        
        # Check for victory before switching turns
        winner = self.check_victory()
        if winner:
            self.winner = winner
            self.phase = self.GAME_OVER
            return False, None
        
        # Switch to next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # If in playing phase, check if current player can move
        if self.phase == self.PLAYING:
            # Check both players to avoid infinite recursion
            players_checked = 0
            
            # Keep track of which players we've checked
            checked_players = set()
            
            while players_checked < len(self.players):
                current_player = self.get_current_player()
                current_id = current_player.player_id
                
                # If we've already checked this player, we're in a stalemate
                if current_id in checked_players:
                    self.stalemate = True
                    self.phase = self.GAME_OVER
                    return False, None
                
                checked_players.add(current_id)
                
                # Check if current player can move
                if self.can_player_move(current_player):
                    # Current player can move, stop here
                    break
                
                # Current player cannot move, mark turn as skipped
                self.turn_skipped = True
                self.skipped_player_id = current_player.player_id
                
                # Try next player
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                players_checked += 1
            
            # If we've checked all players and none can move, game should end in stalemate
            if players_checked >= len(self.players):
                self.stalemate = True
                self.phase = self.GAME_OVER
                return False, None
        
        return self.turn_skipped, self.skipped_player_id
    
    def is_setup_phase(self) -> bool:
        """
        Check if the game is in the setup phase.
        
        Note: In the new game rules, there is no separate setup phase.
        This method is kept for compatibility.
        
        Returns:
            Always False as there is no separate setup phase
        """
        return False
    
    def is_movement_phase(self) -> bool:
        """
        Check if the game is in the movement phase.
        
        Returns:
            True if in movement phase, False otherwise
        """
        return self.phase == self.PLAYING
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self.phase == self.GAME_OVER
    
    def check_victory(self) -> Optional[Player]:
        """
        Check if either player has won the game.
        
        A player wins when all 7 of their pawns have escaped.
        
        Returns:
            The winning player, or None if no player has won yet
        """
        for player in self.players:
            if player.has_won():
                return player
        return None
    
    def can_player_move(self, player: Player) -> bool:
        """
        Check if the given player can make any valid moves.
        
        Args:
            player: The player to check
            
        Returns:
            True if the player can make at least one valid move, False otherwise
        """
        return player.can_move_any_pawn(self.board)
    
    def transition_to_playing_phase(self) -> bool:
        """
        Transition from setup phase to playing phase.
        
        This should be called when all pawns have been placed during setup.
        
        Returns:
            True if transition was successful, False if not in setup phase
        """
        if self.phase != self.SETUP:
            return False
        
        # Check if all pawns have been placed
        total_unplaced = sum(len(player.get_unplaced_pawns()) for player in self.players)
        if total_unplaced == 0:
            self.phase = self.PLAYING
            self.current_player_index = 0  # Player 1 starts the movement phase
            
            # Reset turn management flags
            self.turn_skipped = False
            self.skipped_player_id = None
            self.stalemate = False
            
            return True
        
        return False
    
    def is_setup_complete(self) -> bool:
        """
        Check if the setup phase is complete.
        
        Setup is complete when all pawns from both players have been placed.
        
        Returns:
            True if setup is complete, False otherwise
        """
        for player in self.players:
            if len(player.get_unplaced_pawns()) > 0:
                return False
        return True
    
    def get_winner(self) -> Optional[Player]:
        """
        Get the winner of the game.
        
        Returns:
            The winning player if game is over, None otherwise
        """
        return self.winner
    
    def reset_game(self) -> None:
        """
        Reset the game to initial state.
        
        Clears the board, resets all pawns, and returns to playing phase.
        Performs proper cleanup of all game state variables.
        """
        # Clear the board
        self.board.clear_board()
        
        # Reset all pawns for both players
        for player in self.players:
            # Reset pawns
            for pawn in player.get_pawns():
                pawn._position = None
                pawn._escaped = False
        
        # Reset game state
        self.phase = self.PLAYING
        self.current_player_index = 0
        self.selected_pawn = None
        self.winner = None
        
        # Reset turn management flags
        self.turn_skipped = False
        self.skipped_player_id = None
        self.stalemate = False
    
    def place_pawn(self, pawn, x: int, y: int) -> bool:
        """
        Place a pawn on the board.
        
        Args:
            pawn: The pawn to place
            x: X-coordinate
            y: Y-coordinate
            
        Returns:
            True if pawn was placed successfully, False otherwise
        """
        # Check if the pawn belongs to the current player
        current_player = self.get_current_player()
        if pawn.player != current_player:
            return False
        
        # Check if position is valid starting position for the pawn's player
        if not self.board.is_starting_position(x, y, pawn.player):
            return False
        
        # Try to place the pawn on the board
        if self.board.place_pawn(pawn, x, y):
            pawn.set_position(x, y)
            
            # Switch to next player after placing a pawn
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            
            # Check for victory
            winner = self.check_victory()
            if winner:
                self.winner = winner
                self.phase = self.GAME_OVER
            
            return True
        
        return False
    
    def move_pawn(self, pawn, to_x: int, to_y: int) -> bool:
        """
        Move a pawn.
        
        Args:
            pawn: The pawn to move
            to_x: Destination X-coordinate
            to_y: Destination Y-coordinate
            
        Returns:
            True if move was successful, False otherwise
        """
        if self.phase != self.PLAYING:
            return False
        
        # Check if it's the pawn's owner's turn
        if pawn.player != self.get_current_player():
            return False
        
        current_pos = pawn.get_position()
        if not current_pos:
            return False
        
        from_x, from_y = current_pos
        
        # Get valid moves based on player's direction
        valid_moves = pawn.get_valid_moves(self.board)
        if (to_x, to_y) not in valid_moves:
            return False
        
        # Execute the move
        if self.board.move_pawn(from_x, from_y, to_x, to_y):
            pawn.set_position(to_x, to_y)
            
            # Switch turns after successful move
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            
            # Check for victory
            winner = self.check_victory()
            if winner:
                self.winner = winner
                self.phase = self.GAME_OVER
            
            return True
        
        return False
        
    def escape_pawn(self, pawn) -> bool:
        """
        Remove a pawn from the board when it's at an escape position.
        
        Args:
            pawn: The pawn to escape
            
        Returns:
            True if the pawn was successfully escaped, False otherwise
        """
        if self.phase != self.PLAYING:
            return False
            
        # Check if it's the pawn's owner's turn
        if pawn.player != self.get_current_player():
            return False
            
        # Check if the pawn is on the board
        current_pos = pawn.get_position()
        if not current_pos:
            return False
            
        x, y = current_pos
        
        # Check if the pawn is at an escape position
        if not self.board.is_escape_position(x, y, pawn.player):
            return False
            
        # Remove the pawn from the board and mark it as escaped
        self.board.remove_pawn(x, y)
        pawn.escape()
        
        # Switch turns after successful escape
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Check for victory
        winner = self.check_victory()
        if winner:
            self.winner = winner
            self.phase = self.GAME_OVER
            
        return True