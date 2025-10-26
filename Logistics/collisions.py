import pygame
from Entities.plant_types import MinePlant, BasePlant, FreezePlant

def handle_projectile_collisions(projectiles: list, zombies: list) -> None:
    for proj in projectiles[:]:
        hit = False
        for z in zombies[:]:
            if proj.rect.colliderect(z.rect):
                z.take_damage(1)
                if proj.freeze:
                    z.apply_slow(factor=0.5, ticks=120)
                hit = True
                if z.is_dead():
                    zombies.remove(z)
                break
        if hit and proj in projectiles:
            projectiles.remove(proj)


def handle_zombie_plant_collisions(zombies: list, plants: list) -> None:
    for z in zombies[:]:
        collided = False
        for p in plants[:]:
            if z.rect.colliderect(p.rect):
                collided = True
                if isinstance(p, MinePlant):
                    # skip mine; handled via PlantManager explosion
                    continue
                # shooter being eaten
                z.speed = 0
                if not hasattr(z, "bite_timer"):
                    z.bite_timer = 0
                z.bite_timer += 1
                if z.bite_timer >= 30:
                    p.health -= 1
                    z.bite_timer = 0
                    if p.health <= 0 and p in plants:
                        plants.remove(p)
                        z.speed = z.base_speed
                break
        if not collided:
            z.speed = z.base_speed
