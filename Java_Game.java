import pygame 
import time
num = 1
screen = pygame.display.set_mode((500,500))
Background_day = "Backgroundatdaytime.png"
Background_night = "Cityatnight.png"

background_image = pygame.image.load("Backgroundatdaytime.png").convert()
screen.blit(background_image, [0, 0])
# Changes the Time in game based on a loop and sleep commands 
while num == 1:
  background_image = pygame.image.load("Backgroundatdaytime.png").convert()
  print("1")
  pygame.display.update()
  screen.blit(background_image, [0, 0])
  time.sleep(150)
  background_image = pygame.image.load("Cityatnight.png").convert()
  pygame.display.update()
  screen.blit(background_image, [0, 0])
  time.sleep(150)



pygame.display.flip()
