"""
Main game loop with rendering, input handling, and game logic all mixed together.
Poor design: Everything in one place, tight coupling to Pygame.
"""
import pygame
import sys
import time
from snake_data import snake_positions, direction, speed
from food_manager import check_collision, place_food, food_position, check_wall_collision
from display_config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, COLORS,
    calculate_score, save_high_score, get_high_scores
)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def game_loop():
    """Main game loop - does everything!"""
    global direction  # Bad: modifying global state
    
    # Import globals to modify them
    import snake_data
    import food_manager
    
    # Initialize
    snake_data.snake_positions = [(100, 100), (90, 100), (80, 100)]
    snake_data.direction = 'RIGHT'
    food_manager.food_position = place_food()
    
    game_over = False
    start_time = time.time()
    score = 0
    
    while not game_over:
        # Event handling mixed with game logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Input handling directly modifying global direction
                if event.key == pygame.K_UP and snake_data.direction != 'DOWN':
                    snake_data.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake_data.direction != 'UP':
                    snake_data.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_data.direction != 'RIGHT':
                    snake_data.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_data.direction != 'LEFT':
                    snake_data.direction = 'RIGHT'
        
        # Move snake - directly manipulating the list
        head = snake_data.snake_positions[0]
        
        if snake_data.direction == 'UP':
            new_head = (head[0], head[1] - CELL_SIZE)
        elif snake_data.direction == 'DOWN':
            new_head = (head[0], head[1] + CELL_SIZE)
        elif snake_data.direction == 'LEFT':
            new_head = (head[0] - CELL_SIZE, head[1])
        elif snake_data.direction == 'RIGHT':
            new_head = (head[0] + CELL_SIZE, head[1])
        
        # Insert new head
        snake_data.snake_positions.insert(0, new_head)
        
        # Check food collision - has side effects!
        if check_collision(snake_data.snake_positions[0], food_manager.food_position):
            score += 10  # Scoring logic scattered here too!
            food_manager.food_position = place_food()
            # Note: check_collision already grew the snake (side effect!)
        else:
            # Remove tail if no food eaten
            snake_data.snake_positions.pop()
        
        # Check wall collision
        if check_wall_collision(snake_data.snake_positions[0]):
            game_over = True
        
        # Check self collision - logic directly in main loop
        head = snake_data.snake_positions[0]
        if head in snake_data.snake_positions[1:]:
            game_over = True
        
        # Rendering mixed with game logic
        screen.fill(COLORS['background'])
        
        # Draw snake - directly accessing internal structure
        for i, segment in enumerate(snake_data.snake_positions):
            color = COLORS['snake_head'] if i == 0 else COLORS['snake_body']
            pygame.draw.rect(screen, color,
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            # Draw border for segments
            pygame.draw.rect(screen, COLORS['snake_border'],
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)
        
        # Draw food
        pygame.draw.rect(screen, COLORS['food'],
                        (food_manager.food_position[0], 
                         food_manager.food_position[1], 
                         CELL_SIZE, CELL_SIZE))
        
        # Draw score - mixing rendering with game state
        elapsed_time = int(time.time() - start_time)
        final_score = calculate_score(len(snake_data.snake_positions), elapsed_time)
        score_text = font.render(f'Score: {final_score}', True, COLORS['text'])
        screen.blit(score_text, (10, 10))
        
        # Draw length
        length_text = small_font.render(f'Length: {len(snake_data.snake_positions)}', 
                                       True, COLORS['text'])
        screen.blit(length_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(snake_data.speed)
    
    # Game over - save score directly here
    final_score = calculate_score(len(snake_data.snake_positions), elapsed_time)
    save_high_score(final_score)
    show_game_over_screen(final_score)

def show_game_over_screen(final_score):
    """Display game over screen - still in main.py"""
    screen.fill(COLORS['background'])
    
    # Game over text
    game_over_text = font.render('GAME OVER', True, COLORS['game_over'])
    score_text = font.render(f'Final Score: {final_score}', True, COLORS['text'])
    
    # Get and display high scores - mixing concerns
    high_scores = get_high_scores()
    high_score_title = small_font.render('High Scores:', True, COLORS['text'])
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
    screen.blit(high_score_title, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 20))
    
    # Display top 5 scores
    for i, score in enumerate(high_scores[:5]):
        score_line = small_font.render(f'{i+1}. {score}', True, COLORS['text'])
        screen.blit(score_line, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 50 + i*25))
    
    restart_text = small_font.render('Press SPACE to restart or ESC to quit', 
                                    True, COLORS['text'])
    screen.blit(restart_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT - 50))
    
    pygame.display.flip()
    
    # Wait for input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    game_loop()  # Restart
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_start_screen():
    """Start screen"""
    screen.fill(COLORS['background'])
    
    title_text = font.render('SNAKE GAME', True, COLORS['text'])
    start_text = small_font.render('Press SPACE to start', True, COLORS['text'])
    controls_text = small_font.render('Use arrow keys to move', True, COLORS['text'])
    
    screen.blit(title_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
    screen.blit(start_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 10))
    screen.blit(controls_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

if __name__ == '__main__':
    show_start_screen()
    game_loop()
