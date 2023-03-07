import pygame

# start pygame
pygame.init()

# FPS --> Frame per second
FPS = 30

WIDTH = 800
HEIGHT = 700

# set the color
BLACK = (0,0,0)
GREEN = (0, 255, 0)


# set the resolution of game
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set caption to game
pygame.display.set_caption('My First Game by Pimon')

# manage about time in game
clock = pygame.time.Clock()



class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = 'First_game/aircraft.png'
        self.image = pygame.image.load(img).convert_alpha()
        
        
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(GREEN)

       

        # create rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.y += 5
        if self.rect.bottom > HEIGHT:
            self.rect.y = 0


# create group of sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# the status of game
running = True

while running:
    # run game along with framerate
    clock.tick(FPS)

    # check if the game is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    
    # inset background color
    screen.fill(BLACK)

    # draw the sprites
    all_sprites.draw(screen)

    # let the pygame to display
    pygame.display.flip()

# quit the game
pygame.quit()