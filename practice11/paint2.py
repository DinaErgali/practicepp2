import pygame
import math
import sys

pygame.init()

# --- Window settings ---
WIDTH, HEIGHT = 950, 630
TOOLBAR_W = 180   # Width of the left toolbar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Practice 11")
clock = pygame.time.Clock()
font  = pygame.font.SysFont("Arial", 15, bold=True)
small = pygame.font.SysFont("Arial", 13)

# --- Canvas: a white surface that occupies the right side of the window ---
canvas = pygame.Surface((WIDTH - TOOLBAR_W, HEIGHT))
canvas.fill((255, 255, 255))

# --- Colors ---
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
LGRAY = (215, 215, 220)
DGRAY = (100, 100, 110)
BLUE  = (80,  120, 200)

# --- Color palette ---
palette = [
    (0,   0,   0),    # Black
    (220, 50,  50),   # Red
    (50,  130, 220),  # Blue
    (50,  200, 80),   # Green
    (255, 210, 0),    # Yellow
    (220, 100, 220),  # Purple
    (255, 140, 0),    # Orange
    (255, 255, 255),  # White
    (150, 150, 150),  # Gray
    (0,   200, 200),  # Cyan
]

# --- Tool list: original tools from Practice 10 + 4 new shapes ---
tools = [
    "Pencil",
    "Rectangle",
    "Circle",
    "Eraser",
    "── New ──",        # Separator label (not selectable)
    "Square",           # New: square (equal sides)
    "Right Triangle",   # New: right-angle triangle
    "Equil. Triangle",  # New: equilateral triangle
    "Rhombus",          # New: rhombus (diamond shape)
]
NON_TOOLS = {"── New ──"}   # Labels that cannot be selected as tools

brush_sizes = [3, 7, 14]

# --- Current drawing state ---
current_tool  = "Pencil"
current_color = BLACK
brush_size    = 7
drawing       = False
start_pos     = None
snapshot      = None   # Canvas snapshot saved before drawing a shape (used for live preview)


# --- Helper functions: calculate polygon vertices from drag start/end points ---

def rect_points(x1, y1, x2, y2):
    """Return the four corners of a rectangle."""
    return [(x1,y1), (x2,y1), (x2,y2), (x1,y2)]

def square_points(x1, y1, x2, y2):
    """Return corners of a square using the shorter side of the drag area."""
    side = min(abs(x2-x1), abs(y2-y1))
    sx   = x1 + (side if x2 > x1 else -side)
    sy   = y1 + (side if y2 > y1 else -side)
    return [(x1,y1), (sx,y1), (sx,sy), (x1,sy)]

def right_triangle_points(x1, y1, x2, y2):
    """Return vertices of a right triangle with the right angle at the bottom-left."""
    return [(x1, y1), (x1, y2), (x2, y2)]

def equilateral_triangle_points(x1, y1, x2, y2):
    """Return vertices of an equilateral triangle. Base = drag width; height = base * sqrt(3)/2."""
    bx    = (x1 + x2) / 2                        # x of the base midpoint
    h     = abs(x2 - x1) * math.sqrt(3) / 2      # equilateral triangle height formula
    top_y = y2 - (h if y2 > y1 else -h)
    return [(x1, y2), (x2, y2), (int(bx), int(top_y))]

def rhombus_points(x1, y1, x2, y2):
    """Return the four vertices of a rhombus (top, right, bottom, left midpoints)."""
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]

# Map each shape tool name to its vertex function
SHAPE_FUNCS = {
    "Rectangle":       rect_points,
    "Square":          square_points,
    "Right Triangle":  right_triangle_points,
    "Equil. Triangle": equilateral_triangle_points,
    "Rhombus":         rhombus_points,
}

def draw_shape_on(surface, tool, x1, y1, x2, y2, color, size):
    """Draw the given shape onto a surface using the drag start and end coordinates."""
    if tool == "Circle":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r  = int(math.hypot(x2-x1, y2-y1) / 2)
        if r > 0:
            pygame.draw.circle(surface, color, (cx, cy), r, size)
    elif tool in SHAPE_FUNCS:
        pts = SHAPE_FUNCS[tool](x1, y1, x2, y2)
        if len(pts) >= 2:
            pygame.draw.polygon(surface, color, pts, size)


