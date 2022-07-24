import pygame
import random
import os
import sys

WIDTH = 900
HEIGHT = 600
FPS = 75

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
SLATEGRAY = (112, 128, 144)
LIGHTGREY = (165, 175, 185)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Pong')

game_folder = os.path.dirname(__file__)
snd_folder = os.path.join(game_folder, "GameArt\Shmup\snd")
#bounce = pygame.mixer.Sound(os.path.join(snd_folder, 'pew.wav'))

player_score = 0
opponent_score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,70))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centery = (HEIGHT / 2)
        self.rect.x = 10
        self.speedy = 8

    def update(self): 
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedy -= 8
        if keystate[pygame.K_s]:
            self.speedy += 8
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Opponent(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centery = (HEIGHT / 2)
        self.rect.x = (WIDTH - 20)
        self.speedy = 0

    def update(self):
        self.speedy = 0
        if self.rect.top > pong.rect.top:
            self.speedy -= 7.15
        if self.rect.bottom < pong.rect.bottom:
            self.speedy += 7.25
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Pong(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedx = 6
        self.speedy = 8

    def update(self):
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy *= -1
            #bounce.play()
        if self.rect.left < 0 or self.rect.right > WIDTH:
            #bounce.play()
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
            self.speedy *= random.choice((1,-1))
            self.speedx *= random.choice((1,-1))
        self.rect.y += self.speedy
        self.rect.x += self.speedx

def contact():
    contactPlayer = pygame.sprite.spritecollide(player, mob, False)
    contactOpponent = pygame.sprite.spritecollide(opponent, mob, False)
    if contactPlayer or contactOpponent:
        #bounce.play()
        pong.speedx *= -1 

def scoreTracker():
    global player_score
    global opponent_score
    if pong.rect.left < 0:
        opponent_score += 1
    if pong.rect.right > WIDTH:
        player_score += 1
    if opponent_score == 5:
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_r:
                        opponent.rect.centery = (HEIGHT / 2)
                        opponent.rect.x = (WIDTH - 20)
                        player.rect.centery = (HEIGHT / 2)
                        player_score = 0
                        opponent_score = 0
                        game_loop()
            screen.fill(BLACK)
            draw_score(screen, 'Opponent WINS', 'Press R to Restart', 24, WIDTH / 2, (HEIGHT / 2 - 12))
            pygame.display.flip()
    if player_score == 5:
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_r:
                        player_score = 0
                        opponent_score = 0
                        opponent.rect.centery = (HEIGHT / 2)
                        opponent.rect.x = (WIDTH - 20)
                        player.rect.centery = HEIGHT / 2
                        game_loop()
            screen.fill(BLACK)
            draw_score(screen, 'Player WINS', 'Press R to Restart', 24, WIDTH / 2, (HEIGHT / 2 - 12))
            pygame.display.flip()
    
def boundary():
    boundary = pygame.Surface((1, HEIGHT))
    boundary.fill(WHITE)
    boundary_rect = boundary.get_rect()
    boundary_rect.centerx = WIDTH / 2
    screen.blit(boundary, boundary_rect)

font_name = pygame.font.match_font('calibri')
def draw_score(surf, player, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    player_surface = font.render(player, True, WHITE)
    player_rect = player_surface.get_rect()
    player_rect.midtop = (x, y)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.top = (player_rect.bottom + 5)
    text_rect.centerx = player_rect.centerx
    surf.blit(text_surface, text_rect)
    surf.blit(player_surface, player_rect)

def screen_button(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)

def start_menu():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    game_loop()
        screen.fill(BLACK)
        screen_button(screen, 'Press SPACE to START', 24, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()

all_sprites = pygame.sprite.Group()
mob = pygame.sprite.Group()
player = Player()
opponent = Opponent()
pong = Pong()
all_sprites.add(player)
all_sprites.add(opponent)
mob.add(pong)

def game_loop():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        all_sprites.update()
        mob.update()

        contact()
        scoreTracker()

        screen.fill(BLACK)
        boundary()
        all_sprites.draw(screen)
        mob.draw(screen)
        draw_score(screen, 'Player', str(player_score), 18, 225, 10)
        draw_score(screen, 'Opponent', str(opponent_score), 18, WIDTH - 225, 10)
        pygame.display.flip()

while True:
    start_menu()