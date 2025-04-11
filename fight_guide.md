# Plan: Basic 2D Arcade Fighting Game (Python Arcade Framework)

**Goal:** Create a functional prototype of a 2D fighting game featuring two characters, basic movement, one attack, health bars, rounds, and win conditions using the Arcade library.

**Technology:** Python 3.x, Arcade library (`pip install arcade`).

**Principles:** Object-Oriented Programming (OOP), Modular Design, Clear Code Structure, Arcade Views & Sprites.

---

## Phase 1: Project Setup & Core Structure (Arcade)

1.  **Directory Structure:** Create a project folder (e.g., `arcade_fighter`) with subdirectories: `assets/images`, `assets/sounds`, `src`.
2.  **Install Arcade:** Ensure Arcade is installed (`pip install arcade`).
3.  **Constants:** Define essential constants (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS, colors, physics constants like GRAVITY) in `src/constants.py`.
4.  **Main Game Window:** Create the main script (`main.py`). Define a class inheriting from `arcade.Window`. Initialize it and run `arcade.run()`.
5.  **Game Views:** Plan for Arcade's `View` system:
    *   `StartView`: Displays the initial menu.
    *   `GameView`: Handles the main gameplay loop, drawing, updates, and physics.
    *   `GameOverView`: Displays the winner and restart/quit options.
    *   Implement the basic structure for these views in separate files (e.g., `src/views/start_view.py`, `src/views/game_view.py`, etc.).
6.  **Initial View:** Set the main window to show `StartView` initially.

    ```mermaid
    graph TD
        A[StartView] -- Start Input --> B(Show GameView);
        B[GameView] -- Win Condition Met --> C(Show GameOverView);
        C[GameOverView] -- Restart Input --> B;
        C -- Quit Input --> D[Exit Game];
    ```
    *Diagram: Arcade View Flow*

---

## Phase 2: Asset Management (Arcade)

1.  **Asset Planning:** Identify character sprites (idle, walk, jump, attack), background image, UI elements, sound effects. Placeholders are fine.
2.  **Loading:** Use Arcade's loading functions (`arcade.load_texture`, `arcade.load_sound`). Textures can be loaded within the `Character` class or pre-loaded in the `GameView`'s `setup()` method. Sounds can be loaded similarly. Arcade handles some caching.
3.  **Integration:** Load the background texture in `GameView.setup()` and draw it in `GameView.on_draw()`.

---

## Phase 3: Character Implementation (Arcade Sprite)

1.  **`Character` Class:** Design a class in `src/character.py` inheriting from `arcade.Sprite`.
    *   **Attributes:**
        *   `player_num` (1 or 2)
        *   Health (`hp`, `max_hp`)
        *   State (`state`: 'idle', 'walking', 'jumping', 'attacking', 'hit', 'dead')
        *   Facing direction (`facing_direction`: `arcade.FACE_LEFT` or `arcade.FACE_RIGHT`) - Used to flip textures.
        *   Textures: Store loaded `arcade.Texture` objects for different states/animations (e.g., in lists or dictionaries).
        *   Attack properties (cooldown timer, damage value, hitbox definition relative to sprite center).
        *   Jump status (`is_on_ground` - often managed by the physics engine).
        *   Reference to the `GameView` or physics engine if needed for interactions.
    *   **Methods:**
        *   `__init__(self, player_num, scale=1, ...)`: Constructor. Load initial/default texture. Call `super().__init__()`.
        *   `update_animation(self, delta_time=1/60)`: Override `arcade.Sprite.update_animation`. Switch the sprite's current `texture` based on `state`, `facing_direction`, and animation timers.
        *   `on_update(self, delta_time=1/60)`: Override `arcade.Sprite.on_update`. Handle state logic, cooldowns, etc. *Note: Physics updates position.*
        *   `move(self, direction)`: Set `self.change_x` based on direction and speed constants. Update `facing_direction`.
        *   `jump(self)`: Set `self.change_y` to jump speed if `is_on_ground`.
        *   `attack(self, target_list)`: Set state to 'attacking', start attack timer/cooldown. Logic for checking hits will likely be in `GameView.on_update`.
        *   `take_damage(self, amount)`: Reduce `hp`, set 'hit' state, potentially trigger brief invulnerability. Check for death (`hp <= 0`).
2.  **Sprite Lists:** In `GameView`, create `arcade.SpriteList` instances for players (`self.player_list`) and potentially platforms/walls (`self.platform_list`).
3.  **Instantiation:** In `GameView.setup()`, create two `Character` sprite instances, configure their initial positions and properties, and add them to `self.player_list`.

    ```mermaid
     classDiagram
         class arcade.Sprite {
             +center_x
             +center_y
             +change_x
             +change_y
             +texture
             +update_animation()
             +on_update()
         }
         class Character {
             +int player_num
             +int hp
             +int max_hp
             +string state
             +int facing_direction
             +dict textures
             +AttackData attack_data
             +__init__(player_num, scale, ...)
             +update_animation(delta_time)
             +on_update(delta_time)
             +move(direction)
             +jump()
             +attack(target_list)
             +take_damage(amount)
         }
         class AttackData {
             +tuple hitbox_shape  // e.g., (width, height, offset_x, offset_y)
             +int damage
             +float cooldown
             +float duration
         }
         arcade.Sprite <|-- Character
         Character "1" *-- "1" AttackData : has
    ```
    *Diagram: Character Class (inheriting from Arcade Sprite)*

