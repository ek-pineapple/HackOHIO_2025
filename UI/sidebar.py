import pygame
from Logistics import loading

class Sidebar:
    def __init__(self, screen, width, font):
        self.screen = screen
        self.width = width
        self.font = font
        self.question = None
        self.choices = []
        self.selected = None
        self.result = None
        self.reward_type = None

        # preload plant icons
        self.icons = {
            "easy": loading.load_image("assets/plant_peashooter.png", scale=(50, 60)),
            "medium": loading.load_image("assets/plant_freeze.png", scale=(50, 60)),
            "hard": loading.load_image("assets/plant_mine.png", scale=(50, 50)),
        }

    def set_question(self, question, choices):
        self.question = question
        self.choices = choices
        self.selected = None
        self.result = None

    def draw(self):
        sidebar_rect = pygame.Rect(self.screen.get_width() - self.width, 0, self.width, self.screen.get_height())
        pygame.draw.rect(self.screen, (240, 240, 220), sidebar_rect)

        # Question area
        if not self.question:
            msg = self.font.render("No question yet", True, (80, 80, 80))
            self.screen.blit(msg, (sidebar_rect.x + 20, 40))
            return

        # Draw question text
        q_text = self.font.render(self.question, True, (0, 0, 0))
        self.screen.blit(q_text, (sidebar_rect.x + 20, 40))

        # Draw answer choices
        for i, choice in enumerate(self.choices):
            color = (0, 0, 0)
            if self.selected == i:
                color = (0, 120, 0) if self.result else (180, 0, 0)
            txt = self.font.render(f"{i+1}. {choice}", True, color)
            self.screen.blit(txt, (sidebar_rect.x + 20, 100 + i*40))

        # Reward section
        if self.reward_type:
            label = self.font.render("Reward if correct:", True, (0, 0, 0))
            self.screen.blit(label, (sidebar_rect.x + 20, sidebar_rect.height - 120))

            reward_text = self.font.render(f"{self.reward_type.upper()} plant", True, (0, 100, 0))
            self.screen.blit(reward_text, (sidebar_rect.x + 80, sidebar_rect.height - 80))

            # draw reward icon
            icon = self.icons.get(self.reward_type)
            if icon:
                self.screen.blit(icon, (sidebar_rect.x + 20, sidebar_rect.height - 90))
