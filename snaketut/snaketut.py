import pygame
import sys, random

pygame.init()

clock = pygame.time.Clock()

# screen and display
screen_width = 720
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption("Snake Game")

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

snake = Snake()
food = Food()

while(True):
    draw_grid(screen)
    snake.draw(screen)
    snake.move()
    snake.input_key()
    if snake.get_head_positions() == food.position:
        snake.length += 1
        # snake.score += 1

    food.draw(screen)
    pygame.display.update()

    clock.tick(10) # can affect difficulty