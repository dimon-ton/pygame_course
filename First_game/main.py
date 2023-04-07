import pygame
import random

# start pygame
pygame.init()

# FPS --> Frame per second
FPS = 30

WIDTH = 800
HEIGHT = 700

# set the color RGB
BLACK = (0,0,0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# score when the enemy is collided
SCORE = 0
LIVES = 3


# set the resolution of game
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set caption to game
pygame.display.set_caption('My First Game by Pimon')



# set background
bg = 'background.png'
background = pygame.image.load(bg).convert_alpha()
background_rect = background.get_rect()


# manage about time in game
clock = pygame.time.Clock()



class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = 'aircraft.png'
        self.image = pygame.image.load(img).convert_alpha()
        
        
        
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(GREEN)

        # scale the sprite
        scaled_impage = pygame.transform.scale(self.image, (90,90))
        self.image = scaled_impage

        # create rectangle
        self.rect = self.image.get_rect()
        
        # random x axis
        rand_x = random.randint(self.rect.width, WIDTH - self.rect.width)

        # position from the center of sprite
        self.rect.center = (rand_x, 0)

        # speed y
        self.speed_y = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom > HEIGHT:
            self.rect.y = 0

            # random x again
            rand_x = random.randint(self.rect.width, WIDTH - self.rect.width)
            self.rect.x = rand_x
            self.speed_y = random.randint(2, 5)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = 'bomber.png'
        self.image = pygame.image.load(img).convert_alpha()
        
        
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(GREEN)

       

        # create rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT - self.rect.height)

        # speed x
        self.speed_x = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        group_bullets.add(bullet)


    def update(self):
        # self.rect.y += 5

        self.speed_x = 0
        # check if the key is pressed.
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5

        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5

        self.rect.x += self.speed_x


        if self.rect.bottom > HEIGHT:
            self.rect.y = 0

class Bullet(pygame.sprite.Sprite):

    def __init__(self,x ,y):
        # x = center of the airplane
        # y = get the top of the air plane
        pygame.sprite.Sprite.__init__(self)
       
        
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)

       

        # create rectangle
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # speed x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y

        # delete bullet when the y axis is less than 0.
        if self.rect.y < 0:
            self.kill()





font_name = pygame.font.match_font('tahoma')

def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)




# create group of sprites
all_sprites = pygame.sprite.Group() # box for collecting all sprites
group_enemies = pygame.sprite.Group() # box for collecting enemies
group_bullets = pygame.sprite.Group() # box for collecting bullets


player = Player()
all_sprites.add(player)

# enemy
for i in range(3):
    enemy = Enemy()
    all_sprites.add(enemy)
    group_enemies.add(enemy)

# the status of game
running = True

while running:
    # run game along with framerate
    clock.tick(FPS)

    # check if the game is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # check if the player is collided
    collide_list = pygame.sprite.spritecollide(player, group_enemies, True)

    
    if LIVES != 0 and collide_list:
        player.kill()
        LIVES -= 1
        player = Player()
        all_sprites.add(player)
    elif LIVES == 0:
        running = False


    # bullet collide
    bullet_collide_list = pygame.sprite.groupcollide(group_bullets, group_enemies, True, True)

    for b in bullet_collide_list:
        enemy = Enemy()
        all_sprites.add(enemy)
        group_enemies.add(enemy)
        # add score
        SCORE += 10


    # inset background color
    screen.fill(BLACK)

    screen.blit(background, background_rect)

    draw_text(screen, "SCORE: {}".format(SCORE), 30, WIDTH-180, 10)
    draw_text(screen, "LIVE: {}".format(LIVES), 30, 30, 10)

    # draw the sprites
    all_sprites.draw(screen)

    # let the pygame to display
    pygame.display.flip()

# quit the game
pygame.quit()