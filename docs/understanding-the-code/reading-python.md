# Reading Python Code

Python is designed to be readable - it often looks like simplified English! This guide will help you understand Python code using examples from our Rummikub game.

## The Basics

### Comments - Notes for Humans

```python
# This is a comment - Python ignores it
# Comments explain what the code does

"""
This is a multi-line comment.
It can span several lines.
We use these for longer explanations.
"""
```

Comments are like sticky notes - they help humans understand the code but don't affect what the program does.

### Variables - Storing Information

```python
player_name = "Alice"          # Text (called a "string")
player_score = 0               # Number
has_melded = False            # True/False (called a "boolean")
player_tiles = []             # Empty list (collection)
```

Think of variables as labeled boxes where we store information. The name tells us what's inside!

### Functions - Reusable Instructions

Here's a simple function from our game:

```python
def get_tile_count(self) -> int:
    """Get the number of tiles in the player's hand."""
    return len(self.tiles)
```

Let's break this down:
- `def` = "I'm defining a function"
- `get_tile_count` = The function's name
- `self` = The player we're asking about
- `-> int` = This function gives back a number
- `return` = "Here's the answer"

**In plain English**: "To get a player's tile count, count how many tiles they have and give back that number."

## Common Patterns in Our Game

### 1. If/Else - Making Decisions

```python
if len(tiles) >= 3:
    print("You can make a meld!")
else:
    print("You need at least 3 tiles")
```

This is like asking a question:
- IF you have 3 or more tiles, say one thing
- OTHERWISE (else), say something different

### 2. For Loops - Doing Things Repeatedly

```python
for tile in player.tiles:
    print(tile)
```

**In plain English**: "For each tile that the player has, show it on screen."

It's like saying: "Go through each item in my shopping bag and tell me what it is."

### 3. Lists - Collections of Things

```python
tiles = [tile1, tile2, tile3]    # A list of tiles
tiles.append(tile4)              # Add a tile to the end
tiles.remove(tile2)              # Remove a specific tile
first_tile = tiles[0]            # Get the first tile (counting starts at 0!)
```

Lists are like a row of boxes. You can add boxes, remove boxes, or look at specific boxes.

### 4. Classes - Blueprints

```python
class Player:
    def __init__(self, player_id: int, name: str):
        self.player_id = player_id
        self.name = name
        self.tiles = []
```

A class is like a blueprint for building something. This blueprint says:
- Every player needs an ID number and a name
- Every player starts with an empty list of tiles

## Reading a Complete Function

Let's read a real function from our game:

```python
def is_valid_group(tiles: List[Tile]) -> bool:
    """Check if tiles form a valid group (same number, different colors)."""
    
    # Groups need 3 or 4 tiles
    if len(tiles) < 3 or len(tiles) > 4:
        return False
    
    # All tiles must have the same number
    numbers = [tile.number for tile in tiles]
    if len(set(numbers)) != 1:
        return False
    
    # All tiles must have different colors
    colors = [tile.color for tile in tiles]
    if len(colors) != len(set(colors)):
        return False
    
    return True
```

**Translation to plain English**:

1. "To check if tiles make a valid group..."
2. "First, count the tiles. If less than 3 or more than 4, say NO"
3. "Check if all tiles have the same number. If not, say NO"
4. "Check if all tiles have different colors. If any repeat, say NO"
5. "If we made it this far, everything checked out - say YES"

## Symbols and What They Mean

| Symbol | Meaning | Example |
|--------|---------|---------|
| `=` | Assigns a value | `name = "Alice"` |
| `==` | Checks if equal | `if score == 0:` |
| `!=` | Not equal to | `if player != winner:` |
| `>` | Greater than | `if points > 30:` |
| `>=` | Greater than or equal | `if len(tiles) >= 3:` |
| `:` | Starts a block | `if has_melded:` |
| `.` | Accesses something inside | `player.name` |
| `[]` | List or index | `tiles[0]` |
| `()` | Function call or grouping | `len(tiles)` |

## Type Hints - Extra Clues

You'll see things like:

```python
def add_player(name: str, age: int) -> None:
```

The `: str`, `: int`, and `-> None` are type hints. They're like labels that say:
- `name: str` = name should be text
- `age: int` = age should be a number
- `-> None` = this function doesn't return anything

These help both humans and tools understand what kind of information to expect.

## Try Reading This!

Can you figure out what this code does?

```python
def has_won(player):
    """Check if a player has won the game."""
    if len(player.tiles) == 0:
        return True
    else:
        return False
```

<details>
<summary>Click to see the answer!</summary>

This function checks if a player has won by seeing if they have zero tiles left. In Rummikub, you win by getting rid of all your tiles!

- It looks at how many tiles the player has
- If they have 0 tiles, it returns True (they won!)
- Otherwise, it returns False (they haven't won yet)
</details>

## Tips for Reading Code

1. **Read function names** - They usually say what the function does
2. **Look for comments** - They explain tricky parts
3. **Follow the flow** - Code runs from top to bottom (unless it jumps)
4. **Don't panic** - You don't need to understand every detail
5. **Look for patterns** - The same patterns appear over and over

## Practice Makes Perfect

The best way to get comfortable reading code is to:
1. Pick a small function
2. Try to guess what it does from its name
3. Read through it line by line
4. Check if your guess was right

Start with simple functions like `get_tile_count()` or `has_tile()` and work up to more complex ones.

---

## Next Steps

Now that you can read basic Python:
- 📁 Explore the [Project Structure](project-structure.md) in detail
- 🧩 Learn about [Key Programming Concepts](key-concepts.md)
- 🎮 See how [Game Rules](../game-mechanics/rules.md) become code

Remember: Every expert was once a beginner. Take it one line at a time!