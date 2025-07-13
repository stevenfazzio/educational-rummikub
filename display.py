"""
Console display and user interface for Rummikub.

This module handles all console output formatting and user input,
providing a clear and intuitive interface for playing Rummikub.
"""

import os
import sys
from typing import List, Optional, Tuple, Dict
from textwrap import wrap

from tiles import Tile, Deck, TILE_COLORS
from game import GameState, Move, MoveType
from rules import is_valid_set


class Display:
    """
    Handles console display and formatting for the game.
    
    Provides methods to display game state, format tiles, and handle
    user input in a clean and consistent manner.
    """
    
    def __init__(self, use_color: bool = True, width: int = 80):
        """
        Initialize display settings.
        
        Args:
            use_color: Whether to use ANSI color codes
            width: Console width for formatting
        """
        self.use_color = use_color and self._supports_color()
        self.width = width
        self.color_codes = {
            'red': '\033[91m',
            'blue': '\033[94m',
            'black': '\033[90m',
            'orange': '\033[93m',
            'joker': '\033[95m',
            'reset': '\033[0m',
            'bold': '\033[1m',
            'underline': '\033[4m'
        }
    
    def _supports_color(self) -> bool:
        """Check if the terminal supports color output."""
        # Check for common environment variables
        if os.environ.get('NO_COLOR'):
            return False
        
        # Windows console typically supports ANSI colors in recent versions
        if sys.platform == 'win32':
            return True
        
        # Check TERM environment variable
        term = os.environ.get('TERM', '')
        return term != 'dumb' and 'color' in term.lower()
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self.use_color or color not in self.color_codes:
            return text
        
        return f"{self.color_codes[color]}{text}{self.color_codes['reset']}"
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if sys.platform == 'win32' else 'clear')
    
    def display_header(self, title: str) -> None:
        """Display a formatted header."""
        print("\n" + "=" * self.width)
        print(self._colorize(title.center(self.width), 'bold'))
        print("=" * self.width + "\n")
    
    def display_tile(self, tile: Tile) -> str:
        """
        Format a single tile for display.
        
        Args:
            tile: The tile to format
            
        Returns:
            Formatted string representation
        """
        if tile.is_joker():
            return self._colorize("[Joker]", 'joker')
        
        tile_str = f"[{tile.number} {tile.color}]"
        return self._colorize(tile_str, tile.color)
    
    def display_tiles(self, tiles: List[Tile], prefix: str = "") -> None:
        """
        Display a list of tiles in a formatted way.
        
        Args:
            tiles: List of tiles to display
            prefix: String to prefix each line with
        """
        if not tiles:
            print(f"{prefix}(No tiles)")
            return
        
        # Group tiles into lines that fit console width
        current_line = prefix
        for i, tile in enumerate(tiles):
            tile_str = f"{i+1}. {self.display_tile(tile)}  "
            
            if len(current_line) + len(tile_str) > self.width:
                print(current_line)
                current_line = prefix + "   " + tile_str
            else:
                current_line += tile_str
        
        if current_line.strip():
            print(current_line)
    
    def display_table_sets(self, table_sets: List[List[Tile]]) -> None:
        """Display all sets currently on the table."""
        if not table_sets:
            print("Table: (empty)")
            return
        
        print("Table Sets:")
        print("-" * 40)
        
        for i, tile_set in enumerate(table_sets):
            set_type = "Group" if self._is_group(tile_set) else "Run"
            print(f"{i+1}. {set_type}: ", end="")
            
            tile_strs = [self.display_tile(tile) for tile in tile_set]
            print(" ".join(tile_strs))
        
        print()
    
    def _is_group(self, tiles: List[Tile]) -> bool:
        """Determine if a set is a group (vs a run)."""
        if len(tiles) < 3:
            return False
        
        # Check if all non-joker tiles have the same number
        numbers = set()
        for tile in tiles:
            if not tile.is_joker():
                numbers.add(tile.number)
        
        return len(numbers) == 1
    
    def display_player_hand(self, player_name: str, tiles: List[Tile], 
                          show_value: bool = True) -> None:
        """
        Display a player's hand.
        
        Args:
            player_name: Name of the player
            tiles: Player's tiles
            show_value: Whether to show total hand value
        """
        print(f"\n{self._colorize(player_name + 's tiles:', 'bold')}")
        print("-" * 40)
        
        # Sort tiles for easier viewing
        sorted_tiles = sorted(tiles, key=lambda t: (t.color, t.number))
        self.display_tiles(sorted_tiles, "  ")
        
        if show_value:
            total_value = sum(tile.get_value() for tile in tiles)
            print(f"\nTotal hand value: {total_value} points")
            print(f"Tiles remaining: {len(tiles)}")
    
    def display_game_status(self, game_state: GameState) -> None:
        """Display current game status."""
        status = game_state.get_game_status()
        
        print("\nGame Status:")
        print("-" * 40)
        print(f"Turn: {status['turn_number']}")
        print(f"Current player: {self._colorize(status['current_player'], 'bold')}")
        print(f"Draw pile: {status['draw_pile_size']} tiles remaining")
        
        print("\nPlayers:")
        for player_info in status['players']:
            meld_status = "✓" if player_info['has_melded'] else "✗"
            print(f"  {player_info['name']}: {player_info['tiles_count']} tiles "
                  f"(melded: {meld_status})")
    
    def display_move_result(self, move: Move, success: bool, 
                          message: Optional[str] = None) -> None:
        """Display the result of a move."""
        if success:
            if move.move_type == MoveType.DRAW:
                print("Drew a tile from the pile.")
            elif move.move_type == MoveType.PLAY_NEW_MELD:
                print(f"Played new meld: {len(move.tiles)} tiles")
            elif move.move_type == MoveType.ADD_TO_EXISTING:
                print(f"Added {len(move.tiles)} tile(s) to existing set")
            elif move.move_type == MoveType.REARRANGE_TABLE:
                print("Rearranged table sets")
        else:
            print(self._colorize(f"Invalid move: {message}", 'red'))
    
    def get_tile_selection(self, tiles: List[Tile], 
                         prompt: str = "Select tiles (comma-separated numbers): ",
                         allow_empty: bool = False) -> List[Tile]:
        """
        Get tile selection from user input.
        
        Args:
            tiles: Available tiles to choose from
            prompt: Prompt message
            allow_empty: Whether empty selection is allowed
            
        Returns:
            List of selected tiles
        """
        while True:
            self.display_tiles(tiles)
            selection = input(prompt).strip()
            
            if not selection and allow_empty:
                return []
            
            try:
                # Parse comma-separated numbers
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                
                # Validate indices
                if all(0 <= i < len(tiles) for i in indices):
                    return [tiles[i] for i in indices]
                else:
                    print("Invalid selection. Please enter valid tile numbers.")
            except ValueError:
                print("Invalid input. Please enter comma-separated numbers.")
    
    def get_menu_choice(self, options: List[str], 
                       prompt: str = "Choose an option: ") -> int:
        """
        Display menu and get user choice.
        
        Args:
            options: List of menu options
            prompt: Prompt message
            
        Returns:
            Selected option index (0-based)
        """
        print("\nOptions:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            choice = input(prompt).strip()
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num - 1
                else:
                    print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")
    
    def display_winner(self, winner_name: str, scores: Dict[str, int]) -> None:
        """Display game winner and final scores."""
        self.display_header(f"🎉 {winner_name} Wins! 🎉")
        
        print("Final Scores (lower is better):")
        print("-" * 40)
        
        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        
        for i, (name, score) in enumerate(sorted_scores, 1):
            if score == 0:
                print(f"{i}. {self._colorize(name, 'bold')}: {score} points (Winner!)")
            else:
                print(f"{i}. {name}: {score} points")
    
    def wait_for_input(self, message: str = "Press Enter to continue...") -> None:
        """Wait for user to press Enter."""
        input(message)


class GameInterface:
    """
    High-level game interface that combines display and input handling.
    
    Provides methods for running the game loop with proper display updates.
    """
    
    def __init__(self, display: Optional[Display] = None):
        """
        Initialize game interface.
        
        Args:
            display: Display instance to use (creates default if None)
        """
        self.display = display or Display()
    
    def show_game_state(self, game_state: GameState, 
                       show_all_hands: bool = False) -> None:
        """
        Display complete game state.
        
        Args:
            game_state: Current game state
            show_all_hands: Whether to show all players' hands
        """
        self.display.clear_screen()
        self.display.display_header("Rummikub")
        
        # Show table
        self.display.display_table_sets(game_state.table_sets)
        
        # Show game status
        self.display.display_game_status(game_state)
        
        # Show current player's hand
        current_player = game_state.get_current_player()
        self.display.display_player_hand(current_player.name, 
                                       current_player.tiles)
        
        # Optionally show all hands (for debugging/spectating)
        if show_all_hands:
            print("\n" + "=" * 40 + "\n")
            for player in game_state.players:
                if player != current_player:
                    self.display.display_player_hand(player.name, 
                                                   player.tiles, 
                                                   show_value=False)
    
    def get_human_move(self, game_state: GameState, player_id: int) -> Move:
        """
        Get move from human player with full interface.
        
        Args:
            game_state: Current game state
            player_id: ID of the human player
            
        Returns:
            The player's chosen move
        """
        player = game_state.get_player_by_id(player_id)
        
        # Main menu
        options = ["Draw a tile", "Play new meld", "Add to existing set", 
                  "Rearrange table"]
        
        # Remove draw option if no tiles left
        if not game_state.can_draw():
            options.remove("Draw a tile")
        
        # Remove table manipulation options if haven't melded
        if not player.has_melded:
            options = [opt for opt in options if opt not in 
                      ["Add to existing set", "Rearrange table"]]
        
        choice = self.display.get_menu_choice(options)
        selected_option = options[choice]
        
        if selected_option == "Draw a tile":
            return Move(player_id, MoveType.DRAW)
        
        elif selected_option == "Play new meld":
            selected_tiles = self.display.get_tile_selection(
                player.tiles, 
                "Select tiles for new meld (or press Enter to cancel): ",
                allow_empty=True
            )
            
            if not selected_tiles:
                # Cancelled - show menu again
                return self.get_human_move(game_state, player_id)
            
            return Move(player_id, MoveType.PLAY_NEW_MELD, selected_tiles)
        
        elif selected_option == "Add to existing set":
            # Show table sets
            self.display.display_table_sets(game_state.table_sets)
            
            # Get target set
            set_num = int(input("Which set to add to? (number): ")) - 1
            
            # Get tiles to add
            selected_tiles = self.display.get_tile_selection(
                player.tiles,
                "Select tiles to add: "
            )
            
            return Move(player_id, MoveType.ADD_TO_EXISTING, 
                       selected_tiles, target_set_index=set_num)
        
        elif selected_option == "Rearrange table":
            print("Table rearrangement is not implemented in this interface.")
            # Go back to menu
            return self.get_human_move(game_state, player_id)


if __name__ == "__main__":
    # Example usage
    from tiles import create_tile
    
    display = Display()
    
    # Test tile display
    print("Testing tile display:")
    tiles = [
        create_tile(5, 'red'),
        create_tile(6, 'blue'),
        create_tile(7, 'black'),
        create_tile(8, 'orange'),
        create_tile(0, 'joker')
    ]
    
    for tile in tiles:
        print(f"  {display.display_tile(tile)}")
    
    # Test hand display
    print("\nTesting hand display:")
    display.display_player_hand("Alice", tiles)
    
    # Test table display
    print("\nTesting table display:")
    table_sets = [
        [create_tile(5, 'red'), create_tile(5, 'blue'), create_tile(5, 'black')],
        [create_tile(10, 'orange'), create_tile(11, 'orange'), 
         create_tile(12, 'orange'), create_tile(13, 'orange')]
    ]
    display.display_table_sets(table_sets)