import pygame
from character import *

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

print('width: ', background.get_width())
print('height: ', background.get_height())

print('new width: ', new_width)
print('new height: ', new_height)

scaled_background = pygame.transform.scale(background, (new_width, new_height))

bg_rect = scaled_background.get_rect()


all_sprites = pygame.sprite.Group()

football = Football()
goal_keeper = GoalKeeper()


all_sprites.add(football)
all_sprites.add(goal_keeper)
all_sprites.add(football.goal_post_middle)
all_sprites.add(football.goal_post_left)
all_sprites.add(football.goal_post_right)




space_up = False
space_down = False

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False


    # football.update()
    all_sprites.update()

    # check if the player collide with goal keeper
    
    # key = pygame.key.get_pressed()
    # if key[pygame.K_SPACE]:
    #     collide_bool = football.rect.colliderect(goal_keeper.rect)

    #     print('collide_bool: ', collide_bool)
    #     print('football Moving: ', football.isMoving)
   
    #     if collide_bool:
    #         football.motion_x = 0
    #         football.motion_y = 0
    #     else:
    #         score_text += 1


    # draw the background screen
    screen.blit(scaled_background, bg_rect)

    all_sprites.draw(screen)

    # draw score text on screen
    # print('score: ', score_text)
    score = ScoreLabel(screen, 'SCORE: {}'.format(football.score_text), 30)
    score.draw_text(WIDTH - 165, 20)


    pygame.display.flip()

pygame.quit()