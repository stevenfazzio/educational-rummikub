"""
Tile representation and deck management for Rummikub.

This module provides the core data structures for representing Rummikub tiles
and managing collections of tiles (decks, hands, etc.).
"""

from typing import List, Optional
from dataclasses import dataclass
import random


# Valid tile colors in Rummikub
TILE_COLORS = ['red', 'blue', 'black', 'orange']
JOKER_COLOR = 'joker'

# Tile numbers range from 1 to 13
MIN_TILE_NUMBER = 1
MAX_TILE_NUMBER = 13

# Standard deck composition
TILES_PER_COLOR = 2  # Each number appears twice per color
JOKERS_IN_DECK = 2
TOTAL_TILES = len(TILE_COLORS) * MAX_TILE_NUMBER * TILES_PER_COLOR + JOKERS_IN_DECK


@dataclass
class Tile:
    """
    Represents a single Rummikub tile.
    
    Attributes:
        number: The number on the tile (1-13) or 0 for jokers
        color: The color of the tile or 'joker' for joker tiles
    """
    number: int
    color: str
    
    def __post_init__(self):
        """Validate tile attributes after initialization."""
        if self.color == JOKER_COLOR:
            if self.number != 0:
                raise ValueError("Joker tiles must have number 0")
        else:
            if self.color not in TILE_COLORS:
                raise ValueError(f"Invalid color: {self.color}")
            if not (MIN_TILE_NUMBER <= self.number <= MAX_TILE_NUMBER):
                raise ValueError(f"Number must be between {MIN_TILE_NUMBER} and {MAX_TILE_NUMBER}")
    
    def __str__(self) -> str:
        """Return a readable string representation of the tile."""
        if self.is_joker():
            return "[Joker]"
        return f"[{self.number} {self.color}]"
    
    def __repr__(self) -> str:
        """Return a technical string representation for debugging."""
        return f"Tile(number={self.number}, color='{self.color}')"
    
    def is_joker(self) -> bool:
        """Check if this tile is a joker."""
        return self.color == JOKER_COLOR
    
    def get_value(self) -> int:
        """
        Get the point value of this tile.
        
        Returns:
            The tile's number for regular tiles, 30 for jokers
        """
        if self.is_joker():
            return 30
        return self.number
    
    def can_follow(self, other: 'Tile') -> bool:
        """
        Check if this tile can follow another in a run.
        
        Args:
            other: The tile that would come before this one
            
        Returns:
            True if this tile is exactly one number higher and same color
        """
        if self.is_joker() or other.is_joker():
            return True  # Jokers can go anywhere
        
        return (self.color == other.color and 
                self.number == other.number + 1)
    
    def matches_number(self, other: 'Tile') -> bool:
        """
        Check if this tile has the same number as another.
        
        Args:
            other: The tile to compare with
            
        Returns:
            True if both tiles have the same number (or either is a joker)
        """
        if self.is_joker() or other.is_joker():
            return True
        return self.number == other.number


class Deck:
    """
    Manages a collection of tiles (deck, hand, or table group).
    
    This class provides methods for common tile collection operations
    like shuffling, drawing, and adding tiles.
    """
    
    def __init__(self, tiles: Optional[List[Tile]] = None):
        """
        Initialize a deck with given tiles or empty.
        
        Args:
            tiles: Initial tiles for the deck, or None for empty deck
        """
        self.tiles = tiles if tiles is not None else []
    
    def __len__(self) -> int:
        """Return the number of tiles in the deck."""
        return len(self.tiles)
    
    def __str__(self) -> str:
        """Return a string representation of all tiles."""
        if not self.tiles:
            return "Empty deck"
        return ", ".join(str(tile) for tile in self.tiles)
    
    def __iter__(self):
        """Allow iteration over tiles in the deck."""
        return iter(self.tiles)
    
    def __getitem__(self, index: int) -> Tile:
        """Allow indexing into the deck."""
        return self.tiles[index]
    
    def add_tile(self, tile: Tile) -> None:
        """
        Add a single tile to the deck.
        
        Args:
            tile: The tile to add
        """
        self.tiles.append(tile)
    
    def add_tiles(self, tiles: List[Tile]) -> None:
        """
        Add multiple tiles to the deck.
        
        Args:
            tiles: List of tiles to add
        """
        self.tiles.extend(tiles)
    
    def remove_tile(self, tile: Tile) -> None:
        """
        Remove a specific tile from the deck.
        
        Args:
            tile: The tile to remove
            
        Raises:
            ValueError: If the tile is not in the deck
        """
        self.tiles.remove(tile)
    
    def remove_tiles(self, tiles: List[Tile]) -> None:
        """
        Remove multiple tiles from the deck.
        
        Args:
            tiles: List of tiles to remove
            
        Raises:
            ValueError: If any tile is not in the deck
        """
        for tile in tiles:
            self.remove_tile(tile)
    
    def draw_tile(self) -> Optional[Tile]:
        """
        Draw (remove and return) a tile from the deck.
        
        Returns:
            The drawn tile, or None if deck is empty
        """
        if not self.tiles:
            return None
        return self.tiles.pop()
    
    def draw_tiles(self, count: int) -> List[Tile]:
        """
        Draw multiple tiles from the deck.
        
        Args:
            count: Number of tiles to draw
            
        Returns:
            List of drawn tiles (may be less than count if deck runs out)
        """
        drawn = []
        for _ in range(count):
            tile = self.draw_tile()
            if tile is None:
                break
            drawn.append(tile)
        return drawn
    
    def shuffle(self) -> None:
        """Shuffle the tiles in the deck randomly."""
        random.shuffle(self.tiles)
    
    def sort(self, by_color: bool = True) -> None:
        """
        Sort tiles in the deck.
        
        Args:
            by_color: If True, sort by color then number. Otherwise by number then color.
        """
        if by_color:
            self.tiles.sort(key=lambda t: (t.color, t.number))
        else:
            self.tiles.sort(key=lambda t: (t.number, t.color))
    
    def get_total_value(self) -> int:
        """
        Calculate the total point value of all tiles.
        
        Returns:
            Sum of all tile values
        """
        return sum(tile.get_value() for tile in self.tiles)
    
    def has_tile(self, tile: Tile) -> bool:
        """
        Check if a specific tile is in the deck.
        
        Args:
            tile: The tile to look for
            
        Returns:
            True if the tile is in the deck
        """
        return tile in self.tiles
    
    def count_tiles(self) -> dict:
        """
        Count tiles by color.
        
        Returns:
            Dictionary mapping colors to tile counts
        """
        counts = {color: 0 for color in TILE_COLORS}
        counts[JOKER_COLOR] = 0
        
        for tile in self.tiles:
            counts[tile.color] += 1
            
        return counts
    
    def clear(self) -> None:
        """Remove all tiles from the deck."""
        self.tiles.clear()
    
    def copy(self) -> 'Deck':
        """
        Create a copy of this deck.
        
        Returns:
            A new Deck with copies of all tiles
        """
        return Deck([Tile(tile.number, tile.color) for tile in self.tiles])


