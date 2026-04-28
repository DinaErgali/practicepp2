import pygame
import sys
from datetime import datetime
from tools import *

pygame.init()

WIDTH, HEIGHT = 1000, 650
TOOLBAR_W = 80
TOPBAR_H = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH-TOOLBAR_W, HEIGHT-TOPBAR_H))
canvas.fill((255,255,255))

clock = pygame.time.Clock()

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
GRAY=(240,240,240)

colors=[BLACK,RED,GREEN,BLUE]

tool="pen"
color=BLACK
brush=3

drawing=False
start=None
last=None
current=None

# TEXT
typing=False
text=""
text_pos=(0,0)
text_size=24

font = pygame.font.SysFont("Arial",16)
text_font = pygame.font.SysFont("Arial",text_size)

while True:

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        # keyboard
        if event.type==pygame.KEYDOWN:

            # brush size
            if event.key==pygame.K_1: brush=2
            if event.key==pygame.K_2: brush=5
            if event.key==pygame.K_3: brush=10

            # text size
            if event.key==pygame.K_4:
                text_size+=2
                text_font=pygame.font.SysFont("Arial",text_size)

            if event.key==pygame.K_5:
                text_size=max(10,text_size-2)
                text_font=pygame.font.SysFont("Arial",text_size)

            # save
            if event.key==pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                name=datetime.now().strftime("paint_%H%M%S.png")
                pygame.image.save(canvas,name)

            # text typing
            if typing:

                if event.key==pygame.K_RETURN:
                    img=text_font.render(text,True,color)
                    canvas.blit(img,text_pos)
                    typing=False
                    text=""

                elif event.key==pygame.K_ESCAPE:
                    typing=False
                    text=""

                elif event.key==pygame.K_BACKSPACE:
                    text=text[:-1]

                else:
                    text+=event.unicode


        # mouse down
        if event.type==pygame.MOUSEBUTTONDOWN:

            x,y=event.pos

            # tools
            if x<TOOLBAR_W:

                index=y//60

                tools=[
                    "pen","line","rect","circle",
                    "square","triangle","rhombus",
                    "fill","text","eraser"
                ]

                if index<len(tools):
                    tool=tools[index]

            # colors
            elif y<TOPBAR_H:

                i=(x-TOOLBAR_W)//50
                if i<len(colors):
                    color=colors[i]

            else:

                drawing=True
                start=(x-TOOLBAR_W,y-TOPBAR_H)
                last=start

                if tool=="fill":
                    flood_fill(canvas,start[0],start[1],color)

                if tool=="text":
                    typing=True
                    text=""
                    text_pos=start

        # mouse up
        if event.type==pygame.MOUSEBUTTONUP:

            if drawing:

                end=(event.pos[0]-TOOLBAR_W,
                     event.pos[1]-TOPBAR_H)

                draw_shape(canvas, tool, color, start, end, brush)

            drawing=False


        # mouse move
        if event.type==pygame.MOUSEMOTION:

            current=(event.pos[0]-TOOLBAR_W,
                     event.pos[1]-TOPBAR_H)

            if drawing:

                if tool=="pen":
                    draw_pen(canvas,color,last,current,brush)
                    last=current

                if tool=="eraser":
                    draw_pen(canvas,WHITE,last,current,15)
                    last=current


    # UI
    screen.fill(GRAY)

    pygame.draw.rect(screen,(230,230,230),(0,0,TOOLBAR_W,HEIGHT))

    tools_ui=[
        "Pen","Line","Rect","Circle",
        "Square","Tri","Rhomb",
        "Fill","Text","Erase"
    ]

    for i,t in enumerate(tools_ui):
        y=i*60
        pygame.draw.rect(screen,WHITE,(0,y,TOOLBAR_W,60))
        screen.blit(font.render(t,True,BLACK),(10,y+20))

    # colors
    for i,c in enumerate(colors):
        pygame.draw.rect(screen,c,(TOOLBAR_W+i*50,10,40,40))

    screen.blit(font.render(f"Brush:{brush}",True,BLACK),(820,10))
    screen.blit(font.render(f"Text:{text_size}",True,BLACK),(820,30))

    screen.blit(canvas,(TOOLBAR_W,TOPBAR_H))

    # preview
    if drawing and tool in SHAPE_TOOLS:
        preview=canvas.copy()
        draw_shape(preview, tool, color, start, current, brush)
        screen.blit(preview,(TOOLBAR_W,TOPBAR_H))

    # text preview
    if typing:
        img=text_font.render(text,True,color)
        screen.blit(img,(text_pos[0]+TOOLBAR_W,
                         text_pos[1]+TOPBAR_H))

    pygame.display.flip()
    clock.tick(60)