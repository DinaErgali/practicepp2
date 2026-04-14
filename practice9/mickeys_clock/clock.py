import datetime
import math
import pygame


def get_time():
    """Get current minutes and seconds from system clock."""
    now = datetime.datetime.now()
    return now.minute, min(now.second, 59)  # min() handles leap seconds


def time_to_angle(value):
    """Convert a time value (minutes or seconds) to a clock angle in degrees.
    Each unit = 6 degrees (360 / 60 = 6).
    """
    return value * 6


def draw_clock_face(surface, center, radius):
    """Draw the clock circle and 12 hour tick marks."""
    BLACK = (0, 0, 0)
    GRAY  = (180, 180, 180)

    # Outer circle
    pygame.draw.circle(surface, BLACK, center, radius, 4)

    # 12 hour tick marks
    for i in range(12):
        angle = math.radians(i * 30)
        outer = (center[0] + (radius - 5)  * math.sin(angle),
                 center[1] - (radius - 5)  * math.cos(angle))
        inner = (center[0] + (radius - 20) * math.sin(angle),
                 center[1] - (radius - 20) * math.cos(angle))
        pygame.draw.line(surface, BLACK, outer, inner, 3)
