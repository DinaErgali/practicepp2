"""
Music Player with Keyboard Controls

Controls:
  P = Play
  S = Stop
  N = Next track
  B = Previous (Back)
  Q = Quit
"""

import pygame
import sys
import os
from player import MusicPlayer

# Initialize pygame
pygame.init()

# Window
WIDTH  = 500
HEIGHT = 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")
clock  = pygame.time.Clock()

# Colors
BG     = (30,  30,  50)
WHITE  = (255, 255, 255)
GRAY   = (150, 150, 170)
GREEN  = (80,  200, 100)
RED    = (200, 80,  80)

# Fonts
font_big   = pygame.font.SysFont("Arial", 22, bold=True)
font_small = pygame.font.SysFont("Arial", 16)

# Load music player
music_folder = os.path.join(os.path.dirname(__file__), "music")
os.makedirs(music_folder, exist_ok=True)
player = MusicPlayer(music_folder)

# Main loop
while True:

    # Handle keyboard input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:   # P = Play
                player.play()
            elif event.key == pygame.K_s: # S = Stop
                player.stop()
            elif event.key == pygame.K_n: # N = Next
                player.next_song()
            elif event.key == pygame.K_b: # B = Back (Previous)
                player.prev_song()
            elif event.key == pygame.K_q: # Q = Quit
                pygame.quit()
                sys.exit()

    # Draw background
    screen.fill(BG)

    # Title
    title = font_big.render("Music Player", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # Song info
    song_name = player.get_song_name()
    if len(song_name) > 40:
        song_name = song_name[:37] + "..."

    track_num = f"Track {player.current + 1} / {len(player.playlist)}" if player.playlist else "No tracks"
    name_surf = font_big.render(song_name, True, WHITE)
    num_surf  = font_small.render(track_num, True, GRAY)

    screen.blit(num_surf,  (WIDTH // 2 - num_surf.get_width()  // 2, 80))
    screen.blit(name_surf, (WIDTH // 2 - name_surf.get_width() // 2, 108))

    # Playback status
    status = player.get_status()
    color  = GREEN if status == "Playing" else RED
    status_surf = font_big.render(status, True, color)
    screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, 155))

    # Playback position
    pos_ms  = pygame.mixer.music.get_pos()
    pos_sec = max(pos_ms // 1000, 0)
    pos_str = f"{pos_sec // 60:02d}:{pos_sec % 60:02d}"
    pos_surf = font_small.render(pos_str, True, GRAY)
    screen.blit(pos_surf, (WIDTH // 2 - pos_surf.get_width() // 2, 185))

    # Controls legend
    controls = font_small.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True, GRAY)
    screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, 240))

    # Update display
    pygame.display.flip()
    clock.tick(30)
