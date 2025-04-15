import arcade
import random
import os
import time
import glob
import sys
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from .. import constants as C

class AssetManager:
    """Centralized asset loading and management for all game assets"""
    
    def __init__(self):
        # Get project root path
        self.project_root = Path(__file__).parent.parent.parent
        
        # Textures
        self._texture_cache = {}  # path: texture
        self.occult_symbol = None
        self.backgrounds = []
        self.character_animations = {}  # Dict of character_name:animation_frames
        
        # Audio
        self._sound_cache = {}  # path: sound
        self.music_player = None
        self.current_track = None
        self.current_volume = C.DEFAULT_VOLUME
        self.sound_effects = {}
        
        # Metrics
        self.load_times = {}
        self.load_errors = []
        self.total_assets_loaded = 0
        
        # Initial loading
        self._load_all_assets()

    def _get_asset_path(self, *path_parts) -> str:
        """Construct absolute path to asset from path parts"""
        asset_path = str(self.project_root.joinpath(*path_parts))
        if C.DEBUG_MODE:
            print(f"Resolving asset path: {asset_path}")
        return asset_path

    def _load_all_assets(self):
        """Load all game assets with error handling"""
        start_time = time.time()
        
        self._load_occult_symbol()
        self._load_backgrounds()
        self._load_character_animations()
        
        load_time = time.time() - start_time
        self.load_times['initial_load'] = load_time
        
        if C.DEBUG_MODE:
            print(f"Asset loading completed in {load_time:.2f}s")
            print(f"Loaded {self.total_assets_loaded} assets")
            if self.load_errors:
                print(f"Encountered {len(self.load_errors)} errors")

    def _load_texture(self, *path_parts) -> Optional[arcade.Texture]:
        """Load texture with caching and error handling"""
        path = self._get_asset_path(*path_parts)
        
        if not os.path.exists(path):
            self.load_errors.append(f"Texture not found: {path}")
            return None
            
        if path in self._texture_cache:
            return self._texture_cache[path]
            
        try:
            start = time.time()
            texture = arcade.load_texture(path)
            self._texture_cache[path] = texture
            self.total_assets_loaded += 1
            self.load_times[path] = time.time() - start
            return texture
        except Exception as e:
            self.load_errors.append(f"Texture {path}: {str(e)}")
            return None

    def _load_sound(self, *path_parts) -> Optional[arcade.Sound]:
        """Load sound with caching and error handling"""
        path = self._get_asset_path(*path_parts)
        
        if not os.path.exists(path):
            self.load_errors.append(f"Sound not found: {path}")
            return None
            
        if path in self._sound_cache:
            return self._sound_cache[path]
            
        try:
            start = time.time()
            sound = arcade.load_sound(path)
            self._sound_cache[path] = sound
            self.total_assets_loaded += 1
            self.load_times[path] = time.time() - start
            return sound
        except Exception as e:
            self.load_errors.append(f"Sound {path}: {str(e)}")
            return None

    def _load_occult_symbol(self):
        """Load the occult symbol with fallback"""
        path = self._load_texture("assets", "images", "STATIC", "OCCULT", "image-from-rawpixel-id-6332972-png.png")
        self.occult_symbol = path or arcade.load_texture(":resources:images/items/star.png")

    def _load_backgrounds(self):
        """Load all background images"""
        for bg_path in C.BACKGROUND_IMAGES:
            # Convert background path to parts
            parts = tuple(bg_path.split('/'))
            texture = self._load_texture(*parts)
            if texture:
                self.backgrounds.append(texture)

    def _load_character_animations(self):
        """Load animations for all available characters"""
        chars_dir = self._get_asset_path("assets", "CHAR-ANIM", "PLAYERS")
        for char_name in os.listdir(chars_dir):
            char_path = os.path.join(chars_dir, char_name)
            if os.path.isdir(char_path) and char_name not in ['.', '..']:
                self._load_character_animation(char_name)

    def _load_character_animation(self, char_name: str):
        """Load all animation frames for a specific character"""
        animations = {
            'idle': self._find_character_frames(char_name, ['Idle.png', 'idle.png']),
            'walk': self._find_character_frames(char_name, ['Run.png', 'run.png', 'Walk.png', 'walk.png']),
            'jump': self._find_character_frames(char_name, ['Jump.png', 'jump.png']),
            'fall': self._find_character_frames(char_name, ['Fall.png', 'fall.png']),
            'attack': self._find_attack_frames(char_name),
            'hit': self._find_character_frames(char_name, ['Take hit.png', 'Take Hit.png', 'hit.png', 'Hit.png']),
            'death': self._find_character_frames(char_name, ['Death.png', 'death.png'])
        }
        
        # Filter out empty animations
        self.character_animations[char_name] = {k: v for k, v in animations.items() if v}

    def _find_character_frames(self, char_name: str, possible_names: List[str]) -> List[arcade.Texture]:
        """Find animation frames with flexible naming"""
        for name in possible_names:
            # Check both root Sprites folder and Character subfolder (for Huntress)
            paths_to_try = [
                ("assets", "CHAR-ANIM", "PLAYERS", char_name, "Sprites", name),
                ("assets", "CHAR-ANIM", "PLAYERS", char_name, "Sprites", "Character", name)
            ]
            
            for path_parts in paths_to_try:
                texture = self._load_texture(*path_parts)
                if texture:
                    return [texture]
        return []

    def _find_attack_frames(self, char_name: str) -> List[arcade.Texture]:
        """Find all attack animation frames (numbered or single)"""
        frames = []
        
        # Look for numbered attack frames (Attack1.png, Attack2.png)
        sprites_dir = self._get_asset_path("assets", "CHAR-ANIM", "PLAYERS", char_name, "Sprites")
        numbered_attacks = glob.glob(os.path.join(sprites_dir, "Attack*.png"))
        for attack_path in sorted(numbered_attacks):
            rel_path = os.path.relpath(attack_path, self.project_root)
            path_parts = tuple(rel_path.split(os.sep))
            texture = self._load_texture(*path_parts)
            if texture:
                frames.append(texture)
        
        # Look for single attack frame if no numbered ones found
        if not frames:
            single_attack = self._find_character_frames(char_name, ['Attack.png', 'attack.png'])
            frames.extend(single_attack)
                
        return frames

    def _play_sound(self, sound_path: str) -> Optional[arcade.Sound]:
        """Play a sound effect"""
        sound = self._load_sound(sound_path)
        if sound:
            return sound.play(volume=self.current_volume)
        return None

    def _play_music(self, music_path: str) -> Optional[arcade.Sound]:
        """Play a music track"""
        sound = self._load_sound(music_path)
        if sound:
            self.music_player = sound.play(volume=self.current_volume)
            self.music_player.loop = True
            return self.music_player
        return None