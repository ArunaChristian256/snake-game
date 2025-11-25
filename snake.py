import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game  Edition")

# Clock
clock = pygame.time.Clock()
FPS = 15     # Starting speed

# Colors
BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
SNAKE_COLOR = (50, 205, 50)
FOOD_COLOR = (255, 99, 71)
REWARD_COLOR = (255, 215, 0)
BG_GRADIENT_START = (30, 30, 60)
BG_GRADIENT_END = (50, 50, 100)
TEXT_COLOR = (255, 255, 255)

# Fonts
score_font = pygame.font.SysFont("Verdana", 28, bold=True)
game_over_font = pygame.font.SysFont("Verdana", 60, bold=True)
info_font = pygame.font.SysFont("Verdana", 24)
welcome_font = pygame.font.SysFont("Verdana", 50, bold=True)

# Load High Score
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()

# Background
def draw_gradient_background():
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        r = int(BG_GRADIENT_START[0] * (1 - ratio) + BG_GRADIENT_END[0] * ratio)
        g = int(BG_GRADIENT_START[1] * (1 - ratio) + BG_GRADIENT_END[1] * ratio)
        b = int(BG_GRADIENT_START[2] * (1 - ratio) + BG_GRADIENT_END[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

# UI
def display_ui(score, level):
    text = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    level_text = score_font.render(f"Level: {level}", True, TEXT_COLOR)
    high_text = score_font.render(f"High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(high_text, (10, 90))

# Draw snake and food
def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, SNAKE_COLOR, (*block, CELL_SIZE, CELL_SIZE), border_radius=7)

def draw_food(pos):
    pygame.draw.rect(screen, FOOD_COLOR, (*pos, CELL_SIZE, CELL_SIZE), border_radius=7)

# NEW WELCOME SCREEN
def welcome_screen():
    alpha = 0
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))

    title = "WELCOME TO THE SNAKE GAME"
    subtitle = (
        "In this classic challenge, your mission is simple:\n"
        "Eat food, grow longer, and avoid obstacles.\n"
        "Each level increases the speed — stay focused!"
    )
    start_msg = "Press ENTER to Start"

    title_surf = welcome_font.render(title, True, WHITE)
    start_surf = info_font.render(start_msg, True, WHITE)

    subtitle_lines = subtitle.split("\n")
    rendered_lines = [info_font.render(line, True, (230, 230, 230)) for line in subtitle_lines]

    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_gradient_background()

        # Fade-in animation
        if alpha < 255:
            alpha += 4
        fade_surface.set_alpha(255 - alpha)
        screen.blit(fade_surface, (0, 0))

        # Title
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, HEIGHT//6))

        # Subtitle block (justified center)
        subtitle_y = HEIGHT//3
        for line in rendered_lines:
            screen.blit(line, (WIDTH//2 - line.get_width()//2, subtitle_y))
            subtitle_y += 40

        # Start message
        screen.blit(start_surf, (WIDTH//2 - start_surf.get_width()//2, HEIGHT - 150))

        pygame.display.update()
        clock.tick(60)

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Reward screen
def reward_screen():
    running = True
    while running:
        screen.fill(BLACK)
        draw_gradient_background()

        reward_text = game_over_font.render("🎉 REWARD UNLOCKED! 🎉", True, REWARD_COLOR)
        info_text = info_font.render("You reached 100 points!", True, WHITE)
        continue_text = info_font.render("Press ENTER to Continue", True, WHITE)

        screen.blit(reward_text, (WIDTH//8, HEIGHT//3))
        screen.blit(info_text, (WIDTH//3, HEIGHT//2))
        screen.blit(continue_text, (WIDTH//3, HEIGHT//2 + 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

# Show intro
welcome_screen()


# MAIN GAME VARIABLES
snake = [[100, 100], [80, 100], [60, 100]]
direction = "RIGHT"
food = [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]

score = 0
level = 1
game_over = False
paused = False
reward_given = False

# MAIN LOOP
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
                score = 0
                level = 1
                FPS = 15
                reward_given = False
                game_over = False

    if not paused and not game_over:
        head = snake[0].copy()

        if direction == "UP": head[1] -= CELL_SIZE
        if direction == "DOWN": head[1] += CELL_SIZE
        if direction == "LEFT": head[0] -= CELL_SIZE
        if direction == "RIGHT": head[0] += CELL_SIZE

        snake.insert(0, head)

        # Food collision
        if head == food:
            score += 1

            if score % 10 == 0:
                level += 1
                FPS += 2

            if score >= 100 and not reward_given:
                reward_given = True
                reward_screen()

            food = [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]
        else:
            snake.pop()

        # Wall collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            game_over = True

        # Self collision
        if head in snake[1:]:
            game_over = True

    # Draw everything
    draw_snake(snake)
    draw_food(food)
    display_ui(score, level)

    # Game Over Screen
    if game_over:
        global high_score
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        over_text = game_over_font.render("GAME OVER", True, FOOD_COLOR)
        restart_text = info_font.render("Press R to Restart", True, WHITE)
        screen.blit(over_text, (WIDTH//4, HEIGHT//3))
        screen.blit(restart_text, (WIDTH//3, HEIGHT//2))

    pygame.display.update()
    clock.tick(FPS)
