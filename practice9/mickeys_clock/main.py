import pygame
import sys
import math
import datetime
import os

# Initialize pygame
pygame.init()

# Window
WIDTH  = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (180, 180, 180)
RED   = (200, 0, 0)

# Clock settings
clock  = pygame.time.Clock()
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 180

# Load Mickey hand image
image_path = os.path.join(os.path.dirname(__file__), "images", "mickey_hand.png")
try:
    hand_image = pygame.image.load(image_path).convert_alpha()
    hand_image = pygame.transform.scale(hand_image, (40, 120))
    HAS_IMAGE  = True
except:
    HAS_IMAGE  = False

# Font
font = pygame.font.SysFont("Arial", 36, bold=True)


def draw_hand(surface, angle_deg, length, color, width):
    """Draw a simple line hand (used when no image available)."""
    angle = math.radians(angle_deg)
    end_x = CENTER[0] + length * math.sin(angle)
    end_y = CENTER[1] - length * math.cos(angle)
    pygame.draw.line(surface, color, CENTER, (int(end_x), int(end_y)), width)


def draw_image_hand(surface, angle_deg, length):
    """Rotate mickey hand image and draw it pointing in the correct direction."""
    # Rotate image - pygame rotates counter-clockwise so use negative angle
    rotated = pygame.transform.rotate(hand_image, -angle_deg)
    rect    = rotated.get_rect()

    # Position the image so it points from the center outward
    angle = math.radians(angle_deg)
    offset_x = int((length / 2) * math.sin(angle))
    offset_y = int((length / 2) * math.cos(angle))
    rect.center = (CENTER[0] + offset_x, CENTER[1] - offset_y)

    surface.blit(rotated, rect)


# Main loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get current time
    now     = datetime.datetime.now()
    minutes = now.minute
    seconds = min(now.second, 59)  # handle leap seconds

    # Calculate angles (360 degrees / 60 = 6 degrees per unit)
    # Right hand = minutes
    min_angle = minutes * 6

    # Left hand = seconds (mirror the angle to the left side)
    sec_angle = -(seconds * 6)

    # Draw background
    screen.fill(WHITE)

    # Draw clock face circle
    pygame.draw.circle(screen, BLACK, CENTER, RADIUS, 4)

    # Draw hour tick marks
    for i in range(12):
        angle = math.radians(i * 30)
        outer = (CENTER[0] + (RADIUS - 5)  * math.sin(angle),
                 CENTER[1] - (RADIUS - 5)  * math.cos(angle))
        inner = (CENTER[0] + (RADIUS - 20) * math.sin(angle),
                 CENTER[1] - (RADIUS - 20) * math.cos(angle))
        pygame.draw.line(screen, BLACK, outer, inner, 3)

    # Draw hands
    if HAS_IMAGE:
        draw_image_hand(screen, min_angle, 100)   # right hand = minutes
        draw_image_hand(screen, sec_angle, 130)   # left hand  = seconds
    else:
        draw_hand(screen, min_angle, 100, BLACK, 8)  # minutes
        draw_hand(screen, sec_angle, 130, RED,   4)  # seconds

    # Draw center dot
    pygame.draw.circle(screen, BLACK, CENTER, 8)

    # Display digital time (minutes and seconds only)
    time_text = font.render(f"{minutes:02d}:{seconds:02d}", True, BLACK)
    screen.blit(time_text, (CENTER[0] - time_text.get_width() // 2,
                            CENTER[1] + RADIUS + 10))

    # Update screen every second (as required)
    pygame.display.flip()
    clock.tick(1)  # update once per second
