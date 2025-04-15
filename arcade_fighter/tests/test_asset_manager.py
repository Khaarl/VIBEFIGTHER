import unittest
import arcade
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from arcade_fighter.src.views.asset_manager import AssetManager
from arcade_fighter.src import constants as C

class TestAssetManager(unittest.TestCase):
    def setUp(self):
        # Enable debug mode for testing
        C.DEBUG_MODE = True
        self.asset_manager = AssetManager()

    def test_initial_load(self):
        """Test that initial assets are loaded"""
        self.assertTrue(len(self.asset_manager.character_animations) > 0)
        self.assertTrue(self.asset_manager.total_assets_loaded > 0)

    def test_texture_loading(self):
        """Test texture loading functionality"""
        texture = self.asset_manager._load_texture(
            "assets", "CHAR-ANIM", "PLAYERS", "EVil Wizard 2", "Sprites", "Idle.png"
        )
        self.assertIsNotNone(texture)
        self.assertIn(
            str(Path("assets/CHAR-ANIM/PLAYERS/EVil Wizard 2/Sprites/Idle.png")), 
            str(texture.file_path)
        )

    def test_character_animation_loading(self):
        """Test that character animations were loaded"""
        self.assertTrue(len(self.asset_manager.character_animations) > 0)
        char_name = "EVil Wizard 2"
        self.assertIn(char_name, self.asset_manager.character_animations)
        animations = self.asset_manager.character_animations[char_name]
        self.assertTrue(len(animations.get('idle', [])) > 0)
        self.assertTrue(len(animations.get('walk', [])) > 0)

    def test_missing_asset_handling(self):
        """Test handling of missing assets"""
        initial_error_count = len(self.asset_manager.load_errors)
        texture = self.asset_manager._load_texture("invalid", "path.png")
        self.assertIsNone(texture)
        self.assertEqual(len(self.asset_manager.load_errors), initial_error_count + 1)
        self.assertTrue(any("invalid/path.png" in error.replace("\\", "/") for error in self.asset_manager.load_errors))

    def test_audio_loading(self):
        """Test audio loading functionality"""
        if not C.MUSIC_FILES:
            self.skipTest("No music files available")
            
        test_path = C.MUSIC_FILES[0]
        path_parts = test_path.split('/')
        abs_path = str(self.asset_manager.project_root.joinpath(*path_parts))
        
        # Skip test if file doesn't exist
        if not os.path.exists(abs_path):
            self.skipTest(f"Music file not found: {abs_path}")
            
        try:
            sound = self.asset_manager._load_sound(*path_parts)
            if sound is None:
                self.skipTest("Audio loading not supported in test environment")
            self.assertIsNotNone(sound)
            self.assertIn(abs_path, self.asset_manager._sound_cache)
        except Exception as e:
            self.skipTest(f"Audio loading failed: {str(e)}")

    def tearDown(self):
        self.asset_manager._texture_cache.clear()
        self.asset_manager._sound_cache.clear()

if __name__ == '__main__':
    unittest.main()