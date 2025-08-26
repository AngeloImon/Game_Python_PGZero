from pgzero.builtins import Rect
from constants import (
    WIDTH,
    HEIGHT,
    COLOR_BG,
    COLOR_TITLE,
    COLOR_TEXT,
    COLOR_TEXT_OUTLINE,
    FONT_MAIN,
    FONT_SIZE_TITLE,
    FONT_SIZE_SCORE,
    FONT_SIZE_HINT,
)


class Scoreboard:
    def __init__(self, filename="scores.txt"):
        self.filename = filename
        self.lines = []

    def save(self, name, score):
        # Save a new score entry to the scoreboard file
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"{name}|{score}\n")
        except Exception as e:
            print("Score save error:", e)

    def load(self):
        # Load and sort scores from the scoreboard file
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
            entries = []
            for line in lines:
                parts = line.split("|")
                if len(parts) == 2:
                    name, score = parts[0], parts[1]
                    entries.append((int(score), name))
            entries.sort(reverse=True)
            self.lines = [f"{name} - {score}" for score, name in entries]
        except Exception:
            self.lines = ["Nenhum score salvo."]

    def draw(self, screen, width, height):
        # Draw the scoreboard on the screen
        screen.draw.filled_rect(Rect((0, 0), (width, height)), COLOR_BG)
        screen.draw.text(
            "SCOREBOARD",
            center=(width // 2, 100),
            fontsize=FONT_SIZE_TITLE,
            color=COLOR_TITLE,
            owidth=4,
            ocolor=COLOR_TEXT_OUTLINE,
            sysfontname=FONT_MAIN,
        )
        y = 200
        for line in self.lines[:10]:
            screen.draw.text(
                line,
                center=(width // 2, y),
                fontsize=FONT_SIZE_SCORE,
                color=COLOR_TEXT,
                owidth=2,
                ocolor=COLOR_TEXT_OUTLINE,
                sysfontname=FONT_MAIN,
            )
            y += 60
        screen.draw.text(
            "Pressione ESC para voltar",
            center=(width // 2, height - 60),
            fontsize=FONT_SIZE_HINT,
            color=COLOR_TITLE,
            owidth=2,
            ocolor=COLOR_TEXT_OUTLINE,
            sysfontname=FONT_MAIN,
        )
