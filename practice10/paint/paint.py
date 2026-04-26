import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
TOOLBAR = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (200,200,200)

canvas = pygame.Surface((WIDTH-TOOLBAR, HEIGHT))
canvas.fill(WHITE)

tool = "pen"
color = BLACK

drawing = False
start_pos = None
last_pos = None   # NEW — previous mouse position


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            x,y = event.pos

            if x < TOOLBAR:

                if 10 < y < 40:
                    tool = "pen"

                elif 50 < y < 80:
                    tool = "rect"

                elif 90 < y < 120:
                    tool = "circle"

                elif 130 < y < 160:
                    tool = "eraser"

                elif 200 < y < 230:
                    color = BLACK

                elif 240 < y < 270:
                    color = RED

                elif 280 < y < 310:
                    color = GREEN

                elif 320 < y < 350:
                    color = BLUE

            else:
                drawing = True
                start_pos = (x-TOOLBAR, y)
                last_pos = start_pos

        if event.type == pygame.MOUSEBUTTONUP:

            if drawing:

                end_pos = (event.pos[0]-TOOLBAR, event.pos[1])

                if tool == "rect":
                    pygame.draw.rect(
                        canvas,
                        color,
                        (*start_pos,
                         end_pos[0]-start_pos[0],
                         end_pos[1]-start_pos[1]),
                        2
                    )

                elif tool == "circle":

                    radius = int(((end_pos[0]-start_pos[0])**2 +
                                  (end_pos[1]-start_pos[1])**2)**0.5)

                    pygame.draw.circle(canvas, color, start_pos, radius, 2)

            drawing = False
            last_pos = None

    # smooth drawing
    if drawing:

        mouse = pygame.mouse.get_pos()
        pos = (mouse[0]-TOOLBAR, mouse[1])

        if tool == "pen" and last_pos:
            pygame.draw.line(canvas, color, last_pos, pos, 3)
            last_pos = pos

        if tool == "eraser" and last_pos:
            pygame.draw.line(canvas, WHITE, last_pos, pos, 15)
            last_pos = pos

    # UI
    screen.fill(GRAY)
    pygame.draw.rect(screen, WHITE, (0,0,TOOLBAR,HEIGHT))

    font = pygame.font.SysFont("Arial", 16)

    screen.blit(font.render("Pen",True,BLACK),(10,10))
    screen.blit(font.render("Rect",True,BLACK),(10,50))
    screen.blit(font.render("Circle",True,BLACK),(10,90))
    screen.blit(font.render("Eraser",True,BLACK),(10,130))

    pygame.draw.rect(screen, BLACK, (10,200,30,30))
    pygame.draw.rect(screen, RED, (10,240,30,30))
    pygame.draw.rect(screen, GREEN, (10,280,30,30))
    pygame.draw.rect(screen, BLUE, (10,320,30,30))

    screen.blit(canvas, (TOOLBAR,0))

    pygame.display.flip()
    clock.tick(60)