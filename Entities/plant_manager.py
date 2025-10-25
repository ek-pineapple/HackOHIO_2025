import pygame
from Entities.projectile import Projectile
from Entities.plant_types import BasePlant, FreezePlant, MinePlant

class PlantManager:
    def __init__(self):
        self.plants: list = []
        self.projectiles: list[Projectile] = []

    def add_plant(self, difficulty: str, frames_or_image, position: tuple[int, int]):
        """Add plant by difficulty. Accepts a list of frames OR a single image."""
        # prevent overlapping
        for p in self.plants:
            if p.rect.collidepoint(position):
                return

        # normalize frames
        if isinstance(frames_or_image, list):
            frames = frames_or_image
        else:
            # if a single Surface is passed, just use it as a static 1-frame plant
            frames = [frames_or_image]

        if difficulty == "easy":
            plant = BasePlant(frames, position)
        elif difficulty == "medium":
            plant = FreezePlant(frames, position)
        elif difficulty == "hard":
            plant = MinePlant(frames, position)
        else:
            plant = BasePlant(frames, position)

        self.plants.append(plant)

    def update(self, zombies: list):
        for p in self.plants[:]:
            if isinstance(p, MinePlant):
                p.update(self.projectiles)
                if p.check_explosion(zombies):
                    self.plants.remove(p)
            else:
                p.update(self.projectiles)

        # projectiles
        for proj in self.projectiles[:]:
            proj.update()
            # off-screen
            if proj.rect.x > 2000:  # sufficiently large bound
                self.projectiles.remove(proj)

    def draw(self, screen: pygame.Surface):
        for p in self.plants:
            p.draw(screen)
        for proj in self.projectiles:
            proj.draw(screen)
