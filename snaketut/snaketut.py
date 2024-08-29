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

    def draw(self, surface):
        for i in self.positions:
            rect = pygame.Rect((i[0], i[1]), (tile_size, tile_size))
            pygame.draw.rect(surface, self.color, rect)

snake = Snake()


while(True):
    draw_grid(screen)
    snake.draw(screen)

    pygame.display.update()

    clock.tick(10) # can affect difficulty