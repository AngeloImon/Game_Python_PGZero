import pgzrun
from menu import Menu
from scoreboard import Scoreboard
from settings import Settings
from inputbox import InputBox
from scenario import Scenario
from hero import Hero

SCORES_FILE = "scores.txt"
WIDTH = 1280
HEIGHT = 720
GROUND_HEIGHT = 64


class GameManager:
    """
    Gerencia o estado global do jogo, fluxo de telas, score, input e integração de módulos auxiliares.
    """

    def __init__(self):
        # Initialize auxiliary modules
        self.menu = Menu(WIDTH, HEIGHT)
        self.scoreboard = Scoreboard(SCORES_FILE)
        self.settings = Settings()
        self.settings.load()
        self.state = (
            "menu"  # 'menu', 'jogando', 'game_over', 'input_name', 'scoreboard'
        )
        self.score = 0
        self.platforms_climbed = 0
        self.last_platform_y = None
        self.scenario = None
        self.hero = None
        self.game_over_timer = 0
        self.inputbox_active = False
        self.inputbox_text = ""
        self.inputbox = None

    def start_game(self):
        # Start a new game session
        self.scenario = Scenario(WIDTH, HEIGHT, GROUND_HEIGHT)
        hero_x = WIDTH // 2
        hero_y = HEIGHT - GROUND_HEIGHT - 64
        self.hero = Hero(hero_x, hero_y)
        self.score = 0
        self.platforms_climbed = 0
        self.last_platform_y = None
        self.state = "jogando"
        self.game_over_timer = 0
        self.menu.menu_from_pause = False

    def toggle_music(self):
        # Toggle background music
        self.settings.music_on = not self.settings.music_on
        if self.settings.music_on:
            if not self.settings.music_started:
                music.play("bg_music")
                music.set_volume(0.5)
                self.settings.music_started = True
        else:
            music.stop()
            self.settings.music_started = False

    def quit_game(self):
        # Quit the game
        import sys

        sys.exit(0)

    def draw(self):
        # Draw the current game state
        screen.clear()
        if self.state == "menu":
            self.menu.draw(screen, self.settings.music_on, self.settings.sounds_on)
            return
        elif self.state == "scoreboard":
            self.scoreboard.draw(screen, WIDTH, HEIGHT)
            return
        elif self.state == "input_name":
            self.scenario.draw(screen, camera_y=-self.scenario.camera_y)
            self.hero.draw(camera_y=-self.scenario.camera_y)
            screen.draw.text(
                f"Pontuacao: {self.score}",
                (30, 20),
                fontsize=48,
                color="yellow",
                owidth=2,
                ocolor="black",
                sysfontname="arial",
            )
            if self.inputbox:
                self.inputbox.draw(screen)
            return
        elif self.state == "jogando":
            self.scenario.draw(screen, camera_y=-self.scenario.camera_y)
            self.hero.draw(camera_y=-self.scenario.camera_y)
            screen.draw.text(
                f"Score: {self.score}",
                (30, 20),
                fontsize=48,
                color="yellow",
                owidth=2,
                ocolor="black",
                sysfontname="arial",
            )
        elif self.state == "game_over":
            self.scenario.draw(screen, camera_y=-self.scenario.camera_y)
            self.hero.draw(camera_y=-self.scenario.camera_y)
            screen.draw.text(
                f"Pontuacao: {self.score}",
                (30, 20),
                fontsize=48,
                color="yellow",
                owidth=2,
                ocolor="black",
                sysfontname="arial",
            )
            screen.draw.text(
                "Voce morreu!",
                center=(WIDTH // 2, HEIGHT // 2),
                fontsize=64,
                color="red",
                owidth=4,
                ocolor="black",
                sysfontname="arial",
            )
            screen.draw.text(
                f"Voltando ao menu em {int(3-self.game_over_timer)}",
                center=(WIDTH // 2, HEIGHT // 2 + 80),
                fontsize=48,
                color="white",
                owidth=2,
                ocolor="black",
                sysfontname="arial",
            )

    def update(self, dt):
        # Update game state (called every frame)
        # Música
        if self.settings.music_on:
            if not self.settings.music_started:
                music.play("bg_music")
                music.set_volume(0.5)
                self.settings.music_started = True
        else:
            if self.settings.music_started:
                music.stop()
                self.settings.music_started = False
        # Evita erro quando não está jogando
        if self.state in ("menu", "scoreboard"):
            self.inputbox = None
            self.inputbox_active = False
            return
        if self.state == "input_name":
            # Garante que o inputbox está criado e sincronizado
            if self.inputbox is None:
                self.inputbox = InputBox(
                    WIDTH // 2 - 200, HEIGHT // 2 - 40, 400, 60, maxlen=12
                )
                self.inputbox.text = self.inputbox_text
            return
        if self.state == "game_over":
            self.game_over_timer += dt
            if self.game_over_timer >= 0.5:
                self.state = "input_name"
                self.inputbox_active = True
                self.inputbox_text = ""
                self.inputbox = None
            return
        # Atualiza a câmera para seguir o herói se ele subir
        camera_margin = HEIGHT // 3
        if self.hero.actor.y < self.scenario.camera_y + camera_margin:
            self.scenario.camera_y = self.hero.actor.y - camera_margin
        # Gera plataformas bem acima do topo visível
        if self.scenario.platforms:
            topo_mais_alto = min(p.y for p in self.scenario.platforms)
        else:
            topo_mais_alto = self.scenario.height - self.scenario.ground_height
        self.scenario._create_platforms(start_y=topo_mais_alto - 80, n_platforms=5)
        jump_started = self.hero.update(
            dt, WIDTH, HEIGHT, GROUND_HEIGHT, platforms=self.scenario.platforms
        )
        if jump_started and self.settings.sounds_on:
            sounds.sfx_jump.play()
        # Atualiza moedas (animação)
        for platform in self.scenario.platforms:
            if hasattr(platform, "coin") and platform.coin:
                platform.coin.update(dt)
                hx, hy = self.hero.actor.x, self.hero.actor.y
                cx, cy = platform.coin.x + 16, platform.coin.y + 16
                if abs(hx - cx) < 32 and abs(hy - cy) < 32:
                    platform.coin = None
                    self.score += 100
                    if self.settings.sounds_on:
                        sounds.sfx_coin.play()
            if hasattr(platform, "enemy") and platform.enemy:
                platform.enemy.update(dt)
                ex, ey = platform.enemy.x, platform.enemy.y
                ew, eh = 32, 32
                margin = 0.25
                hw, hh = self.hero.actor.width, self.hero.actor.height
                hx = self.hero.actor.x - hw // 2 + hw * margin
                hy = self.hero.actor.y - hh // 2 + hh * margin
                hw = hw * (1 - 2 * margin)
                hh = hh * (1 - 2 * margin)
                if hx < ex + ew and hx + hw > ex and hy < ey + eh and hy + hh > ey:
                    self.state = "game_over"
                    self.game_over_timer = 0
                    if self.settings.sounds_on:
                        sounds.sfx_disappear.play()
        if self.hero.actor.y - self.scenario.camera_y > HEIGHT:
            self.state = "game_over"
            self.game_over_timer = 0
            if self.settings.sounds_on:
                sounds.sfx_disappear.play()
        if (
            hasattr(self.hero, "vel_y")
            and abs(self.hero.vel_y) > 22
            and not self.hero.jumping
        ):
            self.state = "game_over"
            self.game_over_timer = 0
            if self.settings.sounds_on:
                sounds.sfx_disappear.play()
        hero_y = self.hero.actor.y
        for platform in self.scenario.platforms:
            if not hasattr(platform, "counted"):
                platform.counted = False
            if not platform.counted and hero_y < platform.y:
                self.platforms_climbed += 1
                platform.counted = True
                self.score += 10
        if self.hero.actor.y - self.scenario.camera_y > HEIGHT:
            self.state = "game_over"
            self.game_over_timer = 0
        if (
            hasattr(self.hero, "vel_y")
            and abs(self.hero.vel_y) > 22
            and not self.hero.jumping
        ):
            self.state = "game_over"
            self.game_over_timer = 0
            if self.settings.sounds_on:
                sounds.sfx_disappear.play()

    def on_mouse_down(self, pos):
        # Handle mouse clicks based on game state
        if self.state != "menu":
            return
        opt = self.menu.get_clicked_option(
            pos, self.settings.music_on, self.settings.sounds_on
        )
        if opt is None:
            return
        if self.settings.sounds_on:
            sounds.sfx_bump.play()
        if opt == 0:
            if self.menu.menu_from_pause:
                self.state = "jogando"
                self.menu.menu_from_pause = False
            else:
                self.start_game()
        elif opt == 1:
            self.scoreboard.load()
            self.state = "scoreboard"
        elif opt == 2:
            self.toggle_music()
        elif opt == 3:
            self.settings.sounds_on = not self.settings.sounds_on
        elif opt == 4:
            self.quit_game()

    def on_key_down(self, key):
        # Handle key presses based on game state
        from pgzero.keyboard import keys

        if self.state == "input_name" and self.inputbox_active:
            if self.inputbox is None:
                self.inputbox = InputBox(
                    WIDTH // 2 - 200, HEIGHT // 2 - 40, 400, 60, maxlen=12
                )
                self.inputbox.text = self.inputbox_text

            class FakeEvent:
                def __init__(self, key):
                    self.type = "KEYDOWN"
                    # Mapear teclas especiais
                    if hasattr(key, "name"):
                        if key.name == "BACKSPACE":
                            self.key = "BACKSPACE"
                            self.unicode = ""
                        elif key.name == "RETURN":
                            self.key = "RETURN"
                            self.unicode = ""
                        elif key.name == "SPACE":
                            self.key = "SPACE"
                            self.unicode = " "
                        elif len(key.name) == 1:
                            self.key = key.name
                            self.unicode = key.name
                        else:
                            self.key = key.name
                            self.unicode = ""
                    else:
                        self.key = str(key)
                        self.unicode = ""

            fake_event = FakeEvent(key)
            result = self.inputbox.handle_event(fake_event)
            if result is not None and result.strip():
                self.scoreboard.save(
                    result.strip(),
                    self.score,
                )
                self.inputbox_active = False
                self.inputbox = None
                self.inputbox_text = ""
                self.scoreboard.load()  # Atualiza scoreboard
                self.state = "menu"
            else:
                self.inputbox_text = self.inputbox.text[:12]
            return
        if self.state == "scoreboard" and key == keys.ESCAPE:
            self.state = "menu"
            self.scoreboard.load()
            return
        if key == keys.ESCAPE:
            if self.state == "jogando":
                self.state = "menu"
                self.menu.menu_from_pause = True
                self.scoreboard.load()


# Instância global do gerenciador
manager = GameManager()


def draw():
    manager.draw()


def update(dt):
    manager.update(dt)


def on_mouse_down(pos):
    manager.on_mouse_down(pos)


def on_key_down(key):
    manager.on_key_down(key)


# --- Funções principais ---
def start_game():
    manager.start_game()


def toggle_music():
    manager.toggle_music()


def quit_game():
    manager.quit_game()
