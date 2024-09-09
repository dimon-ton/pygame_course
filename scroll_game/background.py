import settings

import sys
import pymunk
import pygame


pygame.init()


clock = pygame.time.Clock()

ground_scroll = 0
scroll_speed = 4

screen = pygame.display.set_mode(settings.SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird Pymunk')

bg_img = pygame.image.load('./bg.png').convert_alpha()
ground_img = pygame.image.load('./ground.png').convert_alpha()

while True:
    clock.tick(60)

    screen.blit(bg_img, (0, 0))
    screen.blit(ground_img, (ground_scroll, 768))

    ground_scroll -= scroll_speed

    if abs(ground_scroll) > 35:
        ground_scroll = 0

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()