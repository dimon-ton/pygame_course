import sys, random
import pymunk
import pygame

import settings



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
game_over = False
pipe_gap = 250
pipe_freq = 1750 # ms
last_pipe = pygame.time.get_ticks() - pipe_freq
pass_pipe = False
score = 0

# pip ver here

def draw_text(text, font, text_color, x, y):
    render_text = font.render(text, True, text_color)
    screen.blit(render_text, (x, y))


class Bird(pygame.sprite.Sprite):
    CENTER = (settings.SCREEN_WIDTH // 4, settings.SCREEN_HEIGHT // 3)
    FLAP_FORCE = (0, -10000)
    CYCLE_WINGS_TIME = 50
    CYCLE_WINGS_EVENT = pygame.USEREVENT + 1

    def __init__(self, x, y, space, fps):
        self.space = space
        self.fps = fps

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0

        for number in range(1,4):
            img = pygame.image.load(f"./assets/Sprites/bird_{number}.png").convert_alpha()
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.CENTER)

        # check click input
        self.clicked = False


        # space step


        # Cycle wings timer
        pygame.time.set_timer(self.CYCLE_WINGS_EVENT, self.CYCLE_WINGS_TIME)

        # var for pymunk physics
        moment = pymunk.moment_for_box(15, self.image.get_size())
        self.body  = pymunk.Body(15, moment, body_type=pymunk.Body.DYNAMIC)

        space.add(self.body)
        self.body.velocity = (0,0)

    def handle_events(self, event):

        if event.type == self.CYCLE_WINGS_EVENT:
            self.cycle_wings()

    def cycle_wings(self):
        self.images.insert(0, self.images.pop())
        self.image = pygame.transform.rotate(self.images[0], -self.body.velocity.y // 30)


    def flap(self):
        self.body.velocity = (0,0)
        self.body.apply_impulse_at_local_point(Bird.FLAP_FORCE)
        flap_sound.play()
        # play sound here


    def update(self):
        self.space.step(1 / self.fps)
        self.rect.x, self.rect.y = self.body.position # sprite rect into pymunk body pos

        # check game over condition
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.flap()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # check mouse input condition



class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/pipe.png').convert_alpha()
        self.rect = self.image.get_rect()

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]

        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x < 0:
            self.kill()



bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


# instance of bird
flappy = Bird(150, int(settings.SCREEN_HEIGHT / 2), SPACE, settings.FPS)
bird_group.add(flappy)

running = True

while running:
    clock.tick(settings.FPS)

    screen.blit(bg_img, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # draw ground
    screen.blit(ground_img, (ground_scroll, 768))


    # check player score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                score_sound.play()
                pass_pipe = False


    draw_text(str(score), game_font, (255, 255, 255), int(settings.SCREEN_WIDTH / 2), -15, 35)
    # check bird collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        hit_sound.play()
        game_over = True


    # check bird hit ground or goes over the top
    if flappy.rect.bottom >= 768 or flappy.rect.top < 0:
        hit_sound.play()
        game_over = True
    
    if game_over == False:
        # scrolling ground
        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # create new pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)

            bottom_pipe = Pipe(settings.SCREEN_WIDTH, int(settings.SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(settings.SCREEN_WIDTH, int(settings.SCREEN_HEIGHT / 2) + pipe_height, 1)

            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current_time

        pipe_group.update()

    if game_over == True:
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            

    for sprite in bird_group:
        try:
            sprite.handle_events(event)
        except AttributeError:
            pass

    pygame.display.update()