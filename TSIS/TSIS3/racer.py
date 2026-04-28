import pygame
import random
import time

WIDTH = 400
HEIGHT = 600

LANE_COUNT = 5
LANE_WIDTH = WIDTH // LANE_COUNT

# 每个车道中心
LANES = [i * LANE_WIDTH + LANE_WIDTH//2 - 20 for i in range(LANE_COUNT)]

class Game:
    def __init__(self):
        self.player = pygame.Rect(LANES[2], 500, 40, 60)

        self.traffic = []
        self.obstacles = []
        self.powerups = []

        self.score = 0
        self.distance = 0
        self.speed = 5

        self.active_power = None
        self.power_end = 0

        self.coin_sound = pygame.mixer.Sound("assets/coin.wav")

    # -------- SPAWN --------
    def spawn_traffic(self):
        x = random.choice(LANES)
        self.traffic.append(pygame.Rect(x, -60, 40, 60))

    def spawn_obstacle(self):
        x = random.choice(LANES)
        typ = random.choice(["oil", "slow"])
        self.obstacles.append((pygame.Rect(x, -60, 40, 40), typ))

    def spawn_powerup(self):
        x = random.choice(LANES)
        typ = random.choice(["nitro", "shield", "repair"])
        self.powerups.append((pygame.Rect(x, -60, 30, 30), typ, time.time()))

    # -------- UPDATE --------
    def update(self):
        self.score += 1
        self.distance += 1

        if random.randint(1, 25) == 1:
            self.spawn_traffic()

        if random.randint(1, 50) == 1:
            self.spawn_obstacle()

        if random.randint(1, 100) == 1:
            self.spawn_powerup()

        for t in self.traffic:
            t.y += self.speed

        for o, _ in self.obstacles:
            o.y += self.speed

        for p in self.powerups:
            p[0].y += self.speed

        # -------- 碰撞 --------
        for t in self.traffic:
            if self.player.colliderect(t):
                return "game_over"

        for o, _ in self.obstacles:
            if self.player.colliderect(o):
                lane_index = LANES.index(self.player.x)
                new_index = max(0, min(LANE_COUNT-1, lane_index + random.choice([-1,1])))
                self.player.x = LANES[new_index]

        for p in self.powerups[:]:
            rect, typ, spawn = p

            if time.time() - spawn > 6:
                self.powerups.remove(p)
                continue

            if self.player.colliderect(rect):
                self.coin_sound.play()
                self.active_power = typ
                self.power_end = time.time() + 4
                self.powerups.remove(p)

        if time.time() > self.power_end:
            self.active_power = None

        return "running"

    # -------- DRAW --------
    def draw(self, screen):
        screen.fill((40, 40, 40))

        offset = (self.distance * self.speed) % 40

        # 🚧 路边
        pygame.draw.rect(screen, (80,80,80), (0,0,60,HEIGHT))
        pygame.draw.rect(screen, (80,80,80), (WIDTH-60,0,60,HEIGHT))

        # 🛣️ 车道线
        for i in range(1, LANE_COUNT):
            x = i * LANE_WIDTH
            for y in range(-40, HEIGHT, 40):
                pygame.draw.rect(screen, (255,255,255), (x, y+offset, 3, 20))

        # 🚗 玩家车（带灯）
        pygame.draw.rect(screen, (255,0,0), self.player)
        pygame.draw.rect(screen, (255,255,0), (self.player.x+10, self.player.y, 5,5))
        pygame.draw.rect(screen, (255,255,0), (self.player.x+25, self.player.y, 5,5))

        # 🚘 敌车
        for t in self.traffic:
            pygame.draw.rect(screen, (0,100,255), t)
            pygame.draw.rect(screen, (255,255,255), (t.x+10, t.y, 5,5))

        # ⚠️ 障碍
        for o, typ in self.obstacles:
            if typ == "oil":
                pygame.draw.ellipse(screen, (0,0,0), o)
            else:
                pygame.draw.rect(screen, (255,200,0), o)

        # ⚡ 道具（+字母）
        font_small = pygame.font.Font(None, 20)

        for rect, typ, _ in self.powerups:
            if typ == "nitro":
                color = (0,255,0)
                label = "N"
            elif typ == "shield":
                color = (0,200,255)
                label = "S"
            else:
                color = (200,0,200)
                label = "R"

            pygame.draw.circle(screen, color, rect.center, 12)

            text = font_small.render(label, True, (0,0,0))
            screen.blit(text, (rect.x+6, rect.y+5))

        # 📊 UI
        font = pygame.font.Font(None, 28)

        screen.blit(font.render(f"Score: {self.score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Distance: {self.distance}", True, (255,255,255)), (10,35))

        if self.active_power:
            screen.blit(font.render(f"POWER: {self.active_power.upper()}",
                                    True, (0,255,0)), (10,60))