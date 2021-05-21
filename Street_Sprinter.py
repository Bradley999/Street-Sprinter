import random
import pygame
import os
import time
WIDTH = 600
HEIGHT = 1000
FPS = 30
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
vec = pygame.math.Vector2
WHITE = (255, 255, 255)

#ASSET FOLDER
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

pygame.init()
pygame.mixer.init()
accel_snd = pygame.mixer.Sound(os.path.join(img_folder, "Acceleration.wav"))
accel_snd.set_volume(0.2)
boost_snd = pygame.mixer.Sound(os.path.join(img_folder, "Boost.wav"))
boost_snd.set_volume(0.2)
deccel_snd = pygame.mixer.Sound(os.path.join(img_folder, "Deceleration.wav"))
deccel_snd.set_volume(0.2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Sprinter")

#SOUNDTRACK METHHOOD
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(game_folder, "snd")

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
#pygame.mixer.music.play(loops = -1)

#BACKGROUND
bg = pygame.image.load(os.path.join(img_folder, "Road0.png")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_rect = bg.get_rect()
bg_y = 0

#GAME OVER SCREEN
gameover = pygame.image.load(os.path.join(img_folder, "Game_Over0.PNG")).convert()
gameover = pygame.transform.scale(gameover, (WIDTH, HEIGHT))
gameover_rect = gameover.get_rect()

#RADIO FUNCTION/METHOOD
def Radio(track):
    if track == 1:
        pygame.mixer.music.load(os.path.join(img_folder, "Ooh_Ahh(My_Life_Be_Like).wav"))
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops = -1)
    elif track == 2:
        pygame.mixer.music.load(os.path.join(img_folder, "Six Days(Remix).wav"))
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops = -1)
    elif track == 3:
        pygame.mixer.music.load(os.path.join(img_folder, "Furious_Ja_Rule.wav"))
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops = -1)
    elif track == 4:
        pygame.mixer.music.load(os.path.join(img_folder, "Horses.wav"))
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops = -1)
    elif track == 5:
        pygame.mixer.music.load(os.path.join(img_folder, "Pump_It_Up_Joe_Budden.wav"))
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops = -1)
    elif track == 0:
        pygame.mixer.music.stop()
        

#DRAW TEXT FUNCTION
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#SHOW START SCREEN FUNCTION
def show_start_screen():

    screen.blit(bg, bg_rect)
    draw_text(screen, "Street", 64, WIDTH / 2, HEIGHT / 5, RED)
    draw_text(screen, "Sprinter", 64, WIDTH / 2, HEIGHT / 5 + 65, RED)
    draw_text(screen, "ARROW KEYS TO MOVE  SPACE TO SHOOT AND SHIFT TO BOOST!", 18, WIDTH / 2, HEIGHT / 2, RED)
    draw_text(screen, "PRESS ANY KEY TO BEGIN!", 18, WIDTH / 2, HEIGHT * 3 / 4, RED)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                print("KEY PRESSED TO START GAME!")
                waiting = False

#SHOW GAME OVER SCREEN FUNCTION
def show_gameover_screen():
    screen.blit(gameover, gameover_rect)
    pygame.display.flip()
    print("gameover")
    waiting = True
    while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
            

#BULLET CLASS
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "Missile0.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, 125))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.top = y

    def update(self):
        self.rect.y += -10
        if self.rect.bottom < 0:
            self.kill()

#SCORE COUNT
class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "Score_Count0.png")).convert()
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.top = HEIGHT - 150

    def update(self):
        pass

