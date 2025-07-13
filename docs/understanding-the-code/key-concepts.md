# Key Programming Concepts

This guide explains important programming ideas you'll see throughout the Rummikub code. We'll use examples from the game to make these concepts clear.

## 1. Objects and Classes 🏗️

### What Are They?
Think of a **class** as a blueprint, and **objects** as things built from that blueprint.

### Real-World Analogy
- **Class**: A cookie cutter shape
- **Object**: Each individual cookie made with that cutter

### In Our Game:
```python
# The blueprint (class)
class Tile:
    def __init__(self, number, color):
        self.number = number
        self.color = color

# Making objects from the blueprint
red_five = Tile(5, 'red')      # One tile object
blue_five = Tile(5, 'blue')    # Another tile object
```

Each tile is a separate object, but they're all made from the same Tile blueprint.

## 2. Functions and Methods 📦

### What Are They?
**Functions** are reusable sets of instructions. **Methods** are functions that belong to a class.

### Real-World Analogy
A recipe is like a function - a set of steps you can follow whenever you want that result.

### In Our Game:
```python
# A regular function
def create_joker():
    return Tile(0, 'joker')

# A method (function inside a class)
class Player:
    def draw_tile(self, tile):  # This is a method
        self.tiles.append(tile)
```

The difference? Methods work on specific objects (like a specific player), while functions are more general.

## 3. Lists and Collections 📚

### What Are They?
Lists are containers that hold multiple items in order.

### Real-World Analogy
Like a shopping list or a line of people waiting.

### In Our Game:
```python
# A player's hand is a list of tiles
player.tiles = [red_5, blue_6, black_7]

# The table has a list of sets
table_sets = [
    [red_5, blue_5, black_5],      # First set
    [blue_7, blue_8, blue_9]        # Second set
]
```

### Common List Operations:
```python
tiles.append(new_tile)     # Add to end
tiles.remove(old_tile)     # Remove specific item
tiles[0]                   # Get first item (counting starts at 0!)
len(tiles)                 # Count items
```

## 4. Conditionals (If/Else) 🚦

### What Are They?
Ways to make decisions in code.

### Real-World Analogy
Like a choose-your-own-adventure book: "If you have the key, turn to page 50. Otherwise, turn to page 23."

### In Our Game:
```python
if len(tiles) >= 3:
    print("You can make a meld!")
elif len(tiles) == 2:
    print("You need one more tile")
else:
    print("You need more tiles")
```

The code checks conditions in order and does the first matching action.

## 5. Loops 🔄

### What Are They?
Ways to repeat actions.

### Real-World Analogy
Like dealing cards - you repeat "give one card" for each player.

### In Our Game:
```python
# For each player in the game...
for player in players:
    player.draw_tile(deck.draw_tile())

# While the game isn't over...
while game.phase == "in_progress":
    play_turn()
```

## 6. State 💾

### What Is It?
The current situation - all the information about what's happening right now.

### Real-World Analogy
Like a snapshot of a chess board - where every piece is at this moment.

### In Our Game:
The GameState class tracks:
- Whose turn is it?
- What tiles are on the table?
- How many tiles does each player have?
- Has anyone won?

When something changes (like playing tiles), we update the state.

## 7. Validation ✅

### What Is It?
Checking if something is allowed before doing it.

### Real-World Analogy
Like checking if you have enough money before buying something.

### In Our Game:
```python
# Before playing tiles, check if the move is valid
if is_valid_set(tiles):
    play_tiles(tiles)
else:
    show_error("Those tiles don't form a valid set")
```

## 8. Encapsulation 📦

### What Is It?
Keeping related things together and hiding complexity.

### Real-World Analogy
A TV remote has buttons on the outside, but the complex electronics are hidden inside.

### In Our Game:
```python
class Player:
    def get_hand_value(self):
        # The complex calculation is hidden inside
        total = 0
        for tile in self.tiles:
            if tile.is_joker():
                total += 30
            else:
                total += tile.number
        return total

# Using it is simple:
value = player.get_hand_value()
```

## 9. Imports 📥

### What Are They?
Ways to use code from other files.

### Real-World Analogy
Like using tools from different toolboxes.

### In Our Game:
```python
from tiles import Tile, create_standard_deck
from rules import is_valid_set
```

This says: "I need the Tile tool from the tiles toolbox."

## 10. Error Handling 🛡️

### What Is It?
Planning for things that might go wrong.

### Real-World Analogy
Like having a spare tire in your car.

### In Our Game:
```python
def remove_tile(self, tile):
    if tile not in self.tiles:
        raise ValueError(f"Player doesn't have tile: {tile}")
    self.tiles.remove(tile)
```

This checks for problems before they cause crashes.

## Putting It All Together

Here's how these concepts work together in one example:

```python
class Player:                           # CLASS definition
    def __init__(self, name):          # METHOD for initialization
        self.name = name               # STATE (player's name)
        self.tiles = []                # LIST to hold tiles
    
    def play_tiles(self, tiles):       # METHOD with parameter
        if not self.has_tiles(tiles):  # VALIDATION with IF
            return False               # ERROR HANDLING
        
        for tile in tiles:             # LOOP through tiles
            self.tiles.remove(tile)    # Update STATE
        
        return True                    # Success!
```

## Common Patterns

### Pattern 1: Check Then Do
```python
if is_valid_move(move):
    apply_move(move)
```

### Pattern 2: Transform Lists
```python
# Get all red tiles
red_tiles = [tile for tile in tiles if tile.color == 'red']
```

### Pattern 3: Guard Clauses
```python
def do_something(value):
    if value is None:
        return  # Exit early if problem
    
    # Continue with normal logic
```

## Tips for Understanding Code

1. **Follow the Data** - Track how information moves through the program
2. **Read Method Names** - They usually describe what happens
3. **Look for Patterns** - Similar problems are solved in similar ways
4. **Start Small** - Understand one method before tackling a whole class
5. **Use the Debugger** - Step through code line by line (advanced)

---

## Next Steps

Now that you understand these concepts:
- 🎮 See them in action in [Game Mechanics](../game-mechanics/rules.md)
- 🔧 Apply them in [Making Changes](../making-changes/simple-modifications.md)
- 📖 Look them up in the [Glossary](../reference/glossary.md) anytime

Remember: These concepts appear in almost all programs, not just our game. Learning them here will help you understand other code too!