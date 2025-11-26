import pygame
import sys
import random
import time
import requests
import threading

pygame.init()

developer = False

display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
# width, height = 1000, 1000
FPS = 60
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (200, 200, 200)
orange = (255, 165, 0)
light_blue = (173, 116, 233)


# --- POWER-UPS ---
power_up_duration = 5
power_up_spawn_interval = (5, 8)
power_up_size = (50, 50)

pu_platform_w_increase = "platform_w_increase"
pu_platform_w_decrease = "platform_w_decrease"
pu_ball_size_increase = "ball_size_increase"
pu_ball_size_decrease = "ball_size_decrease"
pu_ball_speed_increase = "ball_speed_increase"
pu_ball_speed_decrease = "ball_speed_decrease"
pu_portal_size_increase = "portal_size_increase"
pu_portal_size_decrease = "portal_size_decrease"
pu_spawn_extra_portals = "spawn_extra_portals"
pu_add_lives = "add_lives"

power_up_types = [
  pu_platform_w_increase, pu_platform_w_decrease, 
  pu_ball_size_increase, pu_ball_size_decrease, 
  pu_ball_speed_increase, pu_ball_speed_decrease, 
  pu_portal_size_increase, pu_portal_size_decrease, 
  pu_spawn_extra_portals, 
  pu_add_lives
]

screen = pygame.display.set_mode((width, height))
screen_color = black
pygame.display.set_caption('Bouncing Ball Game')
font = pygame.font.Font(None, 36)

API_BASE = "http://localhost:3000/api"

def submit_score(username, score):
  try:
    res = requests.post(f"{API_BASE}/score", json = {"username": username, "score": score})
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
  pygame.display.flip()
  threading.Thread(target = submit_score, args = ("e", final_score), daemon = True).start()
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

def random_power_up_type():
  weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  return random.choices(power_up_types, weights = weights, k = 1)[0]

def rand_spawn_pos():
  margin = 120
  return [
    random.randint(margin, width - margin - power_up_size[0]), 
    random.randint(margin, height - margin - power_up_size[1] - 200)
  ]


