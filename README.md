# Educational Rummikub

A clean, well-structured implementation of Rummikub designed to be easily understood by beginners learning Python.

## Overview

This repository contains a complete Rummikub game implementation written in clear, readable Python. The codebase is structured to demonstrate good software engineering practices while remaining accessible to those new to programming.

## Project Structure

```
educational-rummikub/
├── tiles.py          # Tile representation and deck management
├── rules.py          # Game rule validation
├── game.py           # Core game logic and state management
├── player.py         # Player class for tracking player state
├── display.py        # Console UI and rendering
├── main.py           # Entry point and game loop
└── tests/            # Unit tests for all modules
```

## Design Principles

1. **Clear Code Architecture** - Modular design with single responsibility per file
2. **Descriptive Naming** - Self-documenting variable and function names
3. **Comprehensive Comments** - Every non-trivial function is well-documented
4. **Standard Python** - Uses only built-in libraries, no external dependencies
5. **Type Hints** - Modern Python with type annotations for clarity

## Getting Started

```bash
# Run the game
python main.py

# Run tests
python -m unittest discover tests/

# Start game with specific players
python main.py --players "Alice,Bob,Charlie"
```

## Code Example

The codebase emphasizes clarity. Here's an example from `tiles.py`:

```python
class Tile:
    """Represents a single Rummikub tile."""
    
    def __init__(self, number: int, color: str):
        """
        Create a new tile.
        
        Args:
            number: The tile's number (1-13) or 0 for joker
            color: One of 'red', 'blue', 'black', 'orange', or 'joker'
        """
        self.number = number
        self.color = color
    
    def __str__(self) -> str:
        """Display tile in readable format: [5 red] or [Joker]"""
        if self.is_joker():
            return "[Joker]"
        return f"[{self.number} {self.color}]"
    
    def is_joker(self) -> bool:
        """Check if this tile is a joker."""
        return self.color == 'joker'
```

## Game Rules

The implementation follows standard Rummikub rules:

- **Sets**: Groups of 3-4 tiles with same number, different colors OR runs of 3+ consecutive numbers in same color
- **Initial Meld**: First play must total 30+ points
- **Jokers**: Can substitute any tile, worth the value of replaced tile
- **Winning**: First player to play all tiles wins

## Playing the Game

The game supports 2-4 human players taking turns at the same computer. The interface is designed to be clear and intuitive:

1. Each player sees their tiles when it's their turn
2. The table shows all played sets
3. Players can play new melds, add to existing sets, or draw
4. The game validates all moves according to Rummikub rules

## Learning from this Codebase

This codebase demonstrates:

- Object-oriented design with classes for game entities
- Separation of concerns (display logic separate from game logic)
- Validation patterns for complex game rules
- State management in turn-based games
- Clean console interface design

## Contributing

When contributing, please maintain:
- Clear, descriptive variable names
- Comprehensive docstrings for all public methods
- Unit tests for new functionality
- Consistent code style (PEP 8)

## License

MIT License - see LICENSE file for details