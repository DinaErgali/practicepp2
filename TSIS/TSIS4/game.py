import pygame, random

CELL = 20
W, H = 400, 400
GRID_W, GRID_H = W//CELL, H//CELL

class SnakeGame:
    def __init__(self, settings):
        self.settings = settings

        self.snake = [(10,10), (9,10), (8,10)]
        self.dir = (1,0)

        self.obstacles = []

        self.food = self.spawn()
        self.poison = self.spawn()

        # -------- POWER SYSTEM --------
        self.power = None
        self.power_pos = None
        self.power_spawn_time = 0

        self.power_active = None
        self.power_end = 0

        self.last_power_time = 0

        self.score = 0
        self.level = 1
        self.base_speed = 8

    def spawn(self):
        while True:
            p = (random.randrange(GRID_W), random.randrange(GRID_H))
            if p not in self.snake and p not in self.obstacles:
                return p

    def update(self, now):

        # ========= POWER SPAWN =========
        if not self.power and now - self.last_power_time > 5000:
            self.power = random.choice(["speed","slow","shield"])
            self.power_pos = self.spawn()
            self.power_spawn_time = now
            self.last_power_time = now

        # ========= POWER EXPIRE =========
        if self.power and now - self.power_spawn_time > 8000:
            self.power = None
            self.power_pos = None

        hx, hy = self.snake[0]
        nx, ny = hx + self.dir[0], hy + self.dir[1]

        hit_wall = not (0 <= nx < GRID_W and 0 <= ny < GRID_H)
        hit_self = (nx,ny) in self.snake
        hit_obs  = (nx,ny) in self.obstacles

        # ========= COLLISION =========
        if hit_wall or hit_self or hit_obs:
            if self.power_active == "shield":
                self.power_active = None
            else:
                return "game_over"

        self.snake.insert(0, (nx,ny))

        # ========= FOOD =========
        if (nx,ny) == self.food:
            self.score += 10
            self.food = self.spawn()

        # ========= POISON =========
        elif (nx,ny) == self.poison:
            self.snake = self.snake[:-2] if len(self.snake) > 2 else []
            if len(self.snake) <= 1:
                return "game_over"
            self.poison = self.spawn()

        else:
            self.snake.pop()

        # ========= PICK POWER =========
        if self.power and (nx,ny) == self.power_pos:
            self.power_active = self.power

            if self.power in ["speed","slow"]:
                self.power_end = now + 5000
            else:
                self.power_end = 0

            self.power = None
            self.power_pos = None

        # ========= POWER END =========
        if self.power_active in ["speed","slow"] and now > self.power_end:
            self.power_active = None

        # ========= LEVEL =========
        if self.score // 50 + 1 > self.level:
            self.level += 1
            if self.level >= 3:
                for _ in range(3):
                    self.obstacles.append(self.spawn())

        return "running"

    def current_fps(self):
        fps = self.base_speed + (self.level-1)*2

        if self.power_active == "speed":
            fps += 5
        if self.power_active == "slow":
            fps = max(4, fps-4)

        return fps

    def draw(self, screen):
        screen.fill((20,20,20))

        if self.settings.get("grid", True):
            for x in range(0,W,CELL):
                pygame.draw.line(screen,(40,40,40),(x,0),(x,H))
            for y in range(0,H,CELL):
                pygame.draw.line(screen,(40,40,40),(0,y),(W,y))

        font_small = pygame.font.Font(None, 18)

        # SNAKE
        for i,(x,y) in enumerate(self.snake):
            color = self.settings.get("snake_color", [0,255,0]) if i==0 else (0,180,0)
            pygame.draw.rect(screen, color, (x*CELL,y*CELL,CELL,CELL))

        # FOOD +
        food_rect = pygame.Rect(self.food[0]*CELL, self.food[1]*CELL, CELL, CELL)
        pygame.draw.rect(screen,(255,255,0), food_rect)
        screen.blit(font_small.render("+", True, (0,0,0)), (food_rect.x+6, food_rect.y+3))

        # POISON X
        poison_rect = pygame.Rect(self.poison[0]*CELL, self.poison[1]*CELL, CELL, CELL)
        pygame.draw.rect(screen,(150,0,0), poison_rect)
        screen.blit(font_small.render("X", True, (255,255,255)), (poison_rect.x+6, poison_rect.y+3))

        # OBSTACLES
        for o in self.obstacles:
            pygame.draw.rect(screen,(120,120,120),(o[0]*CELL,o[1]*CELL,CELL,CELL))

        # POWER-UP
        if self.power:
            if self.power == "speed":
                color = (0,255,0)
                letter = "S"
            elif self.power == "shield":
                color = (0,200,255)
                letter = "H"
            else:
                color = (200,0,200)
                letter = "L"

            r = pygame.Rect(self.power_pos[0]*CELL, self.power_pos[1]*CELL, CELL, CELL)
            pygame.draw.rect(screen, color, r)
            screen.blit(font_small.render(letter, True, (0,0,0)), (r.x+6, r.y+3))

        # UI
        font = pygame.font.Font(None,24)
        screen.blit(font.render(f"Score:{self.score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Level:{self.level}", True, (255,255,255)), (10,30))

        if self.power_active:
            screen.blit(font.render(self.power_active.upper(), True, (0,255,0)), (10,50))