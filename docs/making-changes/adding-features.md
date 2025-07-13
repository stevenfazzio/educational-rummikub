# Adding New Features

Ready to add completely new functionality to the game? This guide will walk you through adding real features!

## Planning Your Feature 📝

Before coding, always:
1. **Define what** the feature does
2. **Decide where** it fits in the code
3. **Plan how** it will work
4. **Consider what** could go wrong

## Feature 1: Undo Last Move 🔄

Let's add an "undo" feature for when players make mistakes!

### Step 1: Plan the Feature
- **What**: Let players undo their last move
- **Where**: Store previous state in GameState
- **How**: Save state before each move, restore on undo
- **Edge cases**: Can't undo after drawing, only current player can undo

### Step 2: Add State Storage
In `game.py`, modify the GameState class:

```python
def __init__(self, player_names: List[str], 
             initial_hand_size: int = 14,
             random_seed: Optional[int] = None):
    # ... existing code ...
    
    # Add these new lines:
    self.previous_state = None
    self.can_undo = False
```

### Step 3: Save State Before Moves
Add this method to GameState:

```python
def save_state(self) -> None:
    """Save current state for undo functionality."""
    import copy
    
    self.previous_state = {
        'player_tiles': [copy.deepcopy(p.tiles) for p in self.players],
        'table_sets': copy.deepcopy(self.table_sets),
        'has_melded': [p.has_melded for p in self.players],
        'current_player': self.current_player_index
    }
```

### Step 4: Modify apply_move()
In the `apply_move` method, add state saving:

```python
def apply_move(self, move: Move) -> Tuple[bool, Optional[str]]:
    # First validate the move
    is_valid, error = self.validate_move(move)
    if not is_valid:
        return False, error
    
    # Save state before applying (NEW!)
    if move.move_type != MoveType.DRAW:
        self.save_state()
        self.can_undo = True
    
    # ... rest of existing apply_move code ...
```

### Step 5: Add Undo Method
```python
def undo_last_move(self) -> Tuple[bool, str]:
    """Undo the last move if possible."""
    if not self.can_undo or self.previous_state is None:
        return False, "Nothing to undo"
    
    # Restore player tiles
    for i, tiles in enumerate(self.previous_state['player_tiles']):
        self.players[i].tiles = tiles
    
    # Restore table
    self.table_sets = self.previous_state['table_sets']
    
    # Restore has_melded flags
    for i, has_melded in enumerate(self.previous_state['has_melded']):
        self.players[i].has_melded = has_melded
    
    # Restore turn
    self.current_player_index = self.previous_state['current_player']
    
    # Can't undo twice
    self.can_undo = False
    
    return True, "Move undone!"
```

### Step 6: Add UI Option
In `display.py`, modify the menu:

```python
# In get_human_move method, add to options:
if game_state.can_undo:
    print("6. Undo last move")
```

### Step 7: Handle the Choice
```python
# In the choice handling section:
elif choice == '6' and game_state.can_undo:
    success, message = game_state.undo_last_move()
    print(f"\n{message}")
    return Move(player_id, MoveType.END_TURN)  # Re-show menu
```

## Feature 2: Game Timer ⏱️

Add a timer to track how long games take!

### Step 1: Import Required Module
At the top of `game.py`:
```python
import time
from datetime import datetime, timedelta
```

### Step 2: Add Timer to GameState
```python
def __init__(self, player_names: List[str], ...):
    # ... existing code ...
    
    # Add timer attributes
    self.start_time = None
    self.end_time = None
```

### Step 3: Start Timer
In the `start_game` method:
```python
def start_game(self) -> None:
    # ... existing code ...
    
    # Start the timer
    self.start_time = time.time()
```

### Step 4: Stop Timer on Win
In `apply_move` where winner is detected:
```python
if is_winning_state(player.tiles):
    self.winner = player
    self.phase = GamePhase.FINISHED
    self.end_time = time.time()  # NEW!
```

### Step 5: Calculate Duration
Add this method:
```python
def get_game_duration(self) -> str:
    """Get game duration in readable format."""
    if not self.start_time:
        return "Not started"
    
    end = self.end_time or time.time()
    duration = int(end - self.start_time)
    
    minutes = duration // 60
    seconds = duration % 60
    
    return f"{minutes}m {seconds}s"
```

### Step 6: Display Duration
In `main.py`, modify `show_game_results`:
```python
def show_game_results(self) -> None:
    """Display final game results and scores."""
    if self.game_state.winner:
        scores = self.game_state.get_scores()
        duration = self.game_state.get_game_duration()  # NEW!
        
        self.display.display_winner(self.game_state.winner.name, scores)
        print(f"\nGame Duration: {duration}")  # NEW!
```

## Feature 3: Statistics Tracking 📊

Track player statistics across games!

### Step 1: Create Stats File
Create a new file `stats.py`:

