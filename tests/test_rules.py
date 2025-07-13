"""
Unit tests for the rules module.

Tests game rule validation including groups, runs, and game logic.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiles import create_tile, create_joker
from rules import (
    is_valid_group, is_valid_run, is_valid_set,
    can_add_tile_to_set, split_set, is_initial_meld_valid,
    find_all_valid_sets, validate_table_state, can_rearrange_table,
    calculate_remaining_tile_value, is_winning_state,
    MIN_SET_SIZE, MAX_GROUP_SIZE, INITIAL_MELD_THRESHOLD
)


class TestValidGroup(unittest.TestCase):
    """Test group validation rules."""
    
    def test_valid_groups(self):
        """Test various valid group configurations."""
        # Basic valid group
        group = [
            create_tile(7, 'red'),
            create_tile(7, 'blue'),
            create_tile(7, 'black')
        ]
        self.assertTrue(is_valid_group(group))
        
        # Group of 4
        group = [
            create_tile(10, 'red'),
            create_tile(10, 'blue'),
            create_tile(10, 'black'),
            create_tile(10, 'orange')
        ]
        self.assertTrue(is_valid_group(group))
        
        # Group with joker
        group = [
            create_tile(3, 'red'),
            create_tile(3, 'blue'),
            create_joker()
        ]
        self.assertTrue(is_valid_group(group))
    
    def test_invalid_groups(self):
        """Test various invalid group configurations."""
        # Too few tiles
        group = [
            create_tile(5, 'red'),
            create_tile(5, 'blue')
        ]
        self.assertFalse(is_valid_group(group))
        
        # Too many tiles
        group = [
            create_tile(5, 'red'),
            create_tile(5, 'blue'),
            create_tile(5, 'black'),
            create_tile(5, 'orange'),
            create_tile(5, 'red')  # Duplicate color!
        ]
        self.assertFalse(is_valid_group(group))
        
        # Different numbers
        group = [
            create_tile(5, 'red'),
            create_tile(6, 'blue'),
            create_tile(7, 'black')
        ]
        self.assertFalse(is_valid_group(group))
        
        # Duplicate colors
        group = [
            create_tile(8, 'red'),
            create_tile(8, 'red'),
            create_tile(8, 'blue')
        ]
        self.assertFalse(is_valid_group(group))
        
        # Too many jokers
        group = [
            create_tile(9, 'red'),
            create_joker(),
            create_joker()
        ]
        self.assertFalse(is_valid_group(group))
        
        # Empty group
        self.assertFalse(is_valid_group([]))


class TestValidRun(unittest.TestCase):
    """Test run validation rules."""
    
    def test_valid_runs(self):
        """Test various valid run configurations."""
        # Basic valid run
        run = [
            create_tile(5, 'blue'),
            create_tile(6, 'blue'),
            create_tile(7, 'blue')
        ]
        self.assertTrue(is_valid_run(run))
        
        # Longer run
        run = [
            create_tile(8, 'red'),
            create_tile(9, 'red'),
            create_tile(10, 'red'),
            create_tile(11, 'red'),
            create_tile(12, 'red')
        ]
        self.assertTrue(is_valid_run(run))
        
        # Run with joker in middle
        run = [
            create_tile(3, 'black'),
            create_joker(),
            create_tile(5, 'black')
        ]
        self.assertTrue(is_valid_run(run))
        
        # Run with joker at end
        run = [
            create_tile(11, 'orange'),
            create_tile(12, 'orange'),
            create_joker()
        ]
        self.assertTrue(is_valid_run(run))
    
    def test_invalid_runs(self):
        """Test various invalid run configurations."""
        # Too few tiles
        run = [
            create_tile(5, 'red'),
            create_tile(6, 'red')
        ]
        self.assertFalse(is_valid_run(run))
        
        # Non-consecutive numbers
        run = [
            create_tile(5, 'blue'),
            create_tile(6, 'blue'),
            create_tile(8, 'blue')  # Skips 7
        ]
        self.assertFalse(is_valid_run(run))
        
        # Different colors
        run = [
            create_tile(5, 'red'),
            create_tile(6, 'blue'),
            create_tile(7, 'black')
        ]
        self.assertFalse(is_valid_run(run))
        
        # Duplicate numbers
        run = [
            create_tile(5, 'red'),
            create_tile(5, 'red'),
            create_tile(6, 'red')
        ]
        self.assertFalse(is_valid_run(run))
        
        # Too many jokers for gap
        run = [
            create_tile(1, 'red'),
            create_joker(),
            create_tile(5, 'red')  # Gap of 3, but only 1 joker
        ]
        self.assertFalse(is_valid_run(run))
        
        # All jokers
        run = [create_joker(), create_joker(), create_joker()]
        self.assertFalse(is_valid_run(run))


class TestValidSet(unittest.TestCase):
    """Test general set validation."""
    
    def test_is_valid_set(self):
        """Test that is_valid_set accepts both groups and runs."""
        # Valid group
        group = [
            create_tile(5, 'red'),
            create_tile(5, 'blue'),
            create_tile(5, 'black')
        ]
        self.assertTrue(is_valid_set(group))
        
        # Valid run
        run = [
            create_tile(10, 'orange'),
            create_tile(11, 'orange'),
            create_tile(12, 'orange')
        ]
        self.assertTrue(is_valid_set(run))
        
        # Invalid set
        invalid = [
            create_tile(5, 'red'),
            create_tile(6, 'blue'),
            create_tile(7, 'black')
        ]
        self.assertFalse(is_valid_set(invalid))


class TestSetManipulation(unittest.TestCase):
    """Test set manipulation functions."""
    
    def test_can_add_tile_to_set(self):
        """Test adding tiles to existing sets."""
        # Add to group
        group = [
            create_tile(8, 'red'),
            create_tile(8, 'blue'),
            create_tile(8, 'black')
        ]
        new_tile = create_tile(8, 'orange')
        can_add, new_set = can_add_tile_to_set(new_tile, group)
        self.assertTrue(can_add)
        self.assertEqual(len(new_set), 4)
        
        # Can't add duplicate color
        bad_tile = create_tile(8, 'red')
        can_add, new_set = can_add_tile_to_set(bad_tile, group)
        self.assertFalse(can_add)
        self.assertIsNone(new_set)
        
        # Add to run
        run = [
            create_tile(5, 'blue'),
            create_tile(6, 'blue'),
            create_tile(7, 'blue')
        ]
        new_tile = create_tile(8, 'blue')
        can_add, new_set = can_add_tile_to_set(new_tile, run)
        self.assertTrue(can_add)
        
        # Add at beginning of run
        new_tile = create_tile(4, 'blue')
        can_add, new_set = can_add_tile_to_set(new_tile, run)
        self.assertTrue(can_add)
    
    def test_split_set(self):
        """Test splitting sets."""
        tiles = [
            create_tile(5, 'red'),
            create_tile(6, 'red'),
            create_tile(7, 'red'),
            create_tile(8, 'red')
        ]
        
        first, second = split_set(tiles, 2)
        self.assertEqual(len(first), 2)
        self.assertEqual(len(second), 2)
        self.assertEqual(first[0].number, 5)
        self.assertEqual(second[0].number, 7)


class TestInitialMeld(unittest.TestCase):
    """Test initial meld validation."""
    
    def test_initial_meld_valid(self):
        """Test valid initial melds."""
        # Exactly 30 points
        meld = [
            create_tile(10, 'red'),
            create_tile(10, 'blue'),
            create_tile(10, 'black')
        ]
        self.assertTrue(is_initial_meld_valid(meld))
        
        # More than 30 points
        meld = [
            create_tile(11, 'red'),
            create_tile(12, 'red'),
            create_tile(13, 'red')
        ]
        self.assertTrue(is_initial_meld_valid(meld))
        
        # With joker (counts as 30)
        meld = [create_joker()]
        self.assertTrue(is_initial_meld_valid(meld))
    
    def test_initial_meld_invalid(self):
        """Test invalid initial melds."""
        # Less than 30 points
        meld = [
            create_tile(7, 'red'),
            create_tile(7, 'blue'),
            create_tile(7, 'black')
        ]
        self.assertFalse(is_initial_meld_valid(meld))
        
        # Empty meld
        self.assertFalse(is_initial_meld_valid([]))


class TestFindValidSets(unittest.TestCase):
    """Test finding valid sets from tiles."""
    
    def test_find_all_valid_sets(self):
        """Test finding all possible valid sets."""
        tiles = [
            create_tile(5, 'red'),
            create_tile(5, 'blue'),
            create_tile(5, 'black'),
            create_tile(6, 'red'),
            create_tile(7, 'red')
        ]
        
        valid_sets = find_all_valid_sets(tiles)
        
        # Should find the group of 5s and the run
        self.assertGreater(len(valid_sets), 0)
        
        # Check that group of 5s is found
        group_found = False
        run_found = False
        
        for tile_set in valid_sets:
            if len(tile_set) == 3 and all(t.number == 5 for t in tile_set):
                group_found = True
            if (len(tile_set) == 3 and 
                tile_set[0].number == 5 and 
                tile_set[1].number == 6 and 
                tile_set[2].number == 7):
                run_found = True
        
        self.assertTrue(group_found)
        self.assertTrue(run_found)


class TestTableValidation(unittest.TestCase):
    """Test table state validation."""
    
    def test_validate_table_state(self):
        """Test validating entire table state."""
        # Valid table
        table = [
            [
                create_tile(5, 'red'),
                create_tile(5, 'blue'),
                create_tile(5, 'black')
            ],
            [
                create_tile(10, 'orange'),
                create_tile(11, 'orange'),
                create_tile(12, 'orange')
            ]
        ]
        
        is_valid, error = validate_table_state(table)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # Invalid table (one bad set)
        table = [
            [
                create_tile(5, 'red'),
                create_tile(5, 'blue'),
                create_tile(5, 'black')
            ],
            [
                create_tile(10, 'orange'),
                create_tile(11, 'blue')  # Wrong color!
            ]
        ]
        
        is_valid, error = validate_table_state(table)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        self.assertIn("Set 2", error)
        
        # Empty set in table
        table = [
            [create_tile(5, 'red'), create_tile(5, 'blue'), create_tile(5, 'black')],
            []
        ]
        
        is_valid, error = validate_table_state(table)
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())


class TestTableRearrangement(unittest.TestCase):
    """Test table rearrangement logic."""
    
    def test_simple_rearrangement(self):
        """Test simple table rearrangement."""
        # Current table has a group
        current_sets = [
            [
                create_tile(5, 'red'),
                create_tile(5, 'blue'),
                create_tile(5, 'black')
            ]
        ]
        
        # Player wants to add orange 5 to make it a group of 4
        new_tiles = [create_tile(5, 'orange')]
        
        can_rearrange, new_arrangement = can_rearrange_table(current_sets, new_tiles)
        self.assertTrue(can_rearrange)
        self.assertIsNotNone(new_arrangement)
        
        # Should have one set with 4 tiles
        self.assertEqual(len(new_arrangement), 1)
        self.assertEqual(len(new_arrangement[0]), 4)


class TestGameLogic(unittest.TestCase):
    """Test general game logic functions."""
    
    def test_calculate_remaining_tile_value(self):
        """Test calculating value of remaining tiles."""
        tiles = [
            create_tile(5, 'red'),
            create_tile(10, 'blue'),
            create_joker()
        ]
        
        value = calculate_remaining_tile_value(tiles)
        self.assertEqual(value, 5 + 10 + 30)  # 45 total
        
        # Empty hand
        self.assertEqual(calculate_remaining_tile_value([]), 0)
    
    def test_is_winning_state(self):
        """Test win condition checking."""
        # No tiles = win
        self.assertTrue(is_winning_state([]))
        
        # Has tiles = not win
        tiles = [create_tile(5, 'red')]
        self.assertFalse(is_winning_state(tiles))


if __name__ == '__main__':
    unittest.main()