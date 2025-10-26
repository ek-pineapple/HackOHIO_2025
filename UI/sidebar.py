import pygame
import random
import json
import os

class Sidebar:
    def __init__(self, screen: pygame.Surface, width: int, font: pygame.font.Font) -> None:
        self.screen = screen
        self.width = width
        self.font = font
        self.bg_color = (220, 220, 220)
        self.text_color = (20, 20, 20)

        # --- Load questions ---
        json_path = os.path.join("assets", "questions.json")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.questions: list[dict] = json.load(f)
            print(f"✅ Loaded {len(self.questions)} questions from {json_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Failed to load questions.json: {e}")
            self.questions = []

        # --- State ---
        self.asked: list[dict] = []
        self.current_question: dict | None = None
        self.feedback: str = ""
        self.active: bool = True  # waiting for answer or ready to ask new question

        # --- Plant reward preview ---
        self.next_plant_name: str | None = None
        self.next_plant_difficulty: str | None = None

        self.load_new_question()

    # ------------------------------------------------------------------
    def load_new_question(self) -> None:
        """Pick a new question that hasn't been answered correctly yet."""
        if not self.questions:
            self.current_question = None
            return

        remaining = [q for q in self.questions if q not in self.asked]
        if remaining:
            self.current_question = random.choice(remaining)
        else:
            self.asked.clear()
            self.current_question = random.choice(self.questions)
        self.feedback = ""
        self.active = True

    # ------------------------------------------------------------------
    def check_answer(self, user_choice: str) -> bool:
        """Check if player's answer is correct and store result."""
        if not self.current_question:
            return False

        index = ord(user_choice.upper()) - ord("A")
        if index < 0 or index >= len(self.current_question["choices"]):
            return False

        chosen_answer = self.current_question["choices"][index]
        correct_answer = self.current_question["answer"]
        correct = chosen_answer == correct_answer

        if correct:
            self.feedback = "✅ Correct!"
            if self.current_question not in self.asked:
                self.asked.append(self.current_question)
            difficulty = self.current_question.get("difficulty", "easy")

            # 🎯 Store the reward plant
            self.next_plant_difficulty = difficulty
            if difficulty == "easy":
                self.next_plant_name = "Peashooter"
            elif difficulty == "medium":
                self.next_plant_name = "Freeze Plant"
            else:
                self.next_plant_name = "Mine"
        else:
            self.feedback = f"❌ Wrong! Correct was: {correct_answer}"
            self.next_plant_name = None
            self.next_plant_difficulty = None

        # Lock out further answers until planting happens
        self.active = False
        return correct

    # ------------------------------------------------------------------
    def consume_plant_reward(self) -> str | None:
        """Called by main.py after the player places the plant."""
        difficulty = self.next_plant_difficulty
        self.next_plant_name = None
        self.next_plant_difficulty = None
        return difficulty

    # ------------------------------------------------------------------
    def get_difficulty(self) -> str:
        """Return difficulty for current question or earned plant."""
        if self.next_plant_difficulty:
            return self.next_plant_difficulty
        if not self.current_question:
            return "easy"
        return self.current_question.get("difficulty", "easy")

    # ------------------------------------------------------------------
    def draw(self) -> None:
        """Render the sidebar and question UI."""
        rect = pygame.Rect(self.screen.get_width() - self.width, 0, self.width, self.screen.get_height())
        pygame.draw.rect(self.screen, self.bg_color, rect)

        header = self.font.render("Study Mode", True, (0, 100, 0))
        self.screen.blit(header, (rect.x + 20, 20))
        pygame.draw.line(self.screen, (0, 0, 0), (rect.x, 60), (rect.x + self.width, 60), 2)

        # --- Question text ---
        if self.current_question:
            q_surface = self.font.render(self.current_question["question"], True, self.text_color)
            self.screen.blit(q_surface, (rect.x + 20, 80))

            y_offset = 120
            for i, choice in enumerate(self.current_question["choices"]):
                label = f"{chr(65 + i)}) {choice}"
                opt_surface = self.font.render(label, True, self.text_color)
                self.screen.blit(opt_surface, (rect.x + 20, y_offset))
                y_offset += 40

        # --- Feedback ---
        if self.feedback:
            color = (0, 150, 0) if "✅" in self.feedback else (200, 0, 0)
            fb_surface = self.font.render(self.feedback, True, color)
            self.screen.blit(fb_surface, (rect.x + 20, y_offset + 20))

        # --- Reward Preview ---
        if self.next_plant_name:
            label = f"Next Plant: {self.next_plant_name}"
            color = (0, 100, 0)
            surface = self.font.render(label, True, color)
            self.screen.blit(surface, (rect.x + 20, rect.bottom - 60))
