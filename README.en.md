README em [Portugês](https://github.com/AngeloImon/Game_Python_PGZero/edit/main/README.md)

# 🎮 Plataformeiro

**Plataformeiro** is a dynamic platform game developed with [PgZero](https://pygame-zero.readthedocs.io/en/stable/), where the player climbs automatically generated platforms, faces enemies, and collects coins to accumulate points. The game has no end — the adventure continues until the hero falls or is defeated.
---

## 🧠 Game Mechanics

- Platforms are generated dynamically, with or without enemies and coins.
- The player earns:
  - **10 points** for each platform climbed
  - **100 points** for each coin collected
- Upon death (by falling or enemy), the score is saved to a `.txt` file.
- The game ends only when the player dies — there is no final stage.

---

## 🕹️ Main Menu

The game features an interactive menu with clickable buttons:

- **Start Game** — starts the adventure  
- **Toggle Music/Sound** — enables or disables sound effects  
- **Exit** — closes the game

---

## 👾 Enemies & Hero

- Various enemies inhabit the scene and pose real danger.  
- Each enemy has its own behavior and moves within its territory.  
- The hero and enemies use **sprite animations** both in motion and idle (e.g., legs, tail, breathing, gaze).

---

## 🧱 Technical Requirements

This project follows specific restrictions:

- **Allowed libraries**:
  - `pgzero`
  - `math`
  - `random`
  - `pygame.Rect` (allowed as an exception)
- **Prohibited libraries**:
  - Any other not listed above
  - **Full Pygame usage is NOT allowed**

---

## 🧑‍💻 Best Practices

- Code written in a **unique and independent** way  
- Variable, function, and class names follow **PEP8** standards  
- Clear logic with no known bugs

---

## 📁 Project Structure
    Game_Python_PGZero/
    ├── game.py
    ├── hero.py
    ├── enemy.py
    ├── platforms.py
    ├── scenario.py
    ├── menu.py
    ├── constants.py
    ├── settings.py
    ├── scores.txt
    ├── images/
    ├── sounds/
    ├── music/
    └── .venv/

---

## 📝 Credits

Developed by [Angelo Imon](https://github.com/AngeloImon).  
Special thanks to [Kenney.nl](https://kenney.nl/assets/new-platformer-pack) for providing visual assets.

---

## 🚀 Getting Started

Clone the repository and run it with PgZero.  
PgZero installation is required — using a virtual environment is recommended.
