import pygame
from Logistics import loading

class Zombie:
    def __init__(self, position: tuple[int, int], speed: int = 1):
        # 4-frame walk cycle
        self.frames = loading.load_sprite_sheet("assets/zombie_walk.png", 4, scale=(110, 140))


        self.fidx = 0.0
        self.anim_speed = 0.15

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)

        self.base_speed = speed
        self.speed = speed
        self.health = 3

        # slow/freeze effect
        self.slow_ticks_left = 0
        self.slow_factor = 1.0

    def apply_slow(self, factor: float = 0.5, ticks: int = 120):
        self.slow_factor = factor
        self.slow_ticks_left = ticks

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_dead(self) -> bool:
        return self.health <= 0

    def update(self):
        # movement
        eff_speed = max(0, int(round(self.base_speed * self.slow_factor)))
        self.speed = eff_speed if eff_speed > 0 else 0
        self.rect.x -= self.speed

        # animate
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
        self.image = self.frames[int(self.fidx)]

        # decay slow
        if self.slow_ticks_left > 0:
            self.slow_ticks_left -= 1
            if self.slow_ticks_left == 0:
                self.slow_factor = 1.0

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        # simple HP bar
        bar_w = self.image.get_width()
        x, y = self.rect.x, self.rect.y - 8
        pygame.draw.rect(screen, (180, 0, 0), (x, y, bar_w, 5))
        green_w = int(bar_w * (self.health / 3))
        pygame.draw.rect(screen, (0, 200, 0), (x, y, green_w, 5))
