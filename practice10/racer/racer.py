import pygame
import random
import sys

pygame.init()

# -----------------------
# Window settings
# -----------------------
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# -----------------------
# Colors
# -----------------------
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
YELLOW = (255,215,0)

# -----------------------
# Player settings
# -----------------------
player_w = 50
player_h = 80
player_x = WIDTH//2
player_y = HEIGHT - 100
player_speed = 5

# -----------------------
# Enemy
# -----------------------
enemy_w = 50
enemy_h = 80
enemy_x = random.randint(0, WIDTH-enemy_w)
enemy_y = -100
enemy_speed = 5

# -----------------------
# Coin
# -----------------------
coin_size = 20
coin_x = random.randint(0, WIDTH-coin_size)
coin_y = -200
coin_speed = 4

coins = 0

# -----------------------
# Game loop
# -----------------------
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move player
    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Keep inside screen
    player_x = max(0, min(WIDTH-player_w, player_x))

    # Move enemy
    enemy_y += enemy_speed

    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(0, WIDTH-enemy_w)

    # Move coin
    coin_y += coin_speed

    if coin_y > HEIGHT:
        coin_y = -100
        coin_x = random.randint(0, WIDTH-coin_size)

    # Collision player & enemy
    player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)

    if player_rect.colliderect(enemy_rect):
        pygame.quit()
        sys.exit()

    # Collision player & coin
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)

    if player_rect.colliderect(coin_rect):
        coins += 1
        coin_y = -100
        coin_x = random.randint(0, WIDTH-coin_size)

    # Draw
    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, player_rect)
    pygame.draw.rect(screen, BLACK, enemy_rect)
    pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), 10)

    # Show coins counter (top right)
    text = font.render(f"Coins: {coins}", True, BLACK)
    screen.blit(text, (WIDTH-130, 10))

    pygame.display.flip()
    clock.tick(60)

