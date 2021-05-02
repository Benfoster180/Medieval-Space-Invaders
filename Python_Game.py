import pygame 
from pygame.locals import *
import random 

#FPS Settings
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Game Name')

#Game reverb
rows = 5
cols = 5
bal_cooldown = 1000 # 
last_bal_shot = pygame.time.get_ticks()


#colors 
BLACK = (0,0,0)
RED = (255,0,0)



#load image
bg = pygame.image.load("BGtesting.png")

def draw_bg():
  screen.blit(bg, (0,0))

#This is where we create the player
class Player(pygame.sprite.Sprite):
  def __init__(self,x,y, health):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("Catapult.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
    self.health_start = health 
    self.health_remaining = health
    self.last_peew_peew = pygame.time.get_ticks()

  def update(self):
    #Speed of the object
    speed = 8
    #Shooting cool down
    cooldown = 500 #Millersecs
    #reaction to key press
    key = pygame.key.get_pressed()
    
    # pLAYER MOVMENT LEFT
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= speed

    #Player movemtn right  
    if key[pygame.K_RIGHT] and self.rect.right < screen_width:
      self.rect.x += speed


    #CURREnt time
    Current_time = pygame.time.get_ticks()
    #peew peww button (shooting)
    if key[pygame.K_SPACE] and Current_time - self.last_peew_peew > cooldown:
      ROCK = Rock(self.rect.centerx, self.rect.top)
      Rock_group.add(ROCK)
      self.last_peew_peew = Current_time

  #Health bar
    pygame.draw.rect(screen, BLACK,(self.rect.x, (self.rect.bottom + 10), self.rect.width,15))
    if self.health_remaining > 0:
      pygame.draw.rect(screen, RED,(self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))


#Create the rock
class Rock(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("Rock.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
  
  def update(self):
    self.rect.y -= 5
    if self.rect.bottom < 0:
      self.kill()


#Ballons

class Ballons(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    #Named ballons like Ballon1
    self.image = pygame.image.load("Ballon" + str(random.randint(1,1)) + ".png")
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
    self.move_counter = 0
    self.move_direction = 1
  
  def update(self):
    self.rect.x += self.move_direction
    self.move_counter += 1
    if abs(self.move_counter) > 75:
      self.move_direction *= -1
      self.move_counter *= self.move_direction



#Sprite Groups
Player_group = pygame.sprite.Group()
Rock_group = pygame.sprite.Group()
Ballon_group = pygame.sprite.Group()
Ballon_attack_group = pygame.sprite.Group()

def create_ballons():
  #gen ballom
  for row in range(rows):
    for item in range(cols):
      BALLON = Ballons(100 + item * 100, 100 + row * 70)
      Ballon_group.add(BALLON)
      
create_ballons()

#Create
PLAYER = Player(int(screen_width/2), screen_height - 100, 3)
Player_group.add(PLAYER)

#Ballon bullet

class Lazer(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("Lazzer.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
  
  def update(self):
    self.rect.y += 2
    if self.rect.top > screen_height:
      self.kill()


run = True

while run:
  #Game code in Here 
  draw_bg()
  clock.tick(fps)


  #Random ballon attack

  #current time
  ballon_time_now = pygame.time.get_ticks()
  #peew peew bal
  if ballon_time_now - last_bal_shot > bal_cooldown and len(Ballon_attack_group) < 5 and len(Ballon_group) > 0:
    attacking_bal = random.choice(Ballon_group.sprites())
    LAZER = Lazer(attacking_bal.rect.centerx, attacking_bal.rect.bottom)
    Ballon_attack_group.add(LAZER)
    last_bal_shot = ballon_time_now

  #event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False

  #Player upade
  PLAYER.update()

  #Sprite group draw
  Player_group.draw(screen)
  Rock_group.draw(screen)
  Ballon_group.draw(screen)
  Ballon_attack_group.draw(screen)

  #Group updates
  Rock_group.update()
  Ballon_group.update()
  Ballon_attack_group.update()

  pygame.display.update()
pygame.quit()
