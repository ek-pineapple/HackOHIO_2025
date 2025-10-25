import pygame
from Logistics import loading

class Zombie:
    def __init__(self, position: tuple[int, int], speed: float = 0.4):
        """Walking zombie with health, animation, and optional slow effect."""
        self.frames = loading.load_sprite_sheet("assets/zombie_walk.png", 4, scale=(110, 140))
        self.fidx = 0.0
        self.anim_speed = 0.15

        # sprite setup
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)

        # movement and position
        self.speed = speed                # base walking speed
        self.base_speed = speed
        self.slow_factor = 1.0
        self.slow_ticks_left = 0
        self.float_x = float(self.rect.x)  # accumulate movement properly

        # health
        self.health = 3

    def apply_slow(self, factor: float = 0.5, ticks: int = 120):
        """Temporarily reduce movement speed."""
        self.slow_factor = factor
        self.slow_ticks_left = ticks

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def is_dead(self) -> bool:
        return self.health <= 0

    def update(self):
        """Update zombie movement and animation."""
        # ✅ guaranteed visible forward motion
        move_speed = max(0.3, self.speed * self.slow_factor)
        self.float_x -= move_speed
        self.rect.x = int(self.float_x)

        # animate
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
        self.image = self.frames[int(self.fidx)]

        # slow decay
        if self.slow_ticks_left > 0:
            self.slow_ticks_left -= 1
            if self.slow_ticks_left == 0:
                self.slow_factor = 1.0

    def draw(self, screen: pygame.Surface):
        """Render zombie and health bar."""
        screen.blit(self.image, self.rect)

        # health bar
        bar_w = self.image.get_width()
        bar_h = 5
        x, y = self.rect.x, self.rect.y - 8
        pygame.draw.rect(screen, (180, 0, 0), (x, y, bar_w, bar_h))
        green_w = int(bar_w * (self.health / 3))
        pygame.draw.rect(screen, (0, 200, 0), (x, y, green_w, bar_h))
