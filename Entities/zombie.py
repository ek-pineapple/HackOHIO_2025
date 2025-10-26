import pygame
from Logistics import loading

class Zombie:
    def __init__(self, position: tuple[int, int], speed: float = 0.4) -> None:
        """Initialize a walking zombie with optional speed override."""
        self.frames: list[pygame.Surface] = loading.load_sprite_sheet(
            "assets/zombie_walk.png", 4, scale=(110, 140)
        )

        self.fidx: float = 0.0
        self.anim_speed: float = 0.15

        self.image: pygame.Surface = self.frames[0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=position)

        # Floating position for smooth sub-pixel movement
        self.x: float = float(self.rect.x)
        self.y: float = float(self.rect.y)

        self.base_speed: float = speed
        self.speed: float = speed
        self.health: int = 3

        # Slow/freeze effect
        self.slow_ticks_left: int = 0
        self.slow_factor: float = 1.0

    def apply_slow(self, factor: float = 0.5, ticks: int = 120) -> None:
        self.slow_factor = factor
        self.slow_ticks_left = ticks

    def take_damage(self, amount: int) -> None:
        self.health = max(0, self.health - amount)

    def is_dead(self) -> bool:
        return self.health <= 0

    def update(self) -> None:
        """Animate and move zombie leftward."""
        eff_speed: float = max(0.0, self.base_speed * self.slow_factor)
        self.x -= eff_speed
        self.rect.x = int(self.x)

        # Animate
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
        self.image = self.frames[int(self.fidx)]

        # Decay slow
        if self.slow_ticks_left > 0:
            self.slow_ticks_left -= 1
            if self.slow_ticks_left == 0:
                self.slow_factor = 1.0

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        bar_w: int = self.image.get_width()
        x, y = self.rect.x, self.rect.y - 8
        pygame.draw.rect(screen, (180, 0, 0), (x, y, bar_w, 5))
        green_w: int = int(bar_w * (self.health / 3))
        pygame.draw.rect(screen, (0, 200, 0), (x, y, green_w, 5))
