import pygame
import os
WIDTH = 600
HEIGHT = 1000
FPS = 30
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

#ASSET FOLDER
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Sprinter")

clock = pygame.time.Clock()

#BACKGROUND
bg = pygame.image.load(os.path.join(img_folder, "Road.png")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_rect = bg.get_rect()
bg_y = 0

#DRAW TEXT FUNCTION
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#SHOW START SCREEN FUNCTION
def show_start_screen():

    #screen.blit(background, background_rect)
    screen.blit(bg, bg_rect)
    draw_text(screen, "Street Sprinter", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "ARROW KEYS TO MOVE AND SPACE TO SHOOT!", 18, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "PRESS ANY KEY TO BEGIN!", 18, WIDTH / 2, HEIGHT * 3 / 4)
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

#ENEMY CLASS
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
        self.image = pygame.transform.scale(self.image, (230, 350))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 10)

    #Update Methood
    def update(self):
        self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.red_cars = [
                            pygame.image.load(os.path.join(img_folder, "P1_Car_RED0.png")).convert(), 
                            pygame.image.load(os.path.join(img_folder, "P1_Car_RED1.png")).convert(), 
                            pygame.image.load(os.path.join(img_folder, "P1_Car_RED2.png")).convert()
                            ]
        self.count = 0
        self.image = self.red_cars[self.count]
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):

        self.image = self.red_cars[self.count]
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.image.set_colorkey(BLACK)
        self.count += 1
        if self.count > 2:
            self.count = 0


    # RETURNS A LIST, keystate, OF ALL PRESSED KEYS
        keystate = pygame.key.get_pressed()


    # CHECKS TO SEE WHICH KEYS WERE IN THE LIST (A.K.A. PRESSED)
        if keystate[pygame.K_d]:
            self.rect.x += 5
        if keystate[pygame.K_a]:
            self.rect.x += -5
        if keystate[pygame.K_w]:
            self.rect.y += -5
        if keystate[pygame.K_s]:
            self.rect.y += 5
    
#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
Grey_Truck = Enemy_G()
all_sprites.add(Grey_Truck)

# GAME LOOP:
#   Process Events
#   Upadte
#   Draw
start = True
running = True
while running:

    #SHOW START SCREEN ONCE
    if start:
        show_start_screen()
        start = False

    clock.tick(FPS)

    #RROCESS EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    #screen.blit(bg, bg_rect)
    rel_y = bg_y % bg.get_rect().height
    screen.blit(bg, (0, rel_y - bg.get_rect().height))
    if rel_y < HEIGHT:
        screen.blit(bg, (0, rel_y))
    bg_y += 7
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()

