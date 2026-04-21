import pygame
import random

pygame.init()

# --- Grid settings ---
CELL   = 25        # Size of each cell in pixels
COLS   = 20        # Number of columns
ROWS   = 20        # Number of rows
INFO_H = 50        # Height of the top info panel
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL + INFO_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font  = pygame.font.SysFont("Arial", 22, bold=True)

# --- Colors ---
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (50,  200, 80)
DARK_GREEN = (30,  140, 55)
RED        = (220, 50,  50)
YELLOW     = (255, 220, 0)
GRAY       = (40,  40,  40)
WALL_COLOR = (90,  90,  90)

# --- Direction vectors ---
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

FOOD_PER_LEVEL = 4   # Number of foods eaten to advance one level

def random_food(snake):
    """Return a random grid position that is not on the snake or the border walls."""
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if (x, y) not in snake:
            return (x, y)

def draw_everything(snake, food, score, level, food_count):
    """Draw all game elements: grid, walls, snake, food, and HUD."""
    screen.fill(GRAY)

    # Draw grid lines
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL, row * CELL + INFO_H, CELL, CELL)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    # Draw border walls (top, bottom, left, right)
    pygame.draw.rect(screen, WALL_COLOR, (0, INFO_H, WIDTH, CELL))
    pygame.draw.rect(screen, WALL_COLOR, (0, INFO_H + (ROWS-1)*CELL, WIDTH, CELL))
    pygame.draw.rect(screen, WALL_COLOR, (0, INFO_H, CELL, HEIGHT - INFO_H))
    pygame.draw.rect(screen, WALL_COLOR, ((COLS-1)*CELL, INFO_H, CELL, HEIGHT - INFO_H))

    # Draw snake segments; head is brighter than the body
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        rect  = pygame.Rect(x * CELL + 2, y * CELL + INFO_H + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(screen, color, rect, border_radius=5)

    # Draw food as a red circle
    fx, fy = food
    cx = fx * CELL + CELL // 2
    cy = fy * CELL + INFO_H + CELL // 2
    pygame.draw.circle(screen, RED, (cx, cy), CELL // 2 - 3)

    # Draw HUD panel: score, level, and foods until next level
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, INFO_H))
    screen.blit(font.render(f"Score: {score}", True, WHITE),  (10, 12))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (WIDTH // 2 - 40, 12))
    next_lv = font.render(f"Next: {FOOD_PER_LEVEL - food_count % FOOD_PER_LEVEL}", True, GREEN)
    screen.blit(next_lv, (WIDTH - next_lv.get_width() - 10, 12))

    pygame.display.flip()

# --- Initial game state ---
snake     = [(COLS // 2, ROWS // 2)]   # Snake starts at the center
direction = RIGHT
next_dir  = RIGHT
food      = random_food(snake)

score      = 0
level      = 1
food_count = 0
speed      = 180   # Milliseconds between each move; lower = faster
move_timer = 0

running = True
while running:
    dt = clock.tick(60)
    move_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Update direction but do not allow reversing into itself
            if event.key == pygame.K_UP    and direction != DOWN:  next_dir = UP
            if event.key == pygame.K_DOWN  and direction != UP:    next_dir = DOWN
            if event.key == pygame.K_LEFT  and direction != RIGHT: next_dir = LEFT
            if event.key == pygame.K_RIGHT and direction != LEFT:  next_dir = RIGHT

    # --- Move the snake once per interval ---
    if move_timer >= speed:
        move_timer = 0
        direction  = next_dir

        # Calculate the new head position
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check wall collision
        if new_head[0] <= 0 or new_head[0] >= COLS - 1 or new_head[1] <= 0 or new_head[1] >= ROWS - 1:
            running = False
            break

        # Check self collision
        if new_head in snake:
            running = False
            break

        snake.insert(0, new_head)

        # Check if the snake ate the food
        if new_head == food:
            score      += 10 * level       # More points at higher levels
            food_count += 1
            food        = random_food(snake)

            # Level up every FOOD_PER_LEVEL foods eaten
            if food_count % FOOD_PER_LEVEL == 0:
                level += 1
                speed  = max(80, speed - 20)   # Speed up, minimum 80ms
        else:
            snake.pop()   # Remove the tail if no food was eaten (snake stays same length)

    draw_everything(snake, food, score, level, food_count)

# --- Game over screen ---
screen.fill(BLACK)
screen.blit(font.render("GAME OVER", True, RED),          (WIDTH//2 - 75, HEIGHT//2 - 40))
screen.blit(font.render(f"Score: {score}", True, WHITE),  (WIDTH//2 - 55, HEIGHT//2))
screen.blit(font.render(f"Level: {level}", True, YELLOW), (WIDTH//2 - 50, HEIGHT//2 + 35))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()