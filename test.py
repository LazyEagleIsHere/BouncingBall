import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Portal')
screen.fill((0, 0, 0))

player = pygame.Surface((50, 50))
player.fill((255, 0, 0))

background = pygame.Surface((width, height))
background.fill((0, 0, 255))
screen.blit(background, (0, 0))

screen.blit(player, (width // 2 - 25, height // 2 - 25))
player_pos = [width // 2 - 25, height // 2 - 25]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    
    screen.blit(player, player_pos)
    pygame.display.flip()
    
    
    
pygame.quit()