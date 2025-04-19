# Plan to Add Level Generation Test Option

## Objective
To add a new option to the main menu of the Arcade Fighter game that allows for easy testing of level generation.

## Analysis of Existing Code
- The core game views (`GameView`, `BaseGameView`, `DebugGameView`) currently handle basic environment setup but do not contain complex level generation logic.
- `BaseGameView` provides a minimal environment with a single platform.
- `StartView` manages the main menu and transitions between different game views, including a "Debug Mode" that leads to `DebugGameView`.

## Proposed Plan

1.  **Create a new view for Level Generation Testing:**
    *   Create a new Python file: `arcade_fighter/src/views/level_test_view.py`.
    *   This view will inherit from `BaseGameView`.
    *   It will be specifically designed to handle and display generated levels.

2.  **Implement Level Generation Logic:**
    *   Add the code responsible for generating levels within `level_test_view.py`.
    *   Consider creating a separate module or class for complex generation algorithms if necessary.
    *   Utilize existing assets from `arcade_fighter/assets/LEVELS/`.
    *   Include parameters or controls within this view to influence the generation process for testing different scenarios.

3.  **Add a "Level Test" button to the Main Menu:**
    *   Modify `arcade_fighter/src/views/start_view.py`.
    *   Add a new button to the main menu (or within the existing "mode_select" menu) labeled "Level Test".

4.  **Modify StartView to transition to the new view:**
    *   Update the `on_mouse_press` method in `StartView.py`.
    *   Configure the new "Level Test" button to switch the current view to the new `LevelTestView` when clicked.

5.  **Initial Level Setup in LevelTestView:**
    *   Implement the `setup` method of `LevelTest_View`.
    *   Call the level generation logic within this method to create and display the initial generated level.

## View Flow Diagram

```mermaid
graph TD
    A[StartView] --> B{Click "New Game"};
    B --> C{Mode Selection};
    C --> D[Standard Mode (GameView)];
    C --> E[Debug Mode (DebugGameView)];
    A --> F{Click "Level Test"};
    F --> G[Level Test View (LevelTestView)];
    G --> A;
    D --> A;
    E --> A;
## LevelTestView Fixes (2025-04-19)

### Issues Identified
1. **Double Initialization**: The `__init__` method contains a redundant call to `super().__init__()`
2. **Double Player Drawing**: The `on_draw` method explicitly calls `self.player_list.draw()` after calling `super().on_draw()`, causing the player to be drawn twice

### Changes Implemented
1. **Removed Redundant Initialization**:
   - Removed the second `super().__init__()` call in `__init__`
   - Parent class initialization now only occurs once

2. **Fixed Double Player Drawing**:
   - Removed the explicit `self.player_list.draw()` call in `on_draw`
   - Now relies solely on `BaseGameView.on_draw()` for player rendering

### Impact Assessment
- These changes:
  - Remove redundant code
  - Fix visual artifacts from double-drawing
  - Maintain all existing functionality
  - Improve code maintainability