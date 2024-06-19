import pygame
import sys
import random
pygame.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
BALL_RADIUS = 20
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 20
FPS = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 116, 233)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing Ball Game')
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]
platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
platform_speed = 10
score = 0
lives = 3
current_level = 1
platform_color = ORANGE

def start_screen():
    screen.fill(BLACK)
    show_text_on_screen("Bouncing Ball Game", 100, HEIGHT // 4)
    show_text_on_screen("Press space bar to start...", 50, HEIGHT // 2)
    show_text_on_screen("Move the platform with arrow keys...", 45, HEIGHT // 1.5)
    pygame.display.flip()
    wait_for_key()

def game_over_screen():
    screen.fill(BLACK)
    show_text_on_screen("Game Over", 50, HEIGHT // 3)
    show_text_on_screen(f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key (except the power key) to restart...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    finished = True
    wait_for_key()

def victory_screen():
    screen.fill(BLACK)
    show_text_on_screen("Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(f"You've won with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key (except the power key) to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    finished = True
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_text_on_screen(text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    screen.blit(text_render, text_rect)

def change_platform_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

start_screen()
game_running = True
while game_running:
#    show_text_on_screen(ball_speed, 30, HEIGHT // 6)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_LSHIFT:
                start_screen()
#    for 
    keys = pygame.key.get_pressed()
    platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
#    platform_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * platform_speed
    platform_pos[0] = max(0, min(platform_pos[0], WIDTH - PLATFORM_WIDTH))
#    platform_pos[1] = max(0, min(platform_pos[1], HEIGHT - PLATFORM_HEIGHT))
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
        if (score % 2 == 0):
            if (score % 8 == 0):
                ball_speed[1] *= 1.65
                platform_speed *= 1.5
            else:
                ball_speed[0] = -ball_speed[0] * 1.5
        else:
            ball_speed[0] = -ball_speed[0]

    if ball_pos[1] <= 0:
        if (score % 2 == 0):
            if (score % 8 == 0):
                ball_speed[1] *= 1.65
                platform_speed *= 1.5
            else:
                ball_speed[1] = -ball_speed[1] * 1.5
        else:
            ball_speed[1] = -ball_speed[1]
        
        
    if (platform_pos[0] <= ball_pos[0] <= platform_pos[0] + PLATFORM_WIDTH and platform_pos[1] <= ball_pos[1] <= platform_pos[1] + PLATFORM_HEIGHT):
        ball_speed[1] = -ball_speed[1]
        score += 1
    
    if score >= current_level * 10:
        current_level += 1
        platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_speed = [random.uniform(ball_speed[0], ball_speed[1]), random.uniform(ball_speed[0], ball_speed[1])]
        platform_color = change_platform_color()

    if ball_pos[1] >= HEIGHT:
        lives -= 1
        platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
        if lives == 0:
            game_over_screen()
            start_screen()
            score = 0
            lives = 3
            current_level = 1
        else:
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]

    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    pygame.draw.rect(screen, platform_color, (int(platform_pos[0]), int(platform_pos[1]), PLATFORM_WIDTH, PLATFORM_HEIGHT))
    info_line_y = 10
    info_spacing = 75 
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, RED, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)
    pygame.display.flip()
    clock.tick(FPS)
        
pygame.quit()