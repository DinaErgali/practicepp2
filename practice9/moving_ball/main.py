import pygame
import sys
from ball import Ball

# Initialize pygame
pygame.init()

# Window
WIDTH  = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")
clock  = pygame.time.Clock()
FPS    = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 18)

# Create ball
ball = Ball(WIDTH, HEIGHT)

# Main loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Move ball on key press (each press = 20 pixels)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move_up()
            elif event.key == pygame.K_DOWN:
                ball.move_down()
            elif event.key == pygame.K_LEFT:
                ball.move_left()
            elif event.key == pygame.K_RIGHT:
                ball.move_right()
            # All other keys are ignored

    # Draw white background
    screen.fill(WHITE)

    # Draw ball
    ball.draw(screen)

    # Show position on screen
    pos_text = font.render(f"Position: ({ball.x}, {ball.y})", True, BLACK)
    screen.blit(pos_text, (10, 10))

    hint = font.render("Arrow keys to move", True, (150, 150, 150))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 30))

    # Update display with frame rate control
    pygame.display.flip()
    clock.tick(FPS)
