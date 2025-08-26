from pgzero.builtins import Actor


class Hero:
    def __init__(self, x, y):
        self.actor = Actor("character_purple_idle")
        self.actor.x = x
        self.actor.y = y
        self.state = "idle"
        self.direction = 1
        self._walk_anim = ["character_purple_walk_a", "character_purple_walk_b"]
        self._walk_index = 0
        self._walk_timer = 0
        self._walk_interval = 0.15
        self._idle_anim = ["character_purple_idle", "character_purple_front"]
        self._idle_index = 0
        self._idle_timer = 0
        self._idle_interval = 0.5
        self.jumping = False
        self.vel_y = 0
        self.gravity = 1.2
        self.dropping = False

    @classmethod
    def centered_on_ground(cls, width, height, ground_height, hero_height=128):
        x = width // 2
        y = height - ground_height - (hero_height // 2)
        return cls(x, y)

    def draw(self, camera_y=0):
        self.actor.angle = 0
        y_original = self.actor.y
        self.actor.y = y_original + camera_y
        self.actor.draw()
        self.actor.y = y_original

    def update(self, dt, width, height, ground_height, platforms=None):
        from pgzero.keyboard import keyboard

        if platforms is None:
            platforms = []

        # Horizontal movement and state
        move = False
        if keyboard.left:
            self.actor.x -= 4
            self.direction = -1
            self.state = "walk"
            move = True
        elif keyboard.right:
            self.actor.x += 4
            self.direction = 1
            self.state = "walk"
            move = True
        else:
            self.state = "idle"

        # Block at screen edges
        half_width = self.actor.width // 2
        if self.actor.x < half_width:
            self.actor.x = half_width
        if self.actor.x > width - half_width:
            self.actor.x = width - half_width

        # Jump
        jump_started = False
        if not self.jumping and keyboard.space:
            self.vel_y = -17
            self.jumping = True
            self.state = "jump"
            jump_started = True

        # Gravity and vertical movement
        self.actor.y += self.vel_y
        self.vel_y += self.gravity

        # Landed on ground
        ground_y = height - ground_height - (self.actor.height // 2)
        landed = False

        # Platform collision
        for platform in platforms:
            plat_top = platform.y
            plat_left = platform.x
            plat_right = platform.x + platform.blocks * platform.block_width
            if (
                self.vel_y >= 0
                and plat_left <= self.actor.x <= plat_right
                and self.actor.y + self.vel_y >= plat_top - (self.actor.height // 2)
                and self.actor.y < plat_top
            ):
                self.actor.y = plat_top - (self.actor.height // 2)
                self.jumping = False
                self.vel_y = 0
                landed = True
                break
        # Disable drop after leaving platform
        if self.dropping:
            on_any = False
            for platform in platforms:
                plat_top = platform.y
                plat_left = platform.x
                plat_right = platform.x + platform.block_width * platform.blocks
                if (
                    plat_left <= self.actor.x <= plat_right
                    and abs(self.actor.y - (plat_top - (self.actor.height // 2))) < 4
                ):
                    on_any = True
                    break
            if not on_any:
                self.dropping = False

        # Land on ground if not on platform
        if not landed and self.actor.y >= ground_y:
            self.actor.y = ground_y
            self.jumping = False
            self.vel_y = 0
        elif not landed:
            self.jumping = True

        # Animation
        if self.jumping or self.state == "jump":
            self.actor.image = "character_purple_jump"
        elif self.state == "walk":
            self._walk_timer += dt
            if self._walk_timer >= self._walk_interval:
                self._walk_index = (self._walk_index + 1) % len(self._walk_anim)
                self._walk_timer = 0
            self.actor.image = self._walk_anim[self._walk_index]
        elif self.state == "idle":
            self._idle_timer += dt
            if self._idle_timer >= self._idle_interval:
                self._idle_index = (self._idle_index + 1) % len(self._idle_anim)
                self._idle_timer = 0
            self.actor.image = self._idle_anim[self._idle_index]

        return jump_started
