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

# colors
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)

# snake
snake = [(100,100)]
dx = 20
dy = 0

# food
food = (200,200)

score = 0
level = 1
speed = 8

def random_food():
    while True:
        x = random.randrange(0, WIDTH, 20)
        y = random.randrange(0, HEIGHT, 20)
        if (x,y) not in snake:
            return (x,y)

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
        score += 1
        food = random_food()

        # level system
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    screen.fill(WHITE)

    # draw snake
    for s in snake:
        pygame.draw.rect(screen, GREEN, (s[0], s[1], 20, 20))

    # draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], 20, 20))

    # score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10,10))

    # level
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(level_text, (10,40))

    pygame.display.flip()
    clock.tick(speed)
