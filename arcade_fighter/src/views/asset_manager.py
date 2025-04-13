import arcade
import random
from typing import Optional, List
from .. import constants as C

class AssetManager:
    """Centralized asset loading and management"""
    
    def __init__(self):
        self.occult_symbol = None
        self.music_player = None
        self.current_track = None
        self.current_volume = C.DEFAULT_VOLUME
        self._load_occult_symbol()
        
    def _load_occult_symbol(self):
        """Load the occult symbol with fallback"""
        try:
            self.occult_symbol = arcade.load_texture(
                "arcade_fighter/assets/images/STATIC/OCCULT/image-from-rawpixel-id-6332972-png.png"
            )
        except FileNotFoundError:
            self.occult_symbol = arcade.load_texture(":resources:images/items/star.png")

    def play_random_music(self, music_files: List[str]) -> Optional[str]:
        """Play a random music track from the provided list"""
        if self.music_player:
            self.music_player.stop()
            
        if not music_files:
            return None
            
        self.current_track = random.choice(music_files)
        sound = arcade.load_sound(self.current_track)
        self.music_player = sound.play(volume=self.current_volume)
        self.music_player.loop = True
        return self.current_track

    def adjust_volume(self, change: float):
        """Adjust volume by specified amount (clamped to 0-1)"""
        self.current_volume = max(0, min(1, self.current_volume + change))
        if self.music_player:
            self.music_player.volume = self.current_volume

    def pause_music(self):
        """Pause the current music track"""
        if self.music_player:
            self.music_player.pause()

    def resume_music(self):
        """Resume paused music"""
        if self.music_player and not self.music_player.playing:
            self.music_player.play()