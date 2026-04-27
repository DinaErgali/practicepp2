import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

snake = [(100,100)]
dx = 20
dy = 0

food = (200,200)
food_value = 1
food_timer = 0

score = 0
speed = 8

# generate random food
def random_food():
    global food_value, food_timer

    while True:
        x = random.randrange(0, WIDTH, 20)
        y = random.randrange(0, HEIGHT, 20)

        if (x,y) not in snake:

            # random weight
            food_value = random.choice([1,2,3])

            # reset timer
            food_timer = pygame.time.get_ticks()

            return (x,y)


food = random_food()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                dx = 0
                dy = -20

            if event.key == pygame.K_DOWN:
                dx = 0
                dy = 20

            if event.key == pygame.K_LEFT:
                dx = -20
                dy = 0

            if event.key == pygame.K_RIGHT:
                dx = 20
                dy = 0

    head = (snake[0][0] + dx, snake[0][1] + dy)

    # wall collision
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # self collision
    if head in snake:
        pygame.quit()
        sys.exit()

    snake.insert(0, head)

    # food collision
    if head == food:
        score += food_value
        food = random_food()
    else:
        snake.pop()

    # food disappearing after 5 sec
    if pygame.time.get_ticks() - food_timer > 5000:
        food = random_food()

    screen.fill(WHITE)

    # snake
    for s in snake:
        pygame.draw.rect(screen, GREEN, (s[0], s[1], 20, 20))

    # food color by weight
    if food_value == 1:
        color = RED
    elif food_value == 2:
        color = BLUE
    else:
        color = BLACK

    pygame.draw.rect(screen, color, (food[0], food[1], 20, 20))

    # score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10,10))

    pygame.display.flip()
    clock.tick(speed)