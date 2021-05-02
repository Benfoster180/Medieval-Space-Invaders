import pygame 
from pygame.locals import *

#FPS Settings
clock = pygame.time.Clock()
fps = 60

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width,screen_height)
pygame.display.set_caption('Game Name')


#load image
bg = pygame.image.load("Game_backdrop.png")

def draw_bg():
  screen.blit(bg, (0,0))

#This is where we create the player
class Player(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("Catapult.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
  
  def update(self):
    #Speed of the object
    speed = 8

    #reaction to key press
    key = pygame.key.get_pressed()
    
    # pLAYER MOVMENT LEFT
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= speed

    #Player movemtn right  
    if key[pygame.K_RIGHT] and self.rect.right < screen_width:
      self.rect.x += speed


#Sprite Groups
Player_group = pygame.sprite.Group()


#Create
PLAYER = Player(int(screen_width/2), screen_height - 100)
Player_group.add(PLAYER)



run = True

while run:
  #Game code in Here 
  draw_bg()
  clock.tick(fps)
  #event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False

  #Player upade
  PLAYER.update()

  #Sprite group draw
  Player_group.draw(screen)


  pygame.display.update()
pygame.quit()
