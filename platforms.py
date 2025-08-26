class Platform:
    def __init__(self, x, y, blocks):
        self.x = x
        self.y = y
        self.blocks = blocks
        self.block_width = 18
        self.block_height = 18

    def draw(self, screen, camera_y=0):
        # Draw the platform blocks
        for i in range(self.blocks):
            screen.blit("wall", (self.x + i * self.block_width, self.y + camera_y))
