# File Reference Guide

Quick reference for what each file does and its key components.

## Core Game Files

### 📄 main.py
**Purpose**: Entry point and game coordinator

**Key Components**:
- `RummikubGame` class - Main game controller
- `run_menu()` - Shows main menu
- `run_game()` - Main game loop
- `parse_arguments()` - Handles command line options

**Important Functions**:
```python
setup_game(player_names, initial_hand_size)
show_game_results()
quick_game()
custom_game()
```

**When to Modify**:
- Adding new menu options
- Changing game setup
- Adding command line arguments

---

### 📄 tiles.py
**Purpose**: Defines tiles and deck management

**Key Components**:
- `Tile` class - Individual game piece
- `Deck` class - Collection of tiles
- Constants: `TILE_COLORS`, `JOKER_COLOR`

**Important Functions**:
```python
create_tile(number, color)
create_joker()
create_standard_deck()
```

**When to Modify**:
- Changing tile properties
- Adding new tile types
- Modifying deck composition

---

### 📄 rules.py
**Purpose**: Game rule validation

**Key Components**:
- Validation functions (all return True/False)
- No state changes - only checks

**Important Functions**:
```python
is_valid_group(tiles)      # Same number, different colors
is_valid_run(tiles)        # Consecutive numbers, same color
is_valid_set(tiles)        # Either group or run
is_initial_meld_valid(tiles)  # 30+ points check
validate_table_state(sets)  # All sets valid
```

**When to Modify**:
- Changing game rules
- Adding new validation
- Adjusting point requirements

---

### 📄 game.py
**Purpose**: Game state management

**Key Components**:
- `GameState` class - Tracks everything
- `GamePhase` enum - Game stages
- `MoveType` enum - Player actions
- `Move` dataclass - Represents player moves

**Important Functions**:
```python
start_game()
validate_move(move)
apply_move(move)
get_current_player()
next_turn()
get_game_status()
```

**When to Modify**:
- Adding new game mechanics
- Changing turn logic
- Adding game features

---

### 📄 player.py
**Purpose**: Player data management

**Key Components**:
- `Player` class - Simple data holder
- No decision logic (humans decide)

**Important Functions**:
```python
add_tile(tile)
remove_tile(tile)
has_tiles(tiles)
get_tile_count()
get_hand_value()
sort_tiles(by_color)
```

**When to Modify**:
- Adding player attributes
- Changing tile management
- Adding player statistics

---

### 📄 display.py
**Purpose**: User interface and interaction

**Key Components**:
- `Display` class - Output formatting
- `GameInterface` class - Input handling
- ANSI color codes

**Important Functions**:
```python
# Display class
clear_screen()
display_tiles(tiles)
display_table(table_sets)
display_player_hand(player)
display_winner(name, scores)

# GameInterface class  
get_menu_choice(options)
get_tile_selection(player)
get_human_move(game_state, player_id)
```

**When to Modify**:
- Changing how things look
- Adding new UI elements
- Modifying user interaction

---

## Test Files

### 📄 tests/test_tiles.py
Tests for tile and deck functionality:
- Tile creation
- Deck shuffling
- Tile validation

### 📄 tests/test_rules.py
Tests for game rules:
- Valid/invalid groups
- Valid/invalid runs
- Initial meld validation

### 📄 tests/test_game.py
Tests for game state:
- Game creation
- Move validation
- Turn management
- Win conditions

### 📄 tests/test_player.py
Tests for player functionality:
- Adding/removing tiles
- Hand management
- Player state

### 📄 tests/test_display.py
Tests for display functions:
- Color formatting
- Menu handling
- Input validation

---

## Quick Lookup Tables

### Where to Find Game Constants

| Constant | File | Location |
|----------|------|----------|
| Tile colors | tiles.py | `TILE_COLORS` |
| Min/max numbers | tiles.py | `MIN_TILE_NUMBER`, `MAX_TILE_NUMBER` |
| Initial meld value | rules.py | `MIN_INITIAL_MELD_VALUE` |
| Min set size | rules.py | `MIN_SET_SIZE` |
| Initial hand size | main.py | `initial_hand_size` parameter |

### Where to Change Game Behavior

| To Change | Modify | Function/Class |
|-----------|--------|----------------|
| Menu options | main.py | `run_menu()` |
| Valid moves | rules.py | `is_valid_*` functions |
| Turn logic | game.py | `apply_move()` |
| What players see | display.py | `show_game_state()` |
| Win conditions | game.py | `is_winning_state()` |
| Tile appearance | display.py | `format_tile()` |

### Common Patterns by File

**tiles.py patterns**:
- Factory functions (`create_*`)
- Validation in `__post_init__`
- Constants at top

**rules.py patterns**:
- Pure functions (no side effects)
- Early returns for invalid cases
- Clear boolean returns

**game.py patterns**:
- State validation before changes
- Enum for phases/types
- Move application pattern

**player.py patterns**:
- Simple data storage
- List manipulation methods
- No game logic

**display.py patterns**:
- Separation of output/input
- Color handling
- Menu loops

---

## File Dependencies

```
main.py
  ├── imports from: game, player, display
  │
game.py
  ├── imports from: tiles, rules, player
  │
display.py
  ├── imports from: tiles, game, player
  │
rules.py
  ├── imports from: tiles
  │
player.py
  ├── imports from: tiles
  │
tiles.py
  └── (no game imports - foundation layer)
```

---

## Adding New Files

If you create new files:

1. **Follow naming conventions**: lowercase with underscores
2. **Add docstring** at top explaining purpose
3. **Import properly**: Only import what you need
4. **Add tests**: Create corresponding test file
5. **Update imports**: Add to files that need it

Example new file structure:
```python
"""
statistics.py - Track game statistics and history.

This module provides functionality for recording and
analyzing game results over time.
"""

from typing import Dict, List
from datetime import datetime

class Statistics:
    """Manages game statistics."""
    pass
```

Remember: Each file should have one clear purpose!