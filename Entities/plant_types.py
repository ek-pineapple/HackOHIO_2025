import pygame
from Entities.projectile import Projectile

class BasePlant:
    """Basic shooting plant — green peashooter."""
    def __init__(self, frames, position):
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)

        self.frame_idx = 0
        self.frame_speed = 0.1

        self.shoot_timer = 0
        self.shoot_interval = 90  # about 1.5 seconds
        self.shoot_limit = 7      # shoots 7 times then disappears
        self.shots_fired = 0

        self.health = 3
        self.projectile_color = "green"

    def update(self, projectiles):
        """Animate, shoot, and manage life cycle."""
        self.frame_idx += self.frame_speed
        if self.frame_idx >= len(self.frames):
            self.frame_idx = 0
        self.image = self.frames[int(self.frame_idx)]

        # Shoot periodically
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval and self.shots_fired < self.shoot_limit:
            self.shoot_timer = 0
            self.shoot(projectiles)

        # Remove after limit reached
        if self.shots_fired >= self.shoot_limit:
            self.health = 0

    def shoot(self, projectiles):
        """Fire a single projectile forward."""
        projectile_pos = (self.rect.right - 10, self.rect.centery)
        projectiles.append(Projectile(projectile_pos, color=self.projectile_color))
        self.shots_fired += 1

    def is_expired(self):
        """Returns True when plant should be removed."""
        return self.health <= 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class FreezePlant(BasePlant):
    """Shoots blue peas that slow zombies."""
    def __init__(self, frames, position):
        super().__init__(frames, position)
        self.projectile_color = "blue"
        self.health = 3

    def shoot(self, projectiles):
        projectile_pos = (self.rect.right - 10, self.rect.centery)
        projectiles.append(Projectile(projectile_pos, color=self.projectile_color, freeze=True))
        self.shots_fired += 1


class MinePlant:
    """Explodes when a zombie touches it."""
    def __init__(self, frames, position):
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)
        self.frame_idx = 0
        self.frame_speed = 0.1

        self.active = False
        self.timer = 180  # 3 seconds to arm
        self.exploded = False
        self.health = 1  # keeps collision code safe

    def update(self, projectiles=None):
        # Arm timer
        if not self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = True

        # Animate idle bounce
        self.frame_idx += self.frame_speed
        if self.frame_idx >= len(self.frames):
            self.frame_idx = 0
        self.image = self.frames[int(self.frame_idx)]

    def check_explosion(self, zombies):
        """Detonates when any zombie overlaps."""
        if not self.active:
            return False

        for z in zombies[:]:
            if self.rect.colliderect(z.rect):
                # big damage
                z.take_damage(3)
                self.exploded = True
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_expired(self):
        """Mines vanish after exploding."""
        return self.exploded
