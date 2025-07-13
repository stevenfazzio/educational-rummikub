# Common Patterns in the Code

This guide shows recurring patterns in our codebase. Understanding these patterns helps you write code that fits well with the existing style.

## Validation Pattern 🛡️

### Pattern: Check Before You Change
Always validate before modifying state.

```python
# Pattern appears in game.py
def apply_move(self, move: Move) -> Tuple[bool, Optional[str]]:
    # 1. Validate first
    is_valid, error = self.validate_move(move)
    if not is_valid:
        return False, error
    
    # 2. Only then make changes
    player.remove_tiles(move.tiles)
    self.table_sets.append(move.tiles)
    
    return True, None
```

### Why This Pattern?
- Prevents invalid state
- Clear error messages
- Easy to test
- Safe rollback

## Factory Function Pattern 🏭

### Pattern: Functions That Create Objects
Instead of complex constructors, use simple creation functions.

```python
# Pattern in tiles.py
def create_tile(number: int, color: str) -> Tile:
    """Create a single tile with validation."""
    return Tile(number, color)

def create_joker() -> Tile:
    """Create a joker tile."""
    return Tile(0, JOKER_COLOR)

def create_standard_deck() -> Deck:
    """Create a complete 106-tile deck."""
    tiles = []
    # ... build tiles ...
    return Deck(tiles)
```

### Why This Pattern?
- Clear names explain what's created
- Hides complexity
- Easy to test
- Consistent creation

## Early Return Pattern 🚪

### Pattern: Exit Early on Invalid Cases
Check error conditions first and return immediately.

```python
# Pattern in rules.py
def is_valid_group(tiles: List[Tile]) -> bool:
    # Check simplest condition first
    if len(tiles) < MIN_SET_SIZE or len(tiles) > MAX_GROUP_SIZE:
        return False
    
    # Check next condition
    if not all_same_number(tiles):
        return False
    
    # Check final condition
    if not all_different_colors(tiles):
        return False
    
    # If we get here, it's valid
    return True
```

### Why This Pattern?
- Reduces nesting
- Clear flow
- Efficient (stops early)
- Easy to add conditions

## State Machine Pattern 🎰

### Pattern: Explicit States Control Flow
Use enums to represent different states.

```python
# Pattern in game.py
class GamePhase(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"

class GameState:
    def start_game(self):
        if self.phase != GamePhase.NOT_STARTED:
            raise ValueError("Game already started")
        
        # Do setup...
        self.phase = GamePhase.IN_PROGRESS
```

### Why This Pattern?
- Clear game flow
- Prevents invalid transitions
- Easy to debug
- Self-documenting

## Command Pattern 🎮

### Pattern: Encapsulate Actions as Objects
Represent player actions as data.

```python
# Pattern with Move class
@dataclass
class Move:
    player_id: int
    move_type: MoveType
    tiles: List[Tile] = field(default_factory=list)
    
# Usage
move = Move(
    player_id=0,
    move_type=MoveType.PLAY_NEW_MELD,
    tiles=selected_tiles
)
```

### Why This Pattern?
- Easy to validate
- Can be stored/undone
- Clear intent
- Testable

## Builder Pattern 🔨

### Pattern: Step-by-Step Construction
Build complex objects piece by piece.

```python
# Pattern in display messages
def format_game_state(self) -> str:
    """Build game state display step by step."""
    output = []
    
    # Add header
    output.append(self._format_header())
    
    # Add table
    output.append(self._format_table())
    
    # Add player info
    output.append(self._format_player_hand())
    
    # Combine all parts
    return '\n'.join(output)
```

### Why This Pattern?
- Clear steps
- Easy to modify
- Reusable parts
- Maintainable

## Collection Processing Pattern 📚

### Pattern: Transform Lists Clearly
Use list comprehensions and clear variable names.

```python
# Get all numbers from tiles
numbers = [tile.number for tile in tiles]

# Filter jokers
regular_tiles = [tile for tile in tiles if not tile.is_joker()]

# Check all same color
colors = [tile.color for tile in tiles]
all_same_color = len(set(colors)) == 1

# Find valid moves
valid_moves = [
    move for move in possible_moves 
    if self.is_valid_move(move)
]
```

### Why This Pattern?
- Readable
- Pythonic
- Efficient
- Functional style

## Error Handling Pattern ⚠️

