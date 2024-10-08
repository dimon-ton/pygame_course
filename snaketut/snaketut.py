import pygame
import sys, random
import time

pygame.init()
pygame.mixer.pre_init(44800, -16, 2, 512)

clock = pygame.time.Clock()

powerup_sound = pygame.mixer.Sound("powerup.ogg")

# screen and display
screen_width = 720
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption("Snake Game")


# game font
# gamefont = pygame.font.Font("monospace", 16)
gamefont = pygame.font.SysFont("monospace", 48)

tile_size = 40
tile_width = screen_width/tile_size
tile_height = screen_height/tile_size

# Draw chess grid
def draw_grid(surface):
    for y in range(0, int(tile_height)):
        for x in range(0, int(tile_width)):
            if (x + y) % 2 == 0:
                rect = pygame.Rect((x*tile_size, y*tile_size), (tile_size, tile_size))
                pygame.draw.rect(surface, (128, 128, 128), rect)
            else:
                rect = pygame.Rect((x*tile_size, y*tile_size), (tile_size, tile_size))
                pygame.draw.rect(surface, (255, 255, 255), rect)


# Tuple base

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2),(screen_height/2))]
        self.color = (0,0,0)
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self, surface):
        for i in self.positions:
            rect = pygame.Rect((i[0], i[1]), (tile_size, tile_size))
            pygame.draw.rect(surface, self.color, rect)

    def get_head_positions(self):
        return self.positions[0]
    

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return 

        else:
            self.direction = point



    def move(self):
        head = self.get_head_positions()
        x,y = self.direction
        new = (((head[0] + (x*tile_size)) % screen_width), (head[1] + (y*tile_size)) % screen_height)
        # check if snake head hits it's own body or not
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset() # game over function


        else: # the head move then remove the tail
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()



    def input_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)

                if event.key == pygame.K_DOWN:
                    self.turn(down)

                if event.key == pygame.K_LEFT:
                    self.turn(left)

                if event.key == pygame.K_RIGHT:
                    self.turn(right)



    def reset(self):
        time.sleep(1)
        self.length = 1
        self.positions = [((screen_width/2),(screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        food.random_position()


class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0)
        self.random_position()
    
    def random_position(self):
        self.position = (random.randint(0, int(tile_width - 1)) * tile_size, random.randint(0, int(tile_height - 1)) * tile_size)


    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (tile_size, tile_size))
        pygame.draw.rect(surface, self.color, rect)


class Brick():
    bricklist = []
    def __init__(self):
        self.position = (0,0)
        self.color = (255, 255, 0)
        self.random_position()


    def random_position(self):
        self.position = (random.randint(0, int(tile_width - 1)) * tile_size, random.randint(0, int(tile_height - 1)) * tile_size)
        self.bricklist.append(self.position)

    def draw(self, surface):
        for i in self.bricklist:
            rect = pygame.Rect((i[0], i[1]), (tile_size, tile_size))
            pygame.draw.rect(surface, self.color, rect)


        # rect = pygame.Rect((self.position[0], self.position[1]), (tile_size, tile_size))
        # pygame.draw.rect(surface, self.color, rect)





class Button:
    def __init__(self, text, width, height, pos):

        self.pressed = False

        self.top_rect = pygame.Rect(pos,(width, height))
        self.top_rect_color = '#475F77'

        # text inside button
        self.text_surf = gamefont.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.top_rect_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)
        self.check_mouseclick()


    def check_mouseclick(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_rect_color = '#34eb43'
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.operate()
            else:
                if self.pressed:
                    self.pressed = False
        else:
            self.top_rect_color = '#205e25'


    def operate(self):
        pass


class GameState():
    def __init__(self):
        # self.state = 'Menu'
        self.state = 'Menu'
    
    def main_game(self):
        pygame.display.update()

        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        brick.draw(screen)
        snake.move()
        snake.input_key()
        if snake.get_head_positions() == food.position:
            pygame.mixer.Sound.play(powerup_sound)
            snake.length += 1
            snake.score += 1
            food.random_position()
            brick.random_position()

        if any(snake.get_head_positions() == i for i in brick.bricklist):
            snake.reset()

            food.random_position()
            brick.bricklist = []
            brick.random_position()
        score_text = gamefont.render("Score {}".format(snake.score), 1, (0,0,0))
        screen.blit(score_text, (10, 15))


    def menu(self):
        # GUI
        pygame.display.update()
        button1.draw()
        button2.draw()
        button3.draw()
        pygame.display.set_caption("Snake Game Menu")
        screen.blit(screen, (0,0)) # Background

        self.click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

                    if button1.top_rect.collidepoint((pygame.mouse.get_pos())):
                        if self.click:
                            self.state = 'Main_Game'


                    if button2.top_rect.collidepoint((pygame.mouse.get_pos())):
                        if self.click:
                            self.state = 'Options'


                    if button3.top_rect.collidepoint((pygame.mouse.get_pos())):
                        if self.click:
                            pygame.quit()
                            sys.exit()

    def options(self):
        global tile_size, screen_width, screen_height, tile_width, tile_height, screen

        option_surface = pygame.Surface((screen_width, screen_height))
        pygame.display.update()
        pygame.display.set_caption("Snake Game Options")
        screen.blit(option_surface, (0,0))
        option1.draw()
        option2.draw()

        self.click = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

                    if option1.top_rect.collidepoint((pygame.mouse.get_pos())):
                        # print("option1 clicked")
                        if self.click:
                            tile_size = 20
                            screen_width = 500
                            screen_height = 500
                            tile_width = screen_width / tile_size
                            tile_height = screen_height / tile_size
                            screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
                            self.state = 'Main_Game'

                    if option2.text_rect.collidepoint((pygame.mouse.get_pos())):
                        if self.click:
                            self.state = 'Main_Game'

                    if  button3.top_rect.collidepoint((pygame.mouse.get_pos())):
                        if self.click:
                            pygame.quit()
                            sys.exit()

    
    def state_manager(self):
        if self.state == 'Main_Game':
            self.main_game()

        if self.state == 'Menu':
            self.menu()

        if self.state == 'Options':
            self.options()

    def run(self):
        self.main_game()


snake = Snake()
food = Food()
brick = Brick()
game = GameState()

# GUI button instance
button1 = Button('Play Game', 300, 60, (screen_width/2 - 150, screen_height/2))
button2 = Button('Options', 300, 60, (screen_width/2 - 150, screen_height/2 + 100))
button3 = Button('Quit Game', 300, 60, (screen_width/2 - 150, screen_height/2 + 200))

# GUI button menu
option1 = Button('500x500', 300, 60, (screen_width/2 - 150, screen_height/2))
option2 = Button('720x720', 300, 60, (screen_width/2 - 150, screen_height/2 + 100))

while True:
  
    game.state_manager()


    # if snake.get_head_positions() == brick.position:
    #     snake.reset()



    clock.tick(10) # can affect difficulty