import pygame

class Projectile:
    def __init__(self, image, position, speed=7, freeze=False):
        # Target: pea ≈ 1/4 of plant (plants ≈120px → pea ≈30px tall)
        desired_height = 30
        w, h = image.get_size()
        scale_factor = desired_height / h
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)

        self.image = pygame.transform.smoothscale(image, (new_w, new_h))
        self.rect = self.image.get_rect(center=position)

        self.speed = speed
        self.freeze = freeze

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
