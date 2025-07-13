# Educational Rummikub

A clean, well-structured implementation of Rummikub designed to be easily understood by beginners learning Python. Features comprehensive documentation that assumes no prior programming knowledge.

## Overview

This repository contains:
- 🎮 A complete, working Rummikub game for 2-4 players
- 📚 Extensive beginner-friendly documentation (~5,000 lines)
- 🧪 Comprehensive unit tests demonstrating best practices
- 💡 Clear code architecture designed for learning

The codebase demonstrates professional Python development while remaining accessible to newcomers.

## Documentation

**Start with the [documentation](docs/index.md)!** It includes:

- **[Getting Started](docs/getting-started/installation.md)** - Install Python and run the game
- **[Understanding the Code](docs/understanding-the-code/overview.md)** - Learn how the pieces fit together
- **[Game Mechanics](docs/game-mechanics/rules.md)** - See how rules become code
- **[Making Changes](docs/making-changes/simple-modifications.md)** - Modify the game yourself
- **[Reference](docs/reference/glossary.md)** - Quick lookups and programming terms

## Project Structure

```
educational-rummikub/
├── docs/                  # Comprehensive documentation
│   ├── getting-started/   # Installation and setup guides
│   ├── understanding-the-code/  # Code architecture and Python basics
│   ├── game-mechanics/    # How Rummikub rules are implemented
│   ├── making-changes/    # Guides for modifying the code
│   └── reference/         # Glossary and quick references
├── tiles.py          # Tile representation and deck management
├── rules.py          # Game rule validation
├── game.py           # Core game logic and state management
├── player.py         # Player class for tracking player state
├── display.py        # Console UI and rendering
├── main.py           # Entry point and game loop
├── tests/            # Unit tests for all modules
├── README.md         # This file
└── CLAUDE.md         # Guidance for AI assistants

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

## Quick Start

```bash
# Clone the repository
git clone https://github.com/stevenfazzio/educational-rummikub.git
cd educational-rummikub

# Run the game
python main.py

# Or jump straight into a 2-player game
python main.py --players "Alice,Bob"
```

## Learning from this Codebase

This codebase demonstrates:

- **Object-oriented design** with clear class hierarchies
- **Separation of concerns** (display, game logic, and rules are separate)
- **Validation patterns** for complex game rules
- **State management** in turn-based games
- **Clean architecture** with no circular dependencies
- **Comprehensive testing** with unit tests for all components
- **Modern Python** with type hints and dataclasses

## Why This Project?

This project serves multiple purposes:

1. **Learn Python** - See how a real application is structured
2. **Understand Software Design** - Study clean architecture patterns
3. **Practice Reading Code** - Everything is extensively documented
4. **Make Modifications** - Guides help you customize the game
5. **Have Fun** - It's a working game you can play!

## Contributing

We welcome contributions that enhance the educational value! Please:

- Read the [contribution guide](docs/contributing.md)
- Maintain clear, beginner-friendly code
- Add helpful comments and documentation
- Include tests for new features
- Follow existing patterns for consistency

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built as an educational resource for Python learners
- Inspired by the classic Rummikub tile game
- Documentation designed for programming beginners
- Special thanks to all contributors who help make this clearer!