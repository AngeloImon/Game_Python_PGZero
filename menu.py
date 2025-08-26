from pgzero.builtins import Rect
from constants import (
    BTN_W,
    BTN_H,
    WIDTH,
    HEIGHT,
    COLOR_BG,
    COLOR_BTN,
    COLOR_TITLE,
    COLOR_TEXT,
    COLOR_TEXT_OUTLINE,
    FONT_MAIN,
    FONT_SIZE_TITLE,
    FONT_SIZE_BTN,
)


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.btn_w = BTN_W
        self.btn_h = BTN_H
        self.options = []
        self.menu_from_pause = False

    def get_buttons(self, music_on, sounds_on):
        # Return the list of menu buttons
        y = 250
        btns = []
        if self.menu_from_pause:
            btns.append(
                (
                    "Continuar",
                    (self.width // 2 - self.btn_w // 2, y, self.btn_w, self.btn_h),
                )
            )
        else:
            btns.append(
                (
                    "Comecar o jogo",
                    (self.width // 2 - self.btn_w // 2, y, self.btn_w, self.btn_h),
                )
            )
        y += 100
        btns.append(
            (
                "Scoreboard",
                (self.width // 2 - self.btn_w // 2, y, self.btn_w, self.btn_h),
            )
        )
        y += 100
        btns.append(
            (
                "Musica: " + ("Ligada" if music_on else "Desligada"),
                (self.width // 2 - self.btn_w // 2, y, self.btn_w, self.btn_h),
            )
        )
        y += 100
        btns.append(
            (
                "Sons: " + ("Ligados" if sounds_on else "Desligados"),
                (self.width // 2 - self.btn_w // 2, y, self.btn_w, self.btn_h),
            )
        )
        y += 100
        btns.append(
            ("Sair", (self.width // 2 - self.btn_w // 2, y, self.btn_w, self.btn_h))
        )
        return btns

    def draw(self, screen, music_on, sounds_on):
        # Draw the menu on the screen
        screen.draw.filled_rect(Rect((0, 0), (self.width, self.height)), COLOR_BG)
        screen.draw.text(
            "PLATAFORMEIRO",
            center=(self.width // 2, 120),
            fontsize=FONT_SIZE_TITLE,
            color=COLOR_TITLE,
            owidth=4,
            ocolor=COLOR_TEXT_OUTLINE,
            sysfontname=FONT_MAIN,
        )
        btns = self.get_buttons(music_on, sounds_on)
        for label, rect in btns:
            screen.draw.filled_rect(Rect(rect), COLOR_BTN)
            screen.draw.text(
                label,
                center=(rect[0] + self.btn_w // 2, rect[1] + self.btn_h // 2),
                fontsize=FONT_SIZE_BTN,
                color=COLOR_TEXT,
                owidth=2,
                ocolor=COLOR_TEXT_OUTLINE,
                sysfontname=FONT_MAIN,
            )

    def get_clicked_option(self, pos, music_on, sounds_on):
        # Return the index of the clicked menu option, or None
        btns = self.get_buttons(music_on, sounds_on)
        for i, (label, rect) in enumerate(btns):
            r = Rect(rect)
            if r.collidepoint(pos):
                return i
        return None
