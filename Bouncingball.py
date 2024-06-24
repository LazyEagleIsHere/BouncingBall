import pygame
import sys
import random
pygame.init()

def main():
    display_info = pygame.display.Info()
    WIDTH, HEIGHT = display_info.current_w, display_info.current_h
    BALL_RADIUS = 20
    PLATFORM_WIDTH, PLATFORM_HEIGHT = 135, 20
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
    ball_speed = [random.uniform(random.uniform(4, 6), random.uniform(4, 6)), random.uniform(random.uniform(-4, -6), random.uniform(-4, -6))]
    platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
    platform_speed = 13
    score = 0
    lives = 3
    current_level = 1
    platform_color = ORANGE

    def start_screen():
        screen.fill(BLACK)
        show_text_on_screen("Bouncing Ball Game", 100, HEIGHT // 4)
        show_text_on_screen("Press spacebar to start...", 50, HEIGHT // 2)
        show_text_on_screen("Move the platform with arrow keys...", 45, HEIGHT // 1.5)
        pygame.display.flip()
        wait_for_key()

    def game_over_screen():
        screen.fill(BLACK)
        show_text_on_screen("Game Over", 100, HEIGHT // 4)
        show_text_on_screen(f"Your final score: {score}", 50, HEIGHT // 2)
        show_text_on_screen("Press spacebar to restart...", 45, HEIGHT //1.5)
        pygame.display.flip()
        wait_for_key()

    def victory_screen():
        screen.fill(BLACK)
        show_text_on_screen("Congratulations!", 100, HEIGHT // 4)
        show_text_on_screen(f"You've won with a score of {score}", 50, HEIGHT // 2)
        show_text_on_screen("Press Exc to exit...", 45, HEIGHT // 1.5)
        pygame.display.flip()
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
        show_text_on_screen(str(ball_speed), 30, HEIGHT // 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_LSHIFT:
                    main()

        keys = pygame.key.get_pressed()
        platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
    #    platform_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * platform_speed
        platform_pos[0] = max(0, min(platform_pos[0], WIDTH - PLATFORM_WIDTH))
    #    platform_pos[1] = max(0, min(platform_pos[1], HEIGHT - PLATFORM_HEIGHT))
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
            if (score % 2 == 0 and ball_speed[0] < 20 and ball_speed[0] > -20):
                ball_speed[0] = -ball_speed[0] * 1.2
                if (platform_speed < 22):
                    platform_speed *= 1.1
            else:
                ball_speed[0] = -ball_speed[0]

        if ball_pos[1] <= 0:
            if (score % 2 == 0 and ball_speed[1] < 20 and ball_speed[1] > -20):
                ball_speed[1] = -ball_speed[1] * 1.2
                if (platform_speed < 22):
                    platform_speed *= 1.1
            else:
                ball_speed[1] = -ball_speed[1]
            
            
        if (platform_pos[0] <= ball_pos[0] <= platform_pos[0] + PLATFORM_WIDTH and platform_pos[1] <= ball_pos[1] <= platform_pos[1] + PLATFORM_HEIGHT):
            ball_speed[1] = -ball_speed[1]
            score += 1
        
        if score >= current_level * 10:
            current_level += 1
            platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
            ball_pos = [WIDTH // 2, HEIGHT // 2]
    #        ball_speed = [random.uniform(ball_speed[0], ball_speed[1]), random.uniform(ball_speed[0], ball_speed[1])]
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
                ball_speed = [random.uniform(4, 6), random.uniform(4, 6)]

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
        speedx_text = font.render(f"x-Speed: {ball_speed[0]}", True, WHITE)
        speedx_rect = speedx_text.get_rect(topleft = (lives_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, BLACK, speedx_rect.inflate(10, 5))
        screen.blit(speedx_text, speedx_rect)
        speedy_text = font.render(f"y-Speed: {ball_speed[1]}", True, WHITE)
        speedy_rect = speedy_text.get_rect(topleft = (speedx_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, BLACK, speedy_rect.inflate(10, 5))
        screen.blit(speedy_text, speedy_rect)
        pygame.display.flip()
        clock.tick(FPS)
            
    pygame.quit()
main()
