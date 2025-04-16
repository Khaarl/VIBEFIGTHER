# Arcade Fighter Architecture Documentation

## Project Structure
```
arcade_fighter/
├── assets/
│   ├── CHAR-ANIM/            # Character animations
│   ├── LEVELS/               # Background/level assets
│   ├── MUSIC/                # Audio files
│   └── images/               # Static images
├── src/
│   ├── constants.py          # Game constants and settings
│   ├── character.py          # Character class implementation
│   ├── views/
│   │   ├── asset_manager.py  # Centralized asset loading and management
│   │   ├── start_view.py     # Main menu view
│   │   ├── game_view.py      # Main game view
│   │   ├── debug_game_view.py # Debug view
│   │   └── game_over_view.py # Game over screen
│   └── main.py               # Entry point
├── tests/
│   ├── test_asset_manager.py # Asset manager tests
│   ├── test_character.py
│   └── test_game_view.py
├── docs/                     # Documentation
├── requirements.txt          # Dependencies
└── ARCHITECTURE.md           # This file
```

## Technical Specifications
- Python Arcade Version: 3.1.0
- Python Version: 3.8+ (compatible)
- Resolution Support: SD (800x600), HD (1280x720), FHD (1920x1080)
- Supported Platforms: Windows, Linux, macOS

## Best Practices

### Code Organization
1. Keep view-specific code in the views/ directory
2. Shared constants go in constants.py
3. Character logic belongs in character.py
4. Asset management handled by asset_manager.py
5. Tests should mirror src/ structure

### Development Guidelines
1. Use type hints for all function signatures
2. Document public methods with docstrings
3. Prefix private methods with _
4. Keep view classes under 500 lines
5. Use constants for magic numbers
6. All asset loading through AssetManager

### Performance Considerations
1. Load assets in setup(), not __init__()
2. Use spatial hashing for collision detection
3. Limit particle effects based on resolution
4. Implement proper state management
5. Cache loaded assets using AssetManager

## Testing and Debugging
1. Comprehensive test coverage for AssetManager
2. Automated path resolution for assets
3. Error handling for missing assets
4. Debug mode for asset loading metrics
5. Run tests with:
```bash
python -m unittest discover tests/
```

## Recommended Development Workflow
1. Create feature branches
2. Write tests for new functionality
3. Run tests before merging:
```bash
python -m pytest tests/
```
4. Document changes in ARCHITECTURE.md
5. Verify asset loading in debug mode