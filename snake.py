import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game - Professional Edition")

# Clock
clock = pygame.time.Clock()
FPS = 15

# Colors
BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
SNAKE_COLOR = (50, 205, 50)
FOOD_COLOR = (255, 99, 71)
BG_GRADIENT_START = (30, 30, 60)
BG_GRADIENT_END = (50, 50, 100)
TEXT_COLOR = (255, 255, 255)

# Fonts
score_font = pygame.font.SysFont("Verdana", 28, bold=True)
game_over_font = pygame.font.SysFont("Verdana", 60, bold=True)
info_font = pygame.font.SysFont("Verdana", 24)
welcome_font = pygame.font.SysFont("Verdana", 50, bold=True)

# Functions
def draw_gradient_background():
    for i in range(HEIGHT):
        color_ratio = i / HEIGHT
        r = int(BG_GRADIENT_START[0] * (1 - color_ratio) + BG_GRADIENT_END[0] * color_ratio)
        g = int(BG_GRADIENT_START[1] * (1 - color_ratio) + BG_GRADIENT_END[1] * color_ratio)
        b = int(BG_GRADIENT_START[2] * (1 - color_ratio) + BG_GRADIENT_END[2] * color_ratio)
        pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, SNAKE_COLOR, (*block, CELL_SIZE, CELL_SIZE), border_radius=8)

def draw_food(position):
    pygame.draw.rect(screen, FOOD_COLOR, (*position, CELL_SIZE, CELL_SIZE), border_radius=8)

def display_score(score):
    text = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))

def welcome_screen():
    screen.fill(BLACK)
    draw_gradient_background()
    welcome_text = welcome_font.render("Welcome to Snake Game!", True, WHITE)
    info_text = info_font.render("Press ENTER to Start", True, WHITE)
    screen.blit(welcome_text, (WIDTH//8, HEIGHT//3))
    screen.blit(info_text, (WIDTH//3, HEIGHT//2))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Main game variables
snake = [[100, 100], [80, 100], [60, 100]]
direction = "RIGHT"
food = [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]
score = 0
game_over = False
paused = False

# Show welcome screen first
welcome_screen()

# Main game loop
while True:
    screen.fill(BLACK)
    draw_gradient_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_r and game_over:
                snake = [[100, 100], [80, 100], [60, 100]]
                direction = "RIGHT"
                food = [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                        random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]
                score = 0
                game_over = False

    if not paused and not game_over:
        # Move snake
        head = snake[0].copy()
        if direction == "UP": head[1] -= CELL_SIZE
        if direction == "DOWN": head[1] += CELL_SIZE
        if direction == "LEFT": head[0] -= CELL_SIZE
        if direction == "RIGHT": head[0] += CELL_SIZE
        snake.insert(0, head)

        # Check food collision
        if head == food:
            score += 1
            food = [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]
        else:
            snake.pop()

        # Check collisions
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            game_over = True
        if head in snake[1:]:
            game_over = True

    # Draw everything
    draw_snake(snake)
    draw_food(food)
    display_score(score)

    if paused:
        pause_text = info_font.render("PAUSED - Press P to resume", True, WHITE)
        screen.blit(pause_text, (WIDTH // 4, HEIGHT // 2))
    if game_over:
        game_over_text = game_over_font.render("GAME OVER", True, FOOD_COLOR)
        restart_text = info_font.render("Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
        screen.blit(restart_text, (WIDTH // 3, HEIGHT // 2))

    pygame.display.update()
    clock.tick(FPS)
