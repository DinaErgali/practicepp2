import pygame
from persistence import load_scores, load_settings

def draw_text(screen, text, x, y):
    font = pygame.font.Font(None, 36)
    img = font.render(text, True, (255,255,255))
    screen.blit(img, (x,y))

def menu_screen(screen):
    screen.fill((0,0,0))
    draw_text(screen, "1 - Play", 150, 200)
    draw_text(screen, "2 - Leaderboard", 150, 250)
    draw_text(screen, "3 - Settings", 150, 300)
    draw_text(screen, "ESC - Quit", 120, 400)

def leaderboard_screen(screen):
    screen.fill((0,0,0))
    scores = load_scores()

    draw_text(screen, "Leaderboard", 120, 100)

    y = 150
    for i, s in enumerate(scores):
        text = f"{i+1}. {s['name']} - {s['score']}"
        draw_text(screen, text, 100, y)
        y += 40

    draw_text(screen, "ESC - Back", 120, 500)

def settings_screen(screen):
    screen.fill((0,0,0))
    settings = load_settings()

    draw_text(screen, "Settings", 150, 150)
    draw_text(screen, f"Sound: {settings['sound']}", 100, 250)
    draw_text(screen, f"Color: {settings['color']}", 100, 300)
    draw_text(screen, f"Difficulty: {settings['difficulty']}", 100, 350)

    draw_text(screen, "ESC - Back", 120, 500)

def game_over_screen(screen, score):
    screen.fill((0,0,0))
    draw_text(screen, "Game Over", 150, 250)
    draw_text(screen, f"Score: {score}", 150, 300)
    draw_text(screen, "ENTER - Menu", 100, 400)