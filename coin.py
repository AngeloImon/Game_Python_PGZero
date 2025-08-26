import random


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = ["coin_gold", "coin_gold_side"]
        self.frame = 0
        self.frame_timer = 0.0
        self.frame_interval = 0.15  # seconds

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_interval:
            self.frame = (self.frame + 1) % len(self.images)
            self.frame_timer = 0.0

    def draw(self, screen, camera_y=0):
        screen.blit(self.images[self.frame], (self.x, self.y + camera_y))
