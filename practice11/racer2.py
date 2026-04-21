import pygame
import random

pygame.init()

# --- Window settings ---
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Practice 11")
clock = pygame.time.Clock()
font  = pygame.font.SysFont("Arial", 22, bold=True)
small = pygame.font.SysFont("Arial", 16)

# --- Colors ---
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (60,  60,  60)
RED    = (220, 50,  50)
BLUE   = (50,  130, 220)
YELLOW = (255, 210, 0)
ORANGE = (255, 140, 0)
CYAN   = (0,   220, 220)

# --- Coin types with different weights (point values), colors, sizes, and spawn chances ---
# chance: out of 100, controls how often each type appears
COIN_TYPES = [
    {"weight": 1, "color": YELLOW, "radius": 10, "chance": 60},  # Common coin
    {"weight": 3, "color": ORANGE, "radius": 13, "chance": 30},  # Medium coin
    {"weight": 5, "color": CYAN,   "radius": 16, "chance": 10},  # Rare coin
]

# Enemy speed increases every time the player accumulates this many coin points
SPEED_UP_EVERY = 5

# --- Player car ---
player       = pygame.Rect(175, 500, 50, 80)
player_speed = 5

# --- Object lists ---
enemies = []
coins   = []

# --- Game state ---
score       = 0
coin_count  = 0      # Total coin points collected (used to trigger speed boosts)
enemy_speed = 5
stripe_y    = 0      # Vertical offset for road stripe animation

def spawn_enemy():
    """Spawn an enemy car in a random lane."""
    x = random.choice([80, 175, 270])
    return pygame.Rect(x, -80, 50, 80)

def spawn_coin():
    """Spawn a coin with a type chosen by weighted random chance."""
    # Roll a number 1-100 and pick the coin type whose cumulative chance covers it
    roll  = random.randint(1, 100)
    total = 0
    chosen = COIN_TYPES[0]
    for ct in COIN_TYPES:
        total += ct["chance"]
        if roll <= total:
            chosen = ct
            break
    x = random.choice([80, 175, 270]) + 15
    return {"rect": pygame.Rect(x - chosen["radius"], -20, chosen["radius"]*2, chosen["radius"]*2),
            "type": chosen}

enemy_timer = 0
coin_timer  = 0

running = True
while running:
    clock.tick(60)
    score += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Player movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]  and player.left  > 65:  player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < 340:  player.x += player_speed

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

    # --- Move all objects downward ---
    for e in enemies:
        e.y += enemy_speed
    for c in coins:
        c["rect"].y += enemy_speed

    # --- Collision with enemy → game over ---
    for e in enemies:
        if player.colliderect(e):
            running = False

    # --- Collision with coin → collect, add weight value, check for speed boost ---
    for c in list(coins):
        if player.colliderect(c["rect"]):
            w = c["type"]["weight"]
            coin_count += w   # Add the coin's weight value to the total

            # Check if coin_count crossed a SPEED_UP_EVERY threshold
            prev = (coin_count - w) // SPEED_UP_EVERY
            curr =  coin_count      // SPEED_UP_EVERY
            if curr > prev:
                enemy_speed = min(enemy_speed + 1, 15)  # Cap speed at 15

            coins.remove(c)

    # --- Remove off-screen objects ---
    enemies = [e for e in enemies if e.y < HEIGHT]
    coins   = [c for c in coins   if c["rect"].y < HEIGHT]

    # --- Animate road stripes scrolling downward ---
    stripe_y = (stripe_y + enemy_speed) % 60

    # --- Draw everything ---
    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY,  (60, 0, 280, HEIGHT))   # Road surface
    pygame.draw.rect(screen, WHITE, (55, 0, 5, HEIGHT))     # Left border
    pygame.draw.rect(screen, WHITE, (340, 0, 5, HEIGHT))    # Right border
    for y in range(-60 + stripe_y, HEIGHT, 60):
        pygame.draw.rect(screen, WHITE, (193, y, 6, 35))    # Dashed center line

    for e in enemies:
        pygame.draw.rect(screen, RED, e, border_radius=5)   # Enemy cars

    # Draw coins with their respective color and size; show point value on top
    for c in coins:
        ct = c["type"]
        cx = c["rect"].centerx
        cy = c["rect"].centery
        pygame.draw.circle(screen, ct["color"], (cx, cy), ct["radius"])
        lbl = small.render(str(ct["weight"]), True, BLACK)   # Point label
        screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    pygame.draw.rect(screen, BLUE, player, border_radius=5)  # Player car

    # HUD: score top-left, coin total top-right, speed info below
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    ct_text = font.render(f"Coins: {coin_count}", True, YELLOW)
    screen.blit(ct_text, (WIDTH - ct_text.get_width() - 10, 10))
    spd_text = small.render(
        f"Speed: {enemy_speed}  (next boost in: {SPEED_UP_EVERY - coin_count % SPEED_UP_EVERY})",
        True, ORANGE)
    screen.blit(spd_text, (10, 38))

    pygame.display.flip()

# --- Game over screen ---
screen.fill(BLACK)
screen.blit(font.render("GAME OVER", True, RED),               (125, 260))
screen.blit(font.render(f"Score: {score}", True, WHITE),       (130, 300))
screen.blit(font.render(f"Coins: {coin_count}", True, YELLOW), (130, 335))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()