import pygame
from Logistics import loading

class Projectile:
    """A simple projectile that can optionally slow zombies."""
    def __init__(self, position: tuple[int, int], color="green", freeze=False, speed=8):
        # Load correct image or create fallback circle
        if color == "blue":
            self.image = loading.load_image("assets/projectile_blue.png", scale=(20, 20))
        else:
            self.image = loading.load_image("assets/projectile_green.png", scale=(20, 20))

        self.rect = self.image.get_rect(center=position)
        self.color = color
        self.freeze = freeze   # whether to apply slow
        self.speed = speed

    def update(self):
        """Move the projectile horizontally."""
        self.rect.x += self.speed

    def draw(self, screen):
        """Render projectile sprite."""
        screen.blit(self.image, self.rect)
