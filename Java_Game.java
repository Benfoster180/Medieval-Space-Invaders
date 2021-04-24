import pygame 
import time
num = 1
screen = pygame.display.set_mode((500,500))
Background_day = "Backgroundatdaytime.png"
Background_night = "Cityatnight.png"


background_image = pygame.image.load("Backgroundatdaytime.png").convert()

screen.blit(background_image, [0, 0])

pygame.display.flip()
