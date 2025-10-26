import pygame
import json
import os
import random


def load_image(path, scale=None, keep_aspect=True):
    """Load an image and optionally scale while keeping proportions."""
    image = pygame.image.load(path).convert_alpha()
    if scale:
        if keep_aspect:
            iw, ih = image.get_size()
            sw, sh = scale
            aspect = iw / ih
            if sw / sh > aspect:  # too wide
                sw = int(sh * aspect)
            else:
                sh = int(sw / aspect)
            image = pygame.transform.smoothscale(image, (sw, sh))
        else:
            image = pygame.transform.smoothscale(image, scale)
    return image

def load_sprite_sheet(path, frame_count, scale=None, keep_aspect=True):
    """Split sprite sheet into frames, optionally scaled proportionally."""
    sheet = load_image(path)
    fw = sheet.get_width() // frame_count
    fh = sheet.get_height()
    frames = []
    for i in range(frame_count):
        frame = sheet.subsurface(pygame.Rect(i * fw, 0, fw, fh))
        if scale:
            if keep_aspect:
                iw, ih = frame.get_size()
                sw, sh = scale
                aspect = iw / ih
                if sw / sh > aspect:
                    sw = int(sh * aspect)
                else:
                    sh = int(sw / aspect)
                frame = pygame.transform.smoothscale(frame, (sw, sh))
            else:
                frame = pygame.transform.smoothscale(frame, scale)
        frames.append(frame)
    return frames


# JSON LOADING
def load_json(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return {}
    with open(path, 'r') as f:
        return json.load(f)
    

# ---------------------------
# QUESTION LOADING UTILITIES
# ---------------------------

def load_questions(path="assets/questions.json"):
    """Load all study questions from JSON file."""
    with open(path, "r") as f:
        return json.load(f)

def get_random_question(questions, difficulty=None):
    """Return a random question. If difficulty is given, filter by it."""
    if difficulty:
        filtered = [q for q in questions if q["difficulty"] == difficulty]
        if filtered:
            return random.choice(filtered)
    return random.choice(questions)
