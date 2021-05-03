import pygame 
from pygame import mixer
from pygame.locals import *
import random 


#player_score = 0

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
#FPS Settings
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800



screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Game Name')


#fonts 
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
font10 = pygame.font.SysFont('Constantia', 10)
#Game reverb
rows = 5
cols = 5
bal_cooldown = 1000 # 
last_bal_shot = pygame.time.get_ticks()
Its_the_final_countdown = 3
last_countdown = pygame.time.get_ticks()
game_over = 0 #0 means game not over -1 means you lose
start_score = 0
#colors 
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)


#load image
bg = pygame.image.load("Background.png")

#Game count down
def draw_text(text,font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x,y))


def scoreboard(player_score,font, text_col, x, y):
  img = font.render(player_score, True, text_col)
  screen.blit(img, (x,y))



#loading audiose
explosion_fx = pygame.mixer.Sound("explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("explosion2.wav")
explosion2_fx.set_volume(0.25)

def draw_bg():
  screen.blit(bg, (0,0))

#This is where we create the player
class Player(pygame.sprite.Sprite):
  def __init__(self,x,y,health):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("Catapult.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
    self.health_start = health 
    self.health_remaining = self.health_start
    self.last_peew_peew = pygame.time.get_ticks()

  def update(self):
    #Speed of the object
    speed = 8
    #Shooting cool down
    cooldown = 500 #Millersecs

    game_over = 0

    #reaction to key press
    key = pygame.key.get_pressed()
    
    # pLAYER MOVMENT LEFT
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= speed

    #Player movemtn right  
    if key[pygame.K_RIGHT] and self.rect.right < screen_width:
      self.rect.x += speed
    
    elif self.health_remaining <= 0:
      exp_exp = Boom_Boom(self.rect.centerx, self.rect.centery,3)
      Boom_Boom_group.add(exp_exp)
      self.kill()

      #Remov this for testing!!!


    #CURREnt time
    Current_time = pygame.time.get_ticks()
    #peew peww button (shooting)
    if key[pygame.K_SPACE] and Current_time - self.last_peew_peew > cooldown:
      ROCK = Rock(self.rect.centerx, self.rect.top)
      Rock_group.add(ROCK)
      self.last_peew_peew = Current_time

    self.mask = pygame.mask.from_surface(self.image)

  #Health bar
    pygame.draw.rect(screen, BLACK,(self.rect.x, (self.rect.bottom + 10), self.rect.width,15))
    if self.health_remaining > 0:
      pygame.draw.rect(screen, RED,(self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
      
    if self.health_remaining == 0:
      explosion_fx.play()
      self.kill()
      game_over = -1
    return game_over

  

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
    if pygame.sprite.spritecollide(self, Ballon_group, True):
      self.kill()
      explosion_fx.play()
      exp_exp = Boom_Boom(self.rect.centerx, self.rect.centery,2)
      Boom_Boom_group.add(exp_exp)

      




#Ballons

class Ballons(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    #Named ballons like Ballon1
    self.image = pygame.image.load("Ballon" + str(random.randint(1,6)) + ".png")
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
Boom_Boom_group = pygame.sprite.Group()

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
    if pygame.sprite.spritecollide(self, Player_group, False, pygame.sprite.collide_mask):
      self.kill()
      explosion2_fx.play()
      #reducehealth
      PLAYER.health_remaining -= 1
      exp_exp = Boom_Boom(self.rect.centerx, self.rect.centery,1)
      Boom_Boom_group.add(exp_exp)
      self.kill()


#Exposlion 
class Boom_Boom(pygame.sprite.Sprite):
  def __init__(self,x,y,size):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    for num in range(1,6):
      img = pygame.image.load(f"exp{num}.png")
      print(img)
      if size == 1:
        pygame.transform.scale(img,(20,20))
      if size == 2:
        pygame.transform.scale(img,(40,40))
      if size == 3:
        pygame.transform.scale(img,(160,160))
      self.images.append(img)
    self.index = 0
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
    self.counter = 0

  def update(self):
    exp_speed = 3 
    #updat Exception
    self.counter += 1

    if self.counter >= exp_speed and self.index < len(self.images) - 1:
      self.counter = 0
      self.index += 1
      self.image = self.images[self.index]
    if self.index >- len(self.images) - 1 and self.counter >= exp_speed:
      self.kill()

run = True

while run:
  #Game code in Here 
  draw_bg()
  clock.tick(fps)
  #scoreboard(str(player_score),font10,WHITE,0,0)


  if Its_the_final_countdown == 0:
    #
    #current time
    ballon_time_now = pygame.time.get_ticks()
    #peew peew bal
    if ballon_time_now - last_bal_shot > bal_cooldown and len(Ballon_attack_group) < 5 and len(Ballon_group) > 0:
      #
      attacking_bal = random.choice(Ballon_group.sprites())
      LAZER = Lazer(attacking_bal.rect.centerx, attacking_bal.rect.bottom)
      Ballon_attack_group.add(LAZER)
      last_bal_shot = ballon_time_now

       #checks if ballon boys are all dead : ( 
    if len(Ballon_group) == 0:
      game_over = 1


    if game_over == 0:
    #Group updates
      game_over = PLAYER.update()
      Rock_group.update()
      Ballon_group.update()
      Ballon_attack_group.update()
    else:
      if game_over == -1:
        draw_text('Game over!', font40, WHITE, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
      if game_over == 1:
        draw_text('You win!', font40, WHITE, int(screen_width / 2 - 110), int(screen_height / 2 + 50))

  if Its_the_final_countdown > 0:
    draw_text('It Show time!', font40, WHITE, int(screen_width / 2 - 110), int(screen_height / 2 + 50))

    draw_text(str(Its_the_final_countdown), font40, WHITE, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
    current_time_countdown = pygame.time.get_ticks()
    if current_time_countdown - last_countdown > 1000:
      Its_the_final_countdown -= 1
      last_countdown = current_time_countdown



  Boom_Boom_group.update()


  #Player upade
   

  #Sprite group draw
  Player_group.draw(screen)
  Rock_group.draw(screen)
  Ballon_group.draw(screen)
  Ballon_attack_group.draw(screen)
  Boom_Boom_group.draw(screen)

 
  #event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False



  pygame.display.update()
pygame.quit()
