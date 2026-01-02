"""
Snake data as global variables - anyone can access and modify!
Poor design: No encapsulation, exposed internal structure.
"""

# Global variables - exposed to everyone!
snake_positions = [(100, 100), (90, 100), (80, 100)]  # List of (x, y) tuples
direction = 'RIGHT'  # Current direction
speed = 10  # Game speed (FPS)

# Anyone can do this from anywhere:
# snake_data.snake_positions.append((110, 100))
# snake_data.direction = 'UP'
# No validation, no control!
