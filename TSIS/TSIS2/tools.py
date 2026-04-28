import pygame
import math
from collections import deque

SHAPE_TOOLS = [
    "line","rect","circle",
    "square","triangle","rhombus"
]

def draw_pen(surface,color,start,end,size):
    pygame.draw.line(surface,color,start,end,size)


def draw_shape(surface, tool, color, start, end, size):

    if tool=="line":
        pygame.draw.line(surface,color,start,end,size)

    elif tool=="rect":
        pygame.draw.rect(surface,color,
            (*start,end[0]-start[0],end[1]-start[1]),size)

    elif tool=="circle":
        r=int(math.hypot(end[0]-start[0],end[1]-start[1]))
        pygame.draw.circle(surface,color,start,r,size)

    elif tool=="square":
        s=end[0]-start[0]
        pygame.draw.rect(surface,color,
            (start[0],start[1],s,s),size)

    elif tool=="triangle":
        pts=[start,(end[0],start[1]),(start[0],end[1])]
        pygame.draw.polygon(surface,color,pts,size)

    elif tool=="rhombus":

        cx=(start[0]+end[0])//2
        cy=(start[1]+end[1])//2

        pts=[
            (cx,start[1]),
            (end[0],cy),
            (cx,end[1]),
            (start[0],cy)
        ]

        pygame.draw.polygon(surface,color,pts,size)


def flood_fill(surface,x,y,new):

    w,h=surface.get_size()
    target=surface.get_at((x,y))

    if target==new:
        return

    q=deque()
    q.append((x,y))

    while q:
        px,py=q.popleft()

        if px<0 or px>=w or py<0 or py>=h:
            continue

        if surface.get_at((px,py))!=target:
            continue

        surface.set_at((px,py),new)

        q.append((px+1,py))
        q.append((px-1,py))
        q.append((px,py+1))
        q.append((px,py-1))