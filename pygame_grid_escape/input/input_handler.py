"""
InputHandler class for Grid Escape game.

This module processes user input and translates it into game actions,
handling mouse clicks for pawn selection and movement.
"""
import pygame
from typing import Tuple, Optional

class InputHandler:
    """
    Handles user input for the Grid Escape game.
    
    The InputHandler is responsible for processing mouse clicks,
    converting pixel coordinates to grid positions, and executing
    appropriate game actions based on the current game state.
    """
    
    def __init__(self, renderer=None):
        """
        Initialize the input handler.
        
        Args:
            renderer: The game renderer for visual feedback
        """
        self.renderer = renderer
    
    def handle_click(self, pos: Tuple[int, int], game_state, renderer) -> bool:
        """
        Process a mouse click at the given position.
        
        Args:
            pos: (x, y) tuple of pixel coordinates
            game_state: The current game state
            renderer: The game renderer
            
        Returns:
            True if the click was processed successfully, False otherwise
        """
        # Store renderer reference for this click handling
        self.renderer = renderer
        
        # Convert pixel coordinates to grid position
        grid_pos = renderer.pixel_to_grid_position(pos)
        
        # Handle game over state first
        if game_state.is_game_over():
            # Check if click is on the restart button area (center of screen)
            center_x, center_y = renderer.WINDOW_WIDTH // 2, renderer.WINDOW_HEIGHT // 2
            restart_area_size = 100  # Size of the clickable area
            
            # Check if click is within the restart button area
            if (abs(pos[0] - center_x) < restart_area_size and 
                abs(pos[1] - (center_y + 40)) < 20):  # +40 is where the restart text is
                game_state.reset_game()
                renderer.show_notification("Game restarted")
                return True
            else:
                renderer.show_notification("Game is over. Press R to restart.")
                return False
        
        # For other phases, handle grid clicks
        if not grid_pos:
            # Click was outside the grid
            game_state.selected_pawn = None
            return False
        
        x, y = grid_pos
        
        # In the new game flow, we handle both placing and moving in a single phase
        return self._handle_game_click(x, y, game_state)
    
    def _handle_setup_phase_click(self, x: int, y: int, game_state) -> bool:
        """
        Handle a click during the setup phase.
        
        During setup, clicks on valid starting positions place pawns.
        
        Args:
            x: Grid X-coordinate
            y: Grid Y-coordinate
            game_state: The current game state
            
        Returns:
            True if a pawn was placed, False otherwise
        """
        current_player = game_state.get_current_player()
        
        # Check if the position is a valid starting position for the current player
        if not game_state.board.is_starting_position(x, y, current_player):
            # Show error message for invalid starting position
            self.renderer.show_error_message(f"Invalid position - must be on Player {current_player.player_id}'s starting row")
            return False
        
        # Check if the position is empty
        if not game_state.board.is_intersection_empty(x, y):
            # Show error message for occupied position
            self.renderer.show_error_message("Position already occupied")
            return False
        
        # Get an unplaced pawn
        unplaced_pawns = current_player.get_unplaced_pawns()
        if not unplaced_pawns:
            # Show error message for no pawns left
            self.renderer.show_error_message("No pawns left to place")
            return False
        
        # Place the pawn
        pawn = unplaced_pawns[0]
        if game_state.place_pawn(pawn, x, y):
            # Show notification about whose turn it is now
            next_player = game_state.get_current_player()
            self.renderer.show_notification(f"Player {next_player.player_id}'s turn")
            
            # Check if we've transitioned to playing phase
            if game_state.is_movement_phase():
                self.renderer.show_notification("Setup complete! Movement phase begins")
            
            return True
        
        return False
    
    def _handle_movement_phase_click(self, x: int, y: int, game_state) -> bool:
        """
        Handle a click during the movement phase.
        
        During movement, clicks either select a pawn or move a selected pawn.
        
        Args:
            x: Grid X-coordinate
            y: Grid Y-coordinate
            game_state: The current game state
            
        Returns:
            True if a pawn was selected or moved, False otherwise
        """
        current_player = game_state.get_current_player()
        
        # If a pawn is already selected
        if game_state.selected_pawn:
            # Check if the click is on a valid move destination
            valid_moves = game_state.selected_pawn.get_valid_moves(game_state.board)
            if (x, y) in valid_moves:
                # Store reference to pawn before move (in case it gets cleared)
                moving_pawn = game_state.selected_pawn
                
                # Move the pawn
                if game_state.move_pawn(moving_pawn, x, y):
                    # Pawn moved successfully, selection is cleared in move_pawn
                    # Show notification for successful move
                    self.renderer.show_notification("Pawn moved")
                    
                    # Check if the pawn escaped
                    if moving_pawn.is_escaped():
                        self.renderer.show_notification("Pawn escaped!")
                    
                    # Check if turn was skipped after this move
                    turn_skipped, skipped_player_id = game_state.turn_skipped, game_state.skipped_player_id
                    if turn_skipped and skipped_player_id:
                        self.renderer.show_notification(f"Player {skipped_player_id}'s turn skipped - no valid moves!")
                    
                    return True
            else:
                # Click was not on a valid move destination
                # Check if it's on another of the player's pawns
                pawn_at_pos = current_player.get_pawn_at_position(x, y)
                if pawn_at_pos:
                    # Select the new pawn
                    game_state.selected_pawn = pawn_at_pos
                    self.renderer.show_notification(f"Selected Player {current_player.player_id}'s pawn")
                    return True
                else:
                    # Check if there's an opponent's pawn at this position
                    opponent = game_state.get_other_player()
                    opponent_pawn = opponent.get_pawn_at_position(x, y)
                    
                    if opponent_pawn:
                        # Show error for clicking on opponent's pawn
                        self.renderer.show_error_message("Cannot move to occupied position")
                    elif not game_state.board.is_valid_position(x, y):
                        # Show error for invalid position
                        self.renderer.show_error_message("Invalid position")
                    elif (x, y) not in game_state.board.get_adjacent_positions(*game_state.selected_pawn.get_position()):
                        # Show error for non-adjacent position
                        self.renderer.show_error_message("Can only move to adjacent positions")
                    else:
                        # Deselect the current pawn
                        game_state.selected_pawn = None
                        self.renderer.show_notification("Pawn deselected")
                    return True
        else:
            # No pawn is selected, try to select one
            pawn_at_pos = current_player.get_pawn_at_position(x, y)
            if pawn_at_pos:
                # Select the pawn
                game_state.selected_pawn = pawn_at_pos
                self.renderer.show_notification(f"Selected Player {current_player.player_id}'s pawn")
                return True
            else:
                # Check if there's an opponent's pawn at this position
                opponent = game_state.get_other_player()
                opponent_pawn = opponent.get_pawn_at_position(x, y)
                
                if opponent_pawn:
                    # Show error for clicking on opponent's pawn
                    self.renderer.show_error_message(f"That's Player {opponent.player_id}'s pawn")
                else:
                    # Show error for clicking on empty space with no pawn selected
                    self.renderer.show_error_message("Select your pawn first")
        
        return False
    
    def get_intersection_from_pixel(self, pos: Tuple[int, int], renderer) -> Optional[Tuple[int, int]]:
        """
        Convert pixel coordinates to grid intersection coordinates.
        
        Args:
            pos: (x, y) tuple of pixel coordinates
            renderer: The game renderer
            
        Returns:
            (grid_x, grid_y) tuple or None if outside the grid
        """
        return renderer.pixel_to_grid_position(pos)
        
    def _handle_game_click(self, x: int, y: int, game_state) -> bool:
        """
        Handle a click during the game.
        
        In each turn, a player can either place a new pawn, move an existing pawn,
        or escape a pawn that's at an exit point.
        
        Args:
            x: Grid X-coordinate
            y: Grid Y-coordinate
            game_state: The current game state
            
        Returns:
            True if an action was performed, False otherwise
        """
        current_player = game_state.get_current_player()
        
        # If a pawn is already selected, try to move it or escape it
        if game_state.selected_pawn:
            # Get the current position of the selected pawn
            current_pos = game_state.selected_pawn.get_position()
            if current_pos:
                current_x, current_y = current_pos
                
                # Check if the pawn is at an escape position and the player clicked on it again
                if game_state.board.is_escape_position(current_x, current_y, current_player) and x == current_x and y == current_y:
                    # Try to escape the pawn
                    if game_state.escape_pawn(game_state.selected_pawn):
                        # Pawn escaped successfully
                        game_state.selected_pawn = None
                        self.renderer.show_notification("Pawn escaped!")
                        
                        # Show whose turn it is now
                        next_player = game_state.get_current_player()
                        self.renderer.show_notification(f"Player {next_player.player_id}'s turn")
                        
                        return True
                
                # Check if the click is on a valid move destination
                valid_moves = game_state.selected_pawn.get_valid_moves(game_state.board)
                if (x, y) in valid_moves:
                    # Store reference to pawn before move (in case it gets cleared)
                    moving_pawn = game_state.selected_pawn
                    
                    # Move the pawn
                    if game_state.move_pawn(moving_pawn, x, y):
                        # Pawn moved successfully, selection is cleared
                        game_state.selected_pawn = None
                        self.renderer.show_notification("Pawn moved")
                        
                        # Check if the pawn is at an escape position
                        if game_state.board.is_escape_position(x, y, current_player):
                            self.renderer.show_notification("Pawn at exit point! Click again to escape.")
                        
                        # Show whose turn it is now
                        next_player = game_state.get_current_player()
                        self.renderer.show_notification(f"Player {next_player.player_id}'s turn")
                        
                        return True
                else:
                    # Click was not on a valid move destination
                    # Check if it's on another of the player's pawns
                    pawn_at_pos = current_player.get_pawn_at_position(x, y)
                    if pawn_at_pos:
                        # Select the new pawn
                        game_state.selected_pawn = pawn_at_pos
                        
                        # Check if this pawn is at an escape position
                        pawn_pos = pawn_at_pos.get_position()
                        if pawn_pos and game_state.board.is_escape_position(pawn_pos[0], pawn_pos[1], current_player):
                            self.renderer.show_notification(f"Selected pawn at exit point. Click again to escape.")
                        else:
                            self.renderer.show_notification(f"Selected Player {current_player.player_id}'s pawn")
                        
                        return True
                    else:
                        # Deselect the current pawn
                        game_state.selected_pawn = None
                        self.renderer.show_notification("Pawn deselected")
                        return True
            
        else:
            # No pawn is selected
            
            # First, check if the click is on an existing pawn
            pawn_at_pos = current_player.get_pawn_at_position(x, y)
            if pawn_at_pos:
                # Select the pawn
                game_state.selected_pawn = pawn_at_pos
                
                # Check if this pawn is at an escape position
                pawn_pos = pawn_at_pos.get_position()
                if pawn_pos and game_state.board.is_escape_position(pawn_pos[0], pawn_pos[1], current_player):
                    self.renderer.show_notification(f"Selected pawn at exit point. Click again to escape.")
                else:
                    self.renderer.show_notification(f"Selected Player {current_player.player_id}'s pawn")
                
                return True
            
            # Check if the position is a valid starting position for the current player
            if game_state.board.is_starting_position(x, y, current_player):
                # Check if the position is empty
                if game_state.board.is_intersection_empty(x, y):
                    # Get an unplaced pawn
                    unplaced_pawns = current_player.get_unplaced_pawns()
                    if unplaced_pawns:
                        # Place the pawn
                        pawn = unplaced_pawns[0]
                        if game_state.place_pawn(pawn, x, y):
                            # Show notification about whose turn it is now
                            next_player = game_state.get_current_player()
                            self.renderer.show_notification(f"Pawn placed. Player {next_player.player_id}'s turn")
                            return True
                    else:
                        self.renderer.show_error_message("No pawns left to place")
                        return False
                else:
                    self.renderer.show_error_message("Position already occupied")
                    return False
            else:
                # Check if there's an opponent's pawn at this position
                opponent = game_state.get_other_player()
                opponent_pawn = opponent.get_pawn_at_position(x, y)
                
                if opponent_pawn:
                    # Show error for clicking on opponent's pawn
                    self.renderer.show_error_message(f"That's Player {opponent.player_id}'s pawn")
                else:
                    # Show error for clicking on invalid position
                    self.renderer.show_error_message(f"Invalid position - Player {current_player.player_id} must place pawns on their starting row")
        
        return False