import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
TOOLBAR = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

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
last_pos = None

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            x,y = event.pos

            if x < TOOLBAR:

                if 10<y<40: tool="pen"
                elif 50<y<80: tool="square"
                elif 90<y<120: tool="rtri"
                elif 130<y<160: tool="etri"
                elif 170<y<200: tool="rhombus"
                elif 210<y<240: tool="eraser"

                elif 260<y<290: color=BLACK
                elif 300<y<330: color=RED
                elif 340<y<370: color=GREEN
                elif 380<y<410: color=BLUE

            else:
                drawing = True
                start_pos = (x-TOOLBAR,y)
                last_pos = start_pos

        if event.type == pygame.MOUSEBUTTONUP:

            if drawing:

                end = (event.pos[0]-TOOLBAR,event.pos[1])

                # square
                if tool=="square":
                    size = end[0]-start_pos[0]
                    pygame.draw.rect(canvas,color,
                        (start_pos[0],start_pos[1],size,size),2)

                # right triangle
                elif tool=="rtri":
                    points = [
                        start_pos,
                        (end[0],start_pos[1]),
                        (start_pos[0],end[1])
                    ]
                    pygame.draw.polygon(canvas,color,points,2)

                # equilateral triangle
                elif tool=="etri":

                    side = end[0]-start_pos[0]
                    h = side * math.sqrt(3)/2

                    p1 = start_pos
                    p2 = (start_pos[0]+side,start_pos[1])
                    p3 = (start_pos[0]+side/2,start_pos[1]-h)

                    pygame.draw.polygon(canvas,color,[p1,p2,p3],2)

                # rhombus
                elif tool=="rhombus":

                    cx = (start_pos[0]+end[0])//2
                    cy = (start_pos[1]+end[1])//2

                    points = [
                        (cx,start_pos[1]),
                        (end[0],cy),
                        (cx,end[1]),
                        (start_pos[0],cy)
                    ]

                    pygame.draw.polygon(canvas,color,points,2)

            drawing=False
            last_pos=None

    # pen
    if drawing:

        mouse = pygame.mouse.get_pos()
        pos = (mouse[0]-TOOLBAR,mouse[1])

        if tool=="pen" and last_pos:
            pygame.draw.line(canvas,color,last_pos,pos,3)
            last_pos=pos

        if tool=="eraser" and last_pos:
            pygame.draw.line(canvas,WHITE,last_pos,pos,15)
            last_pos=pos

    screen.fill(GRAY)
    pygame.draw.rect(screen,WHITE,(0,0,TOOLBAR,HEIGHT))

    font = pygame.font.SysFont("Arial",16)

    screen.blit(font.render("Pen",True,BLACK),(10,10))
    screen.blit(font.render("Square",True,BLACK),(10,50))
    screen.blit(font.render("RightTri",True,BLACK),(10,90))
    screen.blit(font.render("EquiTri",True,BLACK),(10,130))
    screen.blit(font.render("Rhombus",True,BLACK),(10,170))
    screen.blit(font.render("Eraser",True,BLACK),(10,210))

    pygame.draw.rect(screen,BLACK,(10,260,30,30))
    pygame.draw.rect(screen,RED,(10,300,30,30))
    pygame.draw.rect(screen,GREEN,(10,340,30,30))
    pygame.draw.rect(screen,BLUE,(10,380,30,30))

    screen.blit(canvas,(TOOLBAR,0))

    pygame.display.flip()
    clock.tick(60)