import arcade
from .. import constants as C

class ButtonFactory:
    """Factory for creating consistent UI buttons across views"""
    
    @staticmethod
    def create_text_button(
        center_x: float,
        center_y: float,
        text: str,
        width: float = C.BUTTON_WIDTH,
        height: float = C.BUTTON_HEIGHT,
        font_size: int = 24,
        font_color=arcade.color.WHITE,
        face_color=arcade.color.DARK_BLUE_GRAY,
        highlight_color=arcade.color.LIGHT_BLUE,
        shadow_color=arcade.color.BLACK,
        button_height: int = 2
    ):
        """Create a standard text button with consistent styling"""
        return TextButton(
            center_x=center_x,
            center_y=center_y,
            width=width,
            height=height,
            text=text,
            font_size=font_size,
            font_color=font_color,
            face_color=face_color,
            highlight_color=highlight_color,
            shadow_color=shadow_color,
            button_height=button_height
        )

    @staticmethod
    def create_menu_button(
        center_x: float,
        center_y: float,
        text: str,
        menu_type: str = "main"
    ):
        """Create a button with menu-specific styling"""
        colors = {
            "main": arcade.color.DARK_BLUE_GRAY,
            "options": arcade.color.DARK_SLATE_GRAY,
            "video": arcade.color.DARK_SLATE_BLUE,
            "debug": arcade.color.DARK_RED,
            "confirm": arcade.color.DARK_GREEN
        }
        return ButtonFactory.create_text_button(
            center_x=center_x,
            center_y=center_y,
            text=text,
            face_color=colors.get(menu_type, arcade.color.DARK_BLUE_GRAY)
        )

class TextButton:
    """Text button implementation moved from StartView"""
    def __init__(self, center_x, center_y, width, height, text, font_size=18,
                font_color=arcade.color.WHITE, face_color=arcade.color.DARK_BLUE_GRAY,
                highlight_color=arcade.color.LIGHT_BLUE, shadow_color=arcade.color.BLACK,
                button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height
        self.pressed = False
        self._text_obj = None
        self.create_text()

    def create_text(self):
        """Create cached text object"""
        self._text_obj = arcade.Text(
            self.text, self.center_x, self.center_y,
            self.font_color, self.font_size,
            align="center", anchor_x="center", anchor_y="center"
        )

    def draw(self):
        """Draw the button"""
        arcade.draw_lrbt_rectangle_filled(
            self.center_x - self.width/2, self.center_x + self.width/2,
            self.center_y - self.height/2, self.center_y + self.height/2,
            self.face_color)

        if not self.pressed:
            arcade.draw_lrbt_rectangle_filled(
                self.center_x - self.width/2, self.center_x + self.width/2,
                self.center_y, self.center_y + self.button_height,
                self.shadow_color)

        self._text_obj.draw()

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def check_mouse_press(self, x, y):
        """Check if mouse click is within button bounds"""
        if (x > self.center_x - self.width/2 and
            x < self.center_x + self.width/2 and
            y > self.center_y - self.height/2 and
            y < self.center_y + self.height/2):
            self.on_press()
            return True
        return False

    def check_mouse_release(self, x, y):
        """Check if mouse release is within button bounds"""
        if self.pressed:
            self.on_release()
            return (x > self.center_x - self.width/2 and
                    x < self.center_x + self.width/2 and
                    y > self.center_y - self.height/2 and
                    y < self.center_y + self.height/2)
        return False