### Pattern: Return Success/Error Tuples
Functions return (success, error_message).

```python
# Pattern throughout codebase
def validate_move(self, move: Move) -> Tuple[bool, Optional[str]]:
    if not self.is_player_turn(move.player_id):
        return False, "Not your turn"
    
    if not self.player_has_tiles(move.tiles):
        return False, "You don't have those tiles"
    
    return True, None

# Usage
success, error = game.validate_move(move)
if not success:
    print(f"Invalid: {error}")
```

### Why This Pattern?
- No exceptions for normal flow
- Clear error messages
- Easy to handle
- Consistent interface

## Type Hinting Pattern 📝

### Pattern: Clear Type Annotations
Always specify types for clarity.

```python
def calculate_score(tiles: List[Tile]) -> int:
    """Calculate total score of tiles."""
    return sum(tile.number for tile in tiles)

def find_player(
    players: List[Player], 
    player_id: int
) -> Optional[Player]:
    """Find player by ID."""
    for player in players:
        if player.player_id == player_id:
            return player
    return None
```

### Why This Pattern?
- Self-documenting
- IDE support
- Catch errors early
- Clear contracts

## Testing Pattern 🧪

### Pattern: Arrange-Act-Assert
Structure tests consistently.

```python
def test_player_draws_tile(self):
    # Arrange - Set up test conditions
    player = Player(0, "Test")
    initial_count = len(player.tiles)
    new_tile = create_tile(5, 'red')
    
    # Act - Perform the action
    player.add_tile(new_tile)
    
    # Assert - Check the results
    self.assertEqual(len(player.tiles), initial_count + 1)
    self.assertIn(new_tile, player.tiles)
```

### Why This Pattern?
- Clear test structure
- Easy to understand
- Consistent format
- Good documentation

## Display Pattern 🖥️

### Pattern: Separate Formatting from Logic
Keep display logic separate from game logic.

```python
# In display.py - Only formatting
def format_tile(self, tile: Tile) -> str:
    if tile.is_joker():
        return "[Joker]"
    return f"[{tile.number} {tile.color}]"

# In game.py - Only logic
def get_tile_value(tile: Tile) -> int:
    if tile.is_joker():
        return 30
    return tile.number
```

### Why This Pattern?
- Single responsibility
- Easy to change UI
- Testable logic
- Clear separation

## Configuration Pattern ⚙️

### Pattern: Constants at Module Level
Define configuration as constants.

```python
# At top of file
TILE_COLORS = ['red', 'blue', 'black', 'orange']
MIN_PLAYERS = 2
MAX_PLAYERS = 4
INITIAL_HAND_SIZE = 14
MIN_INITIAL_MELD_VALUE = 30

# Use throughout code
if len(players) > MAX_PLAYERS:
    raise ValueError(f"Maximum {MAX_PLAYERS} players allowed")
```

### Why This Pattern?
- Easy to find/change
- No magic numbers
- Self-documenting
- Consistent values

## Documentation Pattern 📚

### Pattern: Docstrings Explain Why and What
Every public function has a docstring.

```python
def is_valid_run(tiles: List[Tile]) -> bool:
    """
    Check if tiles form a valid run.
    
    A valid run contains:
    - At least 3 tiles
    - Consecutive numbers (with jokers filling gaps or extending)
    - All the same color (except jokers)
    - No duplicate numbers
    
    Args:
        tiles: List of tiles to check
        
    Returns:
        True if tiles form a valid run
    """
```

### Why This Pattern?
- Clear purpose
- Usage examples
- Parameter explanation
- Return value clear

## Copy Pattern 📋

### Pattern: Copy When Sharing Data
Prevent accidental modifications.

```python
# When storing tiles
self.table_sets.append(tiles.copy())  # Not just tiles

# When returning lists
def get_tiles(self) -> List[Tile]:
    return self.tiles.copy()  # Prevent external modification

# When passing to functions
validate_arrangement(current_sets.copy())
```

### Why This Pattern?
- Prevents bugs
- Clear ownership
- Safe modifications
- Predictable behavior

---

## Using These Patterns

1. **Consistency** - Use the same pattern throughout
2. **Clarity** - Patterns should make code clearer
3. **Purpose** - Use patterns that solve real problems
4. **Simplicity** - Don't over-engineer

Remember: Patterns are tools. Use them when they help, skip them when they don't!