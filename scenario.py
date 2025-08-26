from platforms import Platform
from coin import Coin
from enemy import Enemy
import random


class Scenario:
    def _make_platform(self, x, y, blocks, allow_coin=True, allow_enemy=True):
        plat = Platform(x, y, blocks)
        if allow_coin and random.random() < 0.15:
            block_width = 18
            coin_x_min = x
            coin_x_max = x + blocks * block_width - 32
            coin_x = random.randint(int(coin_x_min), int(coin_x_max))
            coin_y = y - 32
            plat.coin = Coin(coin_x, coin_y)
        else:
            plat.coin = None
        if allow_enemy and random.random() < 0.3:
            plat.enemy = Enemy(x, y, blocks * 18)
        else:
            plat.enemy = None
        return plat

    def __init__(self, width, height, ground_height=64):
        self.width = width
        self.height = height
        self.ground_height = ground_height
        self.hills_height = 256
        self.hills_width = 256
        self.sky_width = 256
        self.sky_height = 256
        self.camera_y = 0
        self.platforms = []
        hero_jump_height = 110
        ground_top = self.height - self.ground_height
        start_y = ground_top - int(hero_jump_height * 0.9)
        self._create_platforms(start_y=start_y, n_platforms=10)

    def _create_platforms(self, start_y, n_platforms=10):
        hero_width = 128
        hero_jump_height = 110
        hero_jump_dx = 180
        min_width = max(5 * 18, hero_width // 18 * 18 + 2 * 18)
        min_blocks = min_width // 18
        margin_x = 40
        min_vertical = int(hero_jump_height * 0.85)
        max_vertical = int(hero_jump_height * 0.95)
        min_gap = 60
        if self.platforms:
            topo = min(self.platforms, key=lambda p: p.y)
            last_x, last_y = topo.x, topo.y
        else:
            hero_base_y = self.height - self.ground_height
            last_y = hero_base_y - random.randint(min_vertical, max_vertical)
            last_x = random.randint(margin_x, self.width - margin_x - min_blocks * 18)
            first_p = self._make_platform(last_x, last_y, min_blocks)
            self.platforms.append(first_p)
        count = 0
        while count < n_platforms:
            num_paths = random.randint(2, 3)
            vertical_gap = max(min_gap, random.randint(min_vertical, max_vertical))
            level_y = last_y - vertical_gap
            used_x = []
            prev_level = [p for p in self.platforms if abs(p.y - last_y) < 5]
            if not prev_level:
                prev_level = [
                    self._make_platform(
                        last_x, last_y, min_blocks, allow_coin=False, allow_enemy=False
                    )
                ]
            generated = 0
            attempts = 0
            while generated < num_paths and attempts < 20:
                blocks = min_blocks
                if random.random() < 0.2:
                    blocks = int(min_blocks * 2.5)
                platform_width = blocks * 18
                px = random.randint(margin_x, self.width - margin_x - platform_width)
                if not any(abs(px - prev.x) <= hero_jump_dx for prev in prev_level):
                    attempts += 1
                    continue
                overlap = False
                for p in self.platforms:
                    px1 = p.x
                    px2 = p.x + p.width if hasattr(p, "width") else p.x + platform_width
                    x1 = px
                    x2 = px + platform_width
                    if not (x2 + 32 <= px1 or x1 >= px2 + 32):
                        if abs(level_y - p.y) < 36:
                            overlap = True
                            break
                if overlap:
                    attempts += 1
                    continue
                plat = self._make_platform(px, level_y, blocks)
                self.platforms.append(plat)
                used_x.append(px)
                generated += 1
            if generated == 0:
                prev = random.choice(prev_level)
                blocks = min_blocks
                platform_width = blocks * 18
                px = max(margin_x, min(self.width - margin_x - platform_width, prev.x))
                plat = self._make_platform(
                    px, level_y, blocks, allow_coin=False, allow_enemy=False
                )
                self.platforms.append(plat)
                used_x.append(px)
            last_y = level_y
            count += 1

    def draw(self, screen, camera_y=0):
        for x in range(0, self.width, self.sky_width):
            for y in range(0, self.height, self.sky_height):
                screen.blit("background_solid_cloud", (x, y))
        for x in range(0, self.width, self.hills_width):
            for y in range(
                self.height - self.hills_height, self.height, self.hills_height
            ):
                screen.blit("background_color_hills", (x, y))
        tile_width = 64
        for x in range(0, self.width, tile_width):
            screen.blit(
                "terrain_grass_horizontal_middle", (x, self.height - self.ground_height)
            )
        top = -camera_y - self.height * 2
        bottom = -camera_y + self.height * 2
        for platform in self.platforms:
            if top <= platform.y <= bottom:
                platform.draw(screen, camera_y=camera_y)
                if hasattr(platform, "coin") and platform.coin:
                    platform.coin.draw(screen, camera_y=camera_y)
                if hasattr(platform, "enemy") and platform.enemy:
                    platform.enemy.draw(screen, camera_y=camera_y)
        min_keep_y = -camera_y - self.height * 2
        self.platforms = [p for p in self.platforms if p.y >= min_keep_y]

    def ensure_platforms_above(self, min_y):
        platforms_above = [p.y for p in self.platforms if p.y > min_y]
        if not platforms_above:
            self._create_platforms(start_y=min_y + 80, n_platforms=10)
