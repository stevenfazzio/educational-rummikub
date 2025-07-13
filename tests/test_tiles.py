"""
Unit tests for the tiles module.

Tests tile creation, deck management, and tile operations.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiles import (
    Tile, Deck, create_standard_deck, create_tile, create_joker,
    tiles_from_string, TILE_COLORS, TOTAL_TILES
)


class TestTile(unittest.TestCase):
    """Test the Tile class."""
    
    def test_create_regular_tile(self):
        """Test creating regular numbered tiles."""
        tile = Tile(5, 'red')
        self.assertEqual(tile.number, 5)
        self.assertEqual(tile.color, 'red')
        self.assertFalse(tile.is_joker())
        self.assertEqual(tile.get_value(), 5)
    
    def test_create_joker(self):
        """Test creating joker tiles."""
        joker = Tile(0, 'joker')
        self.assertEqual(joker.number, 0)
        self.assertEqual(joker.color, 'joker')
        self.assertTrue(joker.is_joker())
        self.assertEqual(joker.get_value(), 30)
    
    def test_invalid_tile_color(self):
        """Test that invalid colors raise ValueError."""
        with self.assertRaises(ValueError):
            Tile(5, 'purple')
    
    def test_invalid_tile_number(self):
        """Test that invalid numbers raise ValueError."""
        with self.assertRaises(ValueError):
            Tile(14, 'red')  # Too high
        
        with self.assertRaises(ValueError):
            Tile(0, 'red')  # Zero for non-joker
    
    def test_invalid_joker(self):
        """Test that jokers must have number 0."""
        with self.assertRaises(ValueError):
            Tile(5, 'joker')
    
    def test_tile_string_representation(self):
        """Test string representation of tiles."""
        tile = Tile(7, 'blue')
        self.assertEqual(str(tile), "[7 blue]")
        
        joker = create_joker()
        self.assertEqual(str(joker), "[Joker]")
    
    def test_can_follow(self):
        """Test the can_follow method for runs."""
        tile5 = Tile(5, 'red')
        tile6 = Tile(6, 'red')
        tile7 = Tile(7, 'red')
        tile7_blue = Tile(7, 'blue')
        joker = create_joker()
        
        # Valid follows
        self.assertTrue(tile6.can_follow(tile5))
        self.assertTrue(tile7.can_follow(tile6))
        
        # Invalid follows
        self.assertFalse(tile5.can_follow(tile6))  # Wrong order
        self.assertFalse(tile7_blue.can_follow(tile6))  # Different color
        
        # Jokers can follow anything
        self.assertTrue(joker.can_follow(tile5))
        self.assertTrue(tile6.can_follow(joker))
    
    def test_matches_number(self):
        """Test the matches_number method for groups."""
        tile5_red = Tile(5, 'red')
        tile5_blue = Tile(5, 'blue')
        tile6_red = Tile(6, 'red')
        joker = create_joker()
        
        # Same numbers match
        self.assertTrue(tile5_red.matches_number(tile5_blue))
        
        # Different numbers don't match
        self.assertFalse(tile5_red.matches_number(tile6_red))
        
        # Jokers match anything
        self.assertTrue(joker.matches_number(tile5_red))
        self.assertTrue(tile6_red.matches_number(joker))


class TestDeck(unittest.TestCase):
    """Test the Deck class."""
    
    def test_empty_deck(self):
        """Test creating and using an empty deck."""
        deck = Deck()
        self.assertEqual(len(deck), 0)
        self.assertEqual(str(deck), "Empty deck")
        self.assertIsNone(deck.draw_tile())
    
    def test_add_remove_tiles(self):
        """Test adding and removing tiles from deck."""
        deck = Deck()
        tile1 = create_tile(5, 'red')
        tile2 = create_tile(6, 'blue')
        
        # Add tiles
        deck.add_tile(tile1)
        self.assertEqual(len(deck), 1)
        
        deck.add_tiles([tile2])
        self.assertEqual(len(deck), 2)
        
        # Remove tiles
        deck.remove_tile(tile1)
        self.assertEqual(len(deck), 1)
        
        # Try to remove non-existent tile
        with self.assertRaises(ValueError):
            deck.remove_tile(tile1)
    
    def test_draw_tiles(self):
        """Test drawing tiles from deck."""
        deck = Deck()
        tiles = [create_tile(i, 'red') for i in range(1, 6)]
        deck.add_tiles(tiles)
        
        # Draw single tile
        drawn = deck.draw_tile()
        self.assertIsNotNone(drawn)
        self.assertEqual(len(deck), 4)
        
        # Draw multiple tiles
        drawn_tiles = deck.draw_tiles(3)
        self.assertEqual(len(drawn_tiles), 3)
        self.assertEqual(len(deck), 1)
        
        # Try to draw more than available
        drawn_tiles = deck.draw_tiles(5)
        self.assertEqual(len(drawn_tiles), 1)
        self.assertEqual(len(deck), 0)
    
    def test_deck_operations(self):
        """Test various deck operations."""
        deck = Deck()
        tiles = [
            create_tile(5, 'red'),
            create_tile(3, 'blue'),
            create_tile(7, 'red'),
            create_joker()
        ]
        deck.add_tiles(tiles)
        
        # Test iteration
        count = 0
        for tile in deck:
            count += 1
        self.assertEqual(count, 4)
        
        # Test indexing
        self.assertEqual(deck[0], tiles[0])
        
        # Test has_tile
        self.assertTrue(deck.has_tile(tiles[0]))
        self.assertFalse(deck.has_tile(create_tile(10, 'black')))
        
        # Test total value
        expected_value = 5 + 3 + 7 + 30  # Joker is worth 30
        self.assertEqual(deck.get_total_value(), expected_value)
    
    def test_deck_sorting(self):
        """Test deck sorting functionality."""
        deck = Deck()
        tiles = [
            create_tile(5, 'red'),
            create_tile(3, 'blue'),
            create_tile(5, 'blue'),
            create_tile(3, 'red')
        ]
        deck.add_tiles(tiles)
        
        # Sort by color
        deck.sort(by_color=True)
        # Should be: blue tiles first, then red
        self.assertEqual(deck[0].color, 'blue')
        self.assertEqual(deck[1].color, 'blue')
        self.assertEqual(deck[2].color, 'red')
        self.assertEqual(deck[3].color, 'red')
        
        # Sort by number
        deck.sort(by_color=False)
        # Should be: 3s first, then 5s
        self.assertEqual(deck[0].number, 3)
        self.assertEqual(deck[1].number, 3)
        self.assertEqual(deck[2].number, 5)
        self.assertEqual(deck[3].number, 5)
    
    def test_deck_copy(self):
        """Test copying a deck."""
        deck1 = Deck()
        tiles = [create_tile(i, 'red') for i in range(1, 4)]
        deck1.add_tiles(tiles)
        
        deck2 = deck1.copy()
        
        # Should have same tiles
        self.assertEqual(len(deck1), len(deck2))
        
        # But be independent
        deck1.draw_tile()
        self.assertEqual(len(deck1), 2)
        self.assertEqual(len(deck2), 3)
    
    def test_count_tiles(self):
        """Test counting tiles by color."""
        deck = Deck()
        deck.add_tiles([
            create_tile(1, 'red'),
            create_tile(2, 'red'),
            create_tile(3, 'blue'),
            create_joker()
        ])
        
        counts = deck.count_tiles()
        self.assertEqual(counts['red'], 2)
        self.assertEqual(counts['blue'], 1)
        self.assertEqual(counts['black'], 0)
        self.assertEqual(counts['orange'], 0)
        self.assertEqual(counts['joker'], 1)


class TestDeckCreation(unittest.TestCase):
    """Test deck creation functions."""
    
    def test_create_standard_deck(self):
        """Test creating a standard Rummikub deck."""
        deck = create_standard_deck()
        
        # Check total number of tiles
        self.assertEqual(len(deck), TOTAL_TILES)
        
        # Check tile distribution
        counts = deck.count_tiles()
        for color in TILE_COLORS:
            # Each color should have 26 tiles (13 numbers × 2)
            self.assertEqual(counts[color], 26)
        
        # Should have 2 jokers
        self.assertEqual(counts['joker'], 2)
    
    def test_standard_deck_contents(self):
        """Test that standard deck has correct tiles."""
        deck = create_standard_deck()
        
        # Count each number/color combination
        tile_counts = {}
        for tile in deck:
            if not tile.is_joker():
                key = (tile.number, tile.color)
                tile_counts[key] = tile_counts.get(key, 0) + 1
        
        # Each number/color should appear exactly twice
        for count in tile_counts.values():
            self.assertEqual(count, 2)
        
        # Check all combinations exist
        for color in TILE_COLORS:
            for number in range(1, 14):
                key = (number, color)
                self.assertIn(key, tile_counts)


class TestTileCreation(unittest.TestCase):
    """Test tile creation helper functions."""
    
    def test_create_tile_function(self):
        """Test the create_tile helper function."""
        tile = create_tile(8, 'blue')
        self.assertEqual(tile.number, 8)
        self.assertEqual(tile.color, 'blue')
        
        # Test invalid creation
        with self.assertRaises(ValueError):
            create_tile(15, 'red')
    
    def test_create_joker_function(self):
        """Test the create_joker helper function."""
        joker = create_joker()
        self.assertEqual(joker.number, 0)
        self.assertEqual(joker.color, 'joker')
        self.assertTrue(joker.is_joker())
    
    def test_tiles_from_string(self):
        """Test parsing tiles from string representation."""
        # Test long format
        tiles = tiles_from_string("5 red, 6 red, 7 red")
        self.assertEqual(len(tiles), 3)
        self.assertEqual(tiles[0].number, 5)
        self.assertEqual(tiles[0].color, 'red')
        self.assertEqual(tiles[2].number, 7)
        
        # Test short format
        tiles = tiles_from_string("10b,11b,12b")
        self.assertEqual(len(tiles), 3)
        self.assertEqual(tiles[0].number, 10)
        self.assertEqual(tiles[0].color, 'blue')
        
        # Test mixed formats
        tiles = tiles_from_string("1 red, 2r, 3 red")
        self.assertEqual(len(tiles), 3)
        
        # Test with joker
        tiles = tiles_from_string("5r, joker, 7r")
        self.assertEqual(len(tiles), 3)
        self.assertTrue(tiles[1].is_joker())
        
        # Test short joker format
        tiles = tiles_from_string("5r,j,7r")
        self.assertEqual(len(tiles), 3)
        self.assertTrue(tiles[1].is_joker())
    
    def test_invalid_string_format(self):
        """Test invalid string formats raise errors."""
        # Invalid color code
        with self.assertRaises(ValueError):
            tiles_from_string("5x")
        
        # Invalid format
        with self.assertRaises(ValueError):
            tiles_from_string("red 5")  # Wrong order


if __name__ == '__main__':
    unittest.main()