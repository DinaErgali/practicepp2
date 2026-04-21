import pygame
import sys

pygame.init()

# --- Window settings ---
WIDTH, HEIGHT = 900, 620
TOOLBAR_W = 150    # Width of the left toolbar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 17, bold=True)

# --- Canvas: a separate Surface so drawing never touches the toolbar ---
canvas = pygame.Surface((WIDTH - TOOLBAR_W, HEIGHT))
canvas.fill((255, 255, 255))

# --- Colors ---
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
LGRAY  = (220, 220, 225)
DGRAY  = (100, 100, 110)

# --- Color palette available to the user ---
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

# --- Available drawing tools ---
tools       = ["Pencil", "Rectangle", "Circle", "Eraser"]
brush_sizes = [3, 7, 14]

# --- Current state ---
current_tool  = "Pencil"
current_color = BLACK
brush_size    = 7
drawing       = False
start_pos     = None
snapshot      = None    # Canvas snapshot saved before drawing a shape (for live preview)


def draw_toolbar():
    """Draw the left toolbar: tool buttons, color palette, brush sizes, and clear button."""
    pygame.draw.rect(screen, LGRAY, (0, 0, TOOLBAR_W, HEIGHT))
    pygame.draw.line(screen, DGRAY, (TOOLBAR_W, 0), (TOOLBAR_W, HEIGHT), 2)

    y = 12

    # Tool buttons
    screen.blit(font.render("TOOLS", True, DGRAY), (10, y)); y += 22
    for tool in tools:
        color = (80, 120, 200) if tool == current_tool else (190, 190, 195)
        tc    = WHITE if tool == current_tool else BLACK
        pygame.draw.rect(screen, color, (8, y, TOOLBAR_W - 16, 28), border_radius=5)
        screen.blit(font.render(tool, True, tc), (14, y + 6))
        y += 34
    y += 8

    # Color palette grid
    screen.blit(font.render("COLORS", True, DGRAY), (10, y)); y += 22
    for i, col in enumerate(palette):
        cx = 12 + (i % 2) * 34
        cy = y + (i // 2) * 34
        rect = pygame.Rect(cx, cy, 28, 28)
        if col == current_color:
            pygame.draw.rect(screen, (60, 60, 200), rect.inflate(6, 6), border_radius=5)
        pygame.draw.rect(screen, col, rect, border_radius=4)
        pygame.draw.rect(screen, DGRAY, rect, 1, border_radius=4)
    y += (len(palette) // 2) * 34 + 10

    # Preview of the currently selected color
    screen.blit(font.render("SELECTED", True, DGRAY), (10, y)); y += 22
    pygame.draw.rect(screen, current_color, (10, y, TOOLBAR_W - 20, 26), border_radius=5)
    pygame.draw.rect(screen, DGRAY, (10, y, TOOLBAR_W - 20, 26), 1, border_radius=5)
    y += 36

    # Brush size buttons (shown as circles of different sizes)
    screen.blit(font.render("SIZE", True, DGRAY), (10, y)); y += 22
    for i, sz in enumerate(brush_sizes):
        bx = 14 + i * 42
        bc = (80, 120, 200) if sz == brush_size else (190, 190, 195)
        pygame.draw.rect(screen, bc, (bx, y, 36, 30), border_radius=5)
        pygame.draw.circle(screen, WHITE if sz == brush_size else BLACK, (bx + 18, y + 15), sz // 2 + 2)

    # Clear canvas button at the bottom
    pygame.draw.rect(screen, (210, 70, 70), (10, HEIGHT - 44, TOOLBAR_W - 20, 34), border_radius=6)
    screen.blit(font.render("Clear", True, WHITE), (TOOLBAR_W // 2 - 20, HEIGHT - 36))


def handle_toolbar_click(mx, my):
    """Check which toolbar element was clicked and update state accordingly."""
    global current_tool, current_color, brush_size

    # Tool buttons start at y=34, spaced 34px apart
    y = 34
    for tool in tools:
        if pygame.Rect(8, y, TOOLBAR_W - 16, 28).collidepoint(mx, my):
            current_tool = tool
            return
        y += 34
    y += 8

    # Color palette
    palette_y = y + 22
    for i, col in enumerate(palette):
        cx = 12 + (i % 2) * 34
        cy = palette_y + (i // 2) * 34
        if pygame.Rect(cx, cy, 28, 28).collidepoint(mx, my):
            current_color = col
            return

    palette_y += (len(palette) // 2) * 34 + 10

    # Brush size buttons
    size_y = palette_y + 22 + 26 + 36 + 22
    for i, sz in enumerate(brush_sizes):
        bx = 14 + i * 42
        if pygame.Rect(bx, size_y, 36, 30).collidepoint(mx, my):
            brush_size = sz
            return

    # Clear button
    if pygame.Rect(10, HEIGHT - 44, TOOLBAR_W - 20, 34).collidepoint(mx, my):
        canvas.fill(WHITE)


running = True
while running:
    clock.tick(60)
    mx, my    = pygame.mouse.get_pos()
    on_canvas = mx > TOOLBAR_W   # True when the mouse is over the drawing area
    cx, cy    = mx - TOOLBAR_W, my  # Convert screen coords to canvas coords

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if on_canvas:
                drawing   = True
                start_pos = (cx, cy)
                if current_tool in ("Rectangle", "Circle"):
                    snapshot = canvas.copy()   # Save canvas before drawing shape (for preview)
            else:
                handle_toolbar_click(mx, my)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and on_canvas and current_tool in ("Rectangle", "Circle"):
                # On mouse release, commit the final shape to the canvas
                canvas.blit(snapshot, (0, 0))   # Restore snapshot first to remove preview
                if current_tool == "Rectangle":
                    x1, y1 = start_pos
                    rect = pygame.Rect(min(x1, cx), min(y1, cy), abs(cx - x1), abs(cy - y1))
                    pygame.draw.rect(canvas, current_color, rect, brush_size)
                elif current_tool == "Circle":
                    x1, y1 = start_pos
                    cx2 = (x1 + cx) // 2
                    cy2 = (y1 + cy) // 2
                    r   = int(((cx - x1)**2 + (cy - y1)**2)**0.5 / 2)
                    if r > 0:
                        pygame.draw.circle(canvas, current_color, (cx2, cy2), r, brush_size)
            drawing   = False
            start_pos = None
            snapshot  = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing and on_canvas:
                if current_tool == "Pencil":
                    # Connect previous and current mouse positions with a line for smooth drawing
                    prev_cx = cx - event.rel[0]
                    prev_cy = cy - event.rel[1]
                    pygame.draw.line(canvas, current_color, (prev_cx, prev_cy), (cx, cy), brush_size)
                elif current_tool == "Eraser":
                    pygame.draw.circle(canvas, WHITE, (cx, cy), brush_size * 2)

    # --- Render frame ---
    screen.fill(LGRAY)

    # Show live shape preview while dragging, otherwise show the canvas as-is
    if drawing and current_tool in ("Rectangle", "Circle") and snapshot:
        temp = snapshot.copy()
        if current_tool == "Rectangle":
            x1, y1 = start_pos
            rect = pygame.Rect(min(x1, cx), min(y1, cy), abs(cx - x1), abs(cy - y1))
            pygame.draw.rect(temp, current_color, rect, brush_size)
        elif current_tool == "Circle":
            x1, y1 = start_pos
            cx2 = (x1 + cx) // 2
            cy2 = (y1 + cy) // 2
            r   = int(((cx - x1)**2 + (cy - y1)**2)**0.5 / 2)
            if r > 0:
                pygame.draw.circle(temp, current_color, (cx2, cy2), r, brush_size)
        screen.blit(temp, (TOOLBAR_W, 0))
    else:
        screen.blit(canvas, (TOOLBAR_W, 0))

    # Draw eraser cursor outline so the user can see its size
    if current_tool == "Eraser" and on_canvas:
        pygame.draw.circle(screen, DGRAY, (mx, my), brush_size * 2, 2)

    draw_toolbar()
    pygame.display.flip()

pygame.quit()
sys.exit()