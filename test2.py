import pygame
import sys
import random
import time
import requests
import socket

pygame.init()

display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
# width, height = 500, 500
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

# # platform_width, platform_height = width, height // 2 - 50
# platform_width, platform_height = 150, 20
# platform_pos = [width // 2 - platform_width // 2, height - platform_height - 10]
# platform_speed = 20
# platform_color = orange

# # ball[radius] = 30
# # ball_color = white
# # ball[pos] = [width // 2, height // 2]
# # ball_speed = [random.uniform(random.uniform(3, 5), random.uniform(-3, -5)), random.uniform(-3, -5)]

# pos = "pos"
# speed = "speed"
# colour = "colour"
# radius = "radius"
# balls = [{
#   pos: [width // 2, height // 2], 
#   speed: [random.uniform(random.uniform(3, 5), random.uniform(-3, -5)), -abs(random.uniform(-3, -5))], 
#   colour: white, 
#   radius: 30
# }]

# score = 0
# lives = 3
# current_level = 1
# background_colour = 125

# portal_speed = [3, 3]

# portal1_width, portal1_height = 100, 100
# portal1_pos = [200, 200]
# portal1_dir = [0, 0]

# portal2_width, portal2_height = 100, 100
# portal2_pos = [width - 200, height - 250]
# portal2_dir = [0, 0]

# def submit_score(score, level = None):
#   try:
#     payload = {
#       "score": int(score), 
#       "level": level, 
#     }
#     requests.post("http://YOUR_SERVER_HOST:8000/api/submit-score", json=payload, timeout=3)
#     # requests.post("http://127.0.0.1:5500/index.html", json=payload, timeout=3)
  
#   except Exception as e:
#     print("Score submit failed:", e)

