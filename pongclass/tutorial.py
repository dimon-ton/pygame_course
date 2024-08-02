import pygame, sys
import random


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

clock = pygame.time.Clock()


# game variable
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
player_speed = 0
computer_speed = 5

# score system
player_score = 0
computer_score = 0


# sound effect

plop_sound = pygame.mixer.Sound('ping_pong_8bit_plop.ogg')
peep_sound = pygame.mixer.Sound('ping_pong_8bit_peep.ogg')
beep_sound = pygame.mixer.Sound('ping_pong_8bit_beeep.ogg')

game_font = pygame.font.Font('AnonymousPro-Regular.ttf', 30)

# ball animation if the ball is collide with the border of screen then it reflex
def ball_anim():
    global computer_score, player_score
    global ball_speed_y, ball_speed_x


    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        # pygame.mixer.Sound.play(plop_sound)
        pygame.mixer.Sound.play(random.choice((plop_sound, peep_sound)))
        ball_speed_y *= -1

    # player score
    if ball.left <=0:
        player_score += 1
        pygame.mixer.Sound.play(beep_sound)
        ball_restart()
        
    if ball.right >= screen_width:
        # ball_speed_x *= -1
        computer_score += 1
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(computer):
        pygame.mixer.Sound.play(plop_sound)
        ball_speed_x *= -1


def player_anim():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def computer_logic():
    if computer.top < ball.y:
        computer.y += computer_speed
    if computer.bottom > ball.y:
        computer.y -= computer_speed


    if computer.top <= 0:
        computer.top = 0
    if computer.bottom >= screen_height:
        computer.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 5
            if  event.key == pygame.K_DOWN:
                player_speed += 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 5
            if event.key == pygame.K_DOWN:
                player_speed -=5
            


    # game play loop
    ball_anim()
    player_anim()
    computer_logic()


    screen.fill(bg_color)
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, computer)
    pygame.draw.ellipse(screen, red, ball)
    pygame.draw.aaline(screen, white, (screen_width / 2, 0), (screen_width / 2, screen_height))


    player_text = game_font.render(f'{player_score}', True, white)
    screen.blit(player_text, ((660, 485)))


    computer_text = game_font.render(f'{computer_score}', True, white)
    screen.blit(computer_text, ((600, 485)))

    pygame.display.update()
    clock.tick(60)