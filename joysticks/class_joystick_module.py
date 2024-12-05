import pygame
import sys

pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

clock = pygame.time.Clock()

screen = pygame.display.set_mode((900, 600))

class Player():
    def __init__(self):
        self.player = pygame.rect.Rect((300, 300, 100, 100))
        self.color = 'white'


    def change_color(self, color):
        self.color = color

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)

    def move(self, x_speed, y_speed):
        self.player.move_ip(x_speed, y_speed)

player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # joystick event
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
            if pygame.joystick.Joystick(0).get_button(0):
                # Down Face button
                player.change_color("blue")
            
            if pygame.joystick.Joystick(0).get_button(1):
                # Right Face button
                player.change_color("green")

            if pygame.joystick.Joystick(0).get_button(2):
                # Left Face button
                player.change_color("red")

            if pygame.joystick.Joystick(0).get_button(3):
                # Up Face button
                player.change_color("yellow")

        if event.type == pygame.JOYAXISMOTION:
            print(event)
    



    x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(4))
    player.move(x_speed, y_speed)
    print(x_speed)



    clock.tick(60)
    screen.fill((0,0,0))
    player.draw(screen)

    pygame.display.update()