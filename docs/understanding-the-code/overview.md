# Understanding the Code - Overview

Let's explore how Educational Rummikub is built! Don't worry if you've never looked at code before - we'll take it step by step.

## Think of It Like a Board Game Night 🎲

To understand how this game works, imagine organizing a game night:

- **The Host** (`main.py`) - Organizes everything and starts the game
- **The Game Table** (`display.py`) - Where everyone sees and plays the game
- **The Game Master** (`game.py`) - Manages turns and enforces rules
- **The Rulebook** (`rules.py`) - The official rules that say what's legal
- **The Scorecards** (`player.py`) - Tracks what tiles each player has
- **The Game Box** (`tiles.py`) - Contains all the physical game pieces

Each part has a specific job, and they work together to create the game experience!

## System Architecture

Here's how the components connect and interact:

```mermaid
graph TB
    subgraph "User Interface Layer"
        A[main.py<br/>Entry Point] 
        B[display.py<br/>UI & Input]
    end
    
    subgraph "Game Logic Layer"
        C[game.py<br/>Game State]
        D[rules.py<br/>Validation]
    end
    
    subgraph "Data Layer"
        E[player.py<br/>Player Data]
        F[tiles.py<br/>Game Pieces]
    end
    
    A --> B
    A --> C
    B --> C
    C --> D
    C --> E
    D --> F
    E --> F
    
    style A fill:#4FC3F7,stroke:#1976D2,stroke-width:2px,color:#000
    style B fill:#4FC3F7,stroke:#1976D2,stroke-width:2px,color:#000
    style C fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#000
    style D fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#000
    style E fill:#81C784,stroke:#388E3C,stroke-width:2px,color:#000
    style F fill:#81C784,stroke:#388E3C,stroke-width:2px,color:#000
```

The diagram shows three layers:
- **User Interface** (blue): Where players interact with the game
- **Game Logic** (orange): Where game rules and state are managed
- **Data Layer** (green): Where game data structures are defined

## The Files and What They Do

### 🚪 `main.py` - The Host
**What it does**: Entry point that organizes everything

Like a game night host, this file:
- Shows the main menu
- Sets up new games
- Connects all the other pieces
- Starts the game loop

**Key concept**: This is where the program begins.

### 🖥️ `display.py` - The Game Table
**What it does**: Shows the game to players and gets their input

Just like the physical table where you play, this file:
- Shows everyone what's on the table
- Displays each player's tiles (only to them!)
- Gets player choices
- Makes everything look nice with colors

**Key concept**: This is the only file that talks to the player directly.

### 🎮 `game.py` - The Game Master
**What it does**: Manages the game and enforces fairness

Like a game master who runs the game, this file:
- Knows whose turn it is
- Tracks what's on the table
- Applies moves when players make them
- Declares winners

**Key concept**: This file manages the game state (what's happening right now).

### 📋 `rules.py` - The Rulebook
**What it does**: The official rules that determine what's legal

Like consulting the rulebook, this file answers:
- "Is this a valid group?" (like [5 red] [5 blue] [5 black])
- "Is this a valid run?" (like [7 blue] [8 blue] [9 blue])
- "Does this initial meld have enough points?"

**Key concept**: This file never changes the game - it just says "yes" or "no" to moves.

### 👤 `player.py` - The Scorecards
**What it does**: Keeps track of each player's tiles

Like personal scorecards, this file tracks:
- Player's name
- Their tiles (their "hand")
- Whether they've made their initial meld

**Key concept**: This file is about data storage, not decision-making (humans make the decisions).

### 📦 `tiles.py` - The Game Box
**What it does**: Contains all the game pieces

Like the game box with all the tiles, this file:
- Defines what a tile is (number + color)
- Creates a full deck of 106 tiles
- Can shuffle and deal tiles

**Key concept**: This file creates the building blocks everything else uses.

## How They Work Together

Here's what happens when you play a tile:

```
1. display.py shows you the menu and gets your choice
   ↓
2. main.py receives your choice and asks game.py to handle it
   ↓
3. game.py checks with rules.py: "Is this move legal?"
   ↓
4. rules.py examines the tiles and says "yes" or "no"
   ↓
5. If yes, game.py updates the game state
   ↓
6. display.py shows you the updated table
```

## Reading Your First Code

Let's look at a real example from `player.py`:

```python
def add_tile(self, tile: Tile) -> None:
    """Add a single tile to the player's hand."""
    self.tiles.append(tile)
```

Let's break this down:
- `def` means "define a new function" (a set of instructions)
- `add_tile` is the name we're giving these instructions
- `self` refers to the player we're working with
- `tile: Tile` means we expect to receive a tile
- `self.tiles.append(tile)` adds the tile to the player's collection

In plain English: "Here's how to add a tile to a player's hand: take their list of tiles and add the new tile to it."

## Patterns You'll See

As you explore the code, you'll notice patterns:

### 1. **Functions** - Reusable Instructions
```python
def do_something():
    # Instructions here
```

### 2. **Classes** - Blueprints for Objects
```python
class Player:
    # What a player has and can do
```

### 3. **If Statements** - Making Decisions
```python
if player.has_melded:
    # Do this
else:
    # Do that
```

### 4. **Lists** - Collections of Things
```python
tiles = [tile1, tile2, tile3]
```

## Where to Go Next

Now that you have the big picture:

1. **Want to read Python?** → [Reading Python](reading-python.md)
2. **Want details on each file?** → [Project Structure](project-structure.md)
3. **Want to understand programming concepts?** → [Key Concepts](key-concepts.md)
4. **Ready to see how rules work?** → [Game Mechanics](../game-mechanics/rules.md)

## Remember

- 🔍 **You don't need to understand everything at once**
- 📚 **Each file has one main job**
- 🧩 **The files work together like puzzle pieces**
- 💡 **The code is just instructions written in a special language**

Take your time, and don't hesitate to jump between files to see how they connect!