import pygame

pygame.init()

disp = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)

color_value = 0

def rainbow_color(value):
    step = (value // 256) % 6
    pos = value % 256

    if step == 0:
        return (255, pos, 0)
    if step == 1:
        return (255-pos, 255, 0)
    if step == 2:
        return (0, 255, pos)
    if step == 3:
        return (0, 255-pos, 255)
    if step == 4:
        return (pos, 0, 255)
    if step == 5:
        return (255, 0, 255-pos)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    disp.fill( rainbow_color(color_value) )
    pygame.display.flip()

    color_value = (color_value + 1) % (256 * 6)

pygame.quit()