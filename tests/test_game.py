"""
Unit tests for the game module.

Tests game state management, move validation, and game flow.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiles import create_tile, create_joker
from game import (
    GameState, GamePhase, MoveType, Move
)
from player import Player


# Player tests moved to test_player.py


class TestGameState(unittest.TestCase):
    """Test the GameState class."""
    
    def test_game_creation(self):
        """Test creating a new game."""
        game = GameState(["Alice", "Bob"], initial_hand_size=5)
        
        self.assertEqual(game.phase, GamePhase.NOT_STARTED)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.players[0].name, "Alice")
        self.assertEqual(game.players[1].name, "Bob")
        self.assertEqual(game.current_player_index, 0)
        self.assertEqual(len(game.table_sets), 0)
    
    def test_start_game(self):
        """Test starting a game deals initial tiles."""
        game = GameState(["Alice", "Bob"], initial_hand_size=5, random_seed=42)
        
        # Start the game
        game.start_game()
        
        self.assertEqual(game.phase, GamePhase.IN_PROGRESS)
        self.assertEqual(len(game.players[0].tiles), 5)
        self.assertEqual(len(game.players[1].tiles), 5)
        
        # Draw pile should have remaining tiles
        expected_remaining = 106 - (2 * 5)  # Total tiles - dealt tiles
        self.assertEqual(len(game.draw_pile), expected_remaining)
        
        # Can't start again
        with self.assertRaises(ValueError):
            game.start_game()
    
    def test_get_current_player(self):
        """Test getting current player."""
        game = GameState(["Alice", "Bob", "Charlie"])
        
        self.assertEqual(game.get_current_player().name, "Alice")
        
        game.next_turn()
        self.assertEqual(game.get_current_player().name, "Bob")
        
        game.next_turn()
        self.assertEqual(game.get_current_player().name, "Charlie")
        
        game.next_turn()
        self.assertEqual(game.get_current_player().name, "Alice")  # Wraps around
    
    def test_get_player_by_id(self):
        """Test getting player by ID."""
        game = GameState(["Alice", "Bob"])
        
        alice = game.get_player_by_id(0)
        self.assertIsNotNone(alice)
        self.assertEqual(alice.name, "Alice")
        
        bob = game.get_player_by_id(1)
        self.assertIsNotNone(bob)
        self.assertEqual(bob.name, "Bob")
        
        # Invalid ID
        self.assertIsNone(game.get_player_by_id(99))


class TestMoveValidation(unittest.TestCase):
    """Test move validation logic."""
    
    def setUp(self):
        """Set up a game for testing."""
        self.game = GameState(["Alice", "Bob"], initial_hand_size=14, random_seed=42)
        self.game.start_game()
        
        # Give Alice specific tiles for testing
        alice = self.game.players[0]
        alice.tiles = [
            create_tile(10, 'red'),
            create_tile(10, 'blue'),
            create_tile(10, 'black'),
            create_tile(5, 'red'),
            create_tile(6, 'red'),
            create_tile(7, 'red')
        ]
    
    def test_validate_draw_move(self):
        """Test validating draw moves."""
        # Valid draw
        move = Move(0, MoveType.DRAW)
        is_valid, error = self.game.validate_move(move)
        self.assertTrue(is_valid)
        
        # Wrong player's turn
        move = Move(1, MoveType.DRAW)
        is_valid, error = self.game.validate_move(move)
        self.assertFalse(is_valid)
        self.assertIn("turn", error.lower())
    
    def test_validate_play_new_meld(self):
        """Test validating new meld plays."""
        alice = self.game.players[0]
        
        # Valid initial meld (30+ points)
        tiles_to_play = [
            alice.tiles[0],  # 10 red
            alice.tiles[1],  # 10 blue
            alice.tiles[2]   # 10 black
        ]
        move = Move(0, MoveType.PLAY_NEW_MELD, tiles_to_play)
        is_valid, error = self.game.validate_move(move)
        self.assertTrue(is_valid)
        
        # Invalid - not enough points for initial meld
        tiles_to_play = [
            alice.tiles[3],  # 5 red
            alice.tiles[4],  # 6 red
            alice.tiles[5]   # 7 red
        ]
        move = Move(0, MoveType.PLAY_NEW_MELD, tiles_to_play)
        is_valid, error = self.game.validate_move(move)
        self.assertFalse(is_valid)
        self.assertIn("30", error)
        
        # Invalid - tiles don't form valid set
        tiles_to_play = [
            alice.tiles[0],  # 10 red
            alice.tiles[3],  # 5 red
            alice.tiles[4]   # 6 red
        ]
        move = Move(0, MoveType.PLAY_NEW_MELD, tiles_to_play)
        is_valid, error = self.game.validate_move(move)
        self.assertFalse(is_valid)
        self.assertIn("valid set", error.lower())
        
        # Invalid - player doesn't have tiles
        fake_tiles = [
            create_tile(12, 'red'),
            create_tile(12, 'blue'),
            create_tile(12, 'black')
        ]
        move = Move(0, MoveType.PLAY_NEW_MELD, fake_tiles)
        is_valid, error = self.game.validate_move(move)
        self.assertFalse(is_valid)
        self.assertIn("don't have", error.lower())
    
    def test_validate_add_to_existing(self):
        """Test validating adding to existing sets."""
        alice = self.game.players[0]
        
        # First, Alice needs to make initial meld
        alice.has_melded = True
        
        # Add a set to the table
        self.game.table_sets = [[
            create_tile(5, 'blue'),
            create_tile(5, 'black'),
            create_tile(5, 'orange')
        ]]
        
        # Valid - add matching tile
        alice.tiles.append(create_tile(5, 'red'))
        move = Move(0, MoveType.ADD_TO_EXISTING, 
                   [alice.tiles[-1]], target_set_index=0)
        is_valid, error = self.game.validate_move(move)
        self.assertTrue(is_valid)
        
        # Invalid - haven't melded yet
        alice.has_melded = False
        is_valid, error = self.game.validate_move(move)
        self.assertFalse(is_valid)
        self.assertIn("initial meld", error.lower())
        alice.has_melded = True
        
        # Invalid - bad target set index
        move = Move(0, MoveType.ADD_TO_EXISTING, 
                   [alice.tiles[-1]], target_set_index=99)
        is_valid, error = self.game.validate_move(move)
        self.assertFalse(is_valid)
        self.assertIn("target set", error.lower())
        
        # Invalid - would make set invalid (adding wrong number)
        move = Move(0, MoveType.ADD_TO_EXISTING, 
                   [alice.tiles[0]],  # 10 red - wrong number for group of 5s
                   target_set_index=0)
        is_valid, error = self.game.validate_move(move)
        self.assertFalse(is_valid)
        self.assertIn("invalid", error.lower())


class TestMoveApplication(unittest.TestCase):
    """Test applying moves to game state."""
    
    def setUp(self):
        """Set up a game for testing."""
        self.game = GameState(["Alice", "Bob"], initial_hand_size=5, random_seed=42)
        self.game.start_game()
        
        # Give Alice specific tiles
        alice = self.game.players[0]
        alice.tiles = [
            create_tile(10, 'red'),
            create_tile(10, 'blue'),
            create_tile(10, 'black'),
            create_tile(5, 'red'),
            create_tile(6, 'red')
        ]
    
    def test_apply_draw_move(self):
        """Test applying draw moves."""
        alice = self.game.players[0]
        initial_hand_size = len(alice.tiles)
        initial_deck_size = len(self.game.draw_pile)
        
        # Draw a tile
        move = Move(0, MoveType.DRAW)
        success, error = self.game.apply_move(move)
        
        self.assertTrue(success)
        self.assertEqual(len(alice.tiles), initial_hand_size + 1)
        self.assertEqual(len(self.game.draw_pile), initial_deck_size - 1)
        
        # Should be Bob's turn after drawing
        self.assertEqual(self.game.current_player_index, 1)
    
    def test_apply_play_new_meld(self):
        """Test applying new meld plays."""
        alice = self.game.players[0]
        tiles_to_play = [alice.tiles[0], alice.tiles[1], alice.tiles[2]]
        
        # Play the meld
        move = Move(0, MoveType.PLAY_NEW_MELD, tiles_to_play)
        success, error = self.game.apply_move(move)
        
        self.assertTrue(success)
        self.assertEqual(len(alice.tiles), 2)  # Started with 5, played 3
        self.assertEqual(len(self.game.table_sets), 1)
        self.assertEqual(len(self.game.table_sets[0]), 3)
        self.assertTrue(alice.has_melded)
        
        # Should be Bob's turn now
        self.assertEqual(self.game.current_player_index, 1)
    
    def test_win_condition(self):
        """Test that game ends when player runs out of tiles."""
        alice = self.game.players[0]
        alice.has_melded = True
        
        # Play all tiles
        alice.tiles = [
            create_tile(10, 'red'),
            create_tile(10, 'blue'),
            create_tile(10, 'black')
        ]
        
        move = Move(0, MoveType.PLAY_NEW_MELD, alice.tiles.copy())
        success, error = self.game.apply_move(move)
        
        self.assertTrue(success)
        self.assertEqual(len(alice.tiles), 0)
        self.assertEqual(self.game.phase, GamePhase.FINISHED)
        self.assertEqual(self.game.winner, alice)


class TestGameStatus(unittest.TestCase):
    """Test game status and scoring."""
    
    def test_get_game_status(self):
        """Test getting game status summary."""
        game = GameState(["Alice", "Bob"])
        game.start_game()
        
        status = game.get_game_status()
        
        self.assertEqual(status['phase'], 'in_progress')
        self.assertEqual(status['turn_number'], 1)
        self.assertEqual(status['current_player'], 'Alice')
        self.assertEqual(len(status['players']), 2)
        self.assertIsNone(status['winner'])
    
    def test_get_scores(self):
        """Test calculating final scores."""
        game = GameState(["Alice", "Bob"])
        game.start_game()
        
        # Set up end game state
        alice = game.players[0]
        bob = game.players[1]
        
        alice.tiles = []  # Alice wins
        bob.tiles = [
            create_tile(5, 'red'),
            create_tile(10, 'blue'),
            create_joker()
        ]
        
        game.winner = alice
        game.phase = GamePhase.FINISHED
        
        scores = game.get_scores()
        
        self.assertEqual(scores['Alice'], 0)  # Winner gets 0
        self.assertEqual(scores['Bob'], 5 + 10 + 30)  # Penalty points


if __name__ == '__main__':
    unittest.main()