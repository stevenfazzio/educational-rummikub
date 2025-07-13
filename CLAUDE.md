# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a clean, well-structured Rummikub implementation designed to be an exemplar of readable Python code. The codebase serves as a learning resource through its clarity and organization. It implements a multiplayer game for human players taking turns at the same computer.

## Development Commands

```bash
# Run the game
python main.py

# Run tests  
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_rules

# Run with specific players
python main.py --players "Alice,Bob"

# Run without color
python main.py --no-color
```

## Architecture

The codebase follows standard software engineering practices with clear separation of concerns:

- **tiles.py**: Tile and Deck classes, tile factory methods
- **rules.py**: Rule validation functions (is_valid_group, is_valid_run, etc.)
- **game.py**: Game state management, turn logic, win conditions
- **player.py**: Simple Player class for tracking player state
- **display.py**: Console rendering, user input handling
- **main.py**: Application entry point, menu system

## Code Standards

### Style Guidelines

1. **Type Hints**: Use Python type hints for all function signatures
2. **Docstrings**: Google-style docstrings for all public methods
3. **Variable Names**: Full, descriptive names (avoid abbreviations)
4. **Constants**: Use UPPER_CASE for module-level constants
5. **Classes**: Use PascalCase for classes, snake_case for methods

### Example Code Style

```python
from typing import List, Optional, Tuple

class TileGroup:
    """Represents a group of tiles on the table."""
    
    def __init__(self, tiles: List[Tile]):
        """
        Initialize a tile group.
        
        Args:
            tiles: List of tiles forming this group
            
        Raises:
            ValueError: If tiles don't form a valid group
        """
        self.tiles = tiles
        if not self.is_valid():
            raise ValueError("Tiles do not form a valid group")
    
    def is_valid(self) -> bool:
        """Check if this group follows Rummikub rules."""
        return self._is_valid_set() or self._is_valid_run()
```

### Implementation Guidelines

1. **Separate Concerns**: Keep game logic, display, and player state separate
2. **Validate Early**: Check rule validity at the point of action
3. **Immutable Where Possible**: Prefer returning new objects over modifying
4. **Clear Error Messages**: Exceptions should explain what went wrong
5. **Testable Design**: Write code that's easy to unit test

## Testing Approach

- Unit tests for all rule validation logic
- Integration tests for game flow
- Test both valid and invalid scenarios
- Use descriptive test names that explain what's being tested

## Rummikub Rules Reference

### Valid Sets
- **Group**: 3-4 tiles, same number, different colors
- **Run**: 3+ consecutive tiles, same color

### Special Rules
- Initial meld must be 30+ points
- Jokers can replace any tile
- Players can rearrange table tiles during their turn
- Must leave all table groups valid after turn

## Game Flow

1. Players take turns at the same computer
2. Each player sees only their tiles during their turn
3. The display clears between turns for privacy
4. Players can:
   - Play new melds
   - Add to existing sets
   - Rearrange the table
   - Draw a tile

## Common Patterns

### Validation Pattern
```python
def validate_move(move: Move, game_state: GameState) -> bool:
    """Validate a move against current game state."""
    # Check preconditions
    if not move.player.has_tiles(move.tiles):
        return False
    
    # Simulate move
    new_state = game_state.apply_move(move)
    
    # Validate result
    return new_state.is_valid()
```

### Factory Pattern for Tiles
```python
def create_standard_deck() -> List[Tile]:
    """Create a standard 106-tile Rummikub deck."""
    tiles = []
    
    # Create numbered tiles (2 of each)
    for color in TILE_COLORS:
        for number in range(1, 14):
            tiles.extend([Tile(number, color), Tile(number, color)])
    
    # Add jokers
    tiles.extend([Tile(0, 'joker'), Tile(0, 'joker')])
    
    return tiles
```

## Important Notes

- This is a standard Python codebase, not a tutorial
- The game is designed for human players only (no AI)
- Comments explain implementation details, not programming concepts
- Code should be professional yet exceptionally clear
- Avoid "clever" Python idioms that might confuse beginners
- Focus on demonstrating good software design through example

## Player Management

The Player class is intentionally simple:
- Tracks player state (tiles, has_melded flag)
- No decision-making logic (humans make all decisions)
- Clear methods for tile management
- Easy to understand for beginners

## Display Considerations

- Console-based interface using ANSI colors (when supported)
- Clear screen between turns for player privacy
- Intuitive menu system
- Helpful error messages that guide players
- Visual tile representation: [5 red], [Joker], etc.