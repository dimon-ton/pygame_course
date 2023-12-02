import pygame
import os
import math

WIDTH = 626 * 2
HEIGHT = 417 * 2

full_path = os.path.realpath(__file__)
PATH = os.path.dirname(full_path)
IMG_PATH = os.path.join(PATH, "img")

class Football(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        football_img_path = os.path.join(IMG_PATH, 'soccer.png')
        self.image = pygame.image.load(football_img_path).convert_alpha()
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - (self.rect.height / 2))


        # algorithm control the moving of the ball
        self.degree = 90
        self.radian = math.radians(self.degree)

        self.speed = 50

        self.motion_x = math.cos(self.radian) * self.speed
        self.motion_y = math.sin(self.radian) * self.speed

        self.isMoving = False

        self.initial_height = self.rect.height
        self.scale_factor = 1.0

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.isMoving = True

        if self.isMoving:
            self.rect.y -= self.motion_y
            self.rect.x -= self.motion_x

            # Decrease size based on vertical position
            self.scale_factor = max(0.5, (self.rect.y / HEIGHT))  # Adjust scaling range as needed
            scaled_height = int(self.initial_height * self.scale_factor)
            scaled_width = int((self.image.get_width() / self.image.get_height()) * scaled_height)
            self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

            print('scale factor: ', self.scale_factor)

            # If the football reaches the desired position, make it stop
            if self.rect.y < 270:
                self.motion_x = 0
                self.motion_y = 0


class GoalKeeper(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        goalKeeper_img_path = os.path.join(IMG_PATH, 'goalKeeper.png')
        self.image = pygame.image.load(goalKeeper_img_path).convert_alpha()

        # decrease the image size of goal keeper
        self.scale_factor = 0.18
        self.new_width = int(self.image.get_width()*self.scale_factor)
        self.new_height = int(self.image.get_height()*self.scale_factor)

        self.image = pygame.transform.scale(self.image, (self.new_width, self.new_height))



        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH / 2, HEIGHT)
        self.rect.x = (WIDTH / 2) - (self.image.get_width() / 2)
        self.rect.y = (HEIGHT / 2) - 77


     
