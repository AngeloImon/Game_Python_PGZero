import random
from pgzero.builtins import Actor

ENEMY_TYPES = [
    {"name": "worm", "images": ["worm_ring_move_a", "worm_ring_move_b"]},
    {"name": "mouse", "images": ["mouse_walk_a", "mouse_walk_b"]},
    {"name": "slime", "images": ["slime_spike_walk_a", "slime_spike_walk_b"]},
]

ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_GRAVITY = 1.2


class Enemy:
    def __init__(self, x, y, platform_width):
        self.type_data = random.choice(ENEMY_TYPES)
        self.name = self.type_data["name"]
        self.images = self.type_data["images"]
        self.actors = [Actor(img) for img in self.images]
        self.frame = 0
        self.frame_timer = 0.0
        self.frame_interval = 0.18
        self.x = x + (platform_width - ENEMY_WIDTH) / 2
        self.y = y - ENEMY_HEIGHT - 5
        self.platform_width = platform_width
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(1.0, 2.0)
        self.sprite_width = ENEMY_WIDTH
        self.sprite_height = ENEMY_HEIGHT
        self.left_limit = x
        self.right_limit = x + platform_width - self.sprite_width
        self.velocity_y = 0
        self.on_platform = False
        self.platform_top = y
        self.platform_left = x
        self.platform_right = x + platform_width

    def update(self, dt):
        # Update enemy animation and movement
        self.frame_timer += dt
        if self.frame_timer >= self.frame_interval:
            self.frame = (self.frame + 1) % len(self.images)
            self.frame_timer = 0.0
        if not self.on_platform:
            self.y += self.velocity_y
            self.velocity_y += ENEMY_GRAVITY
            feet_y = self.y + ENEMY_HEIGHT
            center_x = self.x + ENEMY_WIDTH // 2
            if (
                self.velocity_y >= 0
                and self.platform_left <= center_x <= self.platform_right
                and feet_y >= self.platform_top
            ):
                self.y = self.platform_top - ENEMY_HEIGHT
                self.velocity_y = 0
                self.on_platform = True
        else:
            self.x += self.direction * self.speed
            if self.x < self.left_limit:
                self.x = self.left_limit
                self.direction = 1
            elif self.x > self.right_limit:
                self.x = self.right_limit
                self.direction = -1

    def draw(self, screen, camera_y=0):
        # Draw the enemy sprite
        actor = self.actors[self.frame]
        actor.x = self.x + ENEMY_WIDTH // 2
        actor.y = self.y + ENEMY_HEIGHT // 2 + camera_y
        actor.draw()
