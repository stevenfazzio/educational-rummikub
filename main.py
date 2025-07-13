"""
Main entry point for the Rummikub game.

This module provides the command-line interface and game loop for playing
Rummikub with multiple human players.
"""

import argparse
import sys
from typing import List, Optional

from game import GameState, GamePhase
from player import Player
from display import Display, GameInterface


class RummikubGame:
    """
    Main game controller that manages the game flow.
    
    Handles game setup, player management, and the main game loop.
    """
    
    def __init__(self, display: Optional[Display] = None):
        """
        Initialize the game controller.
        
        Args:
            display: Display instance for output (creates default if None)
        """
        self.display = display or Display()
        self.interface = GameInterface(self.display)
        self.game_state = None
    
    def setup_game(self, player_names: List[str], 
                   initial_hand_size: int = 14) -> None:
        """
        Set up a new game with specified players.
        
        Args:
            player_names: List of player names
            initial_hand_size: Number of tiles each player starts with
        """
        # Create game state with player names
        self.game_state = GameState(player_names, initial_hand_size)
    
    def run_game(self) -> None:
        """Run the main game loop."""
        if not self.game_state:
            raise RuntimeError("Game not properly set up")
        
        # Start the game
        self.game_state.start_game()
        
        # Main game loop
        while self.game_state.phase == GamePhase.IN_PROGRESS:
            # Display current state
            self.interface.show_game_state(self.game_state)
            
            # Get current player
            current_player = self.game_state.get_current_player()
            
            # Get move from human player
            print(f"\n{current_player.name}'s turn")
            move = self.interface.get_human_move(
                self.game_state, 
                current_player.player_id
            )
            
            # Apply the move
            success, error = self.game_state.apply_move(move)
            
            # Display result
            self.display.display_move_result(move, success, error)
            
            # If move failed, retry
            if not success:
                self.display.wait_for_input()
                continue
            
            # Pause between turns
            if success:
                self.display.wait_for_input()
        
        # Game ended - show results
        self.show_game_results()
    
    def show_game_results(self) -> None:
        """Display final game results and scores."""
        if self.game_state.winner:
            scores = self.game_state.get_scores()
            self.display.display_winner(self.game_state.winner.name, scores)
        else:
            print("Game ended without a winner.")
    
    def run_menu(self) -> None:
        """Run the main menu interface."""
        while True:
            self.display.clear_screen()
            self.display.display_header("Rummikub - Main Menu")
            
            options = [
                "Quick Game (2 Players)",
                "Custom Game (2-4 Players)",
                "How to Play",
                "Exit"
            ]
            
            choice = self.display.get_menu_choice(options)
            
            if choice == 0:  # Quick Game
                self.quick_game()
            elif choice == 1:  # Custom Game
                self.custom_game()
            elif choice == 2:  # How to Play
                self.show_instructions()
            else:  # Exit
                print("Thanks for playing!")
                break
    
    def quick_game(self) -> None:
        """Start a quick 2-player game."""
        print("\nQuick Game Setup")
        print("-" * 40)
        
        # Get player names
        name1 = input("Player 1 name: ").strip() or "Player 1"
        name2 = input("Player 2 name: ").strip() or "Player 2"
        
        self.setup_game([name1, name2])
        self.run_game()
        self.display.wait_for_input("\nPress Enter to return to menu...")
    
    def custom_game(self) -> None:
        """Set up a custom game with user-specified players."""
        self.display.clear_screen()
        self.display.display_header("Custom Game Setup")
        
        # Get number of players
        num_players = 0
        while num_players < 2 or num_players > 4:
            try:
                num_players = int(input("Number of players (2-4): "))
                if num_players < 2 or num_players > 4:
                    print("Please enter a number between 2 and 4")
            except ValueError:
                print("Please enter a valid number")
        
        # Get player names
        player_names = []
        for i in range(num_players):
            name = input(f"Player {i+1} name: ").strip() or f"Player {i+1}"
            player_names.append(name)
        
        # Start the game
        self.setup_game(player_names)
        self.run_game()
        self.display.wait_for_input("\nPress Enter to return to menu...")
    
    def show_instructions(self) -> None:
        """Display game instructions."""
        self.display.clear_screen()
        self.display.display_header("How to Play Rummikub")
        
        instructions = """
Rummikub Rules:

OBJECTIVE:
Be the first player to play all your tiles.

TILES:
- 104 numbered tiles (1-13 in 4 colors: red, blue, black, orange)
- 2 joker tiles (can substitute any tile)

VALID SETS:
1. Groups: 3-4 tiles of the same number, different colors
   Example: [7 red] [7 blue] [7 black]

2. Runs: 3+ consecutive numbers of the same color
   Example: [5 blue] [6 blue] [7 blue] [8 blue]

GAMEPLAY:
1. Each player starts with 14 tiles
2. On your turn, you can:
   - Play valid sets from your hand
   - Add tiles to existing sets on the table
   - Rearrange table tiles to play your tiles
   - Draw a tile if you can't/won't play

INITIAL MELD:
Your first play must total at least 30 points.
(Jokers count as the tile they replace)

WINNING:
First player to play all their tiles wins!
Other players get penalty points for remaining tiles.

TIPS:
- Sort your tiles by color or number to spot patterns
- Plan ahead - sometimes it's better to wait
- Watch what other players need
- Remember: you can rearrange the table!

Press Enter to return to menu...
"""
        print(instructions)
        input()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Play Rummikub in the console",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    parser.add_argument(
        '--players',
        type=str,
        help='Comma-separated list of player names (e.g., "Alice,Bob,Charlie")'
    )
    
    parser.add_argument(
        '--hand-size',
        type=int,
        default=14,
        help='Initial hand size (default: 14)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Create display with color preference
    display = Display(use_color=not args.no_color)
    game = RummikubGame(display)
    
    try:
        if args.players:
            # Start game directly with provided players
            player_names = [name.strip() for name in args.players.split(',')]
            
            if len(player_names) < 2:
                print("Error: Need at least 2 players")
                sys.exit(1)
            elif len(player_names) > 4:
                print("Error: Maximum 4 players allowed")
                sys.exit(1)
            
            game.setup_game(player_names, args.hand_size)
            game.run_game()
        else:
            # Run interactive menu
            game.run_menu()
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()