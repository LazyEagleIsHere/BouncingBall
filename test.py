import pygame
import sys
import random
import time
import requests

pygame.init()

def main():
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    FPS = 60
    clock = pygame.time.Clock()

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    orange = (255, 165, 0)
    light_blue = (173, 116, 233)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Bouncing Ball Game')
    font = pygame.font.Font(None, 36)

    # Platform
    platform_width, platform_height = 150, 20
    platform_pos = [width // 2 - platform_width // 2, height - platform_height - 10]
    platform_speed = 20
    platform_color = orange

    # Balls list
    balls = [{
        "pos": [width // 2, height // 2],
        "speed": [random.choice([-6, 6]), random.choice([-6, 6])],
        "color": white,
        "radius": 30
    }]

    score = 0
    lives = 3
    current_level = 1

    def change_color():
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def show_text(text, font_size, y_position, color=white):
        font = pygame.font.Font(None, font_size)
        text_render = font.render(text, True, color)
        text_rect = text_render.get_rect(center=(width // 2, y_position))
        screen.blit(text_render, text_rect)

    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Move platform
        keys = pygame.key.get_pressed()
        platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
        platform_pos[0] = max(0, min(platform_pos[0], width - platform_width))

        # Update balls
        for ball in balls:
            ball["pos"][0] += ball["speed"][0]
            ball["pos"][1] += ball["speed"][1]

            # Bounce walls
            if ball["pos"][0] - ball["radius"] <= 0 or ball["pos"][0] + ball["radius"] >= width:
                ball["speed"][0] = -ball["speed"][0]
                ball["color"] = change_color()
            if ball["pos"][1] - ball["radius"] <= 0:
                ball["speed"][1] = -ball["speed"][1]
                ball["color"] = change_color()

            # Platform collision
            if (platform_pos[0] <= ball["pos"][0] <= platform_pos[0] + platform_width and
                platform_pos[1] <= ball["pos"][1] + ball["radius"] <= platform_pos[1] + platform_height):
                ball["speed"][1] = -ball["speed"][1]
                score += 1
                ball["color"] = change_color()

                # Level up every 5 points
                if score % 5 == 0:
                    current_level += 1
                    lives += 1
                    # Add a new ball
                    balls.append({
                        "pos": [width // 2, height // 2],
                        "speed": [random.choice([-6, 6]), random.choice([-6, 6])],
                        "color": change_color(),
                        "radius": 30
                    })

            # Missed ball
            if ball["pos"][1] >= height:
                lives -= 1
                ball["pos"] = [width // 2, height // 2]
                ball["speed"][1] = -abs(ball["speed"][1])
                if lives == 0:
                    game_running = False

        # Draw everything
        screen.fill(black)
        pygame.draw.rect(screen, platform_color, (platform_pos[0], platform_pos[1], platform_width, platform_height))
        for ball in balls:
            pygame.draw.circle(screen, ball["color"], (int(ball["pos"][0]), int(ball["pos"][1])), ball["radius"])

        # HUD
        score_text = font.render(f"Score: {score}", True, white)
        level_text = font.render(f"Level: {current_level}", True, white)
        lives_text = font.render(f"Lives: {lives}", True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (150, 10))
        screen.blit(lives_text, (300, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()
