"""
Food management with collision detection.
Poor design: Mixed responsibilities, side effects, direct data manipulation.
"""
import random
from display_config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE
import snake_data  # Direct access to global state

# Global food position - exposed!
food_position = (200, 200)

def place_food():
    """
    Place food at random position.
    Poor design: Hardcoded knowledge of screen dimensions via imports.
    """
    # Direct knowledge of screen layout
    max_x = (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE
    max_y = (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE
    
    x = random.randint(0, max_x) * CELL_SIZE
    y = random.randint(0, max_y) * CELL_SIZE
    
    # Should check if food spawns on snake, but doesn't!
    return (x, y)

def check_collision(head_pos, food_pos):
    """
    Check collision between snake head and food.
    Poor design: Has side effect of growing snake! Mixing collision detection
    with game logic modification.
    """
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        # SIDE EFFECT: Modifies snake directly!
        # This is terrible - a "check" function shouldn't modify state
        tail = snake_data.snake_positions[-1]
        snake_data.snake_positions.append(tail)
        return True
    return False

def check_wall_collision(head_pos):
    """
    Check if snake hit a wall.
    Poor design: Direct knowledge of screen dimensions.
    """
    x, y = head_pos
    
    # Hardcoded screen boundaries
    if x < 0 or x >= SCREEN_WIDTH:
        return True
    if y < 0 or y >= SCREEN_HEIGHT:
        return True
    
    return False