def main():
  pos = "pos"
  speed = "speed"
  colour = "colour"
  radius = "radius"
  size = "size"
  dir = "dir"

  if developer:
    platform_width, platform_height = width, 25
  else:
    platform_width, platform_height = 150, 20
  platform_pos = [width // 2 - platform_width // 2, height - platform_height - 10]
  platform_speed = 20
  platform_colour = orange

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

  # portal_speed = [3, 3]
  # portal1_width, portal1_height = 75, 75
  # portal1_pos = [200, 200]
  # portal1_dir = [0, 0]
  
  # portal2_width, portal2_height = portal1_width, portal1_height
  # portal2_pos = [width - 200, height - 250]
  # portal2_dir = [0, 0]

  portals = [
    {pos: [200, 200], size: [75, 75], dir: [0, 0], colour: red}, 
    {pos: [width - 200, height - 250], size: [75, 75], dir: [0, 0], colour: orange}
  ]
  
  portal_speed = [3, 3]
  
  power_ups = []
  next_spawn_time = time.time() + random.uniform(*power_up_spawn_interval)
  
  timed_effects = {
    "platform_width_multi_end": 0, 
    "ball_radius_multi_end": 0, 
    "ball_speed_multi_end": 0, 
    "portal_size_multi_end": 0
  }
  
  platform_width_multi = 1.0
  ball_radius_multi = 1.0
  ball_speed_multi = 1.0
  portal_size_multi = 1.0
  
  base_platform_width = platform_width
  min_platform_width = 80
  if developer:
    max_platform_width = width
  else:
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
      ppos = rand_spawn_pos()
      pcolour = change_ball_color()
      power_ups.append({
        pos: ppos, 
        size: [*power_up_size], 
        type: ptype, 
        colour: pcolour, 
        "type": ptype, 
        colour: pcolour, 
        "spawn_time": time.time(), 
        "lifetime": 6
      })
      next_spawn_time = time.time() + random.uniform(*power_up_spawn_interval)
    
    for b in balls:
      b[pos] += b[speed] * ball_radius_multi

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
        # ball_rect = pygame.Rect(b[pos].x - b[radius], b[pos].y - b[radius],
        #                         b[radius]*2, b[radius]*2)
        # portal1_rect = pygame.Rect(portal1_pos[0], portal1_pos[1], portal1_width, portal1_height)
        # portal2_rect = pygame.Rect(portal2_pos[0], portal2_pos[1], portal2_width, portal2_height)

        ball_rect = pygame.Rect(b[pos].x - int(b[radius] * ball_radius_multi), 
                                b[pos].y - int(b[radius] * ball_radius_multi), 
                                int(b[radius] * 2 * ball_radius_multi), 
                                int(b[radius]* 2 * ball_radius_multi))
        portal_rects = []
        for p in portals:
          w, h = int(p[size][0] * portal_size_multi), int(p[size][1] * portal_size_multi)
          portal_rects.append((p, pygame.Rect(int(p[pos][0]), int(p[pos][1]), w, h)))
        
        change_speed = random.uniform(0.90, 1.25)
        for idx, (p_from, rect_from) in enumerate(portal_rects):
          if rect_from.colliderect(ball_rect):
            if len(portal_rects) > 1:
              choices = [i for i in range(len(portal_rects)) if i != idx]
              exit_idx = random.choice(choices)
              p_to, rect_to = portal_rects[exit_idx]
              b[pos] = pygame.Vector2(rect_to.centerx, rect_to.top - int(b[radius] * ball_radius_multi) - 5)
              b["teleport_cooldown"] = 0.5
              b[speed].x *= change_speed
              b[speed].y *= change_speed
              break
        
        if b[pos].y >= height:
          lives -= 1
          b[pos] = pygame.Vector2(width // 2, height // 2)
          b[speed].x = random.choice([random.uniform(6, 7), random.uniform(-7, -6)])
          b[speed].y = random.uniform(-9, -7)
          if lives == 0:
            end_screen(score)
            return


    if score % 10 == 0 and score != 0 and last_level_up_score != score:
      last_level_up_score = score
      current_level += 1
      lives += 2
      if base_platform_width <= width // 2 and not developer:
        base_platform_width = min(base_platform_width, int(platform_width * 1.25))
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
    ball_rects = [pygame.Rect(int(b[pos].x - b[radius] * ball_radius_multi), 
                              int(b[pos].y - b[radius] * ball_radius_multi), 
                              int(b[radius] * 2 * ball_radius_multi), 
                              int(b[radius] * 2 * ball_radius_multi)) for b in balls]
    picked_indices = []
    active_notice = ""
    notice_end_time = 0
    
    for i, pu in enumerate(power_ups):
      pu_rect = pygame.Rect(pu[pos][0], pu[pos][1], pu[size][0], pu[size][1])
      if any(pu_rect.colliderect(bruh) for bruh in ball_rects):
        # Apply effect
        t_end = time.time() + power_up_duration
        if pu["type"] == pu_platform_w_increase:
          platform_width_multi *= 1.5
          timed_effects["platform_width_multi_end"] = t_end
        elif pu["type"] == pu_platform_w_decrease:
          platform_width_multi *= 0.8
          timed_effects["platform_width_multi_end"] = t_end

        elif pu["type"] == pu_ball_size_increase:
          ball_radius_multi *= 1.75
          timed_effects["ball_radius_multi_end"] = t_end
        elif pu["type"] == pu_ball_size_decrease:
          ball_radius_multi *= 0.8
          timed_effects["ball_radius_multi_end"] = t_end
        
        elif pu["type"] == pu_ball_speed_increase:
          ball_speed_multi *= 1.25
          timed_effects["ball_speed_multi_end"] = t_end
        elif pu["type"] == pu_ball_speed_decrease:
          ball_speed_multi *= 0.8
          timed_effects["ball_speed_multi_end"] = t_end
        
        elif pu["type"] == pu_portal_size_increase:
          portal_size_multi *= 1.5
          timed_effects["portal_size_multi_end"] = t_end
        elif pu["type"] == pu_portal_size_decrease:
          portal_size_multi *= 0.6
          timed_effects["portal_size_multi_end"] = t_end
        
        elif pu["type"] == pu_spawn_extra_portals:
          if len(portals) < 6:
            portals.append({
              pos: rand_spawn_pos(), 
              size: [75, 75], 
              dir: [random.choice([0, 1]), random.choice([0, 1])], 
              colour: change_platform_color()
            })
        
        elif pu["type"] == pu_add_lives:
          lives += int(random.uniform(1, 3))
        
        # --- NOTICE MESSAGE ---
        active_notice = f"{pu['type']} activated!"
        notice_end_time = time.time() + 3
        
        picked_indices.append(i)
        
    # Remove picked
    for idx in reversed(picked_indices):
      power_ups.pop(idx)

    now_t = time.time()
    power_ups = [pu for pu in power_ups if now_t - pu["spawn_time"] < pu["lifetime"]]
    
    if active_notice and time.time() < notice_end_time:
      notice_text = font.render(active_notice, True, white)
      notice_rect = notice_text.get_rect(center = (width // 2, height // 2))
      screen.blit(notice_text, notice_rect)
    else:
      active_notice = None
    
    # --- PORTAL MOVEMENT ---
    for p in portals:
      w, h = int(p[size][0] * portal_size_multi), int(p[size][1] * portal_size_multi)
      if p[pos][0] - 75 <= 0:
        p[dir][0] = 0
      if p[pos][0] + w + 75 >= width:
        p[dir][0] = 1
      
      if p[pos][1] - 75 <= 0:
        p[dir][1] = 1
      if p[pos][1] + h + 75 >= height:
        p[dir][1] = 0
      
      if p[dir][0] == 0:
        p[pos][0] += portal_speed[0]
      else:
        p[pos][0] -= portal_speed[0]

      if p[dir][1] == 1:
        p[pos][1] += portal_speed[1]
      else:
        p[pos][1] -= portal_speed[1]
    
    # --- TIMERS: revert multipliers ---
    if timed_effects["platform_width_multi_end"] and now_t > timed_effects["platform_width_multi_end"]:
      platform_width_multi = 1.0
      timed_effects["platform_width_multi_end"] = 0
    
    if timed_effects["ball_radius_multi_end"] and now_t > timed_effects["ball_radius_multi_end"]:
      ball_radius_multi = 1.0
      timed_effects["ball_radius_multi_end"] = 0
    
    if timed_effects["ball_speed_multi_end"] and now_t > timed_effects["ball_speed_multi_end"]:
      ball_speed_multi = 1.0
      timed_effects["ball_speed_multi_end"] = 0

    if timed_effects["portal_size_multi_end"] and now_t > timed_effects["portal_size_multi_end"]:
      portal_size_multi = 1.0
      timed_effects["portal_size_multi_end"] = 0

    platform_width_effective = int(base_platform_width * platform_width_multi)
    platform_width_effective = max(min_platform_width, min(max_platform_width, platform_width_effective))
    if not developer:
      platform_pos[0] = max(0, min(platform_pos[0], width - platform_width_effective))
    
    # draw everything
    screen.fill(screen_color)
    for b in balls:
      draw_radius = int(b[radius] * ball_radius_multi)
      pygame.draw.circle(screen, b[colour], (int(b[pos].x), int(b[pos].y)), draw_radius)
    
    pygame.draw.rect(screen, platform_colour, (int(platform_pos[0]), int(platform_pos[1]), platform_width_effective, platform_height))

    for p in portals:
      w, h = int(p[size][0] * portal_size_multi), int(p[size][1] * portal_size_multi)
      pygame.draw.rect(screen, p[colour], (int(p[pos][0]), int(p[pos][1]), w, h))
    
    for pu in power_ups:
      pygame.draw.rect(screen, pu[colour], (pu[pos][0], pu[pos][1], pu[size][0], pu[size][1]))
      label = font.render("E", True, black)
      screen.blit(label, (pu[pos][0] + 8, pu[pos][1] + 8))
    
    # HUD
    
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