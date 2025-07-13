"""
Player class for Rummikub.

This module provides a simple Player class that tracks player state
during a game of Rummikub.
"""

from typing import List
from tiles import Tile


class Player:
    """
    Represents a player in the Rummikub game.
    
    This class tracks the player's state including their tiles,
    whether they've made their initial meld, and their score.
    """
    
    def __init__(self, player_id: int, name: str):
        """
        Initialize a new player.
        
        Args:
            player_id: Unique identifier for the player
            name: The player's display name
        """
        self.player_id = player_id
        self.name = name
        self.tiles: List[Tile] = []
        self.has_melded = False
    
    def add_tile(self, tile: Tile) -> None:
        """
        Add a tile to the player's hand.
        
        Args:
            tile: The tile to add
        """
        self.tiles.append(tile)
    
    def add_tiles(self, tiles: List[Tile]) -> None:
        """
        Add multiple tiles to the player's hand.
        
        Args:
            tiles: List of tiles to add
        """
        self.tiles.extend(tiles)
    
    def remove_tile(self, tile: Tile) -> None:
        """
        Remove a tile from the player's hand.
        
        Args:
            tile: The tile to remove
            
        Raises:
            ValueError: If the tile is not in the player's hand
        """
        self.tiles.remove(tile)
    
    def remove_tiles(self, tiles: List[Tile]) -> None:
        """
        Remove multiple tiles from the player's hand.
        
        Args:
            tiles: List of tiles to remove
            
        Raises:
            ValueError: If any tile is not in the player's hand
        """
        for tile in tiles:
            self.remove_tile(tile)
    
    def has_tile(self, tile: Tile) -> bool:
        """
        Check if the player has a specific tile.
        
        Args:
            tile: The tile to check for
            
        Returns:
            True if the player has the tile
        """
        return tile in self.tiles
    
    def has_tiles(self, tiles: List[Tile]) -> bool:
        """
        Check if the player has all specified tiles.
        
        Args:
            tiles: List of tiles to check for
            
        Returns:
            True if the player has all the tiles
        """
        tiles_copy = self.tiles.copy()
        for tile in tiles:
            if tile in tiles_copy:
                tiles_copy.remove(tile)
            else:
                return False
        return True
    
    def get_tile_count(self) -> int:
        """
        Get the number of tiles in the player's hand.
        
        Returns:
            Number of tiles
        """
        return len(self.tiles)
    
    def get_hand_value(self) -> int:
        """
        Calculate the total point value of tiles in hand.
        
        Returns:
            Sum of all tile values
        """
        return sum(tile.get_value() for tile in self.tiles)
    
    def sort_tiles(self, by_color: bool = True) -> None:
        """
        Sort the player's tiles for easier viewing.
        
        Args:
            by_color: If True, sort by color then number. Otherwise by number then color.
        """
        if by_color:
            self.tiles.sort(key=lambda t: (t.color, t.number))
        else:
            self.tiles.sort(key=lambda t: (t.number, t.color))
    
    def __str__(self) -> str:
        """String representation of the player."""
        return f"{self.name} ({len(self.tiles)} tiles)"
    
    def __repr__(self) -> str:
        """Technical representation for debugging."""
        return f"Player(id={self.player_id}, name='{self.name}', tiles={len(self.tiles)}, has_melded={self.has_melded})"


if __name__ == "__main__":
    # Example usage
    from tiles import create_tile, create_joker
    
    print("Creating a player and managing their tiles:\n")
    
    # Create a player
    player = Player(0, "Alice")
    print(f"Created player: {player}")
    
    # Give them some tiles
    tiles = [
        create_tile(5, 'red'),
        create_tile(5, 'blue'),
        create_tile(5, 'black'),
        create_tile(7, 'red'),
        create_tile(8, 'red'),
        create_joker()
    ]
    
    player.add_tiles(tiles)
    print(f"\nAfter adding tiles: {player}")
    print(f"Hand value: {player.get_hand_value()} points")
    
    # Sort tiles
    player.sort_tiles()
    print("\nTiles sorted by color:")
    for i, tile in enumerate(player.tiles, 1):
        print(f"  {i}. {tile}")
    
    # Check for tiles
    check_tile = create_tile(5, 'red')
    print(f"\nDoes player have {check_tile}? {player.has_tile(check_tile)}")
    
    # Remove some tiles (simulating a play)
    tiles_to_play = [tiles[0], tiles[1], tiles[2]]  # The three 5s
    print(f"\nPlaying tiles: {', '.join(str(t) for t in tiles_to_play)}")
    player.remove_tiles(tiles_to_play)
    player.has_melded = True
    
    print(f"After playing: {player}")
    print(f"Has melded: {player.has_melded}")