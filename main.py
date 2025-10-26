import os
import random
import pygame

from Logistics import constants as cts
from Logistics.file_loader import save_extracted_text
from Logistics.loading import load_questions
from Logistics.game_manager import GameManager
from Logistics.ai_question_gen import generate_questions_from_text

# --- Game States ---
STATE_START = "start"
STATE_UPLOAD = "upload"
STATE_PLAY = "play"
STATE_GAME_OVER = "game_over"

# --- Initialize ---
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
pygame.init()
screen = pygame.display.set_mode((cts.SCREEN_SIZE[0] + cts.SIDEBAR_WIDTH, cts.SCREEN_SIZE[1]))
pygame.display.set_caption("Plants vs. Zombies - Study Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# --- Managers ---
game = GameManager(screen, font)
game_state = STATE_START
uploaded_text_preview = None
uploaded_file_path = None

# ------------------------------------------------------------
# SCREENS
# ------------------------------------------------------------
def draw_start_screen(screen, font):
    screen.fill((90, 200, 90))
    title = font.render("Plants vs. Zombies - Study Edition", True, (0, 0, 0))
    start_text = font.render("Press [SPACE] to Go to Upload Screen", True, (0, 50, 0))
    screen.blit(title, (260, 200))
    screen.blit(start_text, (280, 340))


def draw_upload_screen(screen, font):
    screen.fill((230, 230, 200))
    msg = font.render("Upload your study file (.pdf or .txt)", True, (0, 0, 0))
    upload_text = font.render("Press [U] to Upload", True, (50, 50, 50))
    continue_text = font.render("Press [N] to Start Game", True, (0, 0, 0))
    screen.blit(msg, (200, 260))
    screen.blit(upload_text, (200, 300))
    screen.blit(continue_text, (200, 340))

    global uploaded_text_preview
    if uploaded_text_preview:
        preview_label = font.render("File Preview:", True, (50, 50, 50))
        screen.blit(preview_label, (60, 380))
        preview_lines = uploaded_text_preview.split("\n")[:5]
        y = 410
        for line in preview_lines:
            preview_surface = font.render(line[:70], True, (60, 60, 60))
            screen.blit(preview_surface, (60, y))
            y += 24
    else:
        warning = font.render("(⚠️ PowerPoint uploads are currently disabled)", True, (120, 0, 0))
        screen.blit(warning, (180, 380))


def draw_game_over(screen, font, game: GameManager):
    screen.fill((50, 0, 0))
    over_text = font.render("GAME OVER!", True, (255, 255, 255))
    score_text = font.render(f"Final Score: {game.score}", True, (255, 215, 0))
    accuracy = (game.correct_answers / game.questions_answered * 100) if game.questions_answered else 0
    quiz_text = font.render(
        f"Quiz Accuracy: {game.correct_answers}/{game.questions_answered} ({accuracy:.0f}%)",
        True,
        (200, 200, 200),
    )
    retry_text = font.render("Press [R] to Restart", True, (255, 255, 255))

    screen.blit(over_text, (340, 260))
    screen.blit(score_text, (340, 300))
    screen.blit(quiz_text, (280, 340))
    screen.blit(retry_text, (330, 380))

# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Start Screen ---
        if game_state == STATE_START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = STATE_UPLOAD

        # --- Upload Screen ---
        elif game_state == STATE_UPLOAD:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    # macOS-safe upload (no Tkinter)
                    print("📂 Please enter the full path to your study file (.pdf or .txt):")
                    file_path = input("➡️ File path: ").strip()

                    if os.path.exists(file_path):
                        try:
                            uploaded_file_path = save_extracted_text(file_path)
                            print(f"✅ Uploaded and processed file: {uploaded_file_path}")

                            # --- Generate AI Questions ---
                            ai_questions = generate_questions_from_text(uploaded_file_path)
                            game.sidebar.questions = ai_questions  # Replace questions.json
                            uploaded_text_preview = ai_questions[0]["question"]
                            print(f"🧩 {len(ai_questions)} AI-generated questions loaded for gameplay.")

                        except Exception as e:
                            uploaded_text_preview = f"⚠️ Error: {e}"
                            print(f"⚠️ File or LLM error: {e}")
                    else:
                        print("⚠️ Invalid path or file not found.")

                elif event.key == pygame.K_n:
                    print("🚀 Starting game...")
                    game_state = STATE_PLAY
                    game.sidebar.load_new_question()

        # --- Game Play ---
        elif game_state == STATE_PLAY:
            if event.type == pygame.KEYDOWN:
                game.handle_key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_mouse_event(event)

        # --- Game Over ---
        elif game_state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()
                uploaded_text_preview = None
                uploaded_file_path = None
                game_state = STATE_START

    # --- DRAW PHASE ---
    if game_state == STATE_START:
        draw_start_screen(screen, font)
    elif game_state == STATE_UPLOAD:
        draw_upload_screen(screen, font)
    elif game_state == STATE_PLAY:
        still_playing = game.update()
        game.draw()
        if not still_playing:
            game_state = STATE_GAME_OVER
    elif game_state == STATE_GAME_OVER:
        draw_game_over(screen, font, game)

    pygame.display.flip()
    clock.tick(cts.FPS)

pygame.quit()
