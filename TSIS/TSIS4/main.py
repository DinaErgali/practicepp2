import pygame, sys, json
from game import SnakeGame
from db import save_score, get_top10, get_best

pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

# 读取设置
with open("settings.json","r") as f:
    settings = json.load(f)

state = "menu"
username = ""
game = None
best = 0

def draw_text(text, y, size=32):
    font = pygame.font.Font(None, size)
    t = font.render(text, True, (255,255,255))
    screen.blit(t, (200 - t.get_width()//2, y))

while True:
    now = pygame.time.get_ticks()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------- MENU（用户名输入）--------
        if state == "menu":
            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_RETURN and username != "":
                    best = get_best(username)   # ✅ 个人最佳
                    game = SnakeGame(settings)
                    state = "game"

                elif e.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif e.key == pygame.K_l:
                    state = "leaderboard"

                else:
                    # 输入字符（限制长度）
                    if len(username) < 12 and e.unicode.isprintable():
                        username += e.unicode

        # -------- GAME --------
        elif state == "game":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: game.dir=(0,-1)
                if e.key == pygame.K_DOWN: game.dir=(0,1)
                if e.key == pygame.K_LEFT: game.dir=(-1,0)
                if e.key == pygame.K_RIGHT: game.dir=(1,0)

        # -------- LEADERBOARD --------
        elif state == "leaderboard":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    state = "menu"

        # -------- GAME OVER --------
        elif state == "game_over":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    state = "menu"

    # -------- DRAW --------

    if state == "menu":
        screen.fill((0,0,0))
        draw_text("Enter Username:", 100)
        draw_text(username + "_", 150)

        draw_text("ENTER = Play", 220, 24)
        draw_text("L = Leaderboard", 250, 24)

    elif state == "leaderboard":
        screen.fill((0,0,0))
        draw_text("TOP 10", 30)

        rows = get_top10()
        y = 80

        for i, r in enumerate(rows):
            name, score, level = r
            draw_text(f"{i+1}. {name} {score} (Lv{level})", y, 22)
            y += 30

        draw_text("ESC = Back", 360, 24)

    elif state == "game":
        result = game.update(now)
        game.draw(screen)

        # ✅ 显示个人最佳
        font = pygame.font.Font(None,20)
        screen.blit(font.render(f"Best:{best}", True,(255,255,255)), (300,10))

        if result == "game_over":
            save_score(username, game.score, game.level)  # ✅ 自动保存
            state = "game_over"

    elif state == "game_over":
        screen.fill((0,0,0))
        draw_text("GAME OVER", 140)
        draw_text(f"Score: {game.score}", 180)
        draw_text("ENTER = MENU", 240)

    pygame.display.flip()
    clock.tick(game.current_fps() if game else 10)