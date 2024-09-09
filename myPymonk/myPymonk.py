import pygame
import pymunk
import pymunk.pygame_util
import sys


pygame.init()
screen = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity  = (0, 750)


bird_body = pygame.image.load('./bird.png').convert_alpha()

birds = []
balls = []
boxes = []

def create_bird(space, pos):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, 50)
    space.add(body, shape)
    return shape


def draw_birds(birds):
    for bird in birds:
        pos_X = int(bird.body.position.x)
        pos_Y = int(bird.body.position.y)
        bird_rect = bird_body.get_rect(center = (pos_X, pos_Y))
        screen.blit(bird_body, bird_rect)


def create_static_ball(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (300, 400)
    shape = pymunk.Circle(body, 80)
    space.add(body, shape)
    return shape

def draw_static_ball(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), 100)


def create_static_box(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (100, 100)
    pos_x = int(body.position.x)
    pos_y = int(body.position.y)

    shape = pymunk.Poly.create_box(body, (pos_x, pos_y))
    space.add(body, shape)
    return shape




debug_draw = pymunk.pygame_util.DrawOptions(screen)
balls.append(create_static_ball(space))
create_static_box(space)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            birds.append(create_bird(space, event.pos))


    screen.fill((255, 255, 255))
    draw_birds(birds)
    draw_static_ball(balls)
    # space.debug_draw(debug_draw)

    space.step(1/60)
    pygame.display.update()
    
    clock.tick(60)