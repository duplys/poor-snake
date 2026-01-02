"""
Display configuration mixed with game logic.
Poor design: Scoring logic in a display configuration file!
"""
import os

# Display settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20

# Colors - Pygame specific!
COLORS = {
    'background': (0, 0, 0),
    'snake_head': (0, 200, 0),
    'snake_body': (0, 255, 0),
    'snake_border': (0, 150, 0),
    'food': (255, 0, 0),
    'text': (255, 255, 255),
    'game_over': (255, 0, 0)
}

# Scoring logic - why is this here?!
def calculate_score(length, elapsed_time):
    """
    Calculate game score.
    Poor design: Scoring algorithm in display config file!
    """
    # Score based on length and survival time
    length_score = (length - 3) * 10  # Starting length is 3
    time_bonus = elapsed_time // 10
    return length_score + time_bonus

def save_high_score(score):
    """
    Save high score to file.
    Poor design: File I/O in display config! No error handling!
    """
    # Direct file manipulation - no abstraction
    with open('highscore.txt', 'a') as f:
        f.write(f'{score}\n')

def get_high_scores():
    """
    Read high scores from file.
    Poor design: File I/O in display config! No error handling!
    """
    if not os.path.exists('highscore.txt'):
        return []
    
    with open('highscore.txt', 'r') as f:
        scores = [int(line.strip()) for line in f if line.strip()]
    
    # Sort descending
    scores.sort(reverse=True)
    return scores
```

## `highscore.txt`
```
# This file will be created automatically by the game
# Each line contains one score
