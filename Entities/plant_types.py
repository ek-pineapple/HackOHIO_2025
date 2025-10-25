import pygame
from Entities.projectile import Projectile
from Logistics import loading

# Lazy-load projectile images AFTER pygame display initialized
GREEN_PEA_IMG = None
BLUE_PEA_IMG = None

def get_projectile_images():
    """Load projectile images only after pygame display is ready."""
    global GREEN_PEA_IMG, BLUE_PEA_IMG
    if GREEN_PEA_IMG is None:
        GREEN_PEA_IMG = loading.load_image("assets/projectile_green.png")
    if BLUE_PEA_IMG is None:
        BLUE_PEA_IMG = loading.load_image("assets/projectile_blue.png")
    return GREEN_PEA_IMG, BLUE_PEA_IMG


class BasePlant:
    """Easy: Peashooter – shoots green peas."""
    def __init__(self, frames, position):
        self.frames = frames
        self.fidx = 0.0
        self.anim_speed = 0.15
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)
        self.health = 5
        self.shoot_interval = 90
        self.timer = 0

    def update(self, projectiles):
        green_pea, _ = get_projectile_images()

        # animate
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
        self.image = self.frames[int(self.fidx)]

        # shoot
        self.timer += 1
        if self.timer >= self.shoot_interval:
            pea_pos = (self.rect.right, self.rect.centery)
            projectiles.append(Projectile(green_pea, pea_pos, speed=7, freeze=False))
            self.timer = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # optional HP bar
        bar_w = self.image.get_width()
        x, y = self.rect.x, self.rect.y - 8
        pygame.draw.rect(screen, (180, 0, 0), (x, y, bar_w, 5))
        green_w = int(bar_w * (self.health / 5))
        pygame.draw.rect(screen, (0, 200, 0), (x, y, green_w, 5))


class FreezePlant(BasePlant):
    """Medium: shoots blue peas and slows zombies on hit."""
    def __init__(self, frames, position):
        super().__init__(frames, position)
        self.shoot_interval = 120

    def update(self, projectiles):
        _, blue_pea = get_projectile_images()

        # animate
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
        self.image = self.frames[int(self.fidx)]

        # shoot (blue pea, slower)
        self.timer += 1
        if self.timer >= self.shoot_interval:
            pea_pos = (self.rect.right, self.rect.centery)
            projectiles.append(Projectile(blue_pea, pea_pos, speed=5, freeze=True))
            self.timer = 0


class MinePlant(BasePlant):
    """Hard: explodes on contact – no shooting."""
    def __init__(self, frames, position):
        super().__init__(frames, position)
        self.shoot_interval = 99999  # never shoot
        self.explosion_radius_px = 40

    def check_explosion(self, zombies):
        for z in zombies[:]:
            if self.rect.colliderect(z.rect.inflate(self.explosion_radius_px, 10)):
                zombies.remove(z)
                return True
        return False

    def update(self, projectiles):
        # animate only
        self.fidx += self.anim_speed
        if self.fidx >= len(self.frames):
            self.fidx = 0.0
        self.image = self.frames[int(self.fidx)]
