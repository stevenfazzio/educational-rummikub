"""
Game state management and core game logic for Rummikub.

This module manages the overall game state, handles turns, validates moves,
and enforces game rules throughout play.
"""

from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random

from tiles import Tile, Deck, create_standard_deck
from rules import (
    is_valid_set, is_initial_meld_valid, validate_table_state,
    can_rearrange_table, is_winning_state, calculate_remaining_tile_value
)
from player import Player


class GamePhase(Enum):
    """Represents different phases of the game."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class MoveType(Enum):
    """Types of moves a player can make."""
    DRAW = "draw"
    PLAY_NEW_MELD = "play_new_meld"
    ADD_TO_EXISTING = "add_to_existing"
    REARRANGE_TABLE = "rearrange_table"


@dataclass
class Move:
    """Represents a player's move."""
    player_id: int
    move_type: MoveType
    tiles: List[Tile] = field(default_factory=list)
    target_set_index: Optional[int] = None
    new_table_arrangement: Optional[List[List[Tile]]] = None


class GameState:
    """
    Manages the complete state of a Rummikub game.
    
    This class tracks all game information including players, the table,
    the draw pile, and enforces game rules.
    """
    
    def __init__(self, player_names: List[str], 
                 initial_hand_size: int = 14,
                 random_seed: Optional[int] = None):
        """
        Initialize a new game.
        
        Args:
            player_names: Names of players in the game
            initial_hand_size: Number of tiles each player starts with
            random_seed: Seed for randomization (useful for testing)
        """
        if random_seed is not None:
            random.seed(random_seed)
        
        self.phase = GamePhase.NOT_STARTED
        self.players: List[Player] = []
        self.current_player_index = 0
        self.draw_pile = Deck()
        self.table_sets: List[List[Tile]] = []
        self.turn_number = 0
        self.initial_hand_size = initial_hand_size
        self.last_move: Optional[Move] = None
        self.winner: Optional[Player] = None
        
        # Initialize players
        for i, name in enumerate(player_names):
            self.players.append(Player(player_id=i, name=name))
    
    def start_game(self) -> None:
        """
        Start the game by dealing initial tiles.
        
        Creates a shuffled deck and deals the initial hand to each player.
        """
        if self.phase != GamePhase.NOT_STARTED:
            raise ValueError("Game has already started")
        
        # Create and shuffle deck
        self.draw_pile = create_standard_deck()
        self.draw_pile.shuffle()
        
        # Deal initial tiles to each player
        for player in self.players:
            initial_tiles = self.draw_pile.draw_tiles(self.initial_hand_size)
            player.add_tiles(initial_tiles)
        
        self.phase = GamePhase.IN_PROGRESS
        self.turn_number = 1
    
    def get_current_player(self) -> Player:
        """Get the player whose turn it is."""
        return self.players[self.current_player_index]
    
    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """Get a player by their ID."""
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def validate_move(self, move: Move) -> Tuple[bool, Optional[str]]:
        """
        Validate if a move is legal in the current game state.
        
        Args:
            move: The move to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if it's the right player's turn
        current_player = self.get_current_player()
        if move.player_id != current_player.player_id:
            return False, "Not your turn"
        
        player = self.get_player_by_id(move.player_id)
        if not player:
            return False, "Invalid player"
        
        # Validate based on move type
        if move.move_type == MoveType.DRAW:
            if len(self.draw_pile) == 0:
                return False, "Draw pile is empty"
            return True, None
        
        elif move.move_type == MoveType.PLAY_NEW_MELD:
            # Check if player has the tiles
            if not player.has_tiles(move.tiles):
                return False, "You don't have those tiles"
            
            # Check if it forms a valid set
            if not is_valid_set(move.tiles):
                return False, "Tiles don't form a valid set"
            
            # Check initial meld requirement
            if not player.has_melded:
                if not is_initial_meld_valid(move.tiles):
                    return False, f"Initial meld must be worth at least {30} points"
            
            return True, None
        
        elif move.move_type == MoveType.ADD_TO_EXISTING:
            # Must have melded before
            if not player.has_melded:
                return False, "You must make an initial meld first"
            
            # Check if player has the tiles
            if not player.has_tiles(move.tiles):
                return False, "You don't have those tiles"
            
            # Check if target set exists
            if move.target_set_index is None or move.target_set_index >= len(self.table_sets):
                return False, "Invalid target set"
            
            # Check if adding tiles keeps the set valid
            existing_set = self.table_sets[move.target_set_index]
            new_set = existing_set + move.tiles
            if not is_valid_set(new_set):
                return False, "Adding tiles would make the set invalid"
            
            return True, None
        
        elif move.move_type == MoveType.REARRANGE_TABLE:
            # Must have melded before
            if not player.has_melded:
                return False, "You must make an initial meld first"
            
            # Check if player has the tiles they're adding
            if not player.has_tiles(move.tiles):
                return False, "You don't have those tiles"
            
            # Check if new arrangement is valid
            if move.new_table_arrangement is None:
                return False, "No new arrangement provided"
            
            # Verify all table tiles are accounted for
            current_table_tiles = []
            for tile_set in self.table_sets:
                current_table_tiles.extend(tile_set)
            
            new_table_tiles = []
            for tile_set in move.new_table_arrangement:
                new_table_tiles.extend(tile_set)
            
            # Check that all current table tiles plus new tiles are in new arrangement
            expected_tiles = current_table_tiles + move.tiles
            if len(expected_tiles) != len(new_table_tiles):
                return False, "Not all tiles accounted for in new arrangement"
            
            # Validate new arrangement
            is_valid, error = validate_table_state(move.new_table_arrangement)
            if not is_valid:
                return False, f"Invalid table arrangement: {error}"
            
            return True, None
        
        return False, "Unknown move type"
    
    def apply_move(self, move: Move) -> Tuple[bool, Optional[str]]:
        """
        Apply a validated move to the game state.
        
        Args:
            move: The move to apply
            
        Returns:
            Tuple of (success, error_message)
        """
        # First validate the move
        is_valid, error = self.validate_move(move)
        if not is_valid:
            return False, error
        
        player = self.get_player_by_id(move.player_id)
        
        if move.move_type == MoveType.DRAW:
            # Draw a tile
            drawn_tile = self.draw_pile.draw_tile()
            if drawn_tile:
                player.add_tile(drawn_tile)
            
        elif move.move_type == MoveType.PLAY_NEW_MELD:
            # Remove tiles from player's hand
            player.remove_tiles(move.tiles)
            
            # Add new set to table
            self.table_sets.append(move.tiles.copy())
            
            # Mark player as having melded
            if not player.has_melded:
                player.has_melded = True
        
        elif move.move_type == MoveType.ADD_TO_EXISTING:
            # Remove tiles from player's hand
            player.remove_tiles(move.tiles)
            
            # Add to existing set
            self.table_sets[move.target_set_index].extend(move.tiles)
        
        elif move.move_type == MoveType.REARRANGE_TABLE:
            # Remove tiles from player's hand
            player.remove_tiles(move.tiles)
            
            # Replace table with new arrangement
            self.table_sets = [set_tiles.copy() for set_tiles in move.new_table_arrangement]
        
        # Record the move
        self.last_move = move
        
        # Check win condition
        if is_winning_state(player.tiles):
            self.winner = player
            self.phase = GamePhase.FINISHED
            return True, None
        
        # Move to next turn after any move (including drawing)
        self.next_turn()
        
        return True, None
    
    def next_turn(self) -> None:
        """Advance to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turn_number += 1
    
    def get_game_status(self) -> Dict:
        """
        Get a summary of the current game state.
        
        Returns:
            Dictionary with game status information
        """
        return {
            'phase': self.phase.value,
            'turn_number': self.turn_number,
            'current_player': self.get_current_player().name,
            'draw_pile_size': len(self.draw_pile),
            'table_sets_count': len(self.table_sets),
            'players': [
                {
                    'name': p.name,
                    'tiles_count': p.get_tile_count(),
                    'has_melded': p.has_melded,
                    'hand_value': p.get_hand_value()
                }
                for p in self.players
            ],
            'winner': self.winner.name if self.winner else None
        }
    
    def get_scores(self) -> Dict[str, int]:
        """
        Calculate final scores for all players.
        
        In Rummikub, the winner gets 0 points and others get penalty points
        for their remaining tiles. Lower scores are better.
        
        Returns:
            Dictionary mapping player names to scores
        """
        scores = {}
        
        for player in self.players:
            if player == self.winner:
                scores[player.name] = 0
            else:
                scores[player.name] = calculate_remaining_tile_value(player.tiles)
        
        return scores
    
    def can_draw(self) -> bool:
        """Check if there are tiles left to draw."""
        return len(self.draw_pile) > 0
    
    def get_valid_moves(self, player_id: int) -> List[Move]:
        """
        Get all valid moves for a player (useful for AI).
        
        This is a simplified version that returns basic move types.
        A full implementation would enumerate all possible plays.
        
        Args:
            player_id: The player to get moves for
            
        Returns:
            List of valid moves
        """
        player = self.get_player_by_id(player_id)
        if not player or self.get_current_player().player_id != player_id:
            return []
        
        valid_moves = []
        
        # Can always draw if tiles available
        if self.can_draw():
            valid_moves.append(Move(player_id, MoveType.DRAW))
        
        # Note: A full implementation would find all possible melds,
        # additions to existing sets, and table rearrangements
        
        return valid_moves


if __name__ == "__main__":
    # Example usage and testing
    print("Starting a sample Rummikub game:\n")
    
    # Create a game with 2 players
    game = GameState(["Alice", "Bob"], initial_hand_size=5, random_seed=42)
    
    # Start the game
    game.start_game()
    print("Game started!")
    print(f"Current status: {game.get_game_status()}\n")
    
    # Show Alice's initial hand
    alice = game.players[0]
    print(f"{alice.name}'s tiles:")
    for tile in alice.tiles:
        print(f"  {tile}")
    print(f"Total hand value: {alice.get_hand_value()} points\n")
    
    # Simulate drawing a tile
    draw_move = Move(alice.player_id, MoveType.DRAW)
    success, error = game.apply_move(draw_move)
    if success:
        print(f"{alice.name} drew a tile")
        print(f"New hand size: {alice.get_tile_count()} tiles\n")
    
    # Check game state
    print("Updated game status:")
    for key, value in game.get_game_status().items():
        print(f"  {key}: {value}")