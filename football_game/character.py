import pygame
import os
import math

WIDTH = 626 * 2
HEIGHT = 417 * 2

full_path = os.path.realpath(__file__)
PATH = os.path.dirname(full_path)
IMG_PATH = os.path.join(PATH, "img")



class GoalPostRight(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.goal_post_img_path = os.path.join(IMG_PATH, 'goal_post', 'right.png')
        self.image = pygame.image.load(self.goal_post_img_path).convert_alpha()

        self.image.set_alpha(0)

        self.original_image = self.image.copy()

        # scale GoalPostMiddle

        # Example: Dynamic scaling based on movement or conditions
        # Here, you can adjust the scale_factor based on your game logic
        self.scale_factor = 2  # Set the scale factor as per your requirement

        # Calculate the scaled dimensions
        scaled_height = int(self.image.get_height() * self.scale_factor)
        scaled_width = int(self.image.get_width() * self.scale_factor)

        # Scale the image
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        

        self.rect = self.image.get_rect()
        self.rect.topleft = (890, 240)  # Set the position of the goal post


class GoalPostLeft(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.goal_post_img_path = os.path.join(IMG_PATH, 'goal_post', 'left.png')
        self.image = pygame.image.load(self.goal_post_img_path).convert_alpha()

        self.image.set_alpha(0)

        self.original_image = self.image.copy()

        # scale GoalPostMiddle

        # Example: Dynamic scaling based on movement or conditions
        # Here, you can adjust the scale_factor based on your game logic
        self.scale_factor = 2  # Set the scale factor as per your requirement

        # Calculate the scaled dimensions
        scaled_height = int(self.image.get_height() * self.scale_factor)
        scaled_width = int(self.image.get_width() * self.scale_factor)

        # Scale the image
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        

        self.rect = self.image.get_rect()
        self.rect.topleft = (395, 240)  # Set the position of the goal post

class GoalPostMiddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.goal_post_img_path = os.path.join(IMG_PATH, 'goal_post', 'middle.png')
        self.image = pygame.image.load(self.goal_post_img_path).convert_alpha()

        self.image.set_alpha(0) # make the image transparent

        self.original_image = self.image.copy()

        # scale GoalPostMiddle

        # Example: Dynamic scaling based on movement or conditions
        # Here, you can adjust the scale_factor based on your game logic
        self.scale_factor = 2  # Set the scale factor as per your requirement

        # Calculate the scaled dimensions
        scaled_height = int(self.image.get_height() * self.scale_factor)
        scaled_width = int(self.image.get_width() * self.scale_factor)

        # Scale the image
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        

        self.rect = self.image.get_rect()
        self.rect.topleft = (382, 260)  # Set the position of the goal post

class Football(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        football_img_path = os.path.join(IMG_PATH, 'soccer.png')
        self.image = pygame.image.load(football_img_path).convert_alpha()
        self.original_image = self.image.copy()


        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - (self.rect.height / 2))


        self.isMoving = False

        self.initial_height = self.rect.height
        self.scale_factor = 1.0



        # import football goal post image

        self.goal_post_middle = GoalPostMiddle()
        self.goal_post_left = GoalPostLeft()
        self.goal_post_right = GoalPostRight()

        self.score_text = 0

        self.goal_keeper = GoalKeeper()

    def update(self):


        # get mouse position
        if not self.isMoving:
            global mouse_position
            mouse_position = pygame.mouse.get_pos()

            # print("mouse position: ", mouse_position)
        
        horizontal_position = mouse_position[0]

        # print('vertical postion: ', mouse_position[1])
        
        max_degree = 180
        max_width = 626 * 2

        # get degree of football

        dynamic_degree = (horizontal_position * max_degree) / max_width

        # print('degree: ', dynamic_degree)

        # algorithm control the moving of the ball
        self.degree = dynamic_degree
        self.radian = math.radians(self.degree)

        self.speed = 50

        if self.degree < 70 and self.degree > 55:
            self.limited_y = 270 + (270 - ((270 * dynamic_degree) / 69))
        else:
            self.limited_y = 270

        # if self.rect.y < 270:
        #     self.motion_x = 0
        #     self.motion_y = 0
        # else:
        self.motion_x = math.cos(self.radian) * self.speed
        self.motion_y = math.sin(self.radian) * self.speed


        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.isMoving = True
        elif key[pygame.K_r]:

            self.isMoving = False
            self.rect.center = (WIDTH / 2, HEIGHT - (self.rect.height / 2))
            self.image = self.original_image.copy()
            


        if self.isMoving:
            self.rect.y -= self.motion_y
            self.rect.x -= self.motion_x


            self.collide_keeper = self.rect.collidepoint(self.goal_keeper.rect.center)
            
            print('goal_keeper:', self.collide_keeper)

            if self.rect.colliderect(self.goal_post_middle.rect):
                print('self --> goal post middle', self.rect.colliderect(self.goal_post_middle.rect))
                self.motion_x = 0  # Stop horizontal movement
                self.motion_y = 0  # Stop vertical movement


                self.isMoving = False
                self.score_text += 1

            elif self.rect.colliderect(self.goal_post_left.rect):
                self.motion_x = 0  # Stop horizontal movement
                self.motion_y = 0  # Stop vertical movement
                self.isMoving = False
            elif self.rect.colliderect(self.goal_post_right.rect):
                self.motion_x = 0  # Stop horizontal movement
                self.motion_y = 0  # Stop vertical movement
                self.isMoving = False
                
            elif self.collide_keeper:

                print('self.goal_keeper: ', self.goal_keeper.motion_x)
                self.goal_keeper.motion_x = 0
                print('self.goal_keeper: ', self.goal_keeper.motion_x)
      
   
                              
                self.motion_x = 0  # Stop horizontal movement
                self.motion_y = 0  # Stop vertical movement
                self.isMoving = False


            # Decrease size based on vertical position
            self.scale_factor = max(0.5, (self.rect.y / HEIGHT))  # Adjust scaling range as needed
            scaled_height = int(self.initial_height * self.scale_factor)
            scaled_width = int((self.image.get_width() / self.image.get_height()) * scaled_height)
            self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

            


            # If the football reaches the desired position, make it stop
            # if self.rect.y < 270:
            #     self.motion_x = 0
            #     self.motion_y = 0


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

        self.move_right = True

        self.motion_x = 3

    def update(self):
        

        if self.move_right:
            self.rect.x += self.motion_x
        else:
            self.rect.x -= self.motion_x

        if self.rect.x > 790:
            self.move_right = False
        elif self.rect.x < 320:
            self.move_right = True



     
class ScoreLabel:

    def __init__(self, screen, text, fontSize):
        pygame.init()
        self.screen = screen
        self.text = text
        self.font = pygame.font.Font(None, fontSize)

    def draw_text(self, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(self.text, True, color)
        self.screen.blit(text_surface, (x, y))




