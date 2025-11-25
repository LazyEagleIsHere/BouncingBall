import pygame
import sys
import random
import time
import requests

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
  submit_score("e", final_score)
  pygame.display.flip()
  submit_score("e", final_score)
  wait_for_key()
  start_screen()

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

def main():
  pos = "pos"
  speed = "speed"
  colour = "colour"
  radius = "radius"

  # platform_width, platform_height = width, 100
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
  max_v = 9
  
  score = 0
  lives = 3
  current_level = 1
  last_level_up_score = 0

  portal_speed = [3, 3]
  portal1_width, portal1_height = 75, 75
  portal1_pos = [200, 200]
  portal1_dir = [0, 0]
  
  portal2_width, portal2_height = portal1_width, portal1_height
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
        elif event.key == pygame.K_LSHIFT:
          game_running = False
          start_screen()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      platform_pos[0] += platform_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      platform_pos[0] -= platform_speed
    platform_pos[0] = max(0, min(platform_pos[0], width - platform_width))

    for b in balls:
      b[pos] += b[speed]

      if b[pos].x - b[radius] <= 0 or b[pos].x + b[radius] >= width:
        b[speed].x = -b[speed].x * 1.05
        b[colour] = change_ball_color()

      if b[pos].y - b[radius] <= 0:
        b[speed].y = -b[speed].y * 1.05
        b[colour] = change_ball_color()

      if b[speed].x > max_v:
        b[speed].x = max_v
      elif b[speed].x < -max_v:
        b[speed].x = -max_v
      
      if b[speed].y > max_v:
        b[speed].y = max_v
      elif b[speed].y < -max_v:
        b[speed].y = -max_v
      
      if (platform_pos[0] <= b[pos].x <= platform_pos[0] + platform_width and
          platform_pos[1] <= b[pos].y + b[radius] <= platform_pos[1] + platform_height):
        b[pos].y = platform_pos[1] - b[radius]
        b[speed].y = -abs(b[speed].y)
        score += 1
        b[colour] = change_ball_color()

      # --- PORTAL COLLISION WITH COOLDOWN ---
      if b["teleport_cooldown"] > 0:
        b["teleport_cooldown"] -= 1/FPS
      else:
        ball_rect = pygame.Rect(b[pos].x - b[radius], b[pos].y - b[radius],
                                b[radius]*2, b[radius]*2)
        portal1_rect = pygame.Rect(portal1_pos[0], portal1_pos[1], portal1_width, portal1_height)
        portal2_rect = pygame.Rect(portal2_pos[0], portal2_pos[1], portal2_width, portal2_height)

        change_speed = random.uniform(0.75, 1.55)
        
        if portal1_rect.colliderect(ball_rect):
          b[pos] = pygame.Vector2(portal2_rect.centerx, portal2_rect.top - b[radius] - 5)
          b["teleport_cooldown"] = 0.5
          b[speed].x *= change_speed
          b[speed].y *= change_speed

        elif portal2_rect.colliderect(ball_rect):
          b[pos] = pygame.Vector2(portal1_rect.centerx, portal1_rect.top - b[radius] - 5)
          b["teleport_cooldown"] = 0.5
          b[speed].x *= change_speed
          b[speed].y *= change_speed
      # --- END PORTAL COLLISION ---

      if b[pos].y >= height:
        lives -= 1
        b[pos] = pygame.Vector2(width // 2, height // 2)
        b[speed].y = random.uniform(-9, -7)
        b[speed].x = random.choice([random.uniform(6, 7), random.uniform(-7, -6)])
        
        if lives == 0:
          end_screen(score)
          return

    if score % 10 == 0 and score != 0 and last_level_up_score != score:
      last_level_up_score = score
      current_level += 1
      lives += 2
      if platform_width <= width // 2:
        platform_width = min(platform_width, platform_width * 1.25)
      if len(balls) <= 9:
        balls.append({
          pos: pygame.Vector2(width // 2, height // 2),
          speed: pygame.Vector2(random.choice([random.uniform(6, 7), random.uniform(-7, -6)]),
                            random.uniform(-9, -7)),
          colour: change_ball_color(),
          radius: 30,
          "teleport_cooldown": 0
        })

    # portal movement logic (unchanged)
    if (portal1_pos[0] - 75 <= 0):
      portal1_dir[0] = 0
    if (portal1_pos[0] + portal1_width + 75 >= width):
      portal1_dir[0] = 1
    if (portal1_pos[1] - 75 <= 0):
      portal1_dir[1] = 1
    if (portal1_pos[1] + portal1_height + 175 >= height):
      portal1_dir[1] = 0

    if (portal1_dir[0] == 0):
      portal1_pos[0] += portal_speed[0]
    else:
      portal1_pos[0] -= portal_speed[0]

    if (portal1_dir[1] == 1):
      portal1_pos[1] += portal_speed[1]
    else:
      portal1_pos[1] -= portal_speed[1]

    if (portal2_pos[0] - 75 <= 0):
      portal2_dir[0] = 1
    if (portal2_pos[0] + portal2_width + 75 >= width):
      portal2_dir[0] = 0
    if (portal2_pos[1] - 75 <= 0):
      portal2_dir[1] = 0
    if (portal2_pos[1] + portal2_height + 175 >= height):
      portal2_dir[1] = 1

    if (portal2_dir[0] == 1):
      portal2_pos[0] += portal_speed[0]
    else:
      portal2_pos[0] -= portal_speed[0]

    if (portal2_dir[1] == 0):
      portal2_pos[1] += portal_speed[1]
    else:
      portal2_pos[1] -= portal_speed[1]

    # draw everything
    screen.fill(screen_color)
    for b in balls:
      pygame.draw.circle(screen, b[colour], (int(b[pos].x), int(b[pos].y)), b[radius])
    pygame.draw.rect(screen, platform_color,
                     (int(platform_pos[0]), int(platform_pos[1]), platform_width, platform_height))
    pygame.draw.rect(screen, red,
                     (int(portal1_pos[0]), int(portal1_pos[1]), portal1_width, portal1_height))
    pygame.draw.rect(screen, orange,
                     (int(portal2_pos[0]), int(portal2_pos[1]), portal2_width, portal2_height))

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

start_screen()
pygame.display.flip()