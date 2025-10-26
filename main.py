import pygame
from Logistics import constants as cts
from Logistics.game_manager import GameManager

# --- Game States ---
STATE_START = "start"
STATE_UPLOAD = "upload"
STATE_PLAY = "play"
STATE_GAME_OVER = "game_over"

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((cts.SCREEN_SIZE[0] + cts.SIDEBAR_WIDTH, cts.SCREEN_SIZE[1]))
pygame.display.set_caption("Plants vs. Zombies - Study Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# --- Managers ---
game = GameManager(screen, font)
game_state = STATE_START

# --- Screen helpers ---
def draw_start_screen(screen, font):
    screen.fill((90, 200, 90))
    title = font.render("Plants vs Zombies - Study Edition", True, (0, 0, 0))
    start_text = font.render("Press [SPACE] to Begin Upload", True, (0, 50, 0))
    screen.blit(title, (260, 200))
    screen.blit(start_text, (330, 340))


def draw_upload_screen(screen, font):
    screen.fill((230, 230, 200))
    msg = font.render("Upload your notes here (placeholder screen)", True, (0, 0, 0))
    next_text = font.render("Press [N] to Continue to Game", True, (0, 0, 0))
    screen.blit(msg, (280, 300))
    screen.blit(next_text, (320, 360))


def draw_game_over(screen, font, game: GameManager):
    screen.fill((50, 0, 0))
    over_text = font.render("GAME OVER!", True, (255, 255, 255))

    # 🧠 Show score + quiz accuracy
    score_text = font.render(f"Final Score: {game.score}", True, (255, 215, 0))
    accuracy = (
        (game.correct_answers / game.questions_answered) * 100
        if game.questions_answered > 0
        else 0
    )
    quiz_text = font.render(
        f"Quiz Accuracy: {game.correct_answers}/{game.questions_answered} ({accuracy:.0f}%)",
        True,
        (200, 200, 200),
    )
    retry_text = font.render("Press [R] to Restart", True, (255, 255, 255))

    screen.blit(over_text, (340, 280))
    screen.blit(score_text, (350, 320))
    screen.blit(quiz_text, (300, 360))
    screen.blit(retry_text, (360, 400))


# --- Main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == STATE_START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = STATE_UPLOAD

        elif game_state == STATE_UPLOAD:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                game_state = STATE_PLAY
                game.sidebar.load_new_question()

        elif game_state == STATE_PLAY:
            if event.type == pygame.KEYDOWN:
                game.handle_key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_mouse_event(event)

        elif game_state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()
                game_state = STATE_START

    # --- DRAWING ---
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
