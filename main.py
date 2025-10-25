import random
import pygame
from Logistics import constants as cts
from Logistics import loading
from Logistics.collisions import handle_projectile_collisions, handle_zombie_plant_collisions
from Entities.zombie import Zombie
from Entities.plant_manager import PlantManager
from UI.sidebar import Sidebar

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

# --- Assets ---
background = loading.load_image("assets/background.png", scale=(cts.SCREEN_WIDTH, cts.SCREEN_HEIGHT))
pea_frames    = loading.load_sprite_sheet("assets/plant_peashooter.png", 4, scale=(100, 120))
freeze_frames = loading.load_sprite_sheet("assets/plant_freeze.png", 4, scale=(100, 120))
mine_frames   = loading.load_sprite_sheet("assets/plant_mine.png", 4, scale=(110, 85))

# --- Managers & UI ---
plant_manager = PlantManager()
sidebar = Sidebar(screen, cts.SIDEBAR_WIDTH, font)
zombies = []

spawn_timer = 0
spawn_interval = 180
game_state = STATE_START

# --- Helper Screens ---
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

def draw_game_over(screen, font):
    screen.fill((50, 0, 0))
    over_text = font.render("GAME OVER! Zombies reached your house!", True, (255, 255, 255))
    retry_text = font.render("Press [R] to Restart", True, (255, 255, 255))
    screen.blit(over_text, (250, 320))
    screen.blit(retry_text, (360, 360))

def draw_grid_overlay():
    for r in range(cts.GRID_ROWS):
        for c in range(cts.GRID_COLS):
            x = cts.GRID_OFFSET[0] + c * cts.CELL_SIZE[0]
            y = cts.GRID_OFFSET[1] + r * cts.CELL_SIZE[1]
            pygame.draw.rect(screen, (50, 100, 50), pygame.Rect(x, y, *cts.CELL_SIZE), 1)

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Screen Flow Logic ---
        if game_state == STATE_START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = STATE_UPLOAD

        elif game_state == STATE_UPLOAD:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                game_state = STATE_PLAY

        elif game_state == STATE_PLAY:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if mx <= cts.SCREEN_SIZE[0]:
                    col = (mx - cts.GRID_OFFSET[0]) // cts.CELL_SIZE[0]
                    row = (my - cts.GRID_OFFSET[1]) // cts.CELL_SIZE[1]
                    if 0 <= col < cts.GRID_COLS and 0 <= row < cts.GRID_ROWS:
                        cell_top = cts.GRID_OFFSET[1] + row * cts.CELL_SIZE[1]
                        y = cell_top + (cts.CELL_SIZE[1] // 2) - 60
                        x = cts.GRID_OFFSET[0] + col * cts.CELL_SIZE[0] + 10
                        difficulty = random.choice(["easy", "medium", "hard"])
                        frames = pea_frames if difficulty == "easy" else freeze_frames if difficulty == "medium" else mine_frames
                        plant_manager.add_plant(difficulty, frames, (x, y))
                        print(f"Placed {difficulty} at row {row}, col {col}")

        elif game_state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                zombies.clear()
                plant_manager.plants.clear()
                plant_manager.projectiles.clear()
                game_state = STATE_START

    # --- DRAWING / UPDATING ---
    if game_state == STATE_START:
        draw_start_screen(screen, font)

    elif game_state == STATE_UPLOAD:
        draw_upload_screen(screen, font)

    elif game_state == STATE_PLAY:
        screen.fill(cts.BACKGROUND_COLOR)
        screen.blit(background, (0, 0))

        # Plants
        plant_manager.update(zombies)
        plant_manager.draw(screen)

        # Spawn zombies
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            lane = random.randint(0, cts.GRID_ROWS - 1)
            cell_top = cts.GRID_OFFSET[1] + lane * cts.CELL_SIZE[1]
            y = cell_top + (cts.CELL_SIZE[1] // 2) - 60
            zombies.append(Zombie((cts.SCREEN_SIZE[0] - 40, y)))
            spawn_timer = 0

        # Update zombies
        for z in zombies[:]:
            z.update()
            z.draw(screen)
            if z.is_dead():
                zombies.remove(z)
            elif z.rect.x < 0:
                game_state = STATE_GAME_OVER
                break

        # Collisions
        handle_projectile_collisions(plant_manager.projectiles, zombies)
        handle_zombie_plant_collisions(zombies, plant_manager.plants)
        sidebar.draw()

    elif game_state == STATE_GAME_OVER:
        draw_game_over(screen, font)

    pygame.display.flip()
    clock.tick(cts.FPS)

pygame.quit()
