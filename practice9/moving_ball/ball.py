import pygame


class Ball:

    RADIUS = 25   # radius 25px = diameter 50px (as required)
    STEP   = 20   # move 20 pixels per key press (as required)
    COLOR  = (220, 40, 40)   # red

    def __init__(self, screen_width, screen_height):
        self.screen_w = screen_width
        self.screen_h = screen_height
        # Start at center of screen
        self.x = screen_width  // 2
        self.y = screen_height // 2

    def move_up(self):
        """Move up by STEP pixels. Stop at top edge."""
        new_y = self.y - self.STEP
        if new_y - self.RADIUS >= 0:   # boundary check
            self.y = new_y

    def move_down(self):
        """Move down by STEP pixels. Stop at bottom edge."""
        new_y = self.y + self.STEP
        if new_y + self.RADIUS <= self.screen_h:   # boundary check
            self.y = new_y

    def move_left(self):
        """Move left by STEP pixels. Stop at left edge."""
        new_x = self.x - self.STEP
        if new_x - self.RADIUS >= 0:   # boundary check
            self.x = new_x

    def move_right(self):
        """Move right by STEP pixels. Stop at right edge."""
        new_x = self.x + self.STEP
        if new_x + self.RADIUS <= self.screen_w:   # boundary check
            self.x = new_x

    def draw(self, surface):
        """Draw the red ball on the surface."""
        pygame.draw.circle(surface, self.COLOR, (self.x, self.y), self.RADIUS)
