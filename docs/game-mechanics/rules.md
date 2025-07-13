# Rummikub Rules

Let's learn how to play Rummikub! This guide explains the rules that our computer game follows.

## The Goal 🎯

Be the first player to get rid of all your tiles by playing them on the table in valid sets.

## The Tiles 🎨

Rummikub uses 106 tiles:
- **104 numbered tiles**: Numbers 1-13 in four colors (red, blue, black, orange)
- **2 joker tiles**: Special wild cards that can be any tile

Each number appears twice in each color. So there are two red 5s, two blue 5s, etc.

## Setting Up 🏁

1. All tiles go face-down in the middle
2. Each player draws 14 tiles
3. Players arrange their tiles so only they can see them
4. One player goes first (usually youngest or random)

## Valid Sets ✅

You can only play tiles in valid sets. There are two types:

### 1. Groups (Same Number, Different Colors)
- Must have 3 or 4 tiles
- All tiles must show the same number
- All tiles must be different colors
- ✅ Good: [5 red] [5 blue] [5 black]
- ❌ Bad: [5 red] [5 red] [5 blue] (duplicate color)
- ❌ Bad: [5 red] [5 blue] (only 2 tiles)

### 2. Runs (Consecutive Numbers, Same Color)
- Must have at least 3 tiles
- Numbers must be consecutive
- All tiles must be the same color
- ✅ Good: [5 blue] [6 blue] [7 blue]
- ✅ Good: [10 red] [11 red] [12 red] [13 red]
- ❌ Bad: [5 blue] [7 blue] [8 blue] (missing 6)
- ❌ Bad: [5 blue] [6 red] [7 blue] (different colors)

### Special Rules for Runs:
- 1 comes after 13 (they don't connect)
- Can't do: [12 red] [13 red] [1 red]

## The Initial Meld 🚀

**Important**: Your first play must be worth at least 30 points!

- Each tile is worth its number (5 = 5 points, 13 = 13 points)
- Add up all tiles in your initial play
- Must total 30 or more

Examples:
- ✅ [10 red] [10 blue] [10 black] = 30 points
- ✅ [9 blue] [10 blue] [11 blue] [12 blue] = 42 points
- ❌ [5 red] [6 red] [7 red] = 18 points (not enough!)

You can play multiple sets in your initial meld:
- ✅ [5 red] [5 blue] [5 black] + [7 blue] [8 blue] [9 blue] = 15 + 24 = 39 points

## Your Turn 🎮

On your turn, you can:

### Option 1: Play Tiles
If you have valid sets to play:
1. Place new sets on the table
2. Add tiles to existing sets
3. Rearrange the table to make room for your tiles

### Option 2: Draw a Tile
If you can't or don't want to play:
1. Draw one tile from the pile
2. Your turn ends

**Note**: You must do one or the other - you can't do both!

## Playing After Your Initial Meld 🎯

Once you've made your 30-point initial meld, you can:

### 1. Play New Sets
Place any valid group or run on the table (no minimum points needed now)

### 2. Add to Existing Sets
- Add a [5 orange] to [5 red] [5 blue] [5 black]
- Add [4 blue] to the front of [5 blue] [6 blue] [7 blue]
- Add [13 red] to the end of [10 red] [11 red] [12 red]

### 3. Rearrange the Table
This is where Rummikub gets interesting! You can:
- Split sets apart
- Combine sets
- Move tiles between sets

As long as ALL sets on the table are valid when you're done!

#### Rearranging Example:
Table has: [5 red] [5 blue] [5 black]
You have: [5 orange] and [6 blue]

You could:
1. Add [5 orange] to make [5 red] [5 blue] [5 black] [5 orange]
2. Take the [5 blue] and use it with your [6 blue] and a [7 blue] from another set

## Jokers 🃏

Jokers are wild cards:
- Can represent any tile
- Worth 30 points if left in your hand
- When playing a joker, you must say what it represents

Example:
- Play: [5 red] [Joker] [7 red] and say "The joker is a 6 red"

### Taking Jokers:
On later turns, if you have the actual tile a joker represents, you can:
1. Replace the joker with your tile
2. Use the joker immediately in a new set
3. You cannot add the joker to your hand

## Winning 🏆

The first player to play all their tiles wins!

When someone wins:
- Other players count their remaining tiles
- Each numbered tile = its face value in penalty points
- Each joker = 30 penalty points
- Lower scores are better!

## Important Rules to Remember 📝

1. **Table Must Stay Valid**: After your turn, every set on the table must be valid
2. **No Taking Back**: Once you've played tiles, you can't take them back to your hand
3. **Time Limits**: In friendly games, be reasonable. Don't take forever!
4. **Honesty**: In our computer game, the rules are enforced automatically

## Strategy Tips 💡

- **Save Up**: Sometimes it's better to wait and play multiple sets at once
- **Watch Others**: Pay attention to what tiles others need
- **Use Jokers Wisely**: They're powerful but worth lots of penalty points
- **Think Ahead**: Before rearranging, make sure you can complete your plan

## Common Mistakes to Avoid ❌

1. **Forgetting the 30-point rule** for your first play
2. **Making invalid sets** (like two tiles of the same color in a group)
3. **Leaving the table invalid** after rearranging
4. **Playing a joker** without saying what it represents

---

## Next Steps

Now that you know the rules:
- 🎮 [Play the game](../getting-started/running-the-game.md) and practice!
- 💻 See [how these rules become code](implementation.md)
- 🔄 Learn about [the game flow](game-flow.md) in detail

Remember: The best way to learn is by playing. Don't worry about making mistakes - the computer game won't let you make illegal moves!