def create_standard_deck() -> Deck:
    """
    Create a standard 106-tile Rummikub deck.
    
    A standard deck contains:
    - Numbers 1-13 in each of 4 colors, twice each (104 tiles)
    - 2 joker tiles
    
    Returns:
        A new deck with all standard tiles, unshuffled
    """
    tiles = []
    
    # Add numbered tiles
    for color in TILE_COLORS:
        for number in range(MIN_TILE_NUMBER, MAX_TILE_NUMBER + 1):
            # Add each tile twice
            for _ in range(TILES_PER_COLOR):
                tiles.append(Tile(number, color))
    
    # Add jokers
    for _ in range(JOKERS_IN_DECK):
        tiles.append(Tile(0, JOKER_COLOR))
    
    return Deck(tiles)


def create_tile(number: int, color: str) -> Tile:
    """
    Factory method for creating a single tile.
    
    Args:
        number: The tile number (1-13) or 0 for joker
        color: The tile color or 'joker'
        
    Returns:
        A new Tile instance
        
    Raises:
        ValueError: If the number/color combination is invalid
    """
    return Tile(number, color)


def create_joker() -> Tile:
    """
    Create a joker tile.
    
    Returns:
        A new joker Tile instance
    """
    return Tile(0, JOKER_COLOR)


def tiles_from_string(tile_string: str) -> List[Tile]:
    """
    Parse tiles from a string representation.
    
    Format: "5 red, 6 red, 7 red" or "5r,6r,7r" for short
    
    Args:
        tile_string: String representation of tiles
        
    Returns:
        List of parsed tiles
        
    Raises:
        ValueError: If the string format is invalid
    """
    tiles = []
    color_map = {'r': 'red', 'b': 'blue', 'k': 'black', 'o': 'orange', 'j': 'joker'}
    
    for part in tile_string.split(','):
        part = part.strip()
        
        # Handle long format: "5 red"
        if ' ' in part:
            number_str, color = part.split()
            if color == 'joker':
                tiles.append(create_joker())
            else:
                tiles.append(Tile(int(number_str), color))
        
        # Handle short format: "5r"
        else:
            if part[-1] == 'j':
                tiles.append(create_joker())
            else:
                number = int(part[:-1])
                color = color_map.get(part[-1])
                if color is None:
                    raise ValueError(f"Invalid color code: {part[-1]}")
                tiles.append(Tile(number, color))
    
    return tiles


if __name__ == "__main__":
    # Example usage and basic testing
    print("Creating some example tiles:")
    
    # Create individual tiles
    red_5 = create_tile(5, 'red')
    blue_5 = create_tile(5, 'blue')
    joker = create_joker()
    
    print(f"Red 5: {red_5}")
    print(f"Blue 5: {blue_5}")
    print(f"Joker: {joker}")
    print(f"Joker value: {joker.get_value()} points")
    
    # Create a deck
    print("\nCreating a standard deck:")
    deck = create_standard_deck()
    print(f"Total tiles: {len(deck)}")
    print(f"Tile counts by color: {deck.count_tiles()}")
    
    # Shuffle and draw
    deck.shuffle()
    print("\nDrawing 5 tiles:")
    hand = Deck(deck.draw_tiles(5))
    print(f"Hand: {hand}")
    print(f"Hand value: {hand.get_total_value()} points")
    
    # Parse from string
    print("\nParsing tiles from string:")
    tiles = tiles_from_string("5 red, 6 red, 7 red")
    print("Parsed:", ", ".join(str(t) for t in tiles))
    
    # Short format
    tiles_short = tiles_from_string("10b,11b,12b,13b")
    print("Short format:", ", ".join(str(t) for t in tiles_short))