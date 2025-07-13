"""
Unit tests for the player module.

Tests the Player class functionality.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiles import create_tile, create_joker
from player import Player


class TestPlayer(unittest.TestCase):
    """Test the Player class."""
    
    def test_player_creation(self):
        """Test creating a player."""
        player = Player(0, "Alice")
        self.assertEqual(player.player_id, 0)
        self.assertEqual(player.name, "Alice")
        self.assertEqual(len(player.tiles), 0)
        self.assertFalse(player.has_melded)
    
    def test_add_tile(self):
        """Test adding a single tile."""
        player = Player(0, "Bob")
        tile = create_tile(5, 'red')
        
        player.add_tile(tile)
        self.assertEqual(len(player.tiles), 1)
        self.assertEqual(player.tiles[0], tile)
    
    def test_add_tiles(self):
        """Test adding multiple tiles."""
        player = Player(0, "Charlie")
        tiles = [
            create_tile(5, 'red'),
            create_tile(6, 'blue'),
            create_tile(7, 'black')
        ]
        
        player.add_tiles(tiles)
        self.assertEqual(len(player.tiles), 3)
        self.assertEqual(player.tiles, tiles)
    
    def test_remove_tile(self):
        """Test removing a single tile."""
        player = Player(0, "Diana")
        tile1 = create_tile(5, 'red')
        tile2 = create_tile(6, 'blue')
        
        player.add_tiles([tile1, tile2])
        player.remove_tile(tile1)
        
        self.assertEqual(len(player.tiles), 1)
        self.assertEqual(player.tiles[0], tile2)
    
    def test_remove_tile_not_in_hand(self):
        """Test removing a tile that's not in hand raises error."""
        player = Player(0, "Eve")
        tile = create_tile(5, 'red')
        
        with self.assertRaises(ValueError):
            player.remove_tile(tile)
    
    def test_remove_tiles(self):
        """Test removing multiple tiles."""
        player = Player(0, "Frank")
        tiles = [
            create_tile(5, 'red'),
            create_tile(6, 'blue'),
            create_tile(7, 'black')
        ]
        player.add_tiles(tiles)
        
        # Remove first and last tile
        player.remove_tiles([tiles[0], tiles[2]])
        
        self.assertEqual(len(player.tiles), 1)
        self.assertEqual(player.tiles[0], tiles[1])
    
    def test_has_tile(self):
        """Test checking if player has a specific tile."""
        player = Player(0, "Grace")
        tile1 = create_tile(5, 'red')
        tile2 = create_tile(6, 'blue')
        
        player.add_tile(tile1)
        
        self.assertTrue(player.has_tile(tile1))
        self.assertFalse(player.has_tile(tile2))
    
    def test_has_tiles(self):
        """Test checking if player has multiple tiles."""
        player = Player(0, "Henry")
        tiles = [
            create_tile(5, 'red'),
            create_tile(6, 'blue'),
            create_tile(7, 'black')
        ]
        player.add_tiles(tiles)
        
        # Has these tiles
        self.assertTrue(player.has_tiles([tiles[0], tiles[1]]))
        self.assertTrue(player.has_tiles(tiles))
        
        # Doesn't have this tile
        self.assertFalse(player.has_tiles([create_tile(8, 'orange')]))
        
        # Doesn't have duplicate of existing tile
        self.assertFalse(player.has_tiles([tiles[0], tiles[0]]))
    
    def test_get_tile_count(self):
        """Test getting tile count."""
        player = Player(0, "Ivy")
        self.assertEqual(player.get_tile_count(), 0)
        
        player.add_tiles([
            create_tile(5, 'red'),
            create_tile(6, 'blue')
        ])
        self.assertEqual(player.get_tile_count(), 2)
    
    def test_get_hand_value(self):
        """Test calculating hand value."""
        player = Player(0, "Jack")
        player.add_tiles([
            create_tile(5, 'red'),      # 5 points
            create_tile(10, 'blue'),     # 10 points
            create_joker()               # 30 points
        ])
        
        self.assertEqual(player.get_hand_value(), 45)
    
    def test_empty_hand_value(self):
        """Test hand value for empty hand."""
        player = Player(0, "Kate")
        self.assertEqual(player.get_hand_value(), 0)
    
    def test_sort_tiles_by_color(self):
        """Test sorting tiles by color."""
        player = Player(0, "Liam")
        player.add_tiles([
            create_tile(5, 'red'),
            create_tile(3, 'blue'),
            create_tile(7, 'red'),
            create_tile(2, 'blue')
        ])
        
        player.sort_tiles(by_color=True)
        
        # Should be sorted: blue tiles first, then red
        self.assertEqual(player.tiles[0].color, 'blue')
        self.assertEqual(player.tiles[1].color, 'blue')
        self.assertEqual(player.tiles[2].color, 'red')
        self.assertEqual(player.tiles[3].color, 'red')
        
        # Within same color, sorted by number
        self.assertEqual(player.tiles[0].number, 2)
        self.assertEqual(player.tiles[1].number, 3)
    
    def test_sort_tiles_by_number(self):
        """Test sorting tiles by number."""
        player = Player(0, "Mia")
        player.add_tiles([
            create_tile(5, 'red'),
            create_tile(3, 'blue'),
            create_tile(5, 'blue'),
            create_tile(3, 'red')
        ])
        
        player.sort_tiles(by_color=False)
        
        # Should be sorted by number first
        self.assertEqual(player.tiles[0].number, 3)
        self.assertEqual(player.tiles[1].number, 3)
        self.assertEqual(player.tiles[2].number, 5)
        self.assertEqual(player.tiles[3].number, 5)
    
    def test_string_representation(self):
        """Test string representation of player."""
        player = Player(0, "Noah")
        self.assertEqual(str(player), "Noah (0 tiles)")
        
        player.add_tiles([
            create_tile(5, 'red'),
            create_tile(6, 'blue')
        ])
        self.assertEqual(str(player), "Noah (2 tiles)")
    
    def test_repr(self):
        """Test technical representation of player."""
        player = Player(0, "Olivia")
        player.has_melded = True
        player.add_tile(create_tile(5, 'red'))
        
        repr_str = repr(player)
        self.assertIn("Player(", repr_str)
        self.assertIn("id=0", repr_str)
        self.assertIn("name='Olivia'", repr_str)
        self.assertIn("tiles=1", repr_str)
        self.assertIn("has_melded=True", repr_str)
    
    def test_has_melded_flag(self):
        """Test the has_melded flag."""
        player = Player(0, "Peter")
        self.assertFalse(player.has_melded)
        
        player.has_melded = True
        self.assertTrue(player.has_melded)


if __name__ == '__main__':
    unittest.main()