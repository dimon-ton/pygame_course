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


# set the resolution of game
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set caption to game
pygame.display.set_caption('My First Game by Pimon')

# manage about time in game
clock = pygame.time.Clock()



class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = 'First_game/aircraft.png'
        self.image = pygame.image.load(img).convert_alpha()
        
        
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(GREEN)

       

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
        img = 'First_game/bomber.png'
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



# create group of sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# enemy
for i in range(3):
    enemy = Enemy()
    all_sprites.add(enemy)

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
    
    # inset background color
    screen.fill(BLACK)

    # draw the sprites
    all_sprites.draw(screen)

    # let the pygame to display
    pygame.display.flip()

# quit the game
pygame.quit()