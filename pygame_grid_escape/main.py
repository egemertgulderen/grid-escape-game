#!/usr/bin/env python3
"""
Main entry point for the Grid Escape game.
"""
import pygame
import sys
from game_logic.game_state import GameState
from rendering.renderer import Renderer
from input.input_handler import InputHandler

def main():
    """Main function to initialize and run the game."""
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Grid Escape")
    
    # Initialize game components
    game_state = GameState()
    renderer = Renderer(screen)
    input_handler = InputHandler(renderer)
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    input_handler.handle_click(event.pos, game_state, renderer)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # R key for restart
                    game_state.reset_game()
                    renderer.show_notification("Game restarted")
                    
                # Add keyboard shortcuts for other game actions
                elif event.key == pygame.K_ESCAPE:  # ESC key to deselect pawn
                    if game_state.selected_pawn:
                        game_state.selected_pawn = None
                        renderer.show_notification("Pawn deselected")
        
        # Render the game
        screen.fill((240, 240, 240))  # Light gray background
        renderer.draw_board(game_state.board)
        renderer.draw_pawns(game_state.players)
        renderer.draw_ui(game_state)
        
        # Draw game over screen if game is over
        if game_state.is_game_over():
            renderer.draw_game_over(game_state)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()