def draw_toolbar():
    """Draw the left toolbar: tool buttons, color palette, brush sizes, and clear button."""
    pygame.draw.rect(screen, LGRAY, (0, 0, TOOLBAR_W, HEIGHT))
    pygame.draw.line(screen, DGRAY, (TOOLBAR_W, 0), (TOOLBAR_W, HEIGHT), 2)

    y = 10

    # Tool buttons
    screen.blit(font.render("TOOLS", True, DGRAY), (10, y)); y += 20
    for tool in tools:
        if tool in NON_TOOLS:
            screen.blit(small.render(tool, True, DGRAY), (10, y))   # Separator label
            y += 20
            continue
        active = (tool == current_tool)
        pygame.draw.rect(screen, BLUE if active else (190,190,195),
                         (8, y, TOOLBAR_W-16, 26), border_radius=5)
        screen.blit(font.render(tool, True, WHITE if active else BLACK), (14, y+5))
        y += 30
    y += 6

    # Color palette grid
    screen.blit(font.render("COLORS", True, DGRAY), (10, y)); y += 20
    for i, col in enumerate(palette):
        px = 12 + (i % 2) * 34
        py = y + (i // 2) * 34
        if col == current_color:
            pygame.draw.rect(screen, (60,60,200), pygame.Rect(px,py,28,28).inflate(6,6), border_radius=5)
        pygame.draw.rect(screen, col,  (px, py, 28, 28), border_radius=4)
        pygame.draw.rect(screen, DGRAY,(px, py, 28, 28), 1, border_radius=4)
    y += (len(palette)//2) * 34 + 10

    # Currently selected color preview
    screen.blit(font.render("SELECTED", True, DGRAY), (10, y)); y += 20
    pygame.draw.rect(screen, current_color, (10, y, TOOLBAR_W-20, 24), border_radius=5)
    pygame.draw.rect(screen, DGRAY,         (10, y, TOOLBAR_W-20, 24), 1, border_radius=5)
    y += 34

    # Brush size buttons (displayed as circles of increasing size)
    screen.blit(font.render("SIZE", True, DGRAY), (10, y)); y += 20
    for i, sz in enumerate(brush_sizes):
        bx = 14 + i * 52
        bc = BLUE if sz == brush_size else (190,190,195)
        pygame.draw.rect(screen, bc, (bx, y, 44, 28), border_radius=5)
        pygame.draw.circle(screen, WHITE if sz == brush_size else BLACK, (bx+22, y+14), sz//2+2)

    # Clear canvas button at the bottom
    pygame.draw.rect(screen, (210,70,70), (10, HEIGHT-44, TOOLBAR_W-20, 34), border_radius=6)
    screen.blit(font.render("Clear", True, WHITE), (TOOLBAR_W//2-18, HEIGHT-36))


def handle_toolbar_click(mx, my):
    """Detect which toolbar element was clicked and update the drawing state."""
    global current_tool, current_color, brush_size

    # Tool buttons
    y = 30
    for tool in tools:
        if tool in NON_TOOLS:
            y += 20; continue
        if pygame.Rect(8, y, TOOLBAR_W-16, 26).collidepoint(mx, my):
            current_tool = tool; return
        y += 30
    y += 6

    # Color palette
    py_base = y + 20
    for i, col in enumerate(palette):
        px = 12 + (i % 2) * 34
        py = py_base + (i // 2) * 34
        if pygame.Rect(px, py, 28, 28).collidepoint(mx, my):
            current_color = col; return
    py_base += (len(palette)//2)*34 + 10

    # Brush size buttons
    size_y = py_base + 20 + 24 + 34 + 20
    for i, sz in enumerate(brush_sizes):
        if pygame.Rect(14+i*52, size_y, 44, 28).collidepoint(mx, my):
            brush_size = sz; return

    # Clear button
    if pygame.Rect(10, HEIGHT-44, TOOLBAR_W-20, 34).collidepoint(mx, my):
        canvas.fill(WHITE)


running = True
while running:
    clock.tick(60)
    mx, my    = pygame.mouse.get_pos()
    on_canvas = mx > TOOLBAR_W        # True when the mouse is over the drawing canvas
    cx, cy    = mx - TOOLBAR_W, my   # Convert to canvas-local coordinates

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if on_canvas:
                drawing   = True
                start_pos = (cx, cy)
                # Save a canvas snapshot before drawing any shape tool (for live preview)
                if current_tool not in ("Pencil", "Eraser"):
                    snapshot = canvas.copy()
            else:
                handle_toolbar_click(mx, my)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and on_canvas and current_tool not in ("Pencil", "Eraser"):
                # On release, restore the snapshot then draw the final shape permanently
                canvas.blit(snapshot, (0, 0))
                draw_shape_on(canvas, current_tool,
                              start_pos[0], start_pos[1], cx, cy,
                              current_color, brush_size)
            drawing   = False
            start_pos = None
            snapshot  = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing and on_canvas:
                if current_tool == "Pencil":
                    # Connect the previous and current mouse positions with a line
                    prev_cx = cx - event.rel[0]
                    prev_cy = cy - event.rel[1]
                    pygame.draw.line(canvas, current_color, (prev_cx,prev_cy), (cx,cy), brush_size)
                elif current_tool == "Eraser":
                    pygame.draw.circle(canvas, WHITE, (cx, cy), brush_size*2)

    # --- Render frame ---
    screen.fill(LGRAY)

    # Show live shape preview while dragging; otherwise display the canvas normally
    if drawing and current_tool not in ("Pencil","Eraser") and snapshot:
        temp = snapshot.copy()
        draw_shape_on(temp, current_tool,
                      start_pos[0], start_pos[1], cx, cy,
                      current_color, brush_size)
        screen.blit(temp, (TOOLBAR_W, 0))
    else:
        screen.blit(canvas, (TOOLBAR_W, 0))

    # Show eraser cursor outline so the user can see its area
    if current_tool == "Eraser" and on_canvas:
        pygame.draw.circle(screen, DGRAY, (mx, my), brush_size*2, 2)

    draw_toolbar()
    pygame.display.flip()

pygame.quit()
sys.exit()