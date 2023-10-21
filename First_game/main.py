import pygame
import random
import os

full_path = os.path.realpath(__file__)
PATH = os.path.dirname(full_path)

# start pygame
pygame.init()

# start sound
pygame.mixer.init()




####################### sound effect ################################
# background music
pygame.mixer.music.load(os.path.join(PATH, "background-music.mp3"))
pygame.mixer.music.play(loops=-1) # -1 = loop

# collide sound
explosion = pygame.mixer.Sound(os.path.join(PATH, "explosion.wav"))

laser = pygame.mixer.Sound(os.path.join(PATH, "laser.wav"))
powerup = pygame.mixer.Sound(os.path.join(PATH, "powerup.wav"))
over_sound = pygame.mixer.Sound(os.path.join(PATH, "gameover.wav"))

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
GAMEOVER = False
GAMEOVER_FONT = True
GAMEOVER_TIME = pygame.time.get_ticks()
SOUND_STATE = True




# set the resolution of game
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set caption to game
pygame.display.set_caption('My First Game by Pimon')



# set background
bg = os.path.join(PATH, 'background.png')
background = pygame.image.load(bg).convert_alpha()
background_rect = background.get_rect()


# manage about time in game
clock = pygame.time.Clock()



class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = os.path.join(PATH, 'aircraft.png')
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
        img = os.path.join(PATH, 'bomber.png')
        self.image = pygame.image.load(img).convert_alpha()
        
        
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(GREEN)

       

        # create rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT - self.rect.height)

        # speed x
        self.speed_x = 0

    def shoot(self):
        pygame.mixer.Sound.play(laser)
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        group_bullets.add(bullet)


    def update(self):
        # self.rect.y += 5

        self.speed_x = 0
        # check if the key is pressed.
        keystate = pygame.key.get_pressed()

        if not GAMEOVER:
            if keystate[pygame.K_LEFT] and self.rect.x > 0:
                self.speed_x = -5

            if keystate[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
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

# medical pack

class Medipack(pygame.sprite.Sprite):



    '''

    - กระเป๋าจะตกทุก 30 วินาที
    - เมื่อเราชนกระเป๋า จะได้ชีวิตเพิ่มอีก 1
    - กระเป๋าจะหายไปเมื่อชน
    - มีเสียงติ๊งเมื่อได้รับกระเป๋า
    - เมื่อกระเป๋าลงไปด้านล่างสุดให้รออีก 30 วินาทีกว่ามันจะออกมา

    '''


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = os.path.join(PATH, 'medipack.png')

        # main clock
        self.last = pygame.time.get_ticks()
        self.wait = 20_000
        self.run = False


        self.image = pygame.image.load(img).convert_alpha()
        
        scaled_impage = pygame.transform.scale(self.image, (90,90))
        self.image = scaled_impage

        self.rect = self.image.get_rect()

        rand_x = random.randint(self.rect.width, WIDTH - self.rect.width)
        self.rect.center = (rand_x, -100)

        self.speed_y = random.randint(2, 5)

    def update(self):
        now = pygame.time.get_ticks()

        

        if self.run == True:
            self.rect.y += self.speed_y

        if self.rect.bottom > HEIGHT:
            # เมื่อกระเป๋าพยาบาลหล่นลงไปตรงขอบจอ จะสั่งให้มันหยุดวิ่ง
            self.run = False
            self.rect.y = -100




        if (now - self.last) >= self.wait:
            self.run = True
            self.last = now

            rand_x = random.randint(self.rect.width, WIDTH - self.rect.width)
            self.rect.x = rand_x
            self.speed_y = random.randint(2, 5)


# special bullet

'''
- เมื่อได้รับกระสุนชนิดพิเศษแล้ว จะเป็นกระสุนที่ออกมาเป็นแนวนอน
- ยิงเป็นเส้นตรงยาวเหมือนเลเซอร์
- ยิงนัดเดียวได้เครื่องบินหลายตัว
'''



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
group_medipack = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# enemy
for i in range(3):
    enemy = Enemy()
    all_sprites.add(enemy)
    group_enemies.add(enemy)
    

# add medipack
medipack = Medipack()
all_sprites.add(medipack)
group_medipack.add(medipack)


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

    
    # if LIVES != 0 and collide_list:
    #     player.kill()
    #     LIVES -= 1
    #     player = Player()
    #     all_sprites.add(player)
    # elif LIVES == 0:
    #     running = False


    if collide_list:

        pygame.mixer.Sound.play(explosion)

        enemy = Enemy()
        all_sprites.add(enemy)
        group_enemies.add(enemy)


        # if collided minus one score
        LIVES -= 1

        if LIVES == 0:
            GAMEOVER = True


    collide_medi = pygame.sprite.spritecollide(player, group_medipack, True)


    # plus lives if the medicine box is collided
    if collide_medi:

        pygame.mixer.Sound.play(powerup)

        LIVES += 1

        medipack = Medipack()
        all_sprites.add(medipack)
        group_medipack.add(medipack)






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


    # เมื่อ Game OVer อยากใส่อะไรเข้าไปใส่ได้เลย
    if GAMEOVER:
        if SOUND_STATE:
            pygame.mixer.Sound.play(over_sound)
            SOUND_STATE = False

        now_gameover = pygame.time.get_ticks()
        if GAMEOVER_FONT:
            draw_text(screen, 'GAME OVER', 100, 150, 300)
            if now_gameover - GAMEOVER_TIME >= 1_000:
                GAMEOVER_FONT = False
                GAMEOVER_TIME = now_gameover
        else:
            draw_text(screen, 'GAME OVER', 50, 280, 250)
            if now_gameover - GAMEOVER_TIME >= 1_000:
                GAMEOVER_FONT = True
                GAMEOVER_TIME = now_gameover

        # ทำให้เครื่องบินศัตรูและกระสุนหายไป หลังจาก Game Over
        
        for type in [group_enemies, group_medipack, group_bullets]:
            for charecter in type:
                charecter.kill()

        # for enemy in group_enemies:
        #     enemy.kill()

        # for medic in group_medipack:
        #     medic.kill()
            
        # for bull in group_bullets:
        #     bull.kill()

        



    # draw the sprites
    all_sprites.draw(screen)

    # let the pygame to display
    pygame.display.flip()

# quit the game
pygame.quit()