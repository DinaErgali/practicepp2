import pygame
import random

pygame.init()

# --- Window settings ---
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)

# --- Colors ---
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (60, 60, 60)
RED    = (220, 50, 50)
BLUE   = (50, 130, 220)
YELLOW = (255, 210, 0)

# --- Player car (x, y, width, height) ---
player = pygame.Rect(175, 500, 50, 80)
player_speed = 5

# --- Lists for enemy cars and coins ---
enemies = []
coins   = []

# --- Counters ---
score      = 0
coin_count = 0
stripe_y   = 0   # Vertical offset for road stripe animation

def spawn_enemy():
    """Spawn an enemy car in a random lane (one of three positions)."""
    x = random.choice([80, 175, 270])
    return pygame.Rect(x, -80, 50, 80)

def spawn_coin():
    """Spawn a coin in a random lane."""
    x = random.choice([80, 175, 270]) + 15
    return pygame.Rect(x, -20, 20, 20)

enemy_timer = 0
coin_timer  = 0
enemy_speed = 5

running = True
while running:
    clock.tick(60)
    score += 1
    enemy_speed = 5 + score // 500   # Gradually increase speed over time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Move player left/right with arrow keys ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]  and player.left  > 65:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < 340:
        player.x += player_speed

    # --- Spawn enemy cars on a random interval ---
    enemy_timer += 1
    if enemy_timer > random.randint(60, 90):
        enemies.append(spawn_enemy())
        enemy_timer = 0

    # --- Spawn coins on a random interval ---
    coin_timer += 1
    if coin_timer > random.randint(80, 130):
        coins.append(spawn_coin())
        coin_timer = 0

    # --- Move all enemies and coins downward ---
    for e in enemies:
        e.y += enemy_speed
    for c in coins:
        c.y += enemy_speed

    # --- Collision with enemy car → game over ---
    for e in enemies:
        if player.colliderect(e):
            running = False

    # --- Collision with coin → collect it ---
    for c in list(coins):
        if player.colliderect(c):
            coin_count += 1
            coins.remove(c)

    # --- Remove objects that have gone off screen ---
    enemies = [e for e in enemies if e.y < HEIGHT]
    coins   = [c for c in coins   if c.y < HEIGHT]

    # --- Scroll road stripes downward to create movement illusion ---
    stripe_y = (stripe_y + enemy_speed) % 60

    # --- Draw everything ---
    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY,  (60, 0, 280, HEIGHT))  # Road surface
    pygame.draw.rect(screen, WHITE, (55, 0, 5, HEIGHT))    # Left road border
    pygame.draw.rect(screen, WHITE, (340, 0, 5, HEIGHT))   # Right road border

    # Dashed center line
    for y in range(-60 + stripe_y, HEIGHT, 60):
        pygame.draw.rect(screen, WHITE, (193, y, 6, 35))

    for e in enemies:
        pygame.draw.rect(screen, RED,  e, border_radius=5)        # Enemy cars
    for c in coins:
        pygame.draw.circle(screen, YELLOW, c.center, 10)          # Coins
    pygame.draw.rect(screen, BLUE, player, border_radius=5)       # Player car

    # Score on the top-left
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    # Coin count on the top-right
    ct = font.render(f"Coins: {coin_count}", True, YELLOW)
    screen.blit(ct, (WIDTH - ct.get_width() - 10, 10))

    pygame.display.flip()

# --- Game over screen ---
screen.fill(BLACK)
screen.blit(font.render("GAME OVER", True, RED),                 (125, 260))
screen.blit(font.render(f"Score: {score}", True, WHITE),         (130, 300))
screen.blit(font.render(f"Coins: {coin_count}", True, YELLOW),   (130, 335))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()