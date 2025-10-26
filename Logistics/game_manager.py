import random
import pygame
from Logistics import constants as cts
from Logistics import loading
from Logistics.collisions import handle_projectile_collisions, handle_zombie_plant_collisions
from Entities.zombie import Zombie
from Entities.plant_manager import PlantManager
from UI.sidebar import Sidebar


class GameManager:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        # Core game components
        self.screen = screen
        self.font = font
        self.plant_manager = PlantManager()
        self.sidebar = Sidebar(screen, cts.SIDEBAR_WIDTH, font)
        self.zombies: list[Zombie] = []

        # Assets
        self.background = loading.load_image("assets/background.png", scale=(cts.SCREEN_WIDTH, cts.SCREEN_HEIGHT))
        self.pea_frames = loading.load_sprite_sheet("assets/plant_peashooter.png", 4, scale=(100, 120))
        self.freeze_frames = loading.load_sprite_sheet("assets/plant_freeze.png", 4, scale=(100, 120))
        self.mine_frames = loading.load_sprite_sheet("assets/plant_mine.png", 4, scale=(110, 85))

        # Timers and state
        self.spawn_timer = 0
        self.spawn_interval = 180
        self.score = 0
        self.bottom_offset = 30

        # 🧮 Quiz tracking
        self.correct_answers = 0
        self.questions_answered = 0

    # ----------------------------------------------------------
    def handle_key_event(self, event: pygame.event.Event):
        """Handle quiz input (A/B/C/D answers)."""
        if event.unicode.upper() in ["A", "B", "C", "D"]:
            correct = self.sidebar.check_answer(event.unicode)
            self.questions_answered += 1
            if correct:
                self.correct_answers += 1
                self.score += 10
                print(f"✅ Correct! (+10) | Score: {self.score}")
            else:
                print("❌ Wrong answer — try again later.")

    # ----------------------------------------------------------
    def handle_mouse_event(self, event: pygame.event.Event):
        """Handle plant placement."""
        mx, my = pygame.mouse.get_pos()
        if mx > cts.SCREEN_SIZE[0]:
            return

        col = (mx - cts.GRID_OFFSET[0]) // cts.CELL_SIZE[0]
        row = (my - cts.GRID_OFFSET[1]) // cts.CELL_SIZE[1]
        if not (0 <= col < cts.GRID_COLS and 0 <= row < cts.GRID_ROWS):
            return

        x = cts.GRID_OFFSET[0] + col * cts.CELL_SIZE[0] + 10
        y = cts.GRID_OFFSET[1] + row * cts.CELL_SIZE[1] + (cts.CELL_SIZE[1] // 2) - 60

        reward = self.sidebar.consume_plant_reward()
        if not reward:
            print("⚠️ Answer correctly to earn a plant first!")
            return

        frames = (
            self.pea_frames if reward == "easy"
            else self.freeze_frames if reward == "medium"
            else self.mine_frames
        )

        self.plant_manager.add_plant(reward, frames, (x, y))
        print(f"🌱 Planted {reward} at {x}, {y}")
        self.sidebar.load_new_question()

    # ----------------------------------------------------------
    def spawn_zombie(self):
        """Spawn a zombie at a random row, respecting the bottom offset."""
        lane = random.randint(0, cts.GRID_ROWS - 1)
        cell_top = cts.GRID_OFFSET[1] + lane * cts.CELL_SIZE[1]
        y = cell_top + (cts.CELL_SIZE[1] // 2) - 60 - self.bottom_offset
        self.zombies.append(Zombie((cts.SCREEN_SIZE[0] - 40, y), speed=0.4))

    # ----------------------------------------------------------
    def update(self) -> bool:
        """Main update logic — returns False if game over."""
        self.plant_manager.update(self.zombies)

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_zombie()
            self.spawn_timer = 0

        for z in self.zombies[:]:
            z.update()
            if z.is_dead():
                self.zombies.remove(z)
                self.score += 5
            elif z.rect.x < 0:
                return False  # game over

        handle_projectile_collisions(self.plant_manager.projectiles, self.zombies)
        handle_zombie_plant_collisions(self.zombies, self.plant_manager.plants)
        return True

    # ----------------------------------------------------------
    def draw(self):
        """Draw everything in the game."""
        self.screen.fill(cts.BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))

        # Optional: grid overlay
        for r in range(cts.GRID_ROWS):
            for c in range(cts.GRID_COLS):
                rect = pygame.Rect(
                    cts.GRID_OFFSET[0] + c * cts.CELL_SIZE[0],
                    cts.GRID_OFFSET[1] + r * cts.CELL_SIZE[1],
                    *cts.CELL_SIZE
                )
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)

        self.plant_manager.draw(self.screen)
        for z in self.zombies:
            z.draw(self.screen)
        self.sidebar.draw()

        # --- Score + quiz stats ---
        score_surface = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        correct_surface = self.font.render(
            f"Quiz: {self.correct_answers}/{self.questions_answered} correct",
            True,
            (0, 100, 0)
        )
        self.screen.blit(score_surface, (20, 10))
        self.screen.blit(correct_surface, (20, 40))

    # ----------------------------------------------------------
    def reset(self):
        """Reset state for new game."""
        self.zombies.clear()
        self.plant_manager.plants.clear()
        self.plant_manager.projectiles.clear()
        self.sidebar.asked.clear()
        self.sidebar.load_new_question()
        self.score = 0
        self.correct_answers = 0
        self.questions_answered = 0
