import pygame, sys



pygame.init()

clock = pygame.time.Clock()


# game variable
ball_speed_x = 5
ball_speed_y = 5

def ball_anim():
    global ball_speed_y, ball_speed_x


    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <=0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(player) or ball.colliderect(computer):
        ball_speed_x *= -1


# screen surface setup
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# color
white = 'ghostwhite'
red = 'firebrick1'
# bg_color = pygame.Color('gray32')
bg_color = 'gray32'

# Game rectangles
player = pygame.Rect(screen_width - 30, screen_height / 2 - 70, 10, 140)
computer = pygame.Rect(30, screen_width / 2 - 70, 10, 140)
ball = pygame.Rect(screen_width / 2 - 12.5, screen_height / 2 - 12.5, 25, 25)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # game play loop
    ball_anim()

    screen.fill(bg_color)
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, computer)
    pygame.draw.ellipse(screen, red, ball)
    pygame.draw.aaline(screen, white, (screen_width / 2, 0), (screen_width / 2, screen_height))


    pygame.display.update()
    clock.tick(60)