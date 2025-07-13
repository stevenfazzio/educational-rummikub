"""
Rummikub rule validation and game logic.

This module implements all the rules of Rummikub, providing functions to validate
moves, check win conditions, and ensure game state consistency.
"""

from typing import List, Set, Tuple, Optional
from collections import Counter
from tiles import Tile, Deck, TILE_COLORS


# Game constants
MIN_SET_SIZE = 3
MAX_GROUP_SIZE = 4
INITIAL_MELD_THRESHOLD = 30


def is_valid_group(tiles: List[Tile]) -> bool:
    """
    Check if tiles form a valid group (same number, different colors).
    
    A valid group contains:
    - 3 or 4 tiles
    - All tiles have the same number
    - All tiles have different colors
    - At most one joker
    
    Args:
        tiles: List of tiles to validate
        
    Returns:
        True if tiles form a valid group
    """
    if not tiles:
        return False
    
    # Check size constraints
    if len(tiles) < MIN_SET_SIZE or len(tiles) > MAX_GROUP_SIZE:
        return False
    
    # Separate jokers from regular tiles
    jokers = [t for t in tiles if t.is_joker()]
    regular_tiles = [t for t in tiles if not t.is_joker()]
    
    # At most one joker allowed
    if len(jokers) > 1:
        return False
    
    # If all jokers (shouldn't happen in practice)
    if not regular_tiles:
        return False
    
    # All regular tiles must have the same number
    numbers = {t.number for t in regular_tiles}
    if len(numbers) > 1:
        return False
    
    # All tiles must have different colors
    colors = [t.color for t in regular_tiles]
    if len(colors) != len(set(colors)):
        return False
    
    # Can't have more than 4 tiles (one of each color)
    if len(tiles) > len(TILE_COLORS):
        return False
    
    return True


def is_valid_run(tiles: List[Tile]) -> bool:
    """
    Check if tiles form a valid run (consecutive numbers, same color).
    
    A valid run contains:
    - At least 3 tiles
    - Consecutive numbers (with jokers filling gaps)
    - All tiles of the same color (except jokers)
    
    Args:
        tiles: List of tiles to validate
        
    Returns:
        True if tiles form a valid run
    """
    if not tiles:
        return False
    
    # Check minimum size
    if len(tiles) < MIN_SET_SIZE:
        return False
    
    # Separate jokers from regular tiles
    jokers = [t for t in tiles if t.is_joker()]
    regular_tiles = [t for t in tiles if not t.is_joker()]
    
    # Need at least one regular tile to determine color
    if not regular_tiles:
        return False
    
    # All regular tiles must have the same color
    colors = {t.color for t in regular_tiles}
    if len(colors) > 1:
        return False
    
    run_color = regular_tiles[0].color
    
    # Sort regular tiles by number
    regular_tiles.sort(key=lambda t: t.number)
    
    # Check if we can form a consecutive sequence using jokers
    if not regular_tiles:
        return True  # All jokers (already checked we have at least 3 tiles)
    
    # Calculate gaps between consecutive regular tiles
    jokers_needed = 0
    for i in range(1, len(regular_tiles)):
        gap = regular_tiles[i].number - regular_tiles[i-1].number - 1
        if gap < 0:
            # Duplicate number in same color
            return False
        jokers_needed += gap
    
    # Check if we have enough jokers to fill gaps
    if jokers_needed > len(jokers):
        return False
    
    # Check if total length makes sense
    # (highest number - lowest number + 1) should equal total tiles
    expected_length = regular_tiles[-1].number - regular_tiles[0].number + 1
    if expected_length != len(tiles):
        return False
    
    return True


def is_valid_set(tiles: List[Tile]) -> bool:
    """
    Check if tiles form any valid set (group or run).
    
    Args:
        tiles: List of tiles to validate
        
    Returns:
        True if tiles form a valid group or run
    """
    return is_valid_group(tiles) or is_valid_run(tiles)


