import pygame
import random

pygame.init()

# --- Grid settings ---
CELL   = 25        # Size of each cell in pixels
COLS   = 20        # Number of columns
ROWS   = 20        # Number of rows
INFO_H = 55        # Height of the top info panel
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL + INFO_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Practice 11")
clock = pygame.time.Clock()
font  = pygame.font.SysFont("Arial", 20, bold=True)
small = pygame.font.SysFont("Arial", 15)

# --- Colors ---
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (50,  200, 80)
DARK_GREEN = (30,  140, 55)
GRAY       = (40,  40,  40)
WALL_COLOR = (90,  90,  90)
YELLOW     = (255, 220, 0)
ORANGE     = (255, 140, 0)
CYAN       = (0,   220, 220)
RED        = (220, 50,  50)

# --- Food types with different weights, colors, lifetimes, and spawn chances ---
# lifetime: how long the food stays on the grid (milliseconds)
# chance: spawn probability out of 100
FOOD_TYPES = [
    {"weight": 1, "color": RED,    "lifetime": 8000, "chance": 60},  # Common, lasts 8s
    {"weight": 3, "color": ORANGE, "lifetime": 5000, "chance": 30},  # Medium, lasts 5s
    {"weight": 5, "color": CYAN,   "lifetime": 3000, "chance": 10},  # Rare, lasts 3s
]

FOOD_PER_LEVEL = 4   # Number of foods eaten (regardless of weight) to level up

# --- Direction vectors ---
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

def make_food(snake_body, existing_foods):
    """Create a new food item at a random position not occupied by the snake, walls, or other food."""
    occupied = set(snake_body) | {f["pos"] for f in existing_foods}
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if (x, y) not in occupied:
            break

    # Pick a food type using weighted random chance
    roll  = random.randint(1, 100)
    total = 0
    chosen = FOOD_TYPES[0]
    for ft in FOOD_TYPES:
        total += ft["chance"]
        if roll <= total:
            chosen = ft
            break

    return {
        "pos":     (x, y),
        "type":    chosen,
        "born_at": pygame.time.get_ticks(),  # Timestamp when the food was created
    }

def draw_everything(snake, foods, score, level, food_count):
    """Draw the grid, walls, snake, all food items with timers, and the HUD."""
    screen.fill(GRAY)

    # Draw grid lines
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, (50, 50, 50),
                             pygame.Rect(col*CELL, row*CELL+INFO_H, CELL, CELL), 1)

    # Draw border walls (top, bottom, left, right)
    pygame.draw.rect(screen, WALL_COLOR, (0, INFO_H, WIDTH, CELL))
    pygame.draw.rect(screen, WALL_COLOR, (0, INFO_H+(ROWS-1)*CELL, WIDTH, CELL))
    pygame.draw.rect(screen, WALL_COLOR, (0, INFO_H, CELL, HEIGHT-INFO_H))
    pygame.draw.rect(screen, WALL_COLOR, ((COLS-1)*CELL, INFO_H, CELL, HEIGHT-INFO_H))

    # Draw snake; head segment is brighter green
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color,
                         pygame.Rect(x*CELL+2, y*CELL+INFO_H+2, CELL-4, CELL-4),
                         border_radius=5)

    # Draw each food item with a countdown timer bar
    now = pygame.time.get_ticks()
    for food in foods:
        fx, fy = food["pos"]
        ft     = food["type"]
        cx     = fx * CELL + CELL // 2
        cy     = fy * CELL + INFO_H + CELL // 2

        # Calculate remaining lifetime as a ratio (1.0 = just spawned, 0.0 = about to vanish)
        elapsed = now - food["born_at"]
        ratio   = max(0.0, 1.0 - elapsed / ft["lifetime"])

        # Fade the food color toward gray as it gets closer to disappearing
        r, g, b = ft["color"]
        faded   = (int(r * ratio + 80*(1-ratio)),
                   int(g * ratio + 80*(1-ratio)),
                   int(b * ratio + 80*(1-ratio)))
        pygame.draw.circle(screen, faded, (cx, cy), CELL // 2 - 3)

        # Show the point value of the food
        lbl = small.render(str(ft["weight"]), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

        # Draw a small timer bar below the food that shrinks over time
        bar_w = CELL - 6
        pygame.draw.rect(screen, BLACK, (fx*CELL+3, fy*CELL+INFO_H+CELL-5, bar_w, 4))
        pygame.draw.rect(screen, GREEN, (fx*CELL+3, fy*CELL+INFO_H+CELL-5, int(bar_w*ratio), 4))

    # Draw HUD panel: score, level, and foods until next level
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, INFO_H))
    screen.blit(font.render(f"Score: {score}", True, WHITE),  (10, 14))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (WIDTH//2 - 38, 14))
    nxt = small.render(f"Next lv: {FOOD_PER_LEVEL - food_count % FOOD_PER_LEVEL}", True, GREEN)
    screen.blit(nxt, (WIDTH - nxt.get_width() - 10, 18))

    pygame.display.flip()

# --- Initial game state ---
snake      = [(COLS//2, ROWS//2)]   # Snake starts at the center
direction  = RIGHT
next_dir   = RIGHT
foods      = [make_food(snake, [])] # Start with one food on the grid

score      = 0
level      = 1
food_count = 0    # Counts how many foods have been eaten (used for leveling up)
speed      = 180  # Milliseconds between each snake move
move_timer = 0

running = True
while running:
    dt = clock.tick(60)
    move_timer += dt
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP    and direction != DOWN:  next_dir = UP
            if event.key == pygame.K_DOWN  and direction != UP:    next_dir = DOWN
            if event.key == pygame.K_LEFT  and direction != RIGHT: next_dir = LEFT
            if event.key == pygame.K_RIGHT and direction != LEFT:  next_dir = RIGHT

    # --- Remove expired food items; always keep at least one food on the grid ---
    foods = [f for f in foods if now - f["born_at"] < f["type"]["lifetime"]]
    if len(foods) == 0:
        foods.append(make_food(snake, foods))

    # --- Move the snake once per interval ---
    if move_timer >= speed:
        move_timer = 0
        direction  = next_dir
        new_head   = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check wall collision
        if new_head[0] <= 0 or new_head[0] >= COLS-1 or new_head[1] <= 0 or new_head[1] >= ROWS-1:
            running = False
            break

        # Check self collision
        if new_head in snake:
            running = False
            break

        snake.insert(0, new_head)

        # Check if the snake's head landed on any food
        eaten = None
        for food in foods:
            if new_head == food["pos"]:
                eaten = food
                break

        if eaten:
            w = eaten["type"]["weight"]
            score      += 10 * w * level   # Higher weight and level = more points
            food_count += 1
            foods.remove(eaten)
            foods.append(make_food(snake, foods))   # Spawn a replacement food

            # Level up every FOOD_PER_LEVEL foods eaten
            if food_count % FOOD_PER_LEVEL == 0:
                level += 1
                speed  = max(80, speed - 20)   # Speed up, minimum 80ms
        else:
            snake.pop()   # No food eaten, remove the tail (snake stays same length)

    draw_everything(snake, foods, score, level, food_count)

# --- Game over screen ---
screen.fill(BLACK)
screen.blit(font.render("GAME OVER", True, RED),          (WIDTH//2-72, HEIGHT//2-40))
screen.blit(font.render(f"Score: {score}", True, WHITE),  (WIDTH//2-52, HEIGHT//2))
screen.blit(font.render(f"Level: {level}", True, YELLOW), (WIDTH//2-48, HEIGHT//2+35))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()