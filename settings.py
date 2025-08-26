from constants import SETTINGS_FILE


class Settings:
    def __init__(self):
        self.music_on = True
        self.sounds_on = True
        self.music_started = False
        self.load()

    def load(self):
        # Load music and sound settings from file
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("music="):
                        self.music_on = line.strip().split("=")[1] == "1"
                    elif line.startswith("sounds="):
                        self.sounds_on = line.strip().split("=")[1] == "1"
        except FileNotFoundError:
            self.save()