#NOS CLASS
class NOS(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(img_folder, "NOS_Re-filling0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "NOS_Re-filling1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "NOS_Re-filling2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "NOS_Re-filling3.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "NOS_Re-filling4.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "NOS_Re-filling5.png")).convert()
            ]
        #self.count = 0
        self.level = 5
        self.boosting = False
        self.nos_delay = 400
        self.last_nos = pygame.time.get_ticks() 
        

        self.image = self.images[self.level]
        self.image = pygame.transform.scale(self.image, (60, 216))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 85
        self.rect.top = 20

    def update(self):
        print(self.level)
        if self.boosting:
            now = pygame.time.get_ticks()
            if now -self.last_nos > self.nos_delay:
                self.last_nos = now
                if self.level < 1:
                    self.boosting = False
                else:
                    self.level -= 1
                    self.image = self.images[self.level]
                    self.image = pygame.transform.scale(self.image, (60, 216))
                    self.image.set_colorkey(BLACK)
                    
        else:
            now = pygame.time.get_ticks()
            if now -self.last_nos > self.nos_delay:
                self.last_nos = now
                if  self.level < 5:           
                    self.level += 1
                    self.image = self.images[self.level]
                    self.image = pygame.transform.scale(self.image, (60, 216))
                    self.image.set_colorkey(BLACK)
                       
    def getNOSLevel(self):
        return self.level

    def setNOSBoost(self, boosting):
        self.boosting = boosting

#BULLET COUNT METHOOD/ CLASS
class Bullet_Count(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(img_folder, "sprite_00.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_01.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_02.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_03.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_04.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_05.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_06.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_07.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_08.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_09.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_10.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_11.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_12.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_13.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_14.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "sprite_15.png")).convert()
           
            ]
        #self.count = 0
        self.level = 15
        self.image = self.images[self.level]
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.top = 20

    def update(self):
        self.image = self.images[self.level]
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.image.set_colorkey(BLACK)
        print(self.level)
                       
    def getBullet_Count(self):
        return self.level

    def increaseBullet_Count(self):
        self.level -= 1
        if self.level < 0:
            self.level = 14

    def load_Bullets(self):
        self.level = 14

#HEALTH BAR COUNT CLASS
class Health_Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(img_folder, "Health_Bar0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Health_Bar1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Health_Bar2.png")).convert()
           
            ]
        #self.count = 0
        self.level = 0
        self.image = self.images[self.level]
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.top = 130
    def update(self):
        self.image = self.images[self.level]
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.image.set_colorkey(BLACK)
        print(self.level)
                       
    def getHealth_Count(self):
        return self.level

    def decreaseHealth_Count(self):
        self.level += 1
        if self.level < 0:
            self.level = 0

    def load_Health(self):
        self.level = 2

#RADIO BAR CLASS
class Radio_Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(img_folder, "Health_Bar2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Ooh_Aah_Cover.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Six_Days_Cover.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Health_Bar2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Health_Bar2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Health_Bar2.png")).convert()
           
            ]
        #self.count = 0
        self.level = 0
        self.image = self.images[self.level]
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.top = HEIGHT -260
        
    def update(self):
        self.image = self.images[self.level]
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.image.set_colorkey(BLACK)
        print(self.level)


    def load_radio(self, track):
        self.level = track
    
#RAM GUARD METHOOD/ CLASS
class Ram_Guard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "Ram_Guard0.png")).convert()
        self.image = pygame.transform.scale(self.image, (100, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/ 2
        self.rect.top = 0
        self.reset_delay = 2000
        self.last_reset = pygame.time.get_ticks()

    def update(self):
        self.rect.y += 15
        if self.rect.top > HEIGHT:
            self.kill()
            #now = pygame.time.get_ticks()
            #if now - self.last_reset > self.reset_delay:
                #self.last_reset = now
                #self.rect.bottom = 0

#BULLET RELOAD METHOOD/ CLASS
class Bullet_Strap(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "Bullet_Strap0.png")).convert()
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/ 2
        self.rect.top = 0
        self.reset_delay = 2000
        self.last_reset = pygame.time.get_ticks()
        self.left_lane = vec(220, -180)
        self.right_lane = vec(380, -180)
        self.rect.center = self.left_lane

    def update(self):
        self.rect.y += 15
        if self.rect.top > HEIGHT:
            self.kill()
    def set_lane(self):
        self.lane = random.randint(0, 1)
        if self.lane == 0:
            self.rect.center = self.left_lane
        else:
            self.rect.center = self.right_lane

#TRUCK EXPLOSION
class Truck_Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion4.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion5.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion6.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion7.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Truck_Explosion8.png")).convert()
            ]
        self.count = 0
        self.image = self.images[self.count]
        self.image = pygame.transform.scale(self.image, (230, 350))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
    #Update Methood
    def update(self):
        self.image = self.images[self.count]
        self.image = pygame.transform.scale(self.image, (230, 350))
        self.image.set_colorkey(BLACK)

        self.count += 1
        if self.count > 7:
            self.kill()

#P1 CAR EXPLOSION
class Car_Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(img_folder, "P1_Explosion0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion3.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion4.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion5.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion6.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion7.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "P1_Explosion8.png")).convert(),
            
            ]
        self.count = 0
        self.image = self.images[self.count]
        self.image = pygame.transform.scale(self.image, (200, 300))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
    #Update Methood
    def update(self):
        self.image = self.images[self.count]
        self.image = pygame.transform.scale(self.image, (200, 300))
        self.image.set_colorkey(BLACK)

        self.count += 1
        if self.count > 8:
            self.kill()


