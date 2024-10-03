import pygame
import sys
import random

pygame.init()

def main():    
    display_info = pygame.display.Info()
    WIDTH, HEIGHT = display_info.current_w, display_info.current_h
    FPS = 100
    clock = pygame.time.Clock()
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GRAY = (200, 200, 200)
    ORANGE = (255, 165, 0)
    LIGHT_BLUE = (173, 116, 233)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen_color = BLACK
    pygame.display.set_caption('Bouncing Ball Game')
    font = pygame.font.Font(None, 36)
    
    # PLATFORM_WIDTH1, PLATFORM_HEIGHT1 = WIDTH, 20
    PLATFORM_WIDTH1, PLATFORM_HEIGHT1 = 150, 20
    platform_pos1 = [WIDTH // 2 - PLATFORM_WIDTH1 // 2, HEIGHT - PLATFORM_HEIGHT1 - 10]
    platform_speed = 12
    platform_color = ORANGE
    
    BALL_RADIUS = 30
    ball_color = WHITE
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_speed = [random.uniform(random.uniform(6, 8), random.uniform(-6, -8)), random.uniform(-6, -8)]
    
    score = 0
    lives = 3
    current_level = 1
    background_colour = 125
    
    portal_speed = [3, 3]
    
    portal1_width, portal1_height = 100, 100
    portal1_pos = [200, 200]
    portal1_dir = [0, 0]
    
    portal2_width, portal2_height = 100, 100
    portal2_pos = [WIDTH - 200, HEIGHT - 250]
    portal2_dir = [0, 0]

    def start_screen():
        i = 0
        start = True
        while start:
            screen.fill(rainbow_color(i))
            i = (i + 1) % ((background_colour + 1) * 6)
            show_text_on_screen("Bouncing Ball Game", 100, HEIGHT // 4)
            show_text_on_screen("Press spacebar to start...", 50, HEIGHT // 2)
            show_text_on_screen("Move the platform with arrow keys...", 45, HEIGHT // 1.5)
            show_text_on_screen("Your mission is to get 40 points", 100, HEIGHT // 1.2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def rainbow_color(value):
        step = (value // 126) % 6
        pos = value % 126
        if step == 0:
            return (background_colour, pos, 0)
        if step == 1:
            return (background_colour - pos, background_colour, 0)
        if step == 2:
            return (0, background_colour, pos)
        if step == 3:
            return (0, background_colour - pos, background_colour)
        if step == 4:
            return (pos, 0, background_colour)
        if step == 5:
            return (background_colour, 0, background_colour - pos)

    def end_screen():
        screen.fill(BLACK)
        show_text_on_screen("Good Try! :)", 100, HEIGHT // 4)
        show_text_on_screen(f"Your final score: {score}", 50, HEIGHT // 2)
        show_text_on_screen("Press spacebar to restart...", 45, HEIGHT // 1.5)
        pygame.display.flip()
        wait_for_key()

    def victory_screen():
        win = True
        i = 0
        while win:
            screen.fill(rainbow_color(i))
            i = (i + 1) % ((background_colour + 1) * 6)
            show_text_on_screen("Congratulations!", 100, HEIGHT // 4)
            show_text_on_screen("You Win! :D", 50, HEIGHT // 2)
            show_text_on_screen("Press spacebar to restart...", 45, HEIGHT // 1.5)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        win = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

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
        text_render = font.render(text, True, GRAY)
        text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(text_render, text_rect)

    def change_platform_color():
        return (random.randint(110, 255), random.randint(110, 255), random.randint(110, 255))

    def change_ball_color():
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))      

    start_screen()
    game_running = True
    while game_running:
        if 0 < ball_speed[0] < 6:
            ball_speed[0] = random.uniform(6, 8)
        if -6 < ball_speed[0] < 0:
            ball_speed[0] = random.uniform(-6, -8)
        if ball_speed[0] == 0:
            ball_speed[0] = random.uniform(-8, 8)

        if 0 < ball_speed[1] < 6:
            ball_speed[1] = random.uniform(6, 8)
        if -6 < ball_speed[1] < 0:
            ball_speed[1] = random.uniform(-6, -8)
        if ball_speed[1] == 0:
            ball_speed[1] = random.uniform(-8, 8)
        
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
        platform_pos1[0] += ((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed) - ((keys[pygame.K_a] - keys[pygame.K_d]) * platform_speed)
        if keys[pygame.K_RIGHT] and keys[pygame.K_d]:
            platform_pos1[0] -= (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
        if keys[pygame.K_LEFT] and keys[pygame.K_a]:
            platform_pos1[0] -= (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
        platform_pos1[0] = max(0, min(platform_pos1[0], WIDTH - PLATFORM_WIDTH1))
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]
        
        if (portal1_pos[0] - BALL_RADIUS <= ball_pos[0] <= portal1_pos[0] + portal1_width + BALL_RADIUS and portal1_pos[1] - BALL_RADIUS <= ball_pos[1] <= portal1_pos[1] + portal1_height + BALL_RADIUS):
            ball_pos[0] = random.uniform(portal2_pos[0] - BALL_RADIUS, portal2_pos[0] + portal2_width + BALL_RADIUS)
            ball_pos[1] = random.uniform(portal2_pos[1] - BALL_RADIUS, portal2_pos[1] + portal2_height + BALL_RADIUS)

        if (portal1_pos[0] - BALL_RADIUS - 2 <= 0):
            portal1_dir[0] = 0
            
        if (portal1_pos[0] + portal1_width + BALL_RADIUS + 2 >= WIDTH):
            portal1_dir[0] = 1
            
        if (portal1_pos[1] - BALL_RADIUS - 2 <= 0):
            portal1_dir[1] = 1
        
        if (portal1_pos[1] + portal1_height + BALL_RADIUS >= HEIGHT):
            portal1_dir[1] = 0
        
        if (portal1_dir[0] == 0):
            portal1_pos[0] += portal_speed[0]
        else:
            portal1_pos[0] -= portal_speed[0]
            
        if (portal1_dir[1] == 1):
            portal1_pos[1] += portal_speed[1]
        else:
            portal1_pos[1] -= portal_speed[1]
        
        if (portal2_pos[0] - BALL_RADIUS <= ball_pos[0] <= portal2_pos[0] + portal2_width + BALL_RADIUS and portal2_pos[1] - BALL_RADIUS <= ball_pos[1] <= portal2_pos[1] + portal2_height + BALL_RADIUS):
            ball_pos[0] = random.uniform(portal1_pos[0] - BALL_RADIUS, portal1_pos[0] + portal1_width + BALL_RADIUS)
            ball_pos[1] = random.uniform(portal1_pos[1] - BALL_RADIUS, portal1_pos[1] + portal1_height + BALL_RADIUS)

        if (portal2_pos[0] - BALL_RADIUS - 2 <= 0):
            portal2_dir[0] = 1
            
        if (portal2_pos[0] + portal2_width + BALL_RADIUS + 2 >= WIDTH):
            portal2_dir[0] = 0
            
        if (portal2_pos[1] - BALL_RADIUS - 2 <= 0):
            portal2_dir[1] = 0
        
        if (portal2_pos[1] + portal2_height + BALL_RADIUS >= HEIGHT):
            portal2_dir[1] = 1
        
        if (portal2_dir[0] == 1):
            portal2_pos[0] += portal_speed[0]
        else:
            portal2_pos[0] -= portal_speed[0]
            
        if (portal2_dir[1] == 0):
            portal2_pos[1] += portal_speed[1]
        else:
            portal2_pos[1] -= portal_speed[1]
        
        if ball_pos[0] - BALL_RADIUS - 5 <= 0 or ball_pos[0] + BALL_RADIUS + 5 >= WIDTH:
            if ((score % 2 == 0 and score != 0) and ball_speed[0] < current_level * 10 and ball_speed[0] > -(current_level * 10)):
                ball_speed[0] = -ball_speed[0] * 1.05
                if (platform_speed < 22):
                    platform_speed *= 1.05
            else:
                ball_speed[0] = -ball_speed[0]
            ball_color = change_ball_color()

        if ball_pos[1] <= 0:
            if ((score % 2 == 0 and score != 0) and ball_speed[1] < current_level * 10 and ball_speed[1] > -(current_level * 10)):
                ball_speed[1] = -ball_speed[1] * 1.05
                if (platform_speed < 22):
                    platform_speed *= 1.1
            else:
                ball_speed[1] = -ball_speed[1]
            ball_color = change_ball_color()

        if (platform_pos1[0] <= ball_pos[0] <= platform_pos1[0] + PLATFORM_WIDTH1 and platform_pos1[1] + 10 <= ball_pos[1] + BALL_RADIUS <= platform_pos1[1] + PLATFORM_HEIGHT1):
            if (keys[pygame.K_LEFT] and keys[pygame.K_a]):
                if (ball_speed[0] > 0):
                    ball_speed -= (platform_speed / 3)
                else:
                    ball_speed += (platform_speed / 3)
            if (keys[pygame.K_RIGHT] and keys[pygame.K_d]):
                if (ball_speed[0] > 0):
                    ball_speed[0] += (platform_speed / 2.5)
                else:
                    ball_speed[0] -= (platform_speed / 2.25)
            ball_speed[1] = -ball_speed[1]
            score += 1
            ball_color = change_ball_color()

        if score >= current_level * 10:
            current_level += 1
            if PLATFORM_HEIGHT1 <= 150:
                PLATFORM_HEIGHT1 *= 1.15
            lives += 1
            platform_pos1 = [WIDTH // 2 - PLATFORM_WIDTH1 // 2, HEIGHT - PLATFORM_HEIGHT1 - 10]
            if PLATFORM_WIDTH1 < WIDTH // 2 - 1000:
                PLATFORM_WIDTH1 *= 1.25
                if (PLATFORM_HEIGHT1 <= 150):
                    PLATFORM_HEIGHT1 *= 1.05
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            platform_color = change_platform_color()
            ball_color = change_ball_color()

        if ball_pos[1] >= HEIGHT:
            lives -= 1
            platform_pos1 = [WIDTH // 2 - PLATFORM_WIDTH1 // 2, HEIGHT - PLATFORM_HEIGHT1 - 10]
            if lives == 0:
                end_screen()
                main()
                score = 0
                lives = 3
                current_level = 1
            else:
                ball_pos = [WIDTH // 2, HEIGHT // 2]
                if (ball_speed[1] > 0):
                    ball_speed[1] = -ball_speed[1]

        if score == 40:
            victory_screen()
            main()

        screen.fill(screen_color)
        
        pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
        pygame.draw.rect(screen, platform_color, (int(platform_pos1[0]), int(platform_pos1[1]) + 10, PLATFORM_WIDTH1, PLATFORM_HEIGHT1))
        pygame.draw.rect(screen, RED, (int(portal1_pos[0]), int(portal1_pos[1]), portal1_width, portal1_height))
        pygame.draw.rect(screen, ORANGE, (int(portal2_pos[0]), int(portal2_pos[1]), portal2_width, portal2_height))
        
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
        speedx_rect = speedx_text.get_rect(topleft=(lives_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, BLACK, speedx_rect.inflate(10, 5))
        screen.blit(speedx_text, speedx_rect)
        
        speedy_text = font.render(f"y-Speed: {ball_speed[1]}", True, WHITE)
        speedy_rect = speedy_text.get_rect(topleft=(speedx_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, BLACK, speedy_rect.inflate(10, 5))
        screen.blit(speedy_text, speedy_rect)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
main()