# Testing Your Changes

Testing is how you make sure your code works correctly. Let's learn how to test like a pro!

## Why Test? 🤔

- **Catch bugs early** - Before players find them
- **Prevent breaking things** - Make sure new changes don't break old features  
- **Build confidence** - Know your code works
- **Document behavior** - Tests show how code should work

## Types of Testing 🧪

### 1. Manual Testing (Playing the Game)
The simplest way - just play and see what happens!

### 2. Unit Testing (Testing Individual Parts)
Test specific functions in isolation.

### 3. Integration Testing (Testing How Parts Work Together)
Make sure different pieces work correctly when combined.

## Manual Testing Checklist ✅

When you make changes, always check:

- [ ] Game starts without errors
- [ ] All menu options work
- [ ] Can play tiles successfully
- [ ] Invalid moves show helpful errors
- [ ] Drawing tiles works
- [ ] Winning works correctly
- [ ] Colors display properly
- [ ] No crashes during normal play

## Running Existing Tests 🏃

Our game comes with automated tests! Run them:

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_rules

# Run with details
python -m unittest discover tests/ -v
```

### Understanding Test Output

Good output:
```
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.045s

OK
```

Bad output:
```
F.....E...
======================================================================
FAIL: test_valid_group (tests.test_rules.TestValidation)
----------------------------------------------------------------------
AssertionError: False is not true
```

- `.` = Test passed
- `F` = Test failed
- `E` = Test had an error

## Writing Your First Test 📝

Let's test a simple function!

### Step 1: Create Test File
Create `tests/test_my_changes.py`:

```python
"""
Tests for my custom changes.
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiles import create_tile

class TestMyChanges(unittest.TestCase):
    """Test my custom modifications."""
    
    def test_something_simple(self):
        """Test that 1 + 1 equals 2."""
        result = 1 + 1
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
```

### Step 2: Run Your Test
```bash
python -m unittest tests.test_my_changes
```

You should see:
```
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

## Testing Your Features 🎯

### Example: Testing the Undo Feature

If you added an undo feature, here's how to test it:

```python
def test_undo_move(self):
    """Test that undo restores previous state."""
    # Create a game
    game = GameState(["Alice", "Bob"])
    game.start_game()
    
    # Save initial state
    alice = game.players[0]
    initial_tile_count = len(alice.tiles)
    
    # Make a move (draw a tile)
    move = Move(0, MoveType.DRAW)
    game.apply_move(move)
    
    # Should have one more tile
    self.assertEqual(len(alice.tiles), initial_tile_count + 1)
    
    # Undo the move
    success, message = game.undo_last_move()
    
    # Check undo worked
    self.assertTrue(success)
    self.assertEqual(len(alice.tiles), initial_tile_count)
```

### Example: Testing Color Changes

If you changed tile colors:

```python
def test_new_colors(self):
    """Test that new colors work correctly."""
    from tiles import TILE_COLORS
    
    # Check we have 4 colors
    self.assertEqual(len(TILE_COLORS), 4)
    
    # Check new colors are present
    self.assertIn('green', TILE_COLORS)
    self.assertIn('yellow', TILE_COLORS)
    
    # Create tile with new color
    tile = create_tile(5, 'green')
    self.assertEqual(tile.color, 'green')
    self.assertEqual(tile.number, 5)
```

## Test Patterns 🎨

### Pattern 1: Arrange, Act, Assert

```python
def test_pattern(self):
    # Arrange - Set up the test
    player = Player(0, "Test Player")
    tile = create_tile(5, 'red')
    
    # Act - Do the thing you're testing
    player.add_tile(tile)
    
    # Assert - Check the result
    self.assertIn(tile, player.tiles)
    self.assertEqual(len(player.tiles), 1)
```

### Pattern 2: Test Valid and Invalid Cases

```python
def test_validation(self):
    # Test valid case
    valid_tiles = [
        create_tile(5, 'red'),
        create_tile(5, 'blue'),
        create_tile(5, 'black')
    ]
    self.assertTrue(is_valid_group(valid_tiles))
    
    # Test invalid case
    invalid_tiles = [
        create_tile(5, 'red'),
        create_tile(5, 'red'),  # Duplicate color!
        create_tile(5, 'blue')
    ]
    self.assertFalse(is_valid_group(invalid_tiles))
```

### Pattern 3: Test Edge Cases

```python
def test_edge_cases(self):
    # Empty list
    self.assertFalse(is_valid_group([]))
    
    # Too few tiles
    two_tiles = [create_tile(5, 'red'), create_tile(5, 'blue')]
    self.assertFalse(is_valid_group(two_tiles))
    
    # Maximum tiles
    four_tiles = [
        create_tile(5, 'red'),
        create_tile(5, 'blue'),
        create_tile(5, 'black'),
        create_tile(5, 'orange')
    ]
    self.assertTrue(is_valid_group(four_tiles))
```

## Common Test Methods 🛠️

```python
# Check if equal
self.assertEqual(actual, expected)

# Check if not equal
self.assertNotEqual(actual, expected)

# Check if True/False
self.assertTrue(value)
self.assertFalse(value)

# Check if in collection
self.assertIn(item, collection)
self.assertNotIn(item, collection)

# Check if None
self.assertIsNone(value)
self.assertIsNotNone(value)

# Check if raises exception
with self.assertRaises(ValueError):
    do_something_that_should_fail()
```

## Testing Checklist for New Features ✓

When you add a feature, test:

- [ ] **Normal use** - Does it work as intended?
- [ ] **Edge cases** - Empty lists, None values, extremes
- [ ] **Error cases** - What happens when things go wrong?
- [ ] **Integration** - Does it work with existing features?
- [ ] **Performance** - Is it fast enough?

## Debugging Failed Tests 🔍

When a test fails:

### 1. Read the Error Message
```
AssertionError: 4 != 5
```
This tells you expected 5 but got 4.

### 2. Add Print Statements
```python
def test_something(self):
    result = calculate_value()
    print(f"Debug: result = {result}")  # Temporary!
    self.assertEqual(result, expected)
```

### 3. Run One Test at a Time
```bash
# Run just one test method
python -m unittest tests.test_game.TestGameState.test_start_game
```

### 4. Use pdb (Python Debugger)
```python
def test_complex(self):
    import pdb; pdb.set_trace()  # Stops here!
    # Now you can inspect variables
```

## Test-Driven Development (TDD) 🚦

Advanced technique: Write tests first!

1. **Red** - Write a failing test
2. **Green** - Write code to make it pass
3. **Refactor** - Clean up the code

Example:
```python
# 1. Write test first (it will fail)
def test_new_feature(self):
    result = my_new_function(5)
    self.assertEqual(result, 25)

# 2. Write minimal code to pass
def my_new_function(x):
    return x * 5  # Makes test pass

# 3. Refactor if needed
def my_new_function(x):
    """Calculate five times the input."""
    return x * 5
```

## Testing Tips 💡

### 1. Test One Thing at a Time
```python
# Good - Tests one specific thing
def test_add_tile(self):
    player.add_tile(tile)
    self.assertIn(tile, player.tiles)

# Bad - Tests too many things
def test_everything(self):
    # Tests game, player, tiles, rules...
```

### 2. Use Descriptive Names
```python
# Good
def test_initial_meld_requires_30_points(self):

# Bad  
def test_1(self):
```

### 3. Keep Tests Fast
Tests should run quickly so you run them often.

### 4. Test the Behavior, Not the Implementation
```python
# Good - Tests what it does
self.assertEqual(player.get_tile_count(), 5)

# Bad - Tests how it does it
self.assertEqual(len(player.tiles), 5)
```

## Creating Test Data 🏗️

Make helper functions for common test setups:

```python
def create_test_player(self, name="Test", tiles=None):
    """Create a player for testing."""
    player = Player(0, name)
    if tiles:
        player.add_tiles(tiles)
    return player

def create_valid_group(self):
    """Create a valid group for testing."""
    return [
        create_tile(5, 'red'),
        create_tile(5, 'blue'),
        create_tile(5, 'black')
    ]
```

---

## Practice Exercises 🎯

1. Write a test that verifies drawing a tile increases hand size
2. Test that invalid color names raise an error
3. Write tests for any features you added
4. Create a test that plays an entire game automatically

## Next Steps

- 📚 Check the [reference section](../reference/glossary.md) for testing terms
- 🎨 Study [common patterns](../reference/common-patterns.md) in our tests
- 🤝 [Contribute](../contributing.md) your well-tested features!

Remember: Good tests make good code. Test early, test often!