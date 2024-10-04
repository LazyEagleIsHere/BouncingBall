import pygame
import sys
import random

pygame.init()

def main():    
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    FPS = 100
    clock = pygame.time.Clock()
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    gray = (200, 200, 200)
    orange = (255, 165, 0)
    light_blue = (173, 116, 233)
    
    screen = pygame.display.set_mode((width, height))
    screen_color = black
    pygame.display.set_caption('Bouncing Ball Game')
    font = pygame.font.Font(None, 36)
    
    platform_width1, platform_height1 = width, 20
    # platform_width1, platform_height1 = 150, 20
    platform_pos1 = [width // 2 - platform_width1 // 2, height - platform_height1 - 10]
    platform_speed = 12
    platform_color = orange
    
    ball_radius = 30
    ball_color = white
    ball_pos = [width // 2, height // 2]
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
    portal2_pos = [width - 200, height - 250]
    portal2_dir = [0, 0]

    def start_screen():
        i = 0
        start = True
        while start:
            screen.fill(rainbow_color(i))
            i = (i + 1) % ((background_colour + 1) * 6)
            show_text_on_screen("Bouncing Ball Game", 100, height // 4)
            show_text_on_screen("Press spacebar to start...", 50, height // 2)
            show_text_on_screen("Move the platform with arrow keys...", 45, height // 1.5)
            show_text_on_screen("Your mission is to get 40 points", 100, height // 1.2)
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
        screen.fill(black)
        show_text_on_screen("Good Try! :)", 100, height // 4)
        show_text_on_screen(f"Your final score: {score}", 50, height // 2)
        show_text_on_screen("Press spacebar to restart...", 45, height // 1.5)
        pygame.display.flip()
        wait_for_key()

    def victory_screen():
        win = True
        i = 0
        while win:
            screen.fill(rainbow_color(i))
            i = (i + 1) % ((background_colour + 1) * 6)
            show_text_on_screen("Congratulations!", 100, height // 4)
            show_text_on_screen("You Win! :D", 50, height // 2)
            show_text_on_screen("Press spacebar to restart...", 45, height // 1.5)
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
        text_render = font.render(text, True, gray)
        text_rect = text_render.get_rect(center=(width // 2, y_position))
        screen.blit(text_render, text_rect)

    def change_platform_color():
        return (random.randint(110, 255), random.randint(110, 255), random.randint(110, 255))

    def change_ball_color():
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))      

    start_screen()
    game_running = True
    cooldown = 0
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
        
        show_text_on_screen(str(ball_speed), 30, height // 5)
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
        platform_pos1[0] = max(0, min(platform_pos1[0], width - platform_width1))
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]
        
        if (portal1_pos[0] - ball_radius <= ball_pos[0] <= portal1_pos[0] + portal1_width + ball_radius and portal1_pos[1] - ball_radius <= ball_pos[1] <= portal1_pos[1] + portal1_height + ball_radius) and cooldown == 0:
            ball_pos[0] = random.uniform(portal2_pos[0] - ball_radius, portal2_pos[0] + portal2_width + ball_radius)
            ball_pos[1] = random.uniform(portal2_pos[1] - ball_radius, portal2_pos[1] + portal2_height + ball_radius)
            cooldown = 15

        if (portal1_pos[0] - ball_radius - 2 <= 0):
            portal1_dir[0] = 0
            
        if (portal1_pos[0] + portal1_width + ball_radius + 2 >= width):
            portal1_dir[0] = 1
            
        if (portal1_pos[1] - ball_radius - 2 <= 0):
            portal1_dir[1] = 1
        
        if (portal1_pos[1] + portal1_height + ball_radius >= height):
            portal1_dir[1] = 0
        
        if (portal1_dir[0] == 0):
            portal1_pos[0] += portal_speed[0]
        else:
            portal1_pos[0] -= portal_speed[0]
            
        if (portal1_dir[1] == 1):
            portal1_pos[1] += portal_speed[1]
        else:
            portal1_pos[1] -= portal_speed[1]
        
        if (portal2_pos[0] - ball_radius <= ball_pos[0] <= portal2_pos[0] + portal2_width + ball_radius and portal2_pos[1] - ball_radius <= ball_pos[1] <= portal2_pos[1] + portal2_height + ball_radius) and cooldown == 0:
            ball_pos[0] = random.uniform(portal1_pos[0] - ball_radius, portal1_pos[0] + portal1_width + ball_radius)
            ball_pos[1] = random.uniform(portal1_pos[1] - ball_radius, portal1_pos[1] + portal1_height + ball_radius)
            cooldown = 15

        if (portal2_pos[0] - ball_radius - 2 <= 0):
            portal2_dir[0] = 1
            
        if (portal2_pos[0] + portal2_width + ball_radius + 2 >= width):
            portal2_dir[0] = 0
            
        if (portal2_pos[1] - ball_radius - 2 <= 0):
            portal2_dir[1] = 0
        
        if (portal2_pos[1] + portal2_height + ball_radius >= height):
            portal2_dir[1] = 1
        
        if (portal2_dir[0] == 1):
            portal2_pos[0] += portal_speed[0]
        else:
            portal2_pos[0] -= portal_speed[0]
            
        if (portal2_dir[1] == 0):
            portal2_pos[1] += portal_speed[1]
        else:
            portal2_pos[1] -= portal_speed[1]
        
        if ball_pos[0] - ball_radius - 5 <= 0 or ball_pos[0] + ball_radius + 5 >= width:
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

        if (platform_pos1[0] <= ball_pos[0] <= platform_pos1[0] + platform_width1 and platform_pos1[1] + 10 <= ball_pos[1] + ball_radius <= platform_pos1[1] + platform_height1):
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
            if platform_height1 <= 150:
                platform_height1 *= 1.15
            lives += 1
            platform_pos1 = [width // 2 - platform_width1 // 2, height - platform_height1 - 10]
            if platform_width1 < width // 2 - 1000:
                platform_width1 *= 1.25
                if (platform_height1 <= 150):
                    platform_height1 *= 1.05
            ball_pos = [width // 2, height // 2]
            platform_color = change_platform_color()
            ball_color = change_ball_color()

        if ball_pos[1] >= height:
            lives -= 1
            platform_pos1 = [width // 2 - platform_width1 // 2, height - platform_height1 - 10]
            if lives == 0:
                end_screen()
                main()
                score = 0
                lives = 3
                current_level = 1
            else:
                ball_pos = [width // 2, height // 2]
                if (ball_speed[1] > 0):
                    ball_speed[1] = -ball_speed[1]


        cooldown = max(cooldown - 1, 0)
        if score == 40:
            victory_screen()
            main()

        screen.fill(screen_color)
        
        pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
        pygame.draw.rect(screen, platform_color, (int(platform_pos1[0]), int(platform_pos1[1]) + 10, platform_width1, platform_height1))
        pygame.draw.rect(screen, red, (int(portal1_pos[0]), int(portal1_pos[1]), portal1_width, portal1_height))
        pygame.draw.rect(screen, orange, (int(portal2_pos[0]), int(portal2_pos[1]), portal2_width, portal2_height))
        
        info_line_y = 10
        info_spacing = 75
        score_text = font.render(f"Score: {score}", True, white)
        score_rect = score_text.get_rect(topleft = (10, info_line_y))
        pygame.draw.rect(screen, orange, score_rect.inflate(10, 5))
        screen.blit(score_text, score_rect)
        
        level_text = font.render(f"Level: {current_level}", True, white)
        level_rect = level_text.get_rect(topleft = (score_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, light_blue, level_rect.inflate(10, 5))
        screen.blit(level_text, level_rect)
        
        lives_text = font.render(f"Lives: {lives}", True, white)
        lives_rect = lives_text.get_rect(topleft = (level_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, red, lives_rect.inflate(10, 5))
        screen.blit(lives_text, lives_rect)
        
        speedx_text = font.render(f"x-Speed: {ball_speed[0]}", True, white)
        speedx_rect = speedx_text.get_rect(topleft = (lives_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, black, speedx_rect.inflate(10, 5))
        screen.blit(speedx_text, speedx_rect)
        
        speedy_text = font.render(f"y-Speed: {ball_speed[1]}", True, white)
        speedy_rect = speedy_text.get_rect(topleft = (speedx_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, black, speedy_rect.inflate(10, 5))
        screen.blit(speedy_text, speedy_rect)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
main()