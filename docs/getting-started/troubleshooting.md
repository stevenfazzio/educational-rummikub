# Troubleshooting Guide

Don't worry - everyone runs into problems when they're getting started! This guide will help you fix the most common issues.

## General Tips

Before we dive into specific problems:

1. **Error messages are your friends** - They tell you what went wrong
2. **Exact spelling matters** - `python` is different from `Python` or `pyton`
3. **Spaces and symbols matter** - Type commands exactly as shown
4. **It's okay to start over** - Close the command line and try again

## Common Problems and Solutions

### 🔴 "python is not recognized" or "command not found"

**What it means**: Your computer doesn't know where Python is.

**Try these solutions in order**:

1. **Use python3 instead** (especially on Mac):
   ```bash
   python3 main.py
   ```

2. **Check if Python is installed**:
   - Windows: Try `py --version` or `python --version`
   - Mac: Try `python3 --version`

3. **Reinstall Python** (Windows):
   - Uninstall Python from Settings > Apps
   - Download again from [python.org](https://python.org)
   - ⚠️ CHECK the "Add Python to PATH" box during installation!

4. **Restart your computer** after installing Python

---

### 🔴 "No such file or directory" or "cannot find the path"

**What it means**: The command line is looking in the wrong place for the game.

**Solutions**:

1. **Make sure you're in the right folder**:
   ```bash
   # See where you are:
   pwd     # (Mac/Linux)
   cd      # (Windows)
   ```

2. **Navigate to the game folder**:
   - Option A: Type `cd `, drag the game folder into the terminal, press Enter
   - Option B: Type the full path:
     ```bash
     # Windows example:
     cd C:\Users\YourName\Desktop\educational-rummikub
     
     # Mac example:
     cd /Users/YourName/Desktop/educational-rummikub
     ```

3. **Check the folder has the game files**:
   ```bash
   # List files in current folder:
   dir     # (Windows)
   ls      # (Mac/Linux)
   ```
   You should see `main.py` in the list!

---

### 🔴 "ModuleNotFoundError" or "ImportError"

**What it means**: Python can't find part of the game code.

**Example**:
```
ModuleNotFoundError: No module named 'tiles'
```

**Solutions**:

1. **Make sure you're in the main game folder** (not inside a subfolder)
2. **Check all game files are present**:
   - You should have: `main.py`, `tiles.py`, `game.py`, etc.
   - If files are missing, redownload the game

---

### 🔴 "SyntaxError" with a weird message

**What it means**: There's a typo in the code or command.

**Example**:
```
SyntaxError: invalid syntax
    print("Hello")
          ^
```

**Solutions**:

1. **If typing a command**, check for typos:
   - Wrong: `pyton main.py` or `python main,py`
   - Right: `python main.py`

2. **If the error points to the game code**, the files might be corrupted:
   - Redownload the game
   - Make sure you didn't accidentally edit any files

---

### 🔴 Screen shows weird characters instead of colors

**What it looks like**:
```
[31m[5 red][0m [34m[6 blue][0m
```

**Solution**: Run without colors:
```bash
python main.py --no-color
```

---

### 🔴 "Permission denied"

**What it means**: Your computer won't let Python run.

**Solutions**:

1. **Mac/Linux**: Use `python3` instead of `python`
2. **Make sure you own the files**:
   - Right-click the game folder
   - Check Properties/Get Info
   - Make sure you have read/write permissions

---

### 🔴 Game starts but immediately closes

**What it means**: The game crashed or ended too quickly.

**Solutions**:

1. **Run from command line** (not by double-clicking):
   - Open command line first
   - Navigate to folder
   - Then run `python main.py`

2. **Look for error messages** that appear before it closes

---

## Understanding Error Messages

Here's how to read Python error messages:

```
Traceback (most recent call last):
  File "main.py", line 42, in <module>     ← Where it happened
    game.start()
  File "game.py", line 15, in start
    player = Player(name)
NameError: name 'Player' is not defined    ← What went wrong
```

The important parts:
- **Last line**: Says what went wrong
- **File and line number**: Shows where it happened
- **The arrow (^)**: Points to the exact spot

## Still Stuck?

If none of these solutions work:

### 1. Get Your System Information

Run these commands and save the output:
```bash
# Python version:
python --version

# Current directory:
pwd          # (Mac/Linux)
cd           # (Windows)

# Files in directory:
ls           # (Mac/Linux)
dir          # (Windows)
```

### 2. Try a Fresh Start

1. Delete the game folder
2. Redownload it
3. Follow the [installation guide](installation.md) step by step

### 3. Ask for Help

When asking for help, include:
- What you typed
- The complete error message
- Your operating system (Windows/Mac/Linux)
- Your Python version

## Common Beginner Mistakes

We all make these - don't feel bad!

1. **Forgetting to press Enter** after typing a command
2. **Being in the wrong folder** when running commands
3. **Typing in the wrong window** (make sure you're in the command line)
4. **Using the wrong quotes** - use straight quotes " not curly quotes "
5. **Adding extra spaces** where they don't belong

## You're Doing Great! 

Remember:
- 🌟 Every programmer has been where you are now
- 💪 These problems are temporary - you'll solve them!
- 📚 Each error teaches you something new
- 🎯 Once it's working, you won't have to do this setup again

---

Ready to try again? Head back to [Running the Game](running-the-game.md) and give it another shot!