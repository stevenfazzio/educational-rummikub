# Installing Everything You Need

Before you can play Educational Rummikub, you need to install Python on your computer. Don't worry - it's free and safe!

## What is Python?

Python is the programming language this game is written in. Your computer needs Python installed to understand and run the game's instructions.

Think of it like this: if the game is a recipe, Python is the kitchen where you cook it!

## Step 1: Check if You Already Have Python

You might already have Python! Let's check:

### On Windows:
1. Press the **Windows key** on your keyboard
2. Type `cmd` and press **Enter** (this opens Command Prompt)
3. Type this exactly: `python --version`
4. Press **Enter**

### On Mac:
1. Press **Command + Space** to open Spotlight
2. Type `terminal` and press **Enter**
3. Type this exactly: `python3 --version`
4. Press **Enter**

### What You Should See:
- ✅ If you see something like `Python 3.8.10` (or any number starting with 3), you have Python! Skip to [Getting the Game](#step-3-getting-the-game).
- ❌ If you see an error message, you need to install Python. Continue to Step 2.

## Step 2: Installing Python

### On Windows:

1. **Go to the Python website**: [python.org/downloads](https://python.org/downloads)
2. Click the big yellow **Download Python** button
3. Save the file and run it
4. ⚠️ **IMPORTANT**: Check the box that says **"Add Python to PATH"** before clicking Install
5. Click **Install Now**
6. Wait for it to finish, then click **Close**

<details>
<summary>📸 Click here to see what these steps look like</summary>

The installer will show several screens:
- First screen: CHECK "Add Python to PATH" ✓
- Click "Install Now"
- Let it run (might take a few minutes)
- Click "Close" when done
</details>

### On Mac:

1. **Go to the Python website**: [python.org/downloads](https://python.org/downloads)
2. Click the big yellow **Download Python** button
3. Open the downloaded file
4. Follow the installer (just keep clicking **Continue** and **Install**)
5. Enter your password when asked

### On Linux:
Python usually comes pre-installed! If not, open Terminal and type:
```bash
sudo apt-get update
sudo apt-get install python3
```

## Step 3: Getting the Game

Now let's get the Rummikub game onto your computer:

### Option A: Download as ZIP (Easiest)

1. Go to the game's webpage (ask whoever shared this with you for the link)
2. Look for a green **Code** button
3. Click it and choose **Download ZIP**
4. Save the ZIP file to your Desktop or Downloads folder
5. Find the ZIP file and double-click to unzip it
6. You should now have a folder called `educational-rummikub`

### Option B: Using Git (More Advanced)

If you know what Git is, you can clone the repository:
```bash
git clone [repository-url]
```

## Step 4: Verify Everything Works

Let's make sure everything is set up correctly:

1. Open your command line again (Command Prompt on Windows, Terminal on Mac)
2. Navigate to the game folder:
   - Type `cd ` (with a space after cd)
   - Drag the `educational-rummikub` folder into the command window
   - Press **Enter**
3. Type: `python main.py --help` (or `python3 main.py --help` on Mac)
4. Press **Enter**

### What You Should See:
You should see help text about the game. If you do, congratulations! 🎉 You're ready to [play the game](running-the-game.md).

### If Something Went Wrong:
Check our [Troubleshooting Guide](troubleshooting.md) or see the common issues below.

## Common Issues and Solutions

### "python is not recognized" (Windows)
This usually means Python wasn't added to PATH during installation:
1. Uninstall Python (through Windows Settings > Apps)
2. Reinstall it, making sure to check "Add Python to PATH"

### "No such file or directory"
This means the command line can't find the game folder:
1. Make sure you're in the right folder
2. Try using the full path: `cd C:\Users\YourName\Desktop\educational-rummikub`

### "Permission denied" (Mac/Linux)
Try using `python3` instead of `python`

---

## Next Steps

Great job! You've installed everything you need. Now let's [run the game](running-the-game.md) and start playing!

💡 **Remember**: Installing software can be tricky the first time. If you run into problems, that's normal! Check the [Troubleshooting Guide](troubleshooting.md) or ask for help.