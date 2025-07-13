# Simple Modifications

Ready to make your first changes to the code? Let's start with simple, safe modifications that will help you get comfortable!

## Before You Start 🛡️

1. **Make a backup** of your working game (copy the whole folder)
2. **Run the game** to make sure it works before changing anything
3. **Change one thing at a time** so you know what caused any issues
4. **Test after each change** to catch problems early

## Modification 1: Changing Welcome Messages 👋

Let's personalize the game's messages!

### Find the File
Open `display.py` and search for "Rummikub" to find text we can change.

### Original Code (around line 100)
```python
self.display_header("Rummikub - Main Menu")
```

### Your Change
```python
self.display_header("Sarah's Awesome Rummikub Game!")
```

### Test It
Run the game: `python main.py`
You should see your new title!

### Try These Too
Look for other messages to customize:
- "Thanks for playing!" → "See you next time!"
- "Your turn" → "Time to make your move!"
- "Invalid move" → "Oops! That doesn't work"

## Modification 2: Changing Colors 🎨

Want different colors for the tiles? Let's do it!

### Find the File
Open `tiles.py` and find the color definitions.

### Original Code (around line 10)
```python
TILE_COLORS = ['red', 'blue', 'black', 'orange']
```

### Your Change
```python
TILE_COLORS = ['red', 'blue', 'green', 'yellow']
```

### Important!
You also need to update the color codes in `display.py`:

Find (around line 250):
```python
color_map = {
    'red': '\033[91m',
    'blue': '\033[94m',
    'black': '\033[90m',
    'orange': '\033[93m',
    'joker': '\033[95m'
}
```

Change to:
```python
color_map = {
    'red': '\033[91m',
    'blue': '\033[94m',
    'green': '\033[92m',    # Changed from black
    'yellow': '\033[93m',   # Changed from orange
    'joker': '\033[95m'
}
```

### Understanding Color Codes
These weird `\033[91m` things are ANSI color codes:
- `\033[91m` = Bright red
- `\033[92m` = Bright green
- `\033[93m` = Bright yellow
- `\033[94m` = Bright blue
- `\033[95m` = Bright magenta

## Modification 3: Changing Initial Hand Size 🃏

Want to start with more or fewer tiles?

### Find the File
Open `main.py` and look for hand size settings.

### Original Code (around line 36)
```python
def setup_game(self, player_names: List[str], 
               initial_hand_size: int = 14) -> None:
```

### Your Change
For a quicker game with 10 tiles:
```python
def setup_game(self, player_names: List[str], 
               initial_hand_size: int = 10) -> None:
```

### Also Update the Command Line Default (around line 232)
```python
parser.add_argument(
    '--hand-size',
    type=int,
    default=10,  # Changed from 14
    help='Initial hand size (default: 10)'
)
```

### Test It
Run: `python main.py`
Each player should start with 10 tiles instead of 14!

## Modification 4: Changing Menu Options 📋

Let's add a fun message to the main menu!

### Find the File
Open `main.py` and find the menu options.

### Original Code (around line 102)
```python
options = [
    "Quick Game (2 Players)",
    "Custom Game (2-4 Players)",
    "How to Play",
    "Exit"
]
```

### Your Change
```python
options = [
    "Quick Game (2 Players)",
    "Custom Game (2-4 Players)",
    "How to Play",
    "About This Game",  # New option!
    "Exit"
]
```

### Handle the New Option (around line 115)
```python
elif choice == 2:  # How to Play
    self.show_instructions()
elif choice == 3:  # About This Game (NEW!)
    self.show_about()
else:  # Exit
    print("Thanks for playing!")
    break
```

### Add the New Method
Add this at the end of the RummikubGame class:
```python
def show_about(self) -> None:
    """Display information about the game."""
    self.display.clear_screen()
    self.display.display_header("About This Game")
    
    about_text = """
This is Educational Rummikub!

A learning-friendly implementation designed to help
people understand how games are programmed.

Version: 1.0
Created with Python
Enjoy playing and learning!

Press Enter to return to menu...
"""
    print(about_text)
    input()
```

## Modification 5: Sound Effects (Text-Based) 🔊

Let's add fun text "sounds" when things happen!

### Find the File
Open `display.py` and find where moves are displayed.

### Original Code (around line 380)
```python
def display_move_result(self, move: Move, success: bool, error: Optional[str]) -> None:
    """Display the result of a move."""
    if success:
        if move.move_type == MoveType.PLAY_NEW_MELD:
            print("\n✓ Played new meld successfully!")
```

### Your Change
```python
def display_move_result(self, move: Move, success: bool, error: Optional[str]) -> None:
    """Display the result of a move."""
    if success:
        if move.move_type == MoveType.PLAY_NEW_MELD:
            print("\n🎉 *WHOOSH* ✓ Played new meld successfully!")
        elif move.move_type == MoveType.DRAW:
            print("\n🎴 *DRAW* You picked up a new tile!")
```

### Add More "Sounds"
- Drawing a tile: "*SWISH*"
- Invalid move: "*BUZZER*"
- Winning: "*FANFARE* 🎺"

## Modification 6: Change Point Requirements 📊

Want an easier game? Lower the initial meld requirement!

### Find the File
Open `rules.py` and find the constant.

### Original Code (around line 15)
```python
MIN_INITIAL_MELD_VALUE = 30
```

### Your Change
For an easier game:
```python
MIN_INITIAL_MELD_VALUE = 20  # Easier!
```

Or for a harder game:
```python
MIN_INITIAL_MELD_VALUE = 40  # Harder!
```

## Testing Your Changes 🧪

After each modification:

1. **Save the file** (Ctrl+S or Cmd+S)
2. **Run the game**: `python main.py`
3. **Test the specific feature** you changed
4. **If it breaks**, check for:
   - Typos in your changes
   - Missing colons or quotes
   - Wrong indentation (Python is picky about spacing!)

## Common Mistakes to Avoid ❌

### 1. Indentation Errors
Python uses spaces to organize code. Keep the same spacing!
```python
# WRONG (not aligned)
def my_function():
print("Hello")  # Error!

# RIGHT (aligned)
def my_function():
    print("Hello")  # Good!
```

### 2. Missing Quotes
```python
# WRONG
print(Hello)  # Error!

# RIGHT
print("Hello")  # Good!
```

### 3. Forgetting Colons
```python
# WRONG
if score > 30  # Error!
    print("You can meld!")

# RIGHT
if score > 30:  # Good!
    print("You can meld!")
```

## Your Turn! 🎯

Try these challenges:
1. Change the joker symbol from `[Joker]` to `[🃏]`
2. Add player statistics that show after each game
3. Change the minimum number of players from 2 to 1 (solo practice mode)
4. Add a "hint" option that suggests valid moves
5. Customize the victory message with ASCII art

## Getting Help 🆘

If something goes wrong:
1. **Undo your last change** and test again
2. **Compare with the original** to spot differences
3. **Read the error message** - Python tries to tell you what's wrong
4. **Check the line number** in the error - that's where to look

---

## Next Steps

Feeling confident? Try:
- 🚀 [Adding New Features](adding-features.md)
- 🧪 [Testing Your Changes](testing-changes.md)
- 📚 Understanding [Common Patterns](../reference/common-patterns.md)

Remember: Every programmer started by making small changes. You're doing great!