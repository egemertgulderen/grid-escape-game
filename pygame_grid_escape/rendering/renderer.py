"""
Renderer class for Grid Escape game.

This module handles all pygame drawing operations for the game,
including the board, pawns, UI elements, and visual feedback.
"""
import pygame
import time
from typing import List, Tuple, Optional

class Renderer:
    """
    Handles all pygame drawing operations for the Grid Escape game.
    
    The Renderer is responsible for drawing the game board, pawns,
    UI elements, and providing visual feedback for game state,
    selected pawns, and valid moves.
    """
    
    # Display settings
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    # Board settings
    BOARD_SIZE = 400
    GRID_LINES = 7
    
    # Colors
    BACKGROUND_COLOR = (240, 240, 240)  # Light gray
    GRID_COLOR = (64, 64, 64)           # Dark gray
    HIGHLIGHT_COLOR = (255, 255, 0)     # Yellow
    VALID_MOVE_COLOR = (0, 255, 0)      # Green
    TEXT_COLOR = (0, 0, 0)              # Black
    PLAYER1_COLOR = (0, 102, 204)       # Blue
    PLAYER2_COLOR = (204, 0, 0)         # Red
    PLAYER1_HIGHLIGHT = (173, 216, 230) # Light blue
    PLAYER2_HIGHLIGHT = (255, 182, 193) # Light pink
    ERROR_COLOR = (255, 0, 0)           # Red for error messages
    NOTIFICATION_COLOR = (50, 50, 50)   # Dark gray for notifications
    TURN_INDICATOR_BG = (220, 220, 220) # Light gray for turn indicator background
    
    # UI settings
    PAWN_RADIUS = 15
    HIGHLIGHT_RADIUS = 18
    VALID_MOVE_RADIUS = 10
    STARTING_POS_RADIUS = 12
    PULSING_HIGHLIGHT_MAX = 22          # Maximum radius for pulsing highlight effect
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize the renderer.
        
        Args:
            screen: The pygame surface to draw on
        """
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
        self.large_font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 24)
        
        # Calculate board dimensions and position
        self.board_x = (self.WINDOW_WIDTH - self.BOARD_SIZE) // 2
        self.board_y = (self.WINDOW_HEIGHT - self.BOARD_SIZE) // 2
        self.cell_size = self.BOARD_SIZE // (self.GRID_LINES - 1)
        
        # UI state variables
        self.error_message = None
        self.error_time = 0
        self.notification_message = None
        self.notification_time = 0
        self.pulse_time = 0  # For pulsing effects
    
    def draw_board(self, board):
        """
        Draw the game board with grid lines.
        
        Args:
            board: The game board object
        """
        # Draw grid lines
        for i in range(self.GRID_LINES):
            # Calculate position for this grid line
            x = self.board_x + i * self.cell_size
            y = self.board_y + i * self.cell_size
            
            # Draw horizontal line
            pygame.draw.line(
                self.screen, 
                self.GRID_COLOR, 
                (self.board_x, y), 
                (self.board_x + self.BOARD_SIZE, y), 
                2
            )
            
            # Draw vertical line
            pygame.draw.line(
                self.screen, 
                self.GRID_COLOR, 
                (x, self.board_y), 
                (x, self.board_y + self.BOARD_SIZE), 
                2
            )
        
        # Draw spawn points (circles) at the bottom and right
        for i in range(1, 6):
            # Bottom spawn points for Player 1
            pygame.draw.circle(
                self.screen,
                self.PLAYER1_COLOR,
                (self.board_x + i * self.cell_size, self.board_y + 6 * self.cell_size),
                8,
                2
            )
            
            # Right spawn points for Player 2
            pygame.draw.circle(
                self.screen,
                self.PLAYER2_COLOR,
                (self.board_x + 6 * self.cell_size, self.board_y + i * self.cell_size),
                8,
                2
            )
        
        # Draw exit points (arrow heads) at the top and left
        arrow_size = 8
        for i in range(1, 6):
            # Top exit points for Player 1
            # Draw arrow head pointing up
            pygame.draw.polygon(
                self.screen,
                self.PLAYER1_COLOR,
                [
                    (self.board_x + i * self.cell_size, self.board_y - arrow_size),
                    (self.board_x + i * self.cell_size - arrow_size, self.board_y),
                    (self.board_x + i * self.cell_size + arrow_size, self.board_y)
                ],
                2
            )
            
            # Left exit points for Player 2
            # Draw arrow head pointing left
            pygame.draw.polygon(
                self.screen,
                self.PLAYER2_COLOR,
                [
                    (self.board_x - arrow_size, self.board_y + i * self.cell_size),
                    (self.board_x, self.board_y + i * self.cell_size - arrow_size),
                    (self.board_x, self.board_y + i * self.cell_size + arrow_size)
                ],
                2
            )
    
    def draw_pawns(self, players: List):
        """
        Draw all pawns on the board.
        
        Args:
            players: List of player objects
        """
        for player in players:
            # Draw pawns that are on the board
            for pawn in player.get_pawns_on_board():
                position = pawn.get_position()
                if position:
                    x, y = position
                    screen_x = self.board_x + x * self.cell_size
                    screen_y = self.board_y + y * self.cell_size
                    
                    # Check if the pawn is at an escape position
                    is_at_escape = False
                    if (player.player_id == 1 and y == 0 and 1 <= x <= 5) or \
                       (player.player_id == 2 and x == 0 and 1 <= y <= 5):
                        is_at_escape = True
                    
                    # Draw the pawn
                    pygame.draw.circle(
                        self.screen,
                        player.color,
                        (screen_x, screen_y),
                        self.PAWN_RADIUS
                    )
                    
                    # If the pawn is at an escape position, draw a highlight around it
                    if is_at_escape:
                        # Draw a pulsing glow effect
                        pulse_factor = (pygame.time.get_ticks() % 1000) / 1000  # 0 to 1 over 1 second
                        pulse_radius = self.PAWN_RADIUS + 3 * abs(pulse_factor - 0.5)  # Pulse between sizes
                        
                        pygame.draw.circle(
                            self.screen,
                            (255, 255, 0),  # Yellow highlight
                            (screen_x, screen_y),
                            pulse_radius,
                            2
                        )
    
    def highlight_selected_pawn(self, pawn):
        """
        Draw a highlight around the selected pawn.
        
        Args:
            pawn: The selected pawn
        """
        if pawn and pawn.is_on_board():
            # Use the enhanced pawn highlight effect
            self.draw_enhanced_pawn_highlight(pawn)
    
    def highlight_valid_moves(self, valid_moves: List[Tuple[int, int]]):
        """
        Highlight all valid move destinations.
        
        Args:
            valid_moves: List of (x, y) coordinates representing valid moves
        """
        # Use the enhanced valid moves visualization
        self.draw_enhanced_valid_moves(valid_moves)
    
    def draw_ui(self, game_state):
        """
        Draw UI elements based on the current game state.
        
        Args:
            game_state: The current game state
        """
        # Draw current phase with enhanced styling
        phase_text = ""
        if game_state.is_setup_phase():
            phase_text = "Setup Phase"
        elif game_state.is_movement_phase():
            phase_text = "Movement Phase"
        elif game_state.is_game_over():
            winner = game_state.get_winner()
            if winner:
                phase_text = f"Game Over - Player {winner.player_id} Wins!"
            elif game_state.stalemate:
                phase_text = "Game Over - Stalemate"
            else:
                phase_text = "Game Over"
        
        # Draw phase text with a background
        phase_surface = self.font.render(phase_text, True, self.TEXT_COLOR)
        phase_bg = pygame.Surface((phase_surface.get_width() + 20, phase_surface.get_height() + 10))
        phase_bg.fill(self.TURN_INDICATOR_BG)
        self.screen.blit(phase_bg, (15, 15))
        self.screen.blit(phase_surface, (25, 20))
        
        # Draw enhanced turn indicator
        self.draw_enhanced_turn_indicator(game_state)
        
        # Draw escaped pawns counter (only in movement phase)
        if game_state.is_movement_phase() or game_state.is_game_over():
            self.draw_escaped_pawns_counter(game_state)
        
        # Draw selected pawn indicator if a pawn is selected
        if game_state.selected_pawn:
            self.highlight_selected_pawn(game_state.selected_pawn)
            
            # Draw valid moves for the selected pawn
            valid_moves = game_state.selected_pawn.get_valid_moves(game_state.board)
            self.highlight_valid_moves(valid_moves)
        
        # Draw setup phase information if in setup
        if game_state.is_setup_phase():
            current_player = game_state.get_current_player()
            unplaced_pawns = len(current_player.get_unplaced_pawns())
            total_pawns = 7  # Each player has 7 pawns
            placed_pawns = total_pawns - unplaced_pawns
            
            # Draw pawn counter
            setup_text = f"Player {current_player.player_id}: {placed_pawns}/{total_pawns} pawns placed"
            setup_surface = self.font.render(setup_text, True, current_player.color)
            self.screen.blit(setup_surface, (20, 80))
            
            # Show instructions for setup phase with enhanced styling
            instruction_bg = pygame.Surface((400, 30))
            instruction_bg.fill(self.TURN_INDICATOR_BG)
            instruction_bg.set_alpha(180)
            self.screen.blit(instruction_bg, (20, 110))
            
            instruction_text = "Click on your starting row to place pawns"
            instruction_surface = self.font.render(instruction_text, True, self.TEXT_COLOR)
            self.screen.blit(instruction_surface, (25, 115))
            
            # Show progress for both players
            self.draw_setup_progress(game_state)
            
            # Highlight valid starting positions
            self.highlight_valid_starting_positions(game_state)
        
        # Draw turn skipped notification if applicable
        if game_state.is_movement_phase() and game_state.turn_skipped:
            self.draw_turn_skipped_notification(game_state.skipped_player_id)
        
        # Draw any active error messages or notifications
        self.draw_error_and_notifications()
    
    def draw_game_over(self, game_state):
        """
        Draw game over screen with winner announcement or stalemate.
        
        Args:
            game_state: The current game state
        """
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Create a game over panel
        panel_width = 400
        panel_height = 200
        panel_x = (self.WINDOW_WIDTH - panel_width) // 2
        panel_y = (self.WINDOW_HEIGHT - panel_height) // 2
        
        # Draw panel background
        pygame.draw.rect(
            self.screen,
            (240, 240, 240),  # Light gray
            (panel_x, panel_y, panel_width, panel_height),
            border_radius=15
        )
        
        # Draw panel border
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),  # Dark gray
            (panel_x, panel_y, panel_width, panel_height),
            width=3,
            border_radius=15
        )
        
        # Draw game over title
        title_text = "Game Over"
        title_surface = self.large_font.render(title_text, True, self.TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.WINDOW_WIDTH // 2, panel_y + 40))
        self.screen.blit(title_surface, title_rect)
        
        winner = game_state.get_winner()
        if winner:
            # Draw winner announcement
            text = f"Player {winner.player_id} Wins!"
            text_surface = self.large_font.render(text, True, winner.color)
            text_rect = text_surface.get_rect(center=(self.WINDOW_WIDTH // 2, panel_y + 90))
            self.screen.blit(text_surface, text_rect)
            
            # Draw stats
            stats_text = f"Escaped {len(winner.get_escaped_pawns())}/7 pawns"
            stats_surface = self.font.render(stats_text, True, self.TEXT_COLOR)
            stats_rect = stats_surface.get_rect(center=(self.WINDOW_WIDTH // 2, panel_y + 130))
            self.screen.blit(stats_surface, stats_rect)
        elif game_state.stalemate:
            # Draw stalemate announcement
            text = "Stalemate - No player can move!"
            text_surface = self.font.render(text, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(self.WINDOW_WIDTH // 2, panel_y + 90))
            self.screen.blit(text_surface, text_rect)
            
            # Draw explanation
            explanation = "Both players are blocked"
            explanation_surface = self.font.render(explanation, True, self.TEXT_COLOR)
            explanation_rect = explanation_surface.get_rect(center=(self.WINDOW_WIDTH // 2, panel_y + 130))
            self.screen.blit(explanation_surface, explanation_rect)
        
        # Draw restart instructions
        restart_text = "Press R to play again"
        restart_surface = self.font.render(restart_text, True, self.TEXT_COLOR)
        restart_rect = restart_surface.get_rect(center=(self.WINDOW_WIDTH // 2, panel_y + 170))
        self.screen.blit(restart_surface, restart_rect)
    
    def highlight_valid_starting_positions(self, game_state):
        """
        Highlight valid starting positions for the current player during setup phase.
        
        Args:
            game_state: The current game state
        """
        if not game_state.is_setup_phase():
            return
            
        current_player = game_state.get_current_player()
        valid_positions = game_state.board.get_all_starting_positions(current_player)
        
        # Filter out positions that are already occupied
        valid_positions = [pos for pos in valid_positions 
                          if game_state.board.is_intersection_empty(pos[0], pos[1])]
        
        # Use a different color for starting positions - light blue for player 1, light red for player 2
        if current_player.player_id == 1:
            highlight_color = self.PLAYER1_HIGHLIGHT
        else:
            highlight_color = self.PLAYER2_HIGHLIGHT
            
        # Draw highlights for valid starting positions
        for x, y in valid_positions:
            screen_x = self.board_x + x * self.cell_size
            screen_y = self.board_y + y * self.cell_size
            
            # Draw a filled circle with some transparency
            s = pygame.Surface((self.STARTING_POS_RADIUS * 2, self.STARTING_POS_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                s,
                highlight_color + (150,),  # Add alpha value for transparency
                (self.STARTING_POS_RADIUS, self.STARTING_POS_RADIUS),
                self.STARTING_POS_RADIUS
            )
            self.screen.blit(s, (screen_x - self.STARTING_POS_RADIUS, screen_y - self.STARTING_POS_RADIUS))
        
        # Highlight the entire starting row with a subtle glow
        self.highlight_starting_row(game_state)
    
    def draw_setup_progress(self, game_state):
        """
        Draw a visual representation of setup progress for both players.
        
        Args:
            game_state: The current game state
        """
        # Position for the progress bars
        progress_x = 20
        progress_y = 140
        bar_width = 200
        bar_height = 20
        spacing = 30
        
        # Draw progress for player 1
        player1 = game_state.players[0]
        unplaced_pawns1 = len(player1.get_unplaced_pawns())
        placed_pawns1 = 7 - unplaced_pawns1
        
        # Draw player 1 label
        player1_text = f"Player 1:"
        player1_surface = self.font.render(player1_text, True, player1.color)
        self.screen.blit(player1_surface, (progress_x, progress_y))
        
        # Draw player 1 progress bar background
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),  # Light gray background
            (progress_x + 100, progress_y, bar_width, bar_height)
        )
        
        # Draw player 1 progress bar fill
        if placed_pawns1 > 0:
            fill_width = int((placed_pawns1 / 7) * bar_width)
            pygame.draw.rect(
                self.screen,
                player1.color,
                (progress_x + 100, progress_y, fill_width, bar_height)
            )
        
        # Draw player 1 progress text
        progress_text1 = f"{placed_pawns1}/7"
        progress_surface1 = self.font.render(progress_text1, True, self.TEXT_COLOR)
        text_x1 = progress_x + 100 + (bar_width // 2) - (progress_surface1.get_width() // 2)
        self.screen.blit(progress_surface1, (text_x1, progress_y))
        
        # Draw progress for player 2
        player2 = game_state.players[1]
        unplaced_pawns2 = len(player2.get_unplaced_pawns())
        placed_pawns2 = 7 - unplaced_pawns2
        
        # Draw player 2 label
        player2_text = f"Player 2:"
        player2_surface = self.font.render(player2_text, True, player2.color)
        self.screen.blit(player2_surface, (progress_x, progress_y + spacing))
        
        # Draw player 2 progress bar background
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),  # Light gray background
            (progress_x + 100, progress_y + spacing, bar_width, bar_height)
        )
        
        # Draw player 2 progress bar fill
        if placed_pawns2 > 0:
            fill_width = int((placed_pawns2 / 7) * bar_width)
            pygame.draw.rect(
                self.screen,
                player2.color,
                (progress_x + 100, progress_y + spacing, fill_width, bar_height)
            )
        
        # Draw player 2 progress text
        progress_text2 = f"{placed_pawns2}/7"
        progress_surface2 = self.font.render(progress_text2, True, self.TEXT_COLOR)
        text_x2 = progress_x + 100 + (bar_width // 2) - (progress_surface2.get_width() // 2)
        self.screen.blit(progress_surface2, (text_x2, progress_y + spacing))
    
    def highlight_starting_row(self, game_state):
        """
        Highlight the starting row for the current player during setup phase.
        
        Args:
            game_state: The current game state
        """
        if not game_state.is_setup_phase():
            return
            
        current_player = game_state.get_current_player()
        
        # Determine which row to highlight based on player
        row_y = 4 if current_player.player_id == 1 else 0  # Bottom row for player 1, top row for player 2
        
        # Use a different color for each player
        if current_player.player_id == 1:
            highlight_color = self.PLAYER1_HIGHLIGHT
        else:
            highlight_color = self.PLAYER2_HIGHLIGHT
            
        # Create a semi-transparent surface for the row highlight
        row_width = self.BOARD_SIZE
        row_height = self.cell_size // 2
        
        # Calculate the position of the row
        row_x = self.board_x
        row_screen_y = self.board_y + row_y * self.cell_size - row_height // 2
        
        # Create a semi-transparent surface
        s = pygame.Surface((row_width, row_height), pygame.SRCALPHA)
        s.fill(highlight_color + (50,))  # Very transparent
        
        # Draw the highlight
        self.screen.blit(s, (row_x, row_screen_y))
    
    def pixel_to_grid_position(self, pixel_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Convert pixel coordinates to grid position.
        
        Args:
            pixel_pos: (x, y) tuple of pixel coordinates
            
        Returns:
            (grid_x, grid_y) tuple or None if outside the grid
        """
        x, y = pixel_pos
        
        # Check if click is within board bounds
        if (x < self.board_x - self.PAWN_RADIUS or 
            x > self.board_x + self.BOARD_SIZE + self.PAWN_RADIUS or
            y < self.board_y - self.PAWN_RADIUS or
            y > self.board_y + self.BOARD_SIZE + self.PAWN_RADIUS):
            return None
        
        # Calculate grid position
        grid_x = round((x - self.board_x) / self.cell_size)
        grid_y = round((y - self.board_y) / self.cell_size)
        
        # Check if position is valid (0-6)
        if 0 <= grid_x < 7 and 0 <= grid_y < 7:
            return (grid_x, grid_y)
        
        return None
    
    def grid_to_pixel_position(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """
        Convert grid coordinates to pixel coordinates.
        
        Args:
            grid_x: Grid X-coordinate (0-4)
            grid_y: Grid Y-coordinate (0-4)
            
        Returns:
            (pixel_x, pixel_y) tuple of pixel coordinates
        """
        pixel_x = self.board_x + grid_x * self.cell_size
        pixel_y = self.board_y + grid_y * self.cell_size
        return (pixel_x, pixel_y)
        
    def show_error_message(self, message: str) -> None:
        """
        Display an error message that will fade after a few seconds.
        
        Args:
            message: The error message to display
        """
        self.error_message = message
        self.error_time = time.time()
    
    def show_notification(self, message: str) -> None:
        """
        Display a notification message that will fade after a few seconds.
        
        Args:
            message: The notification message to display
        """
        self.notification_message = message
        self.notification_time = time.time()
    
    def draw_error_and_notifications(self) -> None:
        """
        Draw any active error messages or notifications.
        """
        current_time = time.time()
        
        # Draw error message if active
        if self.error_message:
            # Error messages last for 3 seconds
            if current_time - self.error_time < 3:
                # Calculate alpha based on time remaining (fade out)
                alpha = min(255, int(255 * (3 - (current_time - self.error_time)) / 1.5))
                
                # Create text surface
                error_surface = self.font.render(self.error_message, True, self.ERROR_COLOR)
                
                # Create background with alpha
                bg_surface = pygame.Surface((error_surface.get_width() + 20, error_surface.get_height() + 10), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, alpha // 2))  # Semi-transparent black background
                
                # Position at bottom of screen
                x = (self.WINDOW_WIDTH - bg_surface.get_width()) // 2
                y = self.WINDOW_HEIGHT - bg_surface.get_height() - 20
                
                # Draw background and text
                self.screen.blit(bg_surface, (x, y))
                
                # Apply alpha to text surface
                error_surface.set_alpha(alpha)
                self.screen.blit(error_surface, (x + 10, y + 5))
            else:
                # Clear error message after time expires
                self.error_message = None
        
        # Draw notification if active
        if self.notification_message:
            # Notifications last for 2 seconds
            if current_time - self.notification_time < 2:
                # Calculate alpha based on time remaining (fade out)
                alpha = min(255, int(255 * (2 - (current_time - self.notification_time)) / 1))
                
                # Create text surface
                notification_surface = self.font.render(self.notification_message, True, self.NOTIFICATION_COLOR)
                
                # Position at top center of screen
                x = (self.WINDOW_WIDTH - notification_surface.get_width()) // 2
                y = 80
                
                # Apply alpha to text surface
                notification_surface.set_alpha(alpha)
                self.screen.blit(notification_surface, (x, y))
            else:
                # Clear notification after time expires
                self.notification_message = None
    
    def draw_enhanced_turn_indicator(self, game_state) -> None:
        """
        Draw an enhanced turn indicator showing the current player.
        
        Args:
            game_state: The current game state
        """
        if game_state.is_game_over():
            return
            
        current_player = game_state.get_current_player()
        
        # Create a rounded rectangle for the turn indicator
        indicator_width = 200
        indicator_height = 60
        x = self.WINDOW_WIDTH - indicator_width - 20
        y = 20
        
        # Draw background
        pygame.draw.rect(
            self.screen,
            self.TURN_INDICATOR_BG,
            (x, y, indicator_width, indicator_height),
            border_radius=10
        )
        
        # Draw colored border based on current player
        pygame.draw.rect(
            self.screen,
            current_player.color,
            (x, y, indicator_width, indicator_height),
            width=3,
            border_radius=10
        )
        
        # Draw "Current Turn" text
        turn_text = "Current Turn"
        turn_surface = self.small_font.render(turn_text, True, self.TEXT_COLOR)
        self.screen.blit(turn_surface, (x + 10, y + 5))
        
        # Draw player text
        player_text = f"Player {current_player.player_id}"
        player_surface = self.large_font.render(player_text, True, current_player.color)
        self.screen.blit(player_surface, (x + 10, y + 25))
    
    def draw_enhanced_pawn_highlight(self, pawn) -> None:
        """
        Draw an enhanced highlight effect for the selected pawn.
        
        Args:
            pawn: The selected pawn
        """
        if not pawn or not pawn.is_on_board():
            return
            
        position = pawn.get_position()
        if not position:
            return
            
        x, y = position
        screen_x = self.board_x + x * self.cell_size
        screen_y = self.board_y + y * self.cell_size
        
        # Create pulsing effect
        pulse_factor = (pygame.time.get_ticks() % 1000) / 1000  # 0 to 1 over 1 second
        pulse_radius = self.HIGHLIGHT_RADIUS + 2 * abs(pulse_factor - 0.5)  # Pulse between sizes
        
        # Draw outer glow (semi-transparent)
        glow_surface = pygame.Surface((int(pulse_radius * 2.5), int(pulse_radius * 2.5)), pygame.SRCALPHA)
        for i in range(3):
            size = int(pulse_radius * (1 + i * 0.2))
            alpha = 100 - i * 30
            pygame.draw.circle(
                glow_surface,
                self.HIGHLIGHT_COLOR + (alpha,),
                (int(pulse_radius * 1.25), int(pulse_radius * 1.25)),
                size,
                2
            )
        
        # Position and draw the glow
        glow_x = screen_x - int(pulse_radius * 1.25)
        glow_y = screen_y - int(pulse_radius * 1.25)
        self.screen.blit(glow_surface, (glow_x, glow_y))
        
        # Draw solid highlight circle
        pygame.draw.circle(
            self.screen,
            self.HIGHLIGHT_COLOR,
            (screen_x, screen_y),
            self.HIGHLIGHT_RADIUS,
            2
        )
    
    def draw_enhanced_valid_moves(self, valid_moves: List[Tuple[int, int]]) -> None:
        """
        Draw enhanced visual indicators for valid move destinations.
        
        Args:
            valid_moves: List of (x, y) coordinates representing valid moves
        """
        pulse_factor = (pygame.time.get_ticks() % 1500) / 1500  # 0 to 1 over 1.5 seconds
        
        for x, y in valid_moves:
            screen_x = self.board_x + x * self.cell_size
            screen_y = self.board_y + y * self.cell_size
            
            # Create a pulsing effect for valid moves
            pulse_size = self.VALID_MOVE_RADIUS + pulse_factor * 3
            
            # Draw filled circle with transparency
            s = pygame.Surface((int(pulse_size * 2), int(pulse_size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(
                s,
                self.VALID_MOVE_COLOR + (100,),  # Semi-transparent green
                (int(pulse_size), int(pulse_size)),
                int(pulse_size)
            )
            self.screen.blit(s, (screen_x - int(pulse_size), screen_y - int(pulse_size)))
            
            # Draw outline
            pygame.draw.circle(
                self.screen,
                self.VALID_MOVE_COLOR,
                (screen_x, screen_y),
                self.VALID_MOVE_RADIUS,
                2
            )
    
    def draw_escaped_pawns_counter(self, game_state) -> None:
        """
        Draw counters showing how many pawns each player has escaped.
        
        Args:
            game_state: The current game state
        """
        # Position for the counters
        counter_x = self.WINDOW_WIDTH - 220
        counter_y = 100
        spacing = 30
        
        # Draw header
        header_text = "Escaped Pawns"
        header_surface = self.font.render(header_text, True, self.TEXT_COLOR)
        self.screen.blit(header_surface, (counter_x, counter_y))
        
        # Draw player 1 escaped pawns
        player1 = game_state.players[0]
        escaped_pawns1 = len(player1.get_escaped_pawns())
        player1_text = f"Player 1: {escaped_pawns1}/7"
        player1_surface = self.font.render(player1_text, True, player1.color)
        self.screen.blit(player1_surface, (counter_x, counter_y + spacing))
        
        # Draw player 2 escaped pawns
        player2 = game_state.players[1]
        escaped_pawns2 = len(player2.get_escaped_pawns())
        player2_text = f"Player 2: {escaped_pawns2}/7"
        player2_surface = self.font.render(player2_text, True, player2.color)
        self.screen.blit(player2_surface, (counter_x, counter_y + spacing * 2))
    
    def draw_turn_skipped_notification(self, skipped_player_id: int) -> None:
        """
        Draw a notification when a player's turn is skipped due to no valid moves.
        
        Args:
            skipped_player_id: The ID of the player whose turn was skipped
        """
        if not skipped_player_id:
            return
            
        # Create a notification panel
        panel_width = 300
        panel_height = 60
        panel_x = (self.WINDOW_WIDTH - panel_width) // 2
        panel_y = self.WINDOW_HEIGHT - panel_height - 40
        
        # Get player color based on ID
        player_color = self.PLAYER1_COLOR if skipped_player_id == 1 else self.PLAYER2_COLOR
        
        # Draw panel with semi-transparency
        s = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        s.fill((50, 50, 50, 180))  # Semi-transparent dark background
        self.screen.blit(s, (panel_x, panel_y))
        
        # Draw border with player color
        pygame.draw.rect(
            self.screen,
            player_color,
            (panel_x, panel_y, panel_width, panel_height),
            width=2,
            border_radius=5
        )
        
        # Draw skip notification text
        skip_text = f"Player {skipped_player_id}'s turn skipped"
        skip_surface = self.font.render(skip_text, True, (255, 255, 255))
        skip_rect = skip_surface.get_rect(center=(panel_x + panel_width // 2, panel_y + 20))
        self.screen.blit(skip_surface, skip_rect)
        
        # Draw reason text
        reason_text = "No valid moves available"
        reason_surface = self.small_font.render(reason_text, True, (200, 200, 200))
        reason_rect = reason_surface.get_rect(center=(panel_x + panel_width // 2, panel_y + 40))
        self.screen.blit(reason_surface, reason_rect)