---

## Phase 4: Input Handling (Arcade Views)

1.  **View Methods:** Implement `on_key_press(self, key, modifiers)` and `on_key_release(self, key, modifiers)` within `GameView`.
2.  **Key Mapping:** Define key mappings (e.g., `arcade.key.A`, `arcade.key.W`, `arcade.key.SPACE`) for Player 1 and Player 2 actions.
3.  **Action Triggering:** Based on key events, get the corresponding `Character` sprite from `self.player_list` and call its methods (`move`, `jump`, `attack`). Handle key releases to stop movement (`change_x = 0`).

---

## Phase 5: Physics & Collision (Arcade Physics Engine)

1.  **Physics Engine:** In `GameView.setup()`, create an `arcade.PhysicsEnginePlatformer`.
    *   `self.physics_engine = arcade.PhysicsEnginePlatformer(player_sprite, platform_list, gravity_constant)`
    *   Pass *one* player sprite initially. You'll need to manage physics for both players, potentially by having two engines or updating the engine's player reference, or iterating updates. A common approach is to iterate `self.physics_engine.update()` for each player sprite against the platforms.
2.  **Platforms:** Create an invisible floor sprite and add it to `self.platform_list` so characters have something to stand on.
3.  **Gravity & Movement:** Call `self.physics_engine.update()` in `GameView.on_update()`. This applies gravity and moves sprites based on their `change_x`, `change_y`, handling collisions with `self.platform_list`.
4.  **Collision Checks:**
    *   Character-Boundary: Manually check `sprite.left`, `sprite.right`, etc., against `SCREEN_WIDTH` in `Character.on_update` or `GameView.on_update` and clamp position or velocity.
    *   Character-Character: Use `arcade.check_for_collision_with_list(player1, player2_list)` in `GameView.on_update`. Implement simple push-back logic if collision occurs to prevent overlap.

---

## Phase 6: Combat Mechanics (Arcade Collision)

1.  **Attack Logic:**
    *   When `Character.attack()` is called: set state, start timers.
    *   In `GameView.on_update()`:
        *   Iterate through players. If a player is in the 'attacking' state:
        *   Calculate the current position/rect of their attack hitbox based on their `center_x`, `center_y`, `facing_direction`, and `attack_data.hitbox_shape`.
        *   Check for collision between this hitbox rect and the *other* player's sprite using `arcade.check_for_collision(other_player, hitbox_sprite)` (if hitbox is a temporary sprite) or by checking if the other player's rect overlaps the calculated hitbox rect.
        *   Alternatively, use `arcade.Sprite` for hitboxes and `arcade.check_for_collision_with_list`.
2.  **Damage Application:** If a hit is detected and the attack cooldown/timer allows, call `other_player.take_damage(attacker.attack_data.damage)`. Reset attack flags/timers.
3.  **Visual Feedback:** Handled by `Character.update_animation` switching textures based on state ('attacking', 'hit').

---

## Phase 7: UI Elements (Arcade Drawing)

1.  **Drawing:** In `GameView.on_draw()`:
    *   Call `arcade.start_render()`.
    *   Draw background, platforms, players (`self.platform_list.draw()`, `self.player_list.draw()`).
    *   Use `arcade.draw_lrbt_rectangle_filled` or similar for health bars.
    *   Use `arcade.draw_text` for round indicators, scores, or winner text (in `GameOverView`). Remember Arcade's origin is bottom-left. Consider using an `arcade.Camera` for easier UI positioning if the game view scrolls.
2.  **Updates:** Ensure UI elements reflect current game state (`hp`, round number).

---

## Phase 8: Game State Management & Flow (Arcade Views)

1.  **View Transitions:** Use `self.window.show_view(NewView(...))` in response to events (e.g., key press in `StartView`, win condition met in `GameView`).
2.  **Win/Loss/Round Logic:**
    *   Implement checks in `GameView.on_update()` for `player.hp <= 0`.
    *   Track rounds won.
    *   When a round ends, pause briefly (e.g., using `time.sleep` or a timer within the update loop), then call a reset method (like `self.setup()` or a dedicated `reset_round()`) to reposition characters, restore health, and increment the round counter.
    *   If match ends (player wins enough rounds), transition to `GameOverView`, passing winner info: `self.window.show_view(GameOverView(winner=winner_num))`.
3.  **Setup Method:** Ensure each View's `setup()` method correctly initializes or resets its required state (sprites, scores, physics engine, etc.).

---

## Phase 9: Refinement & Optional AI (Arcade)

1.  **Polish:** Implement actual animations using lists of textures in `Character.update_animation`. Load and play sounds (`arcade.Sound.play()`) triggered by events (jump, attack, hit).
2.  **(Optional) Simple AI:**
    *   In `GameView.on_update()`, add logic to control the AI character sprite (e.g., `player2`).
    *   Base decisions on distance (`arcade.get_distance_between_sprites`), AI state, and timers/randomness. Example: If far, set `ai.change_x` to move closer. If close, randomly `ai.attack()` or move slightly.

---

**Conclusion:**

This revised plan leverages the Python Arcade Framework to build the 2D fighting game. It focuses on using `arcade.Sprite`, `arcade.PhysicsEnginePlatformer`, and the `arcade.View` system for a more structured approach compared to raw Pygame.