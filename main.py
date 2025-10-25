import random
import pygame
from Logistics import constants as cts
from Logistics import loading
from Logistics.collisions import handle_projectile_collisions, handle_zombie_plant_collisions
from Logistics.game_states import (
    STATE_START, STATE_UPLOAD, STATE_PLAY, STATE_GAME_OVER,
    draw_start_screen, draw_upload_screen, draw_game_over
)
from Entities.zombie import Zombie
from Entities.plant_manager import PlantManager
from UI.sidebar import Sidebar


# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((cts.SCREEN_SIZE[0] + cts.SIDEBAR_WIDTH, cts.SCREEN_SIZE[1]))
pygame.display.set_caption("Plants vs. Zombies - Study Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# --- Load Assets ---
background = loading.load_image("assets/background.png", scale=(cts.SCREEN_WIDTH, cts.SCREEN_HEIGHT))
pea_frames    = loading.load_sprite_sheet("assets/plant_peashooter.png", 4, scale=(100, 120))
freeze_frames = loading.load_sprite_sheet("assets/plant_freeze.png", 4, scale=(100, 120))
mine_frames   = loading.load_sprite_sheet("assets/plant_mine.png", 4, scale=(110, 85))

# --- Managers & UI ---
plant_manager = PlantManager()
sidebar = Sidebar(screen, cts.SIDEBAR_WIDTH, font)
zombies = []

spawn_timer = 0
spawn_interval = 180  # ~3s at 60fps
game_state = STATE_START


# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Screen Flow ---
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
                        # prevent too low placement
                        if y > (cts.SCREEN_HEIGHT - cts.BOTTOM_OFFSET - 120):
                            y = cts.SCREEN_HEIGHT - cts.BOTTOM_OFFSET - 120
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

    # --- DRAW/UPDATE ---
    if game_state == STATE_START:
        draw_start_screen(screen, font)

    elif game_state == STATE_UPLOAD:
        draw_upload_screen(screen, font)

    elif game_state == STATE_PLAY:
        screen.fill(cts.BACKGROUND_COLOR)
        screen.blit(background, (0, 0))

        # Plants update/draw
        plant_manager.update(zombies)
        plant_manager.draw(screen)

        # Spawn zombies with offset
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            lane = random.randint(0, cts.GRID_ROWS - 1)
            cell_top = cts.GRID_OFFSET[1] + lane * cts.CELL_SIZE[1]
            y = cell_top + (cts.CELL_SIZE[1] // 2) - 60
            if y > (cts.SCREEN_HEIGHT - cts.BOTTOM_OFFSET - 120):
                y = cts.SCREEN_HEIGHT - cts.BOTTOM_OFFSET - 120
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

        # Handle collisions
        handle_projectile_collisions(plant_manager.projectiles, zombies)
        handle_zombie_plant_collisions(zombies, plant_manager.plants)
        sidebar.draw()

    elif game_state == STATE_GAME_OVER:
        draw_game_over(screen, font)

    pygame.display.flip()
    clock.tick(cts.FPS)

pygame.quit()
