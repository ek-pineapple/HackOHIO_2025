import pygame
from Entities.plant_types import BasePlant, FreezePlant, MinePlant

class PlantManager:
    def __init__(self) -> None:
        self.plants: list[BasePlant | FreezePlant | MinePlant] = []
        self.projectiles: list = []
        self.pending_plant: tuple[str, list[pygame.Surface]] | None = None
        self.shoot_interval: int = 90
        self.timer: int = 0

    # ----------------------------------------------------------------------
    def add_plant(self, difficulty: str, frames: list[pygame.Surface], position: tuple[int, int]) -> None:
        """Add a new plant of the given difficulty at the given position."""
        # Prevent overlapping with an existing plant
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

    # ----------------------------------------------------------------------
    def add_pending_plant(self, position: tuple[int, int]) -> None:
        """Place the plant earned by answering correctly."""
        if not self.pending_plant:
            return
        difficulty, frames = self.pending_plant
        self.add_plant(difficulty, frames, position)
        print(f"🌱 {difficulty.capitalize()} plant placed at {position}")
        self.pending_plant = None

    # ----------------------------------------------------------------------
    def update(self, zombies: list) -> None:
        """Update plants, handle explosions, and update projectiles."""
        for p in self.plants[:]:
            if isinstance(p, MinePlant):
                # Mines still animate even before exploding
                p.update(self.projectiles)
                if p.check_explosion(zombies):
                    self.plants.remove(p)
            else:
                p.update(self.projectiles)
                # Safely check for expiry
                if hasattr(p, "is_expired") and p.is_expired():
                    self.plants.remove(p)

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update()
            if proj.rect.x > 900:
                self.projectiles.remove(proj)

    # ----------------------------------------------------------------------
    def draw(self, screen: pygame.Surface) -> None:
        """Draw all plants and their projectiles."""
        for p in self.plants:
            p.draw(screen)
        for proj in self.projectiles:
            proj.draw(screen)

