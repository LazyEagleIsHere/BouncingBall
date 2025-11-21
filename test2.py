import pygame
import sys
import random
import time
import requests
import socket

pygame.init()

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

def show_text_on_screen(text, font_size, y_position):
  font_local = pygame.font.Font(None, font_size)
  text_render = font_local.render(text, True, gray)
  text_rect = text_render.get_rect(center=(width // 2, y_position))
  screen.blit(text_render, text_rect)

def start_screen():
  start = True
  while start:
    screen.fill(black)
    show_text_on_screen("Bouncing Ball Game", 100, height // 4)
    show_text_on_screen("Press spacebar to start...", 50, height // 2)
    show_text_on_screen("Move the platform with arrow keys...", 65, height // 1.5)
    show_text_on_screen("Mission: Try your best to aim for as high a score as possible", 85, height // 1.2)
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

def draw(text, font_size, y_position):
  font_local = pygame.font.Font(None, font_size)
  text_render = font_local.render(text, True, gray)
  text_rect = text_render.get_rect(center=(width // 2, y_position))
  screen.blit(text_render, text_rect)

def cntdown():
  screen.fill(black)
  cnt = ["3", "2", "1"]
  pygame.mouse.set_visible(0)
  for number in cnt:
    draw(number, 100, height // 2)
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
    time.sleep(1)
    screen.fill(black)

def rainbow_color(value, background_colour=125):
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
  wait_for_key()

def victory_screen():
  win = True
  while win:
    screen.fill(black)
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

def change_platform_color():
  return (random.randint(110, 255), random.randint(110, 255), random.randint(110, 255))

def change_ball_color():
  return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def submit_score(score, level=None):
  try:
    payload = {"score": int(score), "level": level}
    # requests.post("http://YOUR_SERVER_HOST:8000/api/submit-score", json=payload, timeout=3)
  except Exception as e:
    print("Score submit failed:", e)

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
    pos: [width // 2, height // 2],
    speed: [random.choice([random.uniform(3, 5), random.uniform(-5, -3)]),
            random.uniform(-5, -3)],  # start upward
    colour: white,
    radius: 30,
    "teleport_cooldown": 0
  }]

  score = 0
  lives = 3
  current_level = 1
  last_level_up_score = 0
  background_colour = 125

  portal_speed = [3, 3]
  portal1_width, portal1_height = 100, 100
  portal1_pos = [200, 200]
  portal1_dir = [0, 0]
  portal2_width, portal2_height = 100, 100
  portal2_pos = [width - 200, height - 250]
  portal2_dir = [0, 0]

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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      platform_pos[0] += platform_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      platform_pos[0] -= platform_speed
    platform_pos[0] = max(0, min(platform_pos[0], width - platform_width))

    for b in balls:
      if b.get("teleport_cooldown", 0) > 0:
        b["teleport_cooldown"] -= 1

      b[pos][0] += b[speed][0]
      b[pos][1] += b[speed][1]

      if b[pos][0] - b[radius] <= 0 or b[pos][0] + b[radius] >= width:
        b[speed][0] = -b[speed][0] * 1.05
        b[colour] = change_ball_color()

      if b[pos][1] - b[radius] <= 0:
        b[speed][1] = -b[speed][1] * 1.05
        b[colour] = change_ball_color()

      if (platform_pos[0] <= b[pos][0] <= platform_pos[0] + platform_width and
          platform_pos[1] <= b[pos][1] + b[radius] <= platform_pos[1] + platform_height):
        b[speed][1] = -b[speed][1]
        score += 1
        b[colour] = change_ball_color()

      in_portal1 = (portal1_pos[0] - b[radius] <= b[pos][0] <= portal1_pos[0] + portal1_width + b[radius] and
                    portal1_pos[1] - b[radius] <= b[pos][1] <= portal1_pos[1] + portal1_height + b[radius])
      in_portal2 = (portal2_pos[0] - b[radius] <= b[pos][0] <= portal2_pos[0] + portal2_width + b[radius] and
                    portal2_pos[1] - b[radius] <= b[pos][1] <= portal2_pos[1] + portal2_height + b[radius])

      if in_portal1 and b.get("teleport_cooldown", 0) == 0:
        b[pos][0] = random.uniform(portal2_pos[0] - b[radius], portal2_pos[0] + portal2_width + b[radius])
        b[pos][1] = random.uniform(portal2_pos[1] - b[radius], portal2_pos[1] + portal2_height + b[radius])
        b["teleport_cooldown"] = 15

      if in_portal2 and b.get("teleport_cooldown", 0) == 0:
        b[pos][0] = random.uniform(portal1_pos[0] - b[radius], portal1_pos[0] + portal1_width + b[radius])
        b[pos][1] = random.uniform(portal1_pos[1] - b[radius], portal1_pos[1] + portal1_height + b[radius])
        b["teleport_cooldown"] = 15

      if b[pos][1] >= height:
        lives -= 1
        b[pos] = [width // 2, height // 2]
        b[speed][1] = random.uniform(-5, -3)
        b[speed][0] = random.choice([random.uniform(3, 5), random.uniform(-5, -3)])
        if lives == 0:
          submit_score(score, current_level)
          end_screen(score)
          return

    if score % 5 == 0 and score != 0 and last_level_up_score != score:
      last_level_up_score = score
      current_level += 1
      lives += 2
      balls.append({
        pos: [width // 2, height // 2],
        speed: [random.choice([random.uniform(3, 5), random.uniform(-5, -3)]),
                random.uniform(-5, -3)],
        colour: change_ball_color(),
        radius: 30,
        "teleport_cooldown": 0
      })

    if (portal1_pos[0] - 2 <= 0):
      portal1_dir[0] = 0
    if (portal1_pos[0] + portal1_width + 2 >= width):
      portal1_dir[0] = 1
    if (portal1_pos[1] - 2 <= 0):
      portal1_dir[1] = 1
    if (portal1_pos[1] + portal1_height >= height):
      portal1_dir[1] = 0
    if (portal1_dir[0] == 0):
      portal1_pos[0] += portal_speed[0]
    else:
      portal1_pos[0] -= portal_speed[0]
    if (portal1_dir[1] == 1):
      portal1_pos[1] += portal_speed[1]
    else:
      portal1_pos[1] -= portal_speed[1]

    if (portal2_pos[0] - 2 <= 0):
      portal2_dir[0] = 1
    if (portal2_pos[0] + portal2_width + 2 >= width):
      portal2_dir[0] = 0
    if (portal2_pos[1] - 2 <= 0):
      portal2_dir[1] = 0
    if (portal2_pos[1] + portal2_height >= height):
      portal2_dir[1] = 1
    if (portal2_dir[0] == 1):
      portal2_pos[0] += portal_speed[0]
    else:
      portal2_pos[0] -= portal_speed[0]
    if (portal2_dir[1] == 0):
      portal2_pos[1] += portal_speed[1]
    else:
      portal2_pos[1] -= portal_speed[1]

    screen.fill(screen_color)
    for b in balls:
      pygame.draw.circle(screen, b[colour], (int(b[pos][0]), int(b[pos][1])), b[radius])
    pygame.draw.rect(screen, platform_color, (int(platform_pos[0]), int(platform_pos[1]), platform_width, platform_height))
    pygame.draw.rect(screen, red, (int(portal1_pos[0]), int(portal1_pos[1]), portal1_width, portal1_height))
    pygame.draw.rect(screen, orange, (int(portal2_pos[0]), int(portal2_pos[1]), portal2_width, portal2_height))

    info_line_y = 10
    info_spacing = 75

    score_text = font.render(f"Score: {score}", True, white)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, orange, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    level_text = font.render(f"Level: {current_level}", True, white)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, light_blue, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    lives_text = font.render(f"Lives: {lives}", True, white)
    lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, red, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)

    pygame.display.flip()
    clock.tick(FPS)

if __name__ == "__main__":
  while True:
    start_screen()   # show intro
    cntdown()        # 3-2-1
    main()           # run one round, returns on game over
