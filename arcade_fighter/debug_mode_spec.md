# Developer Debug Mode Specification

## Core Features
1. **Debug Mode Toggle**
   - Add to New Game menu
   - Stored in constants.py as `DEBUG_MODE = False`

2. **Simplified Environment**
   - Single player (Player 1 only)
   - Flat test platform
   - Disabled AI/round logic

3. **Debug Overlays**
   - Movement vectors (velocity/acceleration)
   - Hitbox visualization
   - Animation state machine

4. **Hot-Reload System**
   - File watcher for assets
   - Physics parameter sliders
   - Animation blend controls

## Implementation Steps

### constants.py Modifications
```python
# Debug Settings
DEBUG_MODE = False
DEBUG_SHOW_HITBOXES = True
DEBUG_SHOW_VECTORS = True
```

### game_view.py Changes
- Add debug setup section
- Implement debug rendering
- Add hot-reload handlers

### start_view.py Updates
- Add debug menu option
- Toggle debug mode flag