```python
"""
Statistics tracking for Rummikub games.
"""
import json
import os
from typing import Dict, List
from datetime import datetime

class GameStats:
    """Manages game statistics."""
    
    def __init__(self, filename: str = "rummikub_stats.json"):
        self.filename = filename
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        """Load stats from file or create new."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'players': {},
            'games_played': 0
        }
    
    def save_stats(self) -> None:
        """Save stats to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def record_game(self, winner: str, players: List[str], 
                   scores: Dict[str, int], duration: str) -> None:
        """Record results of a game."""
        self.stats['games_played'] += 1
        
        # Update player stats
        for player in players:
            if player not in self.stats['players']:
                self.stats['players'][player] = {
                    'games': 0,
                    'wins': 0,
                    'total_score': 0
                }
            
            player_stats = self.stats['players'][player]
            player_stats['games'] += 1
            player_stats['total_score'] += scores.get(player, 0)
            
            if player == winner:
                player_stats['wins'] += 1
        
        self.save_stats()
    
    def get_player_stats(self, player: str) -> Dict:
        """Get statistics for a specific player."""
        if player not in self.stats['players']:
            return None
        
        stats = self.stats['players'][player]
        win_rate = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
        avg_score = stats['total_score'] / stats['games'] if stats['games'] > 0 else 0
        
        return {
            'games_played': stats['games'],
            'wins': stats['wins'],
            'win_rate': f"{win_rate:.1f}%",
            'average_score': f"{avg_score:.1f}"
        }
```

### Step 2: Use Stats in Main Game
In `main.py`, import and use:

```python
from stats import GameStats

class RummikubGame:
    def __init__(self, display: Optional[Display] = None):
        # ... existing code ...
        self.stats = GameStats()  # NEW!
```

### Step 3: Record Game Results
```python
def show_game_results(self) -> None:
    """Display final game results and scores."""
    if self.game_state.winner:
        scores = self.game_state.get_scores()
        duration = self.game_state.get_game_duration()
        
        # Record stats (NEW!)
        player_names = [p.name for p in self.game_state.players]
        self.stats.record_game(
            self.game_state.winner.name,
            player_names,
            scores,
            duration
        )
        
        # Show results
        self.display.display_winner(self.game_state.winner.name, scores)
        print(f"\nGame Duration: {duration}")
        
        # Show player stats (NEW!)
        print("\nPlayer Statistics:")
        for name in player_names:
            stats = self.stats.get_player_stats(name)
            if stats:
                print(f"{name}: {stats['wins']} wins in {stats['games_played']} games ({stats['win_rate']})")
```

## Feature 4: Hint System 💡

Help new players by suggesting valid moves!

### Step 1: Add Hint Logic
In `rules.py`, add:

```python
def find_valid_melds(tiles: List[Tile]) -> List[List[Tile]]:
    """Find all valid melds in a list of tiles."""
    valid_melds = []
    
    # Check all combinations of 3+ tiles
    from itertools import combinations
    
    for size in range(3, min(len(tiles) + 1, 5)):  # 3-4 tiles
        for combo in combinations(tiles, size):
            combo_list = list(combo)
            if is_valid_set(combo_list):
                valid_melds.append(combo_list)
    
    return valid_melds
```

### Step 2: Add Hint Method to GameState
```python
def get_hint(self, player_id: int) -> Optional[str]:
    """Get a hint for the current player."""
    player = self.get_player_by_id(player_id)
    if not player:
        return None
    
    # Find possible melds
    from rules import find_valid_melds
    possible_melds = find_valid_melds(player.tiles)
    
    if not possible_melds:
        return "No valid melds found. Try drawing a tile!"
    
    # Show first valid meld
    meld = possible_melds[0]
    tiles_str = ", ".join(str(tile) for tile in meld)
    
    # Check if meets initial meld requirement
    if not player.has_melded:
        value = sum(tile.number for tile in meld if not tile.is_joker())
        if value >= 30:
            return f"Try playing: {tiles_str} (worth {value} points!)"
        else:
            return f"You have: {tiles_str} but need 30+ points for initial meld"
    
    return f"You can play: {tiles_str}"
```

### Step 3: Add UI Option
Add hint option to the menu when it's the player's turn!

## Testing Your Features 🧪

For each feature:

1. **Test the happy path** - Does it work normally?
2. **Test edge cases** - What if...
   - Player undoes with no moves?
   - Timer runs for days?
   - Stats file is corrupted?
3. **Test integration** - Does it work with other features?

## Best Practices 💎

### 1. Keep Features Modular
Each feature should be self-contained:
```python
# Good: Feature can be disabled easily
if self.enable_undo:
    self.save_state()

# Bad: Feature mixed throughout code
# Changes scattered everywhere
```

### 2. Add Configuration Options
```python
class GameConfig:
    ENABLE_UNDO = True
    ENABLE_HINTS = True
    ENABLE_TIMER = True
    ENABLE_STATS = True
```

### 3. Handle Errors Gracefully
```python
try:
    stats = self.load_stats()
except FileNotFoundError:
    stats = self.create_default_stats()
except json.JSONDecodeError:
    print("Stats file corrupted, creating new one")
    stats = self.create_default_stats()
```

### 4. Document Your Features
Add docstrings and comments:
```python
def undo_last_move(self) -> Tuple[bool, str]:
    """
    Undo the last move made by the current player.
    
    Returns:
        Tuple of (success, message)
        
    Note:
        - Can only undo non-draw moves
        - Can only undo once per turn
        - Restores complete game state
    """
```

## Challenge Features 🚀

Ready for more? Try implementing:

1. **Save/Load Games** - Let players resume later
2. **Replay Mode** - Watch a game play out move by move  
3. **Tournament Mode** - Track multiple games between same players
4. **Sound Effects** - Add actual sounds (using pygame or similar)
5. **Network Play** - Play with friends over the internet
6. **AI Opponent** - Create a simple computer player
7. **Custom Rules** - Different initial meld values, joker rules, etc.

---

## Next Steps

- 🧪 Don't forget to [test your changes](testing-changes.md)!
- 📚 Review [common patterns](../reference/common-patterns.md) for ideas
- 🤝 Consider [contributing](../contributing.md) your features back!

Remember: Every feature starts as an idea. Plan carefully, implement step by step, and test thoroughly!