import pygame, sys
import random

import pygame_menu
from pygame_menu import themes


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

clock = pygame.time.Clock()


# game variable
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
player_speed = 0
player_two_speed = 0
computer_speed = 5

# score system
player_score = 0
computer_score = 0


# sound effect
sound_enabled = True
plop_sound = pygame.mixer.Sound('ping_pong_8bit_plop.ogg')
peep_sound = pygame.mixer.Sound('ping_pong_8bit_peep.ogg')
beep_sound = pygame.mixer.Sound('ping_pong_8bit_beeep.ogg')

game_font = pygame.font.Font('AnonymousPro-Regular.ttf', 30)

# setting up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
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


# ball animation if the ball is collide with the border of screen then it reflex
def ball_anim():
    global computer_score, player_score
    global ball_speed_y, ball_speed_x


    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        if sound_enabled:

            # pygame.mixer.Sound.play(plop_sound)
            pygame.mixer.Sound.play(random.choice((plop_sound, peep_sound)))


        ball_speed_y *= -1

    # player score
    if ball.left <=0:
        player_score += 1

        if sound_enabled:
            pygame.mixer.Sound.play(beep_sound)

        ball_restart()
        
    if ball.right >= screen_width:
        # ball_speed_x *= -1
        computer_score += 1
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(computer):
        if sound_enabled:
            pygame.mixer.Sound.play(plop_sound)

        ball_speed_x *= -1


def player_anim():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def player_two_anim():
    computer.y += player_two_speed

    if computer.top <= 0:
        computer.top = 0
    if computer.bottom >= screen_height:
        computer.bottom = screen_height

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

def drawgame_layout():


    screen.fill(bg_color)
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, computer)
    pygame.draw.ellipse(screen, red, ball)
    pygame.draw.aaline(screen, white, (screen_width / 2, 0), (screen_width / 2, screen_height))


    player_text = game_font.render(f'{player_score}', True, white)
    screen.blit(player_text, ((660, 485)))


    computer_text = game_font.render(f'{computer_score}', True, white)
    screen.blit(computer_text, ((600, 485)))


def toggle_sound():
    global sound_enabled

    if sound_enabled:
        sound_enabled = False
        print('sound off')
    else:
        sound_enabled = True
        print('sound on')



def change_game_diff(value, difficulty):
    '''
        function to change the difficulty of the game
    '''

    global computer_speed
    
    if value[0][0] == 'Easy':
        computer_speed = difficulty
    elif value[0][0] == 'Medium':
        computer_speed = difficulty
    elif value[0][0] == 'Hard':
        computer_speed = difficulty

    

class Game:
    def __init__(self):
        global computer_speed

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pong Game")  
        game_icon = pygame.image.load('pong_icon.png')
        pygame.display.set_icon(game_icon)
    
    def single_player(self):
        global player_speed, player_text, computer_text, computer_speed
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
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
            drawgame_layout()
            computer_logic()

    
            # update the windows
            pygame.display.update()
            clock.tick(60)

    def two_player(self):
        global player_speed, player_text, computer_text, player_two_speed

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        player_speed -= 5
                    if  event.key == pygame.K_DOWN:
                        player_speed += 5

                    if event.key == pygame.K_w:
                        player_two_speed -= 5
                    if  event.key == pygame.K_s:
                        player_two_speed += 5

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player_speed += 5
                    if event.key == pygame.K_DOWN:
                        player_speed -=5

                    if event.key == pygame.K_w:
                        player_two_speed += 5
                    if event.key == pygame.K_s:
                        player_two_speed -=5

            # game play loop
            ball_anim()
            player_anim()
            player_two_anim()
            drawgame_layout()
 

            # update the windows
            pygame.display.update()
            clock.tick(60)


def exit_game(self):
    pygame.quit()
    sys.exit()

game = Game()

settings_menu = pygame_menu.Menu('Game Settings', screen.get_width(), screen.get_height(), theme=themes.THEME_GREEN)
audio = settings_menu.add.button("Toggle Sound: ON/OFF", toggle_sound)

difficulty = settings_menu.add.selector(
    title = 'Select Difficulty: ',
    items= [('Easy', 3), ('Medium', 5), ('Hard', 7)],
    onchange=change_game_diff,
    selector_id='selector_difficulty'

)

menu = pygame_menu.Menu('Welcome to Pong Game', screen.get_width(), screen.get_height(), theme=themes.THEME_BLUE)
menu.add.button('Single Player', game.single_player)
menu.add.button('Two player', game.two_player)
menu.add.button('Game Settings', settings_menu)
menu.add.button('Quit Game', exit_game)


menu.mainloop(screen)


            








