import settings

import sys, random
import pymunk
import pygame


pygame.init()


clock = pygame.time.Clock()


screen = pygame.display.set_mode(settings.SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird Pymunk')

bg_img = pygame.image.load('./bg.png').convert_alpha()
ground_img = pygame.image.load('./ground.png').convert_alpha()

# load font
game_font = pygame.font.Font("./assets/Flappy-Bird-Font.ttf", 50)

# load sounds
flap_sound = pygame.mixer.Sound("./assets/Audio/flap.wav")
hit_sound = pygame.mixer.Sound("./assets/Audio/hit.wav")
score_sound = pygame.mixer.Sound("./assets/Audio/score.wav")

# Define Gravity
SPACE = pymunk.Space()
SPACE.gravity = (0, 1600)

# Define game variables
ground_scroll = 0
scroll_speed = 4

# game_over = False
# pip ver here



while True:
    clock.tick(settings.FPS)

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