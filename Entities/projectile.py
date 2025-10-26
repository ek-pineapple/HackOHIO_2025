import pygame

class Projectile:
    def __init__(
        self,
        image: pygame.Surface,
        position: tuple[int | float, int | float],
        speed: float = 7,
        freeze: bool = False,
    ) -> None:
        """A single projectile fired by a plant."""
        desired_height = 30
        w, h = image.get_size()
        scale_factor = desired_height / h
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)

        self.image: pygame.Surface = pygame.transform.smoothscale(image, (new_w, new_h))

        # ensure integer center for rect
        center_pos = (int(position[0]), int(position[1]))
        self.rect: pygame.Rect = self.image.get_rect(center=center_pos)

        self.speed: float = speed
        self.freeze: bool = freeze
        self.x: float = float(self.rect.x)  # smooth movement tracking

    def update(self) -> None:
        self.x += self.speed
        self.rect.x = int(self.x)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
