import pygame
from Entities.projectile import Projectile
from Logistics import loading

GREEN_PEA_IMG: pygame.Surface | None = None
BLUE_PEA_IMG: pygame.Surface | None = None


def get_projectile_images() -> tuple[pygame.Surface, pygame.Surface]:
    global GREEN_PEA_IMG, BLUE_PEA_IMG
    if GREEN_PEA_IMG is None:
        GREEN_PEA_IMG = loading.load_image("assets/projectile_green.png")
    if BLUE_PEA_IMG is None:
        BLUE_PEA_IMG = loading.load_image("assets/projectile_blue.png")
    return GREEN_PEA_IMG, BLUE_PEA_IMG


# --------------------------------------------------------------
# Base Plant (Peashooter)
# --------------------------------------------------------------
class BasePlant:
    """Easy: Peashooter – fires once per animation loop and disappears after 7 shots."""
    def __init__(self, frames: list[pygame.Surface], position: tuple[int, int]) -> None:
        self.frames = frames
        self.fidx: float = 0.0
        self.anim_speed: float = 0.15
        self.image: pygame.Surface = self.frames[0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=position)
        self.health: int = 5
        self.timer: int = 0
        self.shots_fired: int = 0
        self.max_shots: int = 7

    def update(self, projectiles: list[Projectile]) -> None:
        green_pea, _ = get_projectile_images()

        prev_frame = int(self.fidx)
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
            # fire once per animation loop
            if self.shots_fired < self.max_shots:
                pea_pos = (self.rect.right, self.rect.centery)
                projectiles.append(Projectile(green_pea, pea_pos, speed=7, freeze=False))
                self.shots_fired += 1

        self.image = self.frames[int(self.fidx)]

    def is_expired(self) -> bool:
        return self.shots_fired >= self.max_shots

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        bar_w = self.image.get_width()
        x, y = self.rect.x, self.rect.y - 8
        pygame.draw.rect(screen, (180, 0, 0), (x, y, bar_w, 5))
        green_w = int(bar_w * (self.health / 5))
        pygame.draw.rect(screen, (0, 200, 0), (x, y, green_w, 5))


# --------------------------------------------------------------
# Freeze Plant
# --------------------------------------------------------------
class FreezePlant(BasePlant):
    """Medium: shoots blue peas and disappears after 7 shots."""
    def __init__(self, frames: list[pygame.Surface], position: tuple[int, int]) -> None:
        super().__init__(frames, position)
        self.anim_speed = 0.15  # can tweak for faster/slower shooting

    def update(self, projectiles: list[Projectile]) -> None:
        _, blue_pea = get_projectile_images()

        prev_frame = int(self.fidx)
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
            if self.shots_fired < self.max_shots:
                pea_pos = (self.rect.right, self.rect.centery)
                projectiles.append(Projectile(blue_pea, pea_pos, speed=5, freeze=True))
                self.shots_fired += 1

        self.image = self.frames[int(self.fidx)]


# --------------------------------------------------------------
# Mine Plant
# --------------------------------------------------------------
class MinePlant(BasePlant):
    """Hard: explodes on contact and disappears immediately."""
    def __init__(self, frames: list[pygame.Surface], position: tuple[int, int]) -> None:
        super().__init__(frames, position)
        self.explosion_radius_px: int = 40
        self.exploded: bool = False

    def check_explosion(self, zombies: list) -> bool:
        exploded = False
        for z in zombies[:]:
            if self.rect.colliderect(z.rect.inflate(self.explosion_radius_px, 10)):
                zombies.remove(z)
                exploded = True
        if exploded:
            self.exploded = True
        return exploded

    def is_expired(self) -> bool:
        return self.exploded

    def update(self, projectiles: list[Projectile]) -> None:
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
        self.image = self.frames[int(self.fidx)]
