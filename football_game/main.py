import pygame
from charecter import *

# get the current path of file
full_path = os.path.realpath(__file__)
PATH = os.path.dirname(full_path)
IMG_PATH = os.path.join(PATH, "img")



pygame.init()


# get the width and height of background
bg_path = os.path.join(IMG_PATH, 'background.jpg')
background = pygame.image.load(bg_path)

FPS = 30
scale_factor = 2
WIDTH = background.get_width()*scale_factor
HEIGHT = background.get_height()*scale_factor

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Game")

# clock = pygame.time.Clock()


# set background
background = background.convert_alpha()

# increase background

new_width = int(background.get_width()*scale_factor)
new_height = int(background.get_height()*scale_factor)

scaled_background = pygame.transform.scale(background, (new_width, new_height))

bg_rect = scaled_background.get_rect()


all_sprites = pygame.sprite.Group()

football = Football()
goal_keeper = GoalKeeper()


all_sprites.add(football)
all_sprites.add(goal_keeper)

space_up = False
space_down = False

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

                
    # football.update()

    all_sprites.update()

    # draw the background screen
    screen.blit(scaled_background, bg_rect)

    all_sprites.draw(screen)

    # draw score text on screen
    score = ScoreLabel(screen, 'SCORE: ', 36)
    score.draw_text(WIDTH - 165, 20)


    pygame.display.flip()

pygame.quit()