#TRUCK CLASS/ ENEMY G
class Enemy_G(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.Grey_Trucks = [
            pygame.image.load(os.path.join(img_folder, "Grey_Truck0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Grey_Truck1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Grey_Truck2.png")).convert()
            ]
        self.count = 0
        self.image = self.Grey_Trucks[self.count]
        self.image = pygame.transform.scale(self.image, (115, 175))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.left_lane = vec(220, -180)
        self.right_lane = vec(380, -180)
        self.rect.center = self.left_lane
        self.reset_delay = 2000
        self.last_reset = pygame.time.get_ticks()

    #Update Methood
    def update(self):
        self.image = self.Grey_Trucks[self.count]
        self.image = pygame.transform.scale(self.image, (115, 175))
        self.image.set_colorkey(BLACK)

        self.count += 1
        if self.count > 2:
            self.count = 0
        self.rect.y += 10
        if self.rect.top > HEIGHT:
            now = pygame.time.get_ticks()
            if now - self.last_reset > self.reset_delay:
                self.last_reset = now
                self.rect.bottom = 0

    #SET LANE FOR ENEMY G/ GREY TRUCK
    def set_lane(self):
        self.lane = random.randint(0, 1)
        if self.lane == 0:
            self.rect.center = self.left_lane
        else:
            self.rect.center = self.right_lane
                
#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.red_cars = [
                            pygame.image.load(os.path.join(img_folder, "P1_Car_RED0.png")).convert(), 
                            pygame.image.load(os.path.join(img_folder, "P1_Car_RED1.png")).convert(), 
                            pygame.image.load(os.path.join(img_folder, "P1_Car_RED2.png")).convert()
                            ]
        self.ram_cars = [
                            pygame.image.load(os.path.join(img_folder, "Ram_Guard_P10.png")).convert(), 
                            pygame.image.load(os.path.join(img_folder, "Ram_Guard_P11.png")).convert(), 
                            pygame.image.load(os.path.join(img_folder, "Ram_Guard_P12.png")).convert()
                            ]
        self.Damaged1 = [ pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged10.png")).convert(), 
                          pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged11.png")).convert(), 
                          pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged12.png")).convert()
                          ]
        self.Damaged2 = [ pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged20.png")).convert(), 
                           pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged21.png")).convert(), 
                           pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged22.png")).convert()
                           ]
        self.Damaged3 = [ pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged30.png")).convert(), 
                           pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged31.png")).convert(), 
                           pygame.image.load(os.path.join(img_folder, "P1_Car_Damaged32.png")).convert()
                           ]
        self.health = 0
        
        self.mode = "Normal_Mode"
        self.count = 0
        self.bullet_count = 15
        self.image = self.red_cars[self.count]
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.ram_delay = 10000
        self.start_ram = pygame.time.get_ticks()

        # NOS BOOST
        self.nos = NOS()
        all_sprites.add(self.nos)
        self.boost_delay = 10000
        self.start_boost = pygame.time.get_ticks()
        self.boost = False
        self.speed = 5

        #Bullet Count
        self.Bullet_Count = Bullet_Count()
        all_sprites.add(self.Bullet_Count)

    def load_Bullets(self):
        self.Bullet_Count.load_Bullets()

    def update(self):

        #NOS BOOST
        self.boost = False
        self.nos.setNOSBoost(False)

        if self.health == 0:
            
        
            if self.mode == "Normal_Mode":
                self.image = self.red_cars[self.count]
            if self.mode == "Ram_Mode":
                now = pygame.time.get_ticks()
                if now - self.start_ram < self.ram_delay:
                    self.image = self.ram_cars[self.count]
                else:
                    self.mode = "Normal_Mode"
        else:
            if self.health == 1:
                self.image = self.Damaged1[self.count]
            elif self.health == 2:
                self.image = self.Damaged2[self.count]
            elif self.health == 3:
                self.image = self.Damaged3[self.count]
                
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.image.set_colorkey(BLACK)
        self.count += 1
        if self.count > 2:
            self.count = 0


    # RETURNS A LIST, keystate, OF ALL PRESSED KEYS
        keystate = pygame.key.get_pressed()

    # CHECKS TO SEE WHICH KEYS WERE IN THE LIST (A.K.A. PRESSED)
        if keystate[pygame.K_d]:
            self.rect.x += self.speed
        if keystate[pygame.K_a]:
            self.rect.x += -self.speed
        if keystate[pygame.K_w]:
            self.rect.y += -self.speed
            boost_snd.stop()
            deccel_snd.stop()
            accel_snd.play()
        if keystate[pygame.K_s]:
            self.rect.y += self.speed
            boost_snd.stop()
            accel_snd.stop()
            deccel_snd.play()
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_LSHIFT]: # NOS BOOST
            self.boost = True
            self.nos.setNOSBoost(True)
            self.speed = 10
            self.rect.y += -self.speed
            accel_snd.stop()
            deccel_snd.stop()
            boost_snd.play()
        else:
            self.speed = 5

        if self.rect.top <= 0:
            self.rect.top = 0

    def update_health(self, h):
        self.health += h

    def get_health(self):
        return self.health

    def setMode(self, mode):
        if mode == "Ram_Mode":
            self.start_ram = pygame.time.get_ticks()
            
        self.mode = mode
        

    def getMode(self):
        return self.mode

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100
        accel_snd.stop()
        boost_snd.stop()
        

