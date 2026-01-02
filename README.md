# Poor Snake

## Description
This project contains a poorly designed Snake game implementation in Python which can be used for refactoring exercises.

## Installing Dependencies

```shell
pip install pygame
```

## Running the game

```shell
python main.py
```

## Problems demonstrated

While the code works, it demonstrates a number of poor design patterns:

1. `main.py`: 200+ lines mixing rendering, input, game logic, and UI
2. `snake_data.py`: Exposed global variables anyone can modify
3. `food_manager.py`:
    - `check_collision()` has side effects (grows snake)
    - Direct manipulation of global `snake_data`
    - Hardcoded knowledge of screen dimensions
4. `display_config.py`:
    - Scoring logic in display configuration
    - File I/O for high scores in wrong place
    - Pygame-specific color format
5. Tight coupling: Every module knows about implementation details of others
6. No interfaces: Direct access to internal structures everywhere
7. Mixed concerns: Logic scattered across inappropriate files
