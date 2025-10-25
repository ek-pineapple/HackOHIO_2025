import pygame

class Sidebar:
    def __init__(self, screen, width, font):
        self.screen = screen
        self.width = width
        self.font = font
        self.bg_color = (220, 220, 220)
        self.text_color = (20, 20, 20)

        # Example placeholders for question display
        self.current_question = "Which plant shoots freezing peas?"
        self.options = ["A) Peashooter", "B) Freeze Plant", "C) Mine Plant"]
        self.feedback = ""

    def draw(self):
        # Sidebar background
        rect = pygame.Rect(self.screen.get_width() - self.width, 0, self.width, self.screen.get_height())
        pygame.draw.rect(self.screen, self.bg_color, rect)

        # Header
        header = self.font.render("Study Mode", True, (0, 100, 0))
        self.screen.blit(header, (rect.x + 20, 20))

        # Divider
        pygame.draw.line(self.screen, (0, 0, 0), (rect.x, 60), (rect.x + self.width, 60), 2)

        # Question text
        question_surface = self.font.render(self.current_question, True, self.text_color)
        self.screen.blit(question_surface, (rect.x + 20, 80))

        # Options
        y_offset = 120
        for option in self.options:
            text_surface = self.font.render(option, True, self.text_color)
            self.screen.blit(text_surface, (rect.x + 20, y_offset))
            y_offset += 40

        # Feedback (like “Correct!” or “Try again”)
        if self.feedback:
            feedback_surface = self.font.render(self.feedback, True, (0, 150, 0))
            self.screen.blit(feedback_surface, (rect.x + 20, y_offset + 20))