#SHOOT METHOOD
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.bullet_count -= 1
            self.last_shot = now
            if self.bullet_count >= 0:
                self.Bullet_Count.increaseBullet_Count()
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            else:
                self.bullet_count = self.Bullet_Count.getBullet_Count()
    
    
#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
Grey_Truck = Enemy_G()
all_sprites.add(Grey_Truck)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs.add(Grey_Truck)
guards = pygame.sprite.Group()
bullet_straps = pygame.sprite.Group()
#nos = NOS()
strap_delay = 15000
last_strap = pygame.time.get_ticks()
#all_sprites.add(nos)
score = Score()
all_sprites.add(score)
Score_Tally = 0
health_bar = Health_Bar()
all_sprites.add(health_bar)
radio_bar = Radio_Bar()
all_sprites.add(radio_bar)

ram_delay = 15000
last_ram = pygame.time.get_ticks() + 3000

end_delay = 300
last_end = pygame.time.get_ticks()

def new_strap():
    bullet_strap = Bullet_Strap()
    bullet_strap.set_lane()
    all_sprites.add(bullet_strap)
    bullet_straps.add(bullet_strap)


def new_guard():
    ram_guard = Ram_Guard()
    all_sprites.add(ram_guard)
    guards.add(ram_guard)

def new_mob():
    Grey_Truck = Enemy_G()
    Grey_Truck.set_lane()
    all_sprites.add(Grey_Truck)
    mobs.add(Grey_Truck)
    
#EXPLOSION METHOOD
def explode(x, y):
        explosion = Truck_Explosion(x, y)
        all_sprites.add(explosion)
def P1_Explode(x, y):
    p1_explosion = Car_Explosion(x, y)
    all_sprites.add(p1_explosion)

# GAME LOOP:
#   Process Events
#   Upadte
#   Draw
start = True
end = False
last_end = pygame.time.get_ticks()
end_delay = 1000
running = True
while running:

    now = pygame.time.get_ticks()

    #SHOW START SCREEN ONCE
    if start:
        show_start_screen()
        start = False

    if end:
        if now - last_end > end_delay:
            show_gameover_screen()
            end = False
            all_sprites.empty()
            Score_Tally = 0
            player == Player()
            all_sprites.add(player)
            new_mob()

    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_0:
                Radio(0)
                radio_bar.load_radio(0)
            elif event.key == pygame.K_1:
                Radio(1)
                radio_bar.load_radio(1)
            elif event.key == pygame.K_2:
                Radio(2)
                radio_bar.load_radio(2)
            elif event.key == pygame.K_3:
                Radio(3)
                radio_bar.load_radio(3)
            elif event.key == pygame.K_4:
                Radio(4)
                radio_bar.load_radio(4)
            elif event.key == pygame.K_5:
                Radio(5)
                radio_bar.load_radio(5)

    
    if now - last_ram > ram_delay:
        last_ram = now
        new_guard()

    if now - last_strap > strap_delay:
        last_strap = now
        new_strap()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        Score_Tally += 1
        explode(hit.rect.centerx, hit.rect.centery)
        new_mob()

    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        if player.getMode() == "Ram_Mode":
            hit.kill()
            explode(hit.rect.centerx, hit.rect.centery)
            new_mob()
        else:
            player.update_health(1)
            hit.kill()
            explode(hit.rect.centerx, hit.rect.centery)
            new_mob()
            if player.get_health() > 3:
                P1_Explode(player.rect.centerx, player.rect.centery)
                player.kill()
                player.hide()
                last_end = pygame.time.get_ticks()
                end = True

    hits = pygame.sprite.spritecollide(player, bullet_straps, False)
    for hit in hits:
        player.load_Bullets()
        hit.kill()
        
        
    all_sprites.update()

    #CHECK FOR RAM
    hits = pygame.sprite.spritecollide(player, guards, True)
    for hit in hits:
        player.setMode("Ram_Mode")
        
    #screen.blit(bg, bg_rect)
    rel_y = bg_y % bg.get_rect().height
    screen.blit(bg, (0, rel_y - bg.get_rect().height))
    if rel_y < HEIGHT:
        screen.blit(bg, (0, rel_y))
    bg_y += 7
    all_sprites.draw(screen)

    draw_text(screen, str(Score_Tally), 28, 85, HEIGHT -100, WHITE)

    pygame.display.flip()

pygame.quit()
