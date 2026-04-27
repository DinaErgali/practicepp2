import pygame
import random
import sys

pygame.init()

# -----------------------
# Window
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
GREEN = (0,200,0)

# -----------------------
# Player
# -----------------------
player = pygame.Rect(180, 500, 50, 80)
player_speed = 5

# -----------------------
# Enemy
# -----------------------
enemy = pygame.Rect(random.randint(0,350), -100, 50, 80)
enemy_speed = 5

# -----------------------
# Coin (with weights)
# -----------------------
coin = pygame.Rect(random.randint(0,380), -200, 20, 20)

coin_value = 1      # weight of coin
coin_color = YELLOW

coins = 0

# function to generate random coin
def new_coin():
    global coin_value, coin_color

    coin.x = random.randint(0,380)
    coin.y = -100

    # random weight
    coin_value = random.choice([1,2,3])

    if coin_value == 1:
        coin_color = YELLOW
    elif coin_value == 2:
        coin_color = GREEN
    else:
        coin_color = RED


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # player movement
    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # keep inside
    player.x = max(0, min(WIDTH-50, player.x))

    # move enemy
    enemy.y += enemy_speed

    if enemy.y > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(0,350)

    # move coin
    coin.y += 4

    if coin.y > HEIGHT:
        new_coin()

    # collision player enemy
    if player.colliderect(enemy):
        pygame.quit()
        sys.exit()

    # collision player coin
    if player.colliderect(coin):

        coins += coin_value
        new_coin()

        # increase speed every 5 coins
        if coins % 5 == 0:
            enemy_speed += 1

    # draw
    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, player)
    pygame.draw.rect(screen, BLACK, enemy)
    pygame.draw.circle(screen, coin_color, coin.center, 10)

    # show coins
    text = font.render(f"Coins: {coins}", True, BLACK)
    screen.blit(text, (250,10))

    pygame.display.flip()
    clock.tick(60)