def can_add_tile_to_set(tile: Tile, existing_set: List[Tile]) -> Tuple[bool, Optional[List[Tile]]]:
    """
    Check if a tile can be added to an existing set.
    
    Args:
        tile: The tile to add
        existing_set: The current set of tiles
        
    Returns:
        Tuple of (can_add, new_set) where new_set is the set with tile added if valid
    """
    if not existing_set:
        return False, None
    
    # Try adding to the set and check if still valid
    new_set = existing_set + [tile]
    
    if is_valid_set(new_set):
        return True, new_set
    
    # For runs, also try inserting at different positions
    if len(existing_set) >= MIN_SET_SIZE:
        # Check if it might be a run
        jokers = [t for t in existing_set if t.is_joker()]
        regular = [t for t in existing_set if not t.is_joker()]
        
        if regular and len({t.color for t in regular}) == 1:
            # Looks like a run, try different positions
            for i in range(len(new_set)):
                test_set = new_set[:i] + [tile] + new_set[i:]
                if is_valid_run(test_set[:-1]):  # Remove the duplicate
                    return True, test_set[:-1]
    
    return False, None


def split_set(tiles: List[Tile], position: int) -> Tuple[List[Tile], List[Tile]]:
    """
    Split a set of tiles at a given position.
    
    Args:
        tiles: The set to split
        position: Where to split (tiles before this index go to first set)
        
    Returns:
        Tuple of (first_set, second_set)
    """
    return tiles[:position], tiles[position:]


def is_initial_meld_valid(tiles: List[Tile]) -> bool:
    """
    Check if tiles meet the initial meld requirement (30+ points).
    
    Args:
        tiles: List of tiles being played
        
    Returns:
        True if total value is at least 30 points
    """
    total_value = sum(tile.get_value() for tile in tiles)
    return total_value >= INITIAL_MELD_THRESHOLD


def find_all_valid_sets(tiles: List[Tile]) -> List[List[Tile]]:
    """
    Find all possible valid sets that can be formed from given tiles.
    
    This is useful for AI players to find possible moves.
    
    Args:
        tiles: List of available tiles
        
    Returns:
        List of valid sets (each set is a list of tiles)
    """
    valid_sets = []
    
    # Try all combinations of 3 or more tiles
    from itertools import combinations
    
    for size in range(MIN_SET_SIZE, min(len(tiles) + 1, 14)):  # Max practical set size
        for combo in combinations(tiles, size):
            tile_list = list(combo)
            if is_valid_set(tile_list):
                valid_sets.append(tile_list)
    
    return valid_sets


