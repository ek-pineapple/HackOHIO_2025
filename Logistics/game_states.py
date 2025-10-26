import pygame
from Logistics import constants as cts

STATE_START = "start"
STATE_UPLOAD = "upload"
STATE_PLAY = "play"
STATE_GAME_OVER = "game_over"

def draw_start_screen(screen, font):
    screen.fill((90, 200, 90))
    title = font.render("Plants vs Zombies - Study Edition", True, (0, 0, 0))
    start_text = font.render("Press [SPACE] to Begin Upload", True, (0, 50, 0))
    screen.blit(title, (260, 200))
    screen.blit(start_text, (330, 340))

def draw_upload_screen(screen, font):
    screen.fill((230, 230, 200))
    msg = font.render("Upload your notes here (placeholder)", True, (0, 0, 0))
    next_text = font.render("Press [N] to Continue to Game", True, (0, 0, 0))
    screen.blit(msg, (280, 300))
    screen.blit(next_text, (320, 360))

def draw_game_over(screen, font):
    screen.fill((50, 0, 0))
    over_text = font.render("GAME OVER! Zombies reached your house!", True, (255, 255, 255))
    retry_text = font.render("Press [R] to Restart", True, (255, 255, 255))
    screen.blit(over_text, (250, 320))
    screen.blit(retry_text, (360, 360))
