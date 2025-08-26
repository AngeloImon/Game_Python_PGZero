from pgzero.builtins import Rect
from constants import (
    COLOR_TEXT,
    COLOR_TEXT_OUTLINE,
    COLOR_TITLE,
    FONT_MAIN,
    FONT_SIZE_SCORE,
    FONT_SIZE_HINT,
)


class InputBox:
    def __init__(self, x, y, w, h, maxlen=10):
        self.rect = (x, y, w, h)
        self.text = ""
        self.active = False
        self.maxlen = maxlen

    def handle_event(self, event):
        # Handle keyboard events for user text input
        if event.type == "KEYDOWN":
            if event.key == "RETURN":
                return self.text
            elif event.key == "BACKSPACE":
                self.text = self.text[:-1]
            elif len(self.text) < self.maxlen:
                if event.unicode.isalnum() or event.unicode in "-_ ":
                    self.text += event.unicode
        return None

    def draw(self, screen):
        # Draw the input box and current text
        x, y, w, h = self.rect
        screen.draw.filled_rect(Rect((x - 3, y - 3), (w + 6, h + 6)), (0, 0, 0))
        screen.draw.filled_rect(Rect((x, y), (w, h)), (255, 255, 255))
        screen.draw.text(
            self.text,
            center=(x + w // 2, y + h // 2),
            fontsize=FONT_SIZE_SCORE,
            color=COLOR_TEXT,
            owidth=2,
            ocolor=COLOR_TEXT_OUTLINE,
            sysfontname=FONT_MAIN,
        )
        screen.draw.text(
            "Digite seu nome e pressione Enter",
            center=(x + w // 2, y - 30),
            fontsize=FONT_SIZE_HINT,
            color=COLOR_TITLE,
            owidth=2,
            ocolor=COLOR_TEXT_OUTLINE,
            sysfontname=FONT_MAIN,
        )
