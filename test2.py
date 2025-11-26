import pygame
import sys
import random
import time
import requests
import threading

pygame.init()

# Use actual display resolution
display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
FPS = 60
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

API_BASE = "http://localhost:3000/api"

def submit_score(username, score):
    try:
        res = requests.post(f"{API_BASE}/score", json={"username": username, "score": score})
        print("Score submitted:", res.json())
    except Exception as e:
        print("Error submitting score:", e)

def show_text_on_screen(text, font_size, y_position):
    font_local = pygame.font.Font(None, font_size)
    text_render = font_local.render(text, True, gray)
    text_rect = text_render.get_rect(center=(width // 2, y_position))
    screen.blit(text_render, text_rect)

def draw(text, font_size, y_position):
    font_local = pygame.font.Font(None, font_size)
    text_render = font_local.render(text, True, gray)
    text_rect = text_render.get_rect(center=(width // 2, y_position))
    screen.blit(text_render, text_rect)

def change_platform_color():
    return (random.randint(110, 255), random.randint(110, 255), random.randint(110, 255))

def change_ball_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# --- POWER-UPS ---
POWER_UP_DURATION = 8
POWER_UP_SPAWN_INTERVAL = (5, 12)
POWER_UP_SIZE = (40, 40)

PU_PLATFORM_W_INCR = "platform_w_incr"
PU_PLATFORM_W_DECR = "platform_w_decr"
PU_BALL_SIZE_INCR = "ball_size_incr"
PU_BALL_SIZE_DECR = "ball_size_decr"
PU_BALL_SPEED_INCR = "ball_speed_incr"
PU_BALL_SPEED_DECR = "ball_speed_decr"
PU_PORTAL_SIZE_INCR = "portal_size_incr"
PU_PORTAL_SIZE_DECR = "portal_size_decr"
PU_SPAWN_EXTRA_PORTALS = "spawn_extra_portals"

POWER_UP_TYPES = [
    PU_PLATFORM_W_INCR, PU_PLATFORM_W_DECR,
    PU_BALL_SIZE_INCR, PU_BALL_SIZE_DECR,
    PU_BALL_SPEED_INCR, PU_BALL_SPEED_DECR,
    PU_PORTAL_SIZE_INCR, PU_PORTAL_SIZE_DECR,
    PU_SPAWN_EXTRA_PORTALS
]

def random_power_up_type():
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 0.6]
    return random.choices(POWER_UP_TYPES, weights=weights, k=1)[0]

def rand_spawn_position():
    margin = 120
    return [
        random.randint(margin, width - margin - POWER_UP_SIZE[0]),
        random.randint(margin, height - margin - POWER_UP_SIZE[1] - 200)
    ]

def start_screen():
    start = True
    while start:
        screen.fill(black)
        show_text_on_screen("Bouncing Ball Game", 100, height // 4)
        show_text_on_screen("Press spacebar to start...", 50, height // 2)
        show_text_on_screen("Move the platform with arrow keys...", 65, height // 1.5)
        show_text_on_screen("Mission: Aim for the highest score!", 85, height // 1.2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False
                    cntdown()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def cntdown():
    screen.fill(black)
    cnt = ["3", "2", "1"]
    pygame.mouse.set_visible(0)
    for number in cnt:
        draw(number, 100, height // 2)
        pygame.display.flip()
        time.sleep(1)
        screen.fill(black)
    main()

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

def end_screen(final_score):
    screen.fill(black)
    show_text_on_screen("Good Try! :)", 100, height // 4)
    show_text_on_screen(f"Your final score: {final_score}", 50, height // 2)
    show_text_on_screen("Press spacebar to restart...", 45, height // 1.5)
    pygame.display.flip()
    threading.Thread(target = submit_score, args = ("e", final_score), daemon = True).start()
    wait_for_key()
    start_screen()

def main():
    pos = "pos"
    speed = "speed"
    colour = "colour"
    radius = "radius"

    platform_width, platform_height = 150, 20
    platform_pos = [width // 2 - platform_width // 2, height - platform_height - 10]
    platform_speed = 20
    platform_color = orange

    balls = [{
        pos: pygame.Vector2(width // 2, height // 2),
        speed: pygame.Vector2(random.choice([random.uniform(6, 8), random.uniform(-8, -6)]),
                              random.uniform(-7, -6)),
        colour: white,
        radius: 30,
        "teleport_cooldown": 0
    }]
    
    max_v = 10

    score = 0
    lives = 3
    current_level = 1
    last_level_up_score = 0

    portals = [
        {"pos": [200, 200], "size": [75, 75], "dir": [0, 0], "color": red},
        {"pos": [width - 200, height - 250], "size": [75, 75], "dir": [0, 0], "color": orange}
    ]
    portal_speed = [3, 3]

    power_ups = []
    next_spawn_time = time.time() + random.uniform(*POWER_UP_SPAWN_INTERVAL)

    timed_effects = {
        "platform_width_mult_end": 0,
        "ball_radius_mult_end": 0,
        "ball_speed_mult_end": 0,
        "portal_size_mult_end": 0
    }
    platform_width_mult = 1.0
    ball_radius_mult = 1.0
    ball_speed_mult = 1.0
    portal_size_mult = 1.0

    base_platform_width = platform_width
    min_platform_width = 80
    max_platform_width = width // 2

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
                elif event.key == pygame.K_LSHIFT:
                    game_running = False
                    start_screen()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            platform_pos[0] += platform_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            platform_pos[0] -= platform_speed

        # Power-up spawn
        if time.time() >= next_spawn_time and len(power_ups) < 3:
            ptype = random_power_up_type()
            ppos = rand_spawn_position()
            pcolor = change_platform_color()
            power_ups.append({
                "pos": ppos,
                "size": [*POWER_UP_SIZE],
                "type": ptype,
                "color": pcolor,
                "spawn_time": time.time(),
                "lifetime": 6
            })
            next_spawn_time = time.time() + random.uniform(*POWER_UP_SPAWN_INTERVAL)

        # Ball updates
        for b in balls:
            b[pos] += b[speed] * ball_speed_mult

            b[speed].x = min(max_v, b[speed].x)
            b[speed].y = min(max_v, b[speed].y)
            
            if b[pos].x - b[radius] <= 0 or b[pos].x + b[radius] >= width:
                b[speed].x = -b[speed].x * 1.05
                b[colour] = change_ball_color()

            if b[pos].y - b[radius] <= 0:
                b[speed].y = -b[speed].y * 1.05
                b[colour] = change_ball_color()

            if (platform_pos[0] <= b[pos].x <= platform_pos[0] + int(base_platform_width * platform_width_mult) and
                platform_pos[1] <= b[pos].y + int(b[radius]*ball_radius_mult) <= platform_pos[1] + platform_height):
                b[pos].y = platform_pos[1] - int(b[radius]*ball_radius_mult)
                b[speed].y = -abs(b[speed].y)
                score += 1
                b[colour] = change_ball_color()

            # Teleport cooldown
            if b["teleport_cooldown"] > 0:
                b["teleport_cooldown"] -= 1/FPS
            else:
                ball_rect = pygame.Rect(b[pos].x - int(b[radius]*ball_radius_mult),
                                        b[pos].y - int(b[radius]*ball_radius_mult),
                                        int(b[radius]*2*ball_radius_mult),
                                        int(b[radius]*2*ball_radius_mult))
                portal_rects = []
                for p in portals:
                    w = int(p["size"][0] * portal_size_mult)
                    h = int(p["size"][1] * portal_size_mult)
                    portal_rects.append((p, pygame.Rect(int(p["pos"][0]), int(p["pos"][1]), w, h)))

                change_speed = random.uniform(0.75, 1.15)
                for idx, (p_from, rect_from) in enumerate(portal_rects):
                    if rect_from.colliderect(ball_rect):
                        if len(portal_rects) > 1:
                            choices = [i for i in range(len(portal_rects)) if i != idx]
                            exit_idx = random.choice(choices)
                            p_to, rect_to = portal_rects[exit_idx]
                            b[pos] = pygame.Vector2(rect_to.centerx,
                                                    rect_to.top - int(b[radius]*ball_radius_mult) - 5)
                            b["teleport_cooldown"] = 0.5
                            b[speed].x *= change_speed
                            b[speed].y *= change_speed
                            break

            if b[pos].y >= height:
                lives -= 1
                b[pos] = pygame.Vector2(width // 2, height // 2)
                b[speed].y = random.uniform(-9, -7)
                b[speed].x = random.choice([random.uniform(6, 7), random.uniform(-7, -6)])
                if lives == 0:
                    end_screen(score)
                    return

        # --- BALL SPLITTING EVERY 10 POINTS ---
        if score % 10 == 0 and score != 0 and last_level_up_score != score:
            last_level_up_score = score
            current_level += 1
            lives += 2
            if base_platform_width <= width // 2:
                base_platform_width = min(base_platform_width, int(base_platform_width * 1.25))
            if len(balls) <= 9:
                balls.append({
                    pos: pygame.Vector2(width // 2, height // 2),
                    speed: pygame.Vector2(random.choice([random.uniform(6, 7), random.uniform(-7, -6)]),
                                          random.uniform(-9, -7)),
                    colour: change_ball_color(),
                    radius: 30,
                    "teleport_cooldown": 0
                })

        # --- POWER-UP PICKUP & EXPIRATION ---
        ball_rects = [pygame.Rect(int(b[pos].x - b[radius]*ball_radius_mult),
                                  int(b[pos].y - b[radius]*ball_radius_mult),
                                  int(b[radius]*2*ball_radius_mult),
                                  int(b[radius]*2*ball_radius_mult)) for b in balls]
        picked_indices = []
        for i, pu in enumerate(power_ups):
            pu_rect = pygame.Rect(pu["pos"][0], pu["pos"][1], pu["size"][0], pu["size"][1])
            if any(pu_rect.colliderect(br) for br in ball_rects):
                # Apply effect
                t_end = time.time() + POWER_UP_DURATION
                if pu["type"] == PU_PLATFORM_W_INCR:
                    platform_width_mult *= 1.25
                    timed_effects["platform_width_mult_end"] = t_end
                elif pu["type"] == PU_PLATFORM_W_DECR:
                    platform_width_mult *= 0.8
                    timed_effects["platform_width_mult_end"] = t_end
                elif pu["type"] == PU_BALL_SIZE_INCR:
                    ball_radius_mult *= 1.25
                    timed_effects["ball_radius_mult_end"] = t_end
                elif pu["type"] == PU_BALL_SIZE_DECR:
                    ball_radius_mult *= 0.8
                    timed_effects["ball_radius_mult_end"] = t_end
                elif pu["type"] == PU_BALL_SPEED_INCR:
                    ball_speed_mult *= 1.25
                    timed_effects["ball_speed_mult_end"] = t_end
                elif pu["type"] == PU_BALL_SPEED_DECR:
                    ball_speed_mult *= 0.8
                    timed_effects["ball_speed_mult_end"] = t_end
                elif pu["type"] == PU_PORTAL_SIZE_INCR:
                    portal_size_mult *= 1.2
                    timed_effects["portal_size_mult_end"] = t_end
                elif pu["type"] == PU_PORTAL_SIZE_DECR:
                    portal_size_mult *= 0.85
                    timed_effects["portal_size_mult_end"] = t_end
                elif pu["type"] == PU_SPAWN_EXTRA_PORTALS:
                    if len(portals) < 6:
                        portals.append({
                            "pos": rand_spawn_position(),
                            "size": [75, 75],
                            "dir": [random.choice([0,1]), random.choice([0,1])],
                            "color": change_platform_color()
                        })

                # --- NOTICE MESSAGE CENTERED ---
                notice_text = font.render(f"{pu['type']} activated!", True, white)
                notice_rect = notice_text.get_rect(center=(width // 2, height // 2))
                screen.blit(notice_text, notice_rect)
                pygame.display.flip()
                # time.sleep(1)

                picked_indices.append(i)

        # Remove picked
        for idx in reversed(picked_indices):
            power_ups.pop(idx)

        # Remove expired
        now_t = time.time()
        power_ups = [pu for pu in power_ups if now_t - pu["spawn_time"] < pu["lifetime"]]

        # --- PORTAL MOVEMENT ---
        for p in portals:
            w = int(p["size"][0] * portal_size_mult)
            h = int(p["size"][1] * portal_size_mult)
            if p["pos"][0] - 75 <= 0:
                p["dir"][0] = 0
            if p["pos"][0] + w + 75 >= width:
                p["dir"][0] = 1
            if p["pos"][1] - 75 <= 0:
                p["dir"][1] = 1
            if p["pos"][1] + h + 175 >= height:
                p["dir"][1] = 0

            if p["dir"][0] == 0:
                p["pos"][0] += portal_speed[0]
            else:
                p["pos"][0] -= portal_speed[0]

            if p["dir"][1] == 1:
                p["pos"][1] += portal_speed[1]
            else:
                p["pos"][1] -= portal_speed[1]

        # --- TIMERS: revert multipliers ---
        if timed_effects["platform_width_mult_end"] and now_t > timed_effects["platform_width_mult_end"]:
            platform_width_mult = 1.0
            timed_effects["platform_width_mult_end"] = 0
        if timed_effects["ball_radius_mult_end"] and now_t > timed_effects["ball_radius_mult_end"]:
            ball_radius_mult = 1.0
            timed_effects["ball_radius_mult_end"] = 0
        if timed_effects["ball_speed_mult_end"] and now_t > timed_effects["ball_speed_mult_end"]:
            ball_speed_mult = 1.0
            timed_effects["ball_speed_mult_end"] = 0
        if timed_effects["portal_size_mult_end"] and now_t > timed_effects["portal_size_mult_end"]:
            portal_size_mult = 1.0
            timed_effects["portal_size_mult_end"] = 0

        platform_width_effective = int(base_platform_width * platform_width_mult)
        platform_width_effective = max(min_platform_width, min(max_platform_width, platform_width_effective))
        platform_pos[0] = max(0, min(platform_pos[0], width - platform_width_effective))

        # --- DRAW ---
        screen.fill(screen_color)

        for b in balls:
            draw_radius = int(b[radius] * ball_radius_mult)
            pygame.draw.circle(screen, b[colour], (int(b[pos].x), int(b[pos].y)), draw_radius)

        pygame.draw.rect(screen, platform_color,
                         (int(platform_pos[0]), int(platform_pos[1]), platform_width_effective, platform_height))

        for p in portals:
            w = int(p["size"][0] * portal_size_mult)
            h = int(p["size"][1] * portal_size_mult)
            pygame.draw.rect(screen, p["color"], (int(p["pos"][0]), int(p["pos"][1]), w, h))

        for pu in power_ups:
            pygame.draw.rect(screen, pu["color"], (pu["pos"][0], pu["pos"][1], pu["size"][0], pu["size"][1]))
            label = font.render("EEE", True, black)
            screen.blit(label, (pu["pos"][0] + 8, pu["pos"][1] + 8))

        # HUD
        score_text = font.render(f"Score: {score}", True, white)
        score_rect = score_text.get_rect(topleft=(10, 10))
        pygame.draw.rect(screen, orange, score_rect.inflate(10, 5))
        screen.blit(score_text, score_rect)

        level_text = font.render(f"Level: {current_level}", True, white)
        level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + 75, 10))
        pygame.draw.rect(screen, light_blue, level_rect.inflate(10, 5))
        screen.blit(level_text, level_rect)

        lives_text = font.render(f"Lives: {lives}", True, white)
        lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + 75, 10))
        pygame.draw.rect(screen, red, lives_rect.inflate(10, 5))
        screen.blit(lives_text, lives_rect)

        # Show active effects summary
        # effect_msgs = []
        # if platform_width_mult != 1.0: effect_msgs.append(f"Plat W x{platform_width_mult:.2f}")
        # if ball_radius_mult != 1.0: effect_msgs.append(f"Ball R x{ball_radius_mult:.2f}")
        # if ball_speed_mult != 1.0: effect_msgs.append(f"Ball V x{ball_speed_mult:.2f}")
        # if portal_size_mult != 1.0: effect_msgs.append(f"Portal x{portal_size_mult:.2f}")
        # if effect_msgs:
        #     eff_text = font.render(" | ".join(effect_msgs), True, white)
        #     eff_rect = eff_text.get_rect(center=(width // 2, 50))  # centered near top
        #     pygame.draw.rect(screen, gray, eff_rect.inflate(10, 5))
        #     screen.blit(eff_text, eff_rect)

        pygame.display.flip()
        clock.tick(FPS)

# --- START GAME ---
start_screen()
pygame.display.flip()