def start_screen():
  # i = 0
  start = True
  while start:
    # screen.fill(rainbow_color(i))
    # i = (i + 1) % ((background_colour + 1) * 6)

    screen.fill(black)
    
    show_text_on_screen("Bouncing Ball Game", 100, height // 4)
    show_text_on_screen("Press spacebar to start...", 50, height // 2)
    show_text_on_screen("Move the platform with arrow keys...", 65, height // 1.5)
    # show_text_on_screen("Your mission is to get 40 points", 100, height // 1.2)
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

def draw(text, font_size, y_position):
  font = pygame.font.Font(None, font_size)
  text_render = font.render(text, True, gray)
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
  
  main()

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
  # i = 0
  while win:
    # screen.fill(rainbow_color(i))
    # i = (i + 1) % ((background_colour + 1) * 6)

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
          cntdown()
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

def main():
  global platform_speed, platform_height, platform_width, platform_pos, score, lives, current_level, background_colour

  # platform_width, platform_height = width, height // 2 - 50
  platform_width, platform_height = 150, 20
  platform_pos = [width // 2 - platform_width // 2, height - platform_height - 10]
  platform_speed = 20
  platform_color = orange

  # ball[radius] = 30
  # ball_color = white
  # ball[pos] = [width // 2, height // 2]
  # ball_speed = [random.uniform(random.uniform(3, 5), random.uniform(-3, -5)), random.uniform(-3, -5)]

  pos = "pos"
  speed = "speed"
  colour = "colour"
  radius = "radius"
  balls = [{
    pos: [width // 2, height // 2], 
    speed: [random.choice([random.uniform(3, 5), random.uniform(-5, -3)]), random.uniform(-5, -3)], 
    colour: white, 
    radius: 30
  }]

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

  game_running = True
  screen.fill(black)
  while game_running:
    keys = pygame.key.get_pressed()
    platform_pos[0] += ((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed) - ((keys[pygame.K_a] - keys[pygame.K_d]) * platform_speed)
    if keys[pygame.K_RIGHT] and keys[pygame.K_d]:
      platform_pos[0] -= (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
    if keys[pygame.K_LEFT] and keys[pygame.K_a]:
      platform_pos[0] -= (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
    platform_pos[0] = max(0, min(platform_pos[0], width - platform_width))
    
    for ball in balls:
      ball[pos][0] += ball[speed][0]
      ball[pos][1] += ball[speed][1]
      
      # hit walls
      if ball[pos][0] - ball[radius] <= 0 or ball[pos][0] + ball[radius] >= width:
        ball[speed][0] = -ball[speed][0] * 1.05
        ball[colour] = change_ball_color()
      
      if ball[pos][1] - ball[radius] <= 0:
        ball[speed][1] = -ball[speed][1] * 1.05
        ball[colour] = change_ball_color()
      
      # hit platform
      if (platform_pos[0] <= ball[pos][0] <= platform_pos[0] + platform_width and
          platform_pos[1] <= ball[pos][1] + ball[radius] <= platform_pos[1] + platform_height):
        ball[speed][1] = -ball[speed][1]
        score += 1
        ball[colour] = change_ball_color()
        
      if score % 5 == 0 and score != 0:
        current_level += 1
        lives += 2
        balls.append({
          pos: [width // 2, height // 2], 
          speed: [random.uniform(random.uniform(3, 5), random.uniform(-3, -5)), random.uniform(-3, -5)], 
          colour: change_ball_color(), 
          radius: 30
        })
      
      # red portal settings
      # ball and portal collide
      if (portal1_pos[0] - ball[radius] <= ball[pos][0] <= portal1_pos[0] + portal1_width + ball[radius] 
          and portal1_pos[1] - ball[radius] <= ball[pos][1] <= portal1_pos[1] + portal1_height + ball[radius]):
        ball[pos][0] = random.uniform(portal2_pos[0] - ball[radius], portal2_pos[0] + portal2_width + ball[radius])
        ball[pos][1] = random.uniform(portal2_pos[1] - ball[radius], portal2_pos[1] + portal2_height + ball[radius])
      
      # orange portal settings
      # ball and portal collide
      if (portal2_pos[0] - ball[radius] <= ball[pos][0] <= portal2_pos[0] + portal2_width + ball[radius] 
          and portal2_pos[1] - ball[radius] <= ball[pos][1] <= portal2_pos[1] + portal2_height + ball[radius]):
        ball[pos][0] = random.uniform(portal1_pos[0] - ball[radius], portal1_pos[0] + portal1_width + ball[radius])
        ball[pos][1] = random.uniform(portal1_pos[1] - ball[radius], portal1_pos[1] + portal1_height + ball[radius])
      
      if ball[pos][1] >= height:
        lives -= 1
        ball[pos] = [width // 2, height // 2]
        ball[speed][1] = -abs(ball[speed][1])
        if lives == 0:
          game_running = False
          end_screen()
          score = 0
          lives = 3
          current_level = 1
          # print(lives)
    
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

    # portal feature: red portal is spin, orange portal is teleport

    # portal change dir
    if (portal1_pos[0] - ball[radius] - 2 <= 0):
      portal1_dir[0] = 0

    if (portal1_pos[0] + portal1_width + ball[radius] + 2 >= width):
      portal1_dir[0] = 1

    if (portal1_pos[1] - ball[radius] - 2 <= 0):
      portal1_dir[1] = 1

    if (portal1_pos[1] + portal1_height + ball[radius] >= height):
      portal1_dir[1] = 0

    if (portal1_dir[0] == 0):
      portal1_pos[0] += portal_speed[0]
    else:
      portal1_pos[0] -= portal_speed[0]

    if (portal1_dir[1] == 1):
      portal1_pos[1] += portal_speed[1]
    else:
      portal1_pos[1] -= portal_speed[1]

    # portal change dir
    if (portal2_pos[0] - ball[radius] - 2 <= 0):
      portal2_dir[0] = 1

    if (portal2_pos[0] + portal2_width + ball[radius] + 2 >= width):
      portal2_dir[0] = 0

    if (portal2_pos[1] - ball[radius] - 2 <= 0):
      portal2_dir[1] = 0

    if (portal2_pos[1] + portal2_height + ball[radius] >= height):
      portal2_dir[1] = 1

    if (portal2_dir[0] == 1):
      portal2_pos[0] += portal_speed[0]
    else:
      portal2_pos[0] -= portal_speed[0]

    if (portal2_dir[1] == 0):
      portal2_pos[1] += portal_speed[1]
    else:
      portal2_pos[1] -= portal_speed[1]

    if score >= current_level * 10:
      current_level += 1
      if platform_height <= 150:
        platform_height *= 1.15
      lives += 1
      platform_pos = [width // 2 - platform_width // 2, height - platform_height - 10]
      if platform_width < width // 2 - 1000:
        # platform_width *= 1.25
        platform_width *= 1.5
        # if (platform_height <= 150):
        #   platform_height *= 1.05
        
      # # reset ball position
      # ball[pos] = [width // 2, height // 2]
      
      # # change platform and ball colour for each level
      # platform_color = change_platform_color()
      # ball[colour] = change_ball_color()

      screen.fill(screen_color)

      for ball in balls:
        pygame.draw.circle(screen, ball[colour], (int(ball[pos][0]), int(ball[pos][1])), ball[radius])
            
      pygame.draw.rect(screen, platform_color, (int(platform_pos[0]), int(platform_pos[1]) + 10, platform_width, platform_height))
      pygame.draw.rect(screen, red, (int(portal1_pos[0]), int(portal1_pos[1]), portal1_width, portal1_height)) # red portal
      pygame.draw.rect(screen, orange, (int(portal2_pos[0]), int(portal2_pos[1]), portal2_width, portal2_height)) # orange portal

      # count score
      info_line_y = 10
      info_spacing = 75
      score_text = font.render(f"Score: {score}", True, white)
      score_rect = score_text.get_rect(topleft = (10, info_line_y))
      pygame.draw.rect(screen, orange, score_rect.inflate(10, 5))
      screen.blit(score_text, score_rect)

      # show current level
      level_text = font.render(f"Level: {current_level}", True, white)
      level_rect = level_text.get_rect(topleft = (score_rect.topright[0] + info_spacing, info_line_y))
      pygame.draw.rect(screen, light_blue, level_rect.inflate(10, 5))
      screen.blit(level_text, level_rect)

      # show remaining lives
      lives_text = font.render(f"Lives: {lives}", True, white)
      lives_rect = lives_text.get_rect(topleft = (level_rect.topright[0] + info_spacing, info_line_y))
      pygame.draw.rect(screen, red, lives_rect.inflate(10, 5))
      screen.blit(lives_text, lives_rect)

      pygame.display.flip()
      clock.tick(FPS)
    pygame.display.flip()

start_screen()
pygame.display.flip()