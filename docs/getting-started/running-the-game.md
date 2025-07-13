# Running the Game

Now that you have Python installed, let's play Rummikub! This guide will walk you through starting your first game.

## Opening the Command Line

First, we need to open the command line (that black window where you type commands):

### Windows:
1. Press **Windows key**
2. Type `cmd`
3. Press **Enter**

### Mac:
1. Press **Command + Space**
2. Type `terminal`
3. Press **Enter**

Don't worry if the command line looks intimidating - you'll only need to type a few simple things!

## Getting to the Game Folder

Now we need to tell the computer where to find the game:

1. Type `cd ` (that's cd followed by a space)
2. Find your `educational-rummikub` folder in Windows Explorer or Finder
3. Drag the folder into the command line window
4. Press **Enter**

You should see the command line change to show you're in the game folder.

💡 **Tip**: If you saved the game to your Desktop, you can also type:
- Windows: `cd Desktop\educational-rummikub`
- Mac: `cd ~/Desktop/educational-rummikub`

## Starting Your First Game

Now for the fun part! Type this command and press **Enter**:

```bash
python main.py
```

(On Mac, you might need to use `python3 main.py` instead)

## What You'll See

### The Main Menu

```
=====================================
       Rummikub - Main Menu
=====================================

1. Quick Game (2 Players)
2. Custom Game (2-4 Players)
3. How to Play
4. Exit

Enter your choice (1-4):
```

Let's start with a quick game! Type `1` and press **Enter**.

### Setting Up Players

The game will ask for player names:

```
Quick Game Setup
----------------------------------------
Player 1 name: Alice
Player 2 name: Bob
```

Type each name and press **Enter**. If you just press **Enter** without typing, it will use default names.

### Playing the Game

The game will show you:
1. The tiles on the table (empty at first)
2. Your current tiles
3. A menu of actions you can take

Here's what a turn looks like:

```
=======================================
           Table Sets
=======================================
(No sets on table yet)

Alice's tiles:
1. [3 red]    4. [7 blue]   7. [10 black]
2. [3 blue]   5. [8 red]    8. [11 red]
3. [5 red]    6. [9 red]    9. [12 blue]

Your Options:
1. Sort tiles by color
2. Sort tiles by number
3. Play new meld
4. Draw a tile

Enter your choice (1-4):
```

## Understanding the Display

### Tiles
Each tile shows as `[number color]`, for example:
- `[5 red]` = A red tile with the number 5
- `[10 blue]` = A blue tile with the number 10
- `[Joker]` = A special joker tile

### Colors
The game uses four colors:
- 🔴 Red
- 🔵 Blue
- ⚫ Black
- 🟠 Orange

If your command line supports colors, tiles will appear in their actual colors!

## Basic Actions

### 1. Sorting Your Tiles
Press `1` or `2` to sort your tiles by color or number. This helps you spot patterns!

### 2. Playing Tiles
Press `3` to play tiles. You'll need to form valid sets:
- **Groups**: 3-4 tiles with the same number, different colors (like [5 red] [5 blue] [5 black])
- **Runs**: 3+ consecutive numbers in the same color (like [5 red] [6 red] [7 red])

### 3. Drawing a Tile
Press `4` if you can't (or don't want to) play. You'll get one new tile and your turn ends immediately.

## Your First Meld

Remember: Your first play must be worth at least 30 points! The tiles' numbers are their point values.

**Try This**: Look for three tiles that add up to 30 or more, like:
- [10 red] [10 blue] [10 black] = 30 points ✓
- [11 red] [12 red] [13 red] = 36 points ✓
- [5 red] [6 red] [7 red] = 18 points ✗ (not enough!)

## Ending the Game

The game continues until someone plays all their tiles. You'll see:

```
🎉 Alice wins! 🎉

Final Scores (lower is better):
Alice: 0 points
Bob: 45 points

Press Enter to return to menu...
```

## Quick Commands Summary

Here are all the ways to start the game:

```bash
# Basic game (opens menu)
python main.py

# Start with specific players
python main.py --players "Alice,Bob,Charlie"

# Play without colors (if colors don't work right)
python main.py --no-color

# See all options
python main.py --help
```

## Troubleshooting

### "python: command not found"
- Try `python3` instead of `python`
- Make sure you [installed Python](installation.md)

### Game crashes or shows errors
- Make sure you're in the right folder
- Check the [Troubleshooting Guide](troubleshooting.md)

### Can't see colors properly
- Run with: `python main.py --no-color`

---

## What's Next?

Now that you can play the game:
- 📖 Learn [how the code works](../understanding-the-code/overview.md)
- 🎮 Understand [game strategies](../game-mechanics/rules.md)
- 🔧 Try [making simple changes](../making-changes/simple-modifications.md)

Have fun playing! Remember, the goal is to be the first player to get rid of all your tiles by forming valid sets on the table.