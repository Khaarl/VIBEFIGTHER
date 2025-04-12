# Arcade Fighter Architecture Guide

## System Requirements
- Python 3.7+
- Arcade 3.1.0
- Pyglet (included with Arcade)

## Key Version-Specific Notes (Arcade 3.1.0)

### Drawing Functions
- Use `draw_xywh_rectangle_filled` instead of `draw_rectangle_filled`
- Text rendering should use `Text` objects instead of `draw_text`
- Sprite drawing requires SpriteLists

### Important Changes from Older Versions
1. Rectangle drawing:
```python
# Old (pre-3.0):
arcade.draw_rectangle_filled(x, y, width, height, color)

# New (3.1.0):
arcade.draw_xywh_rectangle_filled(x, y, width, height, color)
```

2. Text rendering:
```python
# Old:
arcade.draw_text("text", x, y, color, size)

# New:
text = arcade.Text("text", x, y, color, size)
text.draw()
```

## Current Implementation Status
- Menu system implemented
- Resolution switching working
- Needs text rendering updates
- Needs rectangle drawing fixes

## Recommended Fixes
1. Update all rectangle drawing calls
2. Replace draw_text with Text objects
3. Verify sprite drawing code