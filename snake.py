import pygame
import random
import sys
import os
from pathlib import Path

# --- Configuration globale ---
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
FPS = 15

# Colors
WHITE = (245, 245, 245)
BLACK = (18, 18, 18)
GRAY = (120, 120, 130)
ACCENT = (40, 180, 99)
ACCENT2 = (45, 130, 200)
WARN = (220, 80, 60)
GOLD = (235, 190, 50)

# Fichiers
DATA_DIR = Path(__file__).parent
HIGHSCORE_FILE = DATA_DIR / "highscore.txt"

# --- Utilitaires ---
def load_highscore():
    try:
        return int(HIGHSCORE_FILE.read_text().strip())
    except Exception:
        return 0

def save_highscore(score):
    try:
        HIGHSCORE_FILE.write_text(str(score))
    except Exception:
        pass

def grid_to_pixel(pos):
    x, y = pos
    return x * CELL_SIZE, y * CELL_SIZE

# --- Classes du jeu ---
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        mid = (COLS // 2, ROWS // 2)
        self.body = [mid, (mid[0]-1, mid[1]), (mid[0]-2, mid[1])]
        self.dir = (1, 0)
        self.grow_pending = 0
        self.alive = True

    def head(self):
        return self.body[0]

    def move(self):
        if not self.alive:
            return
        x, y = self.head()
        dx, dy = self.dir
        new_head = ((x + dx) % COLS, (y + dy) % ROWS)
        # collision with self
        if new_head in self.body[:-1]:
            self.alive = False
            return
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def change_dir(self, new_dir):
        # prevent reversing
        dx, dy = new_dir
        cdx, cdy = self.dir
        if (dx == -cdx and dy == -cdy) or (dx == cdx and dy == cdy):
            return
        self.dir = (dx, dy)

    def grow(self, amount=1):
        self.grow_pending += amount

class Food:
    def __init__(self, obstacles, snake_body):
        self.pos = None
        self.kind = "normal"  # normal or bonus
        self.obstacles = obstacles
        self.snake_body = snake_body
        self.spawn()

    def spawn(self, kind=None):
        self.kind = kind if kind else ("bonus" if random.random() < 0.08 else "normal")
        choices = [(x, y) for x in range(COLS) for y in range(ROWS)
                   if (x, y) not in self.obstacles and (x, y) not in self.snake_body]
        self.pos = random.choice(choices) if choices else (0,0)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_med = pygame.font.SysFont("Arial", 28)
        self.font_small = pygame.font.SysFont("Arial", 18)
        self.highscore = load_highscore()
        self.reset_all()

    def reset_all(self):
        self.snake = Snake()
        self.level = 1
        self.score = 0
        self.speed = FPS
        self.obstacles = set()
        self.generate_obstacles_for_level()
        self.food = Food(self.obstacles, self.snake.body)
        self.running = False
        self.paused = False
        self.game_over = False
        self.ticks = 0

    def generate_obstacles_for_level(self):
        # Clear and generate obstacles based on level
        self.obstacles.clear()
        num = max(0, self.level - 1) * 6  # increase with level
        # create some rows/blocks
        for _ in range(num):
            w = random.randint(2, 6)
            h = random.randint(1, 3)
            x0 = random.randint(0, COLS - w - 1)
            y0 = random.randint(0, ROWS - h - 1)
            for xx in range(x0, x0 + w):
                for yy in range(y0, y0 + h):
                    self.obstacles.add((xx, yy))

    def check_collisions(self):
        head = self.snake.head()
        if head in self.obstacles:
            self.snake.alive = False

    def eat_food_check(self):
        if self.snake.head() == self.food.pos:
            if self.food.kind == "normal":
                self.score += 10
                self.snake.grow(1)
            else:
                # bonus: extra points + grow more
                self.score += 30
                self.snake.grow(3)
            # level up every 50 points
            new_level = 1 + self.score // 50
            if new_level > self.level:
                self.level = new_level
                self.speed = FPS + (self.level - 1) * 3
                self.generate_obstacles_for_level()
            self.food = Food(self.obstacles, self.snake.body)

    def update(self):
        if not self.running or self.paused or self.game_over:
            return
        # movement based on speed (use ticks to regulate)
        self.ticks += 1
        step = max(1, 15 - (self.speed // 5))  # adjust step to keep gameplay consistent
        if self.ticks % step == 0:
            self.snake.move()
            self.check_collisions()
            self.eat_food_check()
            if not self.snake.alive:
                self.game_over = True
                if self.score > self.highscore:
                    self.highscore = self.score
                    save_highscore(self.highscore)

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (30,30,30), (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (30,30,30), (0,y), (WIDTH,y))

    def draw_ui(self):
        # top bar
        pygame.draw.rect(self.screen, BLACK, (0,0, WIDTH, 48))
        title = self.font_med.render("Jeux Nioka", True, WHITE)
        self.screen.blit(title, (12,8))
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        lvl_text = self.font_small.render(f"Niveau: {self.level}", True, WHITE)
        hs_text = self.font_small.render(f"Highscore: {self.highscore}", True, WHITE)
        self.screen.blit(score_text, (WIDTH-200, 6))
        self.screen.blit(lvl_text, (WIDTH-340, 6))
        self.screen.blit(hs_text, (WIDTH-320, 26))

    def draw_snake(self):
        for i, part in enumerate(self.snake.body):
            px, py = grid_to_pixel(part)
            rect = pygame.Rect(px+1, py+1, CELL_SIZE-2, CELL_SIZE-2)
            if i == 0:
                pygame.draw.rect(self.screen, ACCENT2, rect, border_radius=6)
            else:
                pygame.draw.rect(self.screen, ACCENT, rect, border_radius=5)

    def draw_food(self):
        px, py = grid_to_pixel(self.food.pos)
        rect = pygame.Rect(px+4, py+4, CELL_SIZE-8, CELL_SIZE-8)
        if self.food.kind == "normal":
            pygame.draw.ellipse(self.screen, WARN, rect)
        else:
            pygame.draw.ellipse(self.screen, GOLD, rect)
            # small sparkle
            pygame.draw.rect(self.screen, WHITE, (px+6, py+6, 4, 4))

    def draw_obstacles(self):
        for ob in self.obstacles:
            px, py = grid_to_pixel(ob)
            rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (70,70,80), rect)

    def render(self):
        # background
        self.screen.fill((12, 12, 14))
        #playfield panel
        pygame.draw.rect(self.screen, (20,20,24), (0,48, WIDTH, HEIGHT-48))
        # draw elements
        # self.draw_grid()  # Uncomment for grid look
        self.draw_obstacles()
        self.draw_food()
        self.draw_snake()
        self.draw_ui()
        if not self.running and not self.game_over:
            self.draw_start_overlay()
        if self.paused:
            self.draw_paused_overlay()
        if self.game_over:
            self.draw_gameover_overlay()
        pygame.display.flip()

    def draw_start_overlay(self):
        s = pygame.Surface((WIDTH, HEIGHT-48), pygame.SRCALPHA)
        s.fill((5,5,5,160))
        self.screen.blit(s, (0,48))
        txt = self.font_large.render("Appuyez sur [ESPACE] pour démarrer", True, WHITE)
        r = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(txt, r)
        hint = self.font_med.render("Flèches pour diriger • P pour Pause • Q pour Quitter", True, GRAY)
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, r.bottom + 18))

    def draw_paused_overlay(self):
        s = pygame.Surface((WIDTH, HEIGHT-48), pygame.SRCALPHA)
        s.fill((8,8,8,180))
        self.screen.blit(s, (0,48))
        txt = self.font_large.render("Pause", True, WHITE)
        r = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(txt, r)

    def draw_gameover_overlay(self):
        s = pygame.Surface((WIDTH, HEIGHT-48), pygame.SRCALPHA)
        s.fill((0,0,0,200))
        self.screen.blit(s, (0,48))
        title = self.font_large.render("Game Over", True, ACCENT2)
        r = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        self.screen.blit(title, r)
        score_txt = self.font_med.render(f"Score: {self.score}   Highscore: {self.highscore}", True, WHITE)
        self.screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, r.bottom + 10))
        replay = self.font_small.render("Appuyez sur R pour recommencer, Q pour quitter", True, GRAY)
        self.screen.blit(replay, (WIDTH//2 - replay.get_width()//2, r.bottom + 46))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                pygame.quit()
                sys.exit(0)
            if event.key == pygame.K_SPACE and not self.running:
                self.running = True
                self.paused = False
                self.game_over = False
            if event.key == pygame.K_p:
                if self.running and not self.game_over:
                    self.paused = not self.paused
            if event.key == pygame.K_r and self.game_over:
                self.reset_all()
                self.running = True
            if event.key in (pygame.K_UP, pygame.K_w):
                self.snake.change_dir((0, -1))
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.snake.change_dir((0, 1))
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.snake.change_dir((-1, 0))
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.snake.change_dir((1, 0))

    def loop_once(self):
        # event handling
        for event in pygame.event.get():
            self.handle_event(event)
        self.update()
        self.render()
        # cap framerate relative to speed
        self.clock.tick(self.speed + 8)

def main():
    pygame.init()
    # Setup display
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeux Nioka")
    game = Game(screen)
    # main loop
    while True:
        game.loop_once()

if __name__ == "__main__":
    main()
