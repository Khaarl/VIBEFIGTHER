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
            text_color=font_color, # Renamed font_color to text_color
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
    """Simple button with text that changes color when hovered"""
    def __init__(self, center_x, center_y, width, height, text,
                 font_size=18, face_color=arcade.color.DARK_BLUE_GRAY,
                 highlight_color=arcade.color.WHITE, text_color=arcade.color.WHITE,
                 shadow_color=arcade.color.BLACK, button_height=2): # Added shadow_color and button_height
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.text_color = text_color
        self.highlighted = False
        self.shadow_color = shadow_color # Store shadow_color
        self.button_height = button_height # Store button_height (Note: This name might conflict with the height parameter)
        
    def draw(self):
        """Draw the button with highlight if mouse is hovering"""
        # Draw button rectangle
        # Calculate coordinates for lrbt rectangle
        left = self.center_x - self.width / 2
        right = self.center_x + self.width / 2
        bottom = self.center_y - self.height / 2
        top = self.center_y + self.height / 2
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, self.face_color)
        
        # Draw border if highlighted
        if self.highlighted:
            arcade.draw_rectangle_outline(self.center_x, self.center_y,
                                          self.width + 4, self.height + 4,
                                          self.highlight_color, 2)
        
        # Draw text
        arcade.draw_text(self.text, self.center_x, self.center_y, 
                         self.text_color, font_size=self.font_size,
                         anchor_x="center", anchor_y="center")
                         
    def check_mouse_hover(self, x, y):
        """Check if mouse is hovering over button"""
        if (abs(x - self.center_x) <= self.width / 2 and
                abs(y - self.center_y) <= self.height / 2):
            self.highlighted = True
        else:
            self.highlighted = False
        return self.highlighted
    
    def check_mouse_press(self, x, y):
        """Check if mouse is pressing the button"""
        return (abs(x - self.center_x) <= self.width / 2 and
                abs(y - self.center_y) <= self.height / 2)