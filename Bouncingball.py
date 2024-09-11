import pygame
import sys
import random
pygame.init()

def main():
    display_info = pygame.display.Info()
    WIDTH, HEIGHT = display_info.current_w, display_info.current_h
    BALL_RADIUS = 30
    PLATFORM_WIDTH1, PLATFORM_HEIGHT1 = 150, 20
    FPS = 100
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    LIGHT_BLUE = (173, 116, 233)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen_color = BLACK
    pygame.display.set_caption('Bouncing Ball Game')
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_speed = [0, 0]
    ball_speed = [random.uniform(random.uniform(4, 6), random.uniform(-4, -6)), random.uniform(-4, -6)]
    # ball_speed = [random.uniform(random.uniform(4, 6), random.uniform(4, 6)), random.uniform(random.uniform(-4, -6), random.uniform(-4, -6))]
    platform_pos1 = [WIDTH // 2 - PLATFORM_WIDTH1 // 2, HEIGHT - PLATFORM_HEIGHT1 - 10]
    block = [random.uniform]
    platform_speed = 13
    score = 0
    lives = 3
    current_level = 1
    platform_color = ORANGE
    ball_color = WHITE

    def start_screen():
        screen.fill(screen_color)
        show_text_on_screen("Bouncing Ball Game", 100, HEIGHT // 4)
        show_text_on_screen("Press spacebar to start...", 50, HEIGHT // 2)
        # pygame.draw.rect(screen, WHITE, [WIDTH // 2 - 75, HEIGHT // 2 + 100, 140, 65])
        # sf = pygame.font.SysFont('Corbel', 60)
        # text = sf.render('Start', True, BLACK)
        # screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2 + 100))
        show_text_on_screen("Move the platform with arrow keys...", 45, HEIGHT // 1.5)
        pygame.display.flip()
        # while True:
        #     for event in pygame.event.get():
        #         mouse = pygame.mouse.get_pos()
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()
        #         elif event.type == pygame.MOUSEBUTTONDOWN:
        #             if WIDTH // 2 <= mouse[0] <= WIDTH // 2 + 140 and HEIGHT // 2 <= mouse[1] <= HEIGHT // 2 + 65:
        #                 pygame.quit()
        wait_for_key()

    def end_screen():
        screen.fill(BLACK)
        show_text_on_screen("Good Try!", 100, HEIGHT // 4)
        show_text_on_screen(f"Your final score: {score}", 50, HEIGHT // 2)
        show_text_on_screen("Press spacebar to restart...", 45, HEIGHT //1.5)
        pygame.display.flip()
        wait_for_key()

    # def victory_screen():
    #     screen.fill(BLACK)
    #     show_text_on_screen("Congratulations!", 100, HEIGHT // 4)
    #     show_text_on_screen(f"You've won with a score of {score}", 50, HEIGHT // 2)
    #     show_text_on_screen("Press Exc to exit...", 45, HEIGHT // 1.5)
    #     pygame.display.flip()
    #     wait_for_key()
    
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
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     mouse = pygame.mouse.get_pos()
                #     if (WIDTH // 2 - 75 <= mouse[0] <= WIDTH // 2 + 140 and HEIGHT // 2 + 100 <= mouse[1] <= HEIGHT // 2 + 65):
                #         waiting == False

    def show_text_on_screen(text, font_size, y_position):
        font = pygame.font.Font(None, font_size)
        text_render = font.render(text, True, WHITE)
        text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(text_render, text_rect)

    def change_platform_color():
        return (random.randint(110, 255), random.randint(110, 255), random.randint(110, 255))
    
    def change_ball_color():
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def change_screen_color():
        return (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))

    start_screen()
    game_running = True
    while game_running:
        if ball_speed[0] < 0:
            if ball_speed[0] > -4:
                ball_speed[0] = random.uniform(-4, -6)
        if ball_speed[0] > 0:
            if ball_speed[0] < 4:
                ball_speed[0] = random.uniform(4, 6)
        if ball_speed[1] < 0:
            if ball_speed[1] > -4:
                ball_speed[1] = random.uniform(-4, -6)
        if ball_speed[1] > 0:
            if ball_speed[1] < 4:
                ball_speed[1] = random.uniform(4, 6)

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
        platform_pos1[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
        platform_pos1[0] = max(0, min(platform_pos1[0], WIDTH - PLATFORM_WIDTH1))
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
            if ((score % 2 == 0 and score != 0) and ball_speed[0] < current_level * 10 and ball_speed[0] > -(current_level * 10)):
                ball_speed[0] = -ball_speed[0] * 1.2
                if (platform_speed < 22):
                    platform_speed *= 1.1
            else:
                ball_speed[0] = -ball_speed[0]
            ball_color = change_ball_color()
            # screen_color = change_screen_color()

        if ball_pos[1] <= 0:
            if ((score % 2 == 0 and score != 0) and ball_speed[1] < current_level * 10 and ball_speed[1] > -(current_level * 10)):
                ball_speed[1] = -ball_speed[1] * 1.2
                if (platform_speed < 22):
                    platform_speed *= 1.1
            else:
                ball_speed[1] = -ball_speed[1]
            ball_color = change_ball_color()
            # screen_color = change_screen_color()


        if (platform_pos1[0] <= ball_pos[0] <= platform_pos1[0] + PLATFORM_WIDTH1 and platform_pos1[1] <= ball_pos[1] <= platform_pos1[1] + PLATFORM_HEIGHT1):
            ball_speed[1] = -ball_speed[1]
            score += 1
            ball_color = change_ball_color()
            # screen_color = change_screen_color()

        if score >= current_level * 10:
            show_text_on_screen(f"Level Up!", 100, HEIGHT // 2 - 50)
            counter, text = 3, '3'.rjust(3)
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            font = pygame.font.SysFont('Consolas', 30)
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        counter -= 1
                        text = str(counter).rjust(3) if counter > 0 else run = False
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            pygame.quit()
                            sys.exit()
                screen.blit(font.render(text, True, BLACK, (32, 48)))
                pygame.display.flip()
                clock.tick(60)
            current_level += 1
            lives += 1
            platform_pos1 = [WIDTH // 2 - PLATFORM_WIDTH1 // 2, HEIGHT - PLATFORM_HEIGHT1 - 10]
            if PLATFORM_WIDTH1 < WIDTH // 2:
                PLATFORM_WIDTH1 *= 1.25
                PLATFORM_HEIGHT1 *= 1.05
            BALL_RADIUS *= 1.15
            ball_pos = [WIDTH // 2, HEIGHT // 2]
    #        ball_speed = [random.uniform(ball_speed[0], ball_speed[1]), random.uniform(ball_speed[0], ball_speed[1])]
            platform_color = change_platform_color()
            ball_color = change_ball_color()
            # screen_color = change_screen_color()

        if ball_pos[1] >= HEIGHT:
            lives -= 1
            platform_pos1 = [WIDTH // 2 - PLATFORM_WIDTH1 // 2, HEIGHT - PLATFORM_HEIGHT1 - 10]
            if lives == 0:
                end_screen()
                start_screen()
                score = 0
                lives = 3
                current_level = 1
            else:
                ball_pos = [WIDTH // 2, HEIGHT // 2]
                if current_level != 1:
                    ball_speed = [(current_level - 1) * 10, -abs((current_level - 1) * 10)]
                else:
                    ball_speed = [random.uniform(random.uniform(4, 6), random.uniform(-4, -6)) * 1.5, random.uniform(-4, -6) * 1.5]

        screen.fill(screen_color)
        pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
        pygame.draw.rect(screen, platform_color, (int(platform_pos1[0]), int(platform_pos1[1]), PLATFORM_WIDTH1, PLATFORM_HEIGHT1))
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