def validate_table_state(table_sets: List[List[Tile]]) -> Tuple[bool, Optional[str]]:
    """
    Validate that all sets on the table are valid.
    
    Args:
        table_sets: List of tile sets currently on the table
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    for i, tile_set in enumerate(table_sets):
        if not tile_set:
            return False, f"Set {i+1} is empty"
        
        if not is_valid_set(tile_set):
            return False, f"Set {i+1} is not a valid group or run"
    
    return True, None


def can_rearrange_table(current_sets: List[List[Tile]], 
                       new_tiles: List[Tile]) -> Tuple[bool, Optional[List[List[Tile]]]]:
    """
    Check if table can be rearranged with new tiles to form all valid sets.
    
    This is a simplified version - a full implementation would need
    more sophisticated algorithms for complex rearrangements.
    
    Args:
        current_sets: Current sets on the table
        new_tiles: New tiles being added
        
    Returns:
        Tuple of (can_rearrange, new_arrangement)
    """
    # Collect all tiles (table + new)
    all_tiles = new_tiles.copy()
    for tile_set in current_sets:
        all_tiles.extend(tile_set)
    
    # Try to form valid sets with all tiles
    # This is a simplified greedy approach
    remaining_tiles = all_tiles.copy()
    new_sets = []
    
    # First, try to preserve existing valid sets if possible
    for original_set in current_sets:
        if is_valid_set(original_set):
            # Check if we still have these tiles available
            set_tiles = []
            tiles_found = True
            for tile in original_set:
                if tile in remaining_tiles:
                    set_tiles.append(tile)
                    remaining_tiles.remove(tile)
                else:
                    tiles_found = False
                    break
            
            if tiles_found:
                new_sets.append(set_tiles)
            else:
                # Put back the tiles we removed
                remaining_tiles.extend(set_tiles)
    
    # Try to form new sets with remaining tiles
    while len(remaining_tiles) >= MIN_SET_SIZE:
        found_set = False
        
        # Try to find any valid set
        for size in range(min(len(remaining_tiles), 13), MIN_SET_SIZE - 1, -1):
            from itertools import combinations
            for combo in combinations(remaining_tiles, size):
                if is_valid_set(list(combo)):
                    new_set = list(combo)
                    new_sets.append(new_set)
                    for tile in new_set:
                        remaining_tiles.remove(tile)
                    found_set = True
                    break
            if found_set:
                break
        
        if not found_set:
            break
    
    # Check if all tiles were used
    if remaining_tiles:
        return False, None
    
    return True, new_sets


def calculate_remaining_tile_value(tiles: List[Tile]) -> int:
    """
    Calculate the total value of remaining tiles (for scoring).
    
    Args:
        tiles: List of remaining tiles
        
    Returns:
        Total point value
    """
    return sum(tile.get_value() for tile in tiles)


def is_winning_state(player_tiles: List[Tile]) -> bool:
    """
    Check if a player has won (no tiles remaining).
    
    Args:
        player_tiles: The player's current tiles
        
    Returns:
        True if the player has no tiles left
    """
    return len(player_tiles) == 0


if __name__ == "__main__":
    # Example usage and testing
    from tiles import create_tile, create_joker
    
    print("Testing Rummikub rules validation:\n")
    
    # Test valid group
    print("Valid group test:")
    group = [
        create_tile(7, 'red'),
        create_tile(7, 'blue'),
        create_tile(7, 'black')
    ]
    print(f"Tiles: {', '.join(str(t) for t in group)}")
    print(f"Is valid group: {is_valid_group(group)}")
    
    # Test invalid group (duplicate colors)
    print("\nInvalid group test (duplicate colors):")
    invalid_group = [
        create_tile(7, 'red'),
        create_tile(7, 'red'),
        create_tile(7, 'blue')
    ]
    print(f"Tiles: {', '.join(str(t) for t in invalid_group)}")
    print(f"Is valid group: {is_valid_group(invalid_group)}")
    
    # Test valid run
    print("\nValid run test:")
    run = [
        create_tile(5, 'blue'),
        create_tile(6, 'blue'),
        create_tile(7, 'blue'),
        create_tile(8, 'blue')
    ]
    print(f"Tiles: {', '.join(str(t) for t in run)}")
    print(f"Is valid run: {is_valid_run(run)}")
    
    # Test run with joker
    print("\nRun with joker test:")
    run_with_joker = [
        create_tile(10, 'red'),
        create_joker(),
        create_tile(12, 'red'),
        create_tile(13, 'red')
    ]
    print(f"Tiles: {', '.join(str(t) for t in run_with_joker)}")
    print(f"Is valid run: {is_valid_run(run_with_joker)}")
    
    # Test initial meld
    print("\nInitial meld test:")
    initial_meld = [
        create_tile(10, 'red'),
        create_tile(10, 'blue'),
        create_tile(10, 'black')
    ]
    print(f"Tiles: {', '.join(str(t) for t in initial_meld)}")
    print(f"Total value: {sum(t.get_value() for t in initial_meld)}")
    print(f"Meets initial meld requirement: {is_initial_meld_valid(initial_meld)}")