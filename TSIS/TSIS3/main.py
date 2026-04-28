import pygame
import sys
from racer import Game, LANES
from persistence import save_score
import ui

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Game")

clock = pygame.time.Clock()

state = "menu"
game = None
username = "Player"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------- MENU --------
        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game = Game()
                    state = "game"
                elif event.key == pygame.K_2:
                    state = "leaderboard"
                elif event.key == pygame.K_3:
                    state = "settings"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # -------- GAME --------
        elif state == "game":
            if event.type == pygame.KEYDOWN:

                # ✅ 安全获取当前车道（不会报错）
                lane_index = min(
                    range(len(LANES)),
                    key=lambda i: abs(LANES[i] - game.player.x)
                )

                # 左右移动（严格在车道内）
                if event.key == pygame.K_LEFT and lane_index > 0:
                    game.player.x = LANES[lane_index - 1]

                if event.key == pygame.K_RIGHT and lane_index < len(LANES) - 1:
                    game.player.x = LANES[lane_index + 1]

        # -------- LEADERBOARD / SETTINGS --------
        elif state in ["leaderboard", "settings"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"

        # -------- GAME OVER --------
        elif state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = "menu"

    # -------- DRAW --------
    if state == "menu":
        ui.menu_screen(screen)

    elif state == "leaderboard":
        ui.leaderboard_screen(screen)

    elif state == "settings":
        ui.settings_screen(screen)

    elif state == "game":
        result = game.update()
        game.draw(screen)

        if result == "game_over":
            save_score(username, game.score, game.distance)
            state = "game_over"

    elif state == "game_over":
        ui.game_over_screen(screen, game.score)

    pygame.display.flip()
    clock.tick(60)