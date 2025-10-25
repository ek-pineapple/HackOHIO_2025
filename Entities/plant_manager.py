import pygame
from Entities.plant_types import BasePlant, FreezePlant, MinePlant

class PlantManager:
    def __init__(self):
        self.plants = []
        self.projectiles = []
        self.pending_plant = None  # (difficulty, frames)
        self.shoot_interval = 90
        self.timer = 0

    def add_plant(self, difficulty, frames, position):
        # Prevent overlapping
        for p in self.plants:
            if p.rect.collidepoint(position):
                return

        if difficulty == "easy":
            new_plant = BasePlant(frames, position)
        elif difficulty == "medium":
            new_plant = FreezePlant(frames, position)
        elif difficulty == "hard":
            new_plant = MinePlant(frames, position)
        else:
            new_plant = BasePlant(frames, position)

        self.plants.append(new_plant)

    def add_pending_plant(self, position):
        """Place the plant earned by answering correctly."""
        if not self.pending_plant:
            return
        difficulty, frames = self.pending_plant
        self.add_plant(difficulty, frames, position)
        print(f"🌱 {difficulty.capitalize()} plant placed at {position}")
        self.pending_plant = None

    def update(self, zombies):
        """Update plants and projectiles."""
        for p in self.plants[:]:
            if isinstance(p, MinePlant):
                if p.check_explosion(zombies):
                    self.plants.remove(p)
            else:
                p.update(self.projectiles)
                if p.is_expired():
                    self.plants.remove(p)

        for proj in self.projectiles[:]:
            proj.update()
            if proj.rect.x > 900:
                self.projectiles.remove(proj)

    def draw(self, screen):
        for p in self.plants:
            p.draw(screen)
        for proj in self.projectiles:
            proj.draw(screen)
