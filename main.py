import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
COORDSX, COORDSY = 450, 250

possible_spawns = [50, 100,  150, 200, 250, 300, 350, 400, 450]
bullets = []
monsters = []
BULLET_VEL = 14
MONSTER_VEL = 5
SPACESHIP_WITDH, SPACESHIP_HEIGHT = 55, 40
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
BORDER = pygame.Rect(0, 0, 900, 500)

FPS = 60
VEL = 5
GAME_INFO = {
    "MAX_MONSTERS": 5,
    "SCORE": 0

}

MONSTER_HIT = pygame.USEREVENT + 1
PLAYER_HIT = pygame.USEREVENT + 2
MONSTER_SPAWN = pygame.USEREVENT + 3
DIFFICULTY_INCREASE = pygame.USEREVENT + 4

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    "Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WITDH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

def player_movementhandle(pressed_keys, player):
        if pressed_keys[pygame.K_a] and player.x - VEL > 0:
            player.x -= VEL
        if pressed_keys[pygame.K_d] and player.x + VEL < 450:
            player.x += VEL
        if pressed_keys[pygame.K_w] and player.y - VEL > 0:
            player.y -= VEL
        if pressed_keys[pygame.K_s] and player.y + VEL < 450:
            player.y += VEL

def player_bulletshandle(bullets):
    for bullet in bullets:
        bullet.x += BULLET_VEL
        if bullet.x > WIDTH:bullets.remove(bullet)

def hitreg(bullets, monsters, player):
    for monster in monsters:
        if monster.colliderect(player):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))
                print("!")
        for bullet in bullets:
            if bullet.colliderect(monster):
                pygame.event.post(pygame.event.Event(MONSTER_HIT))
                bullets.remove(bullet)
                monsters.remove(monster)

def mob_handle(monsters):
    for monster in monsters:
        monster.x -= MONSTER_VEL
        if monster.x < -50:monsters.remove(monster)

def draw_window(player, bullets, monsters):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(YELLOW_SPACESHIP, (player.x, player.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for monster in monsters:
        pygame.draw.rect(WIN, BLACK, monster)

    pygame.display.update()

def monsterspawner():
    if len(monsters) < GAME_INFO["MAX_MONSTERS"]:
        monster = pygame.Rect(
            920, random.choice(possible_spawns), SPACESHIP_WITDH, SPACESHIP_HEIGHT)
        monsters.append(monster)


clock = pygame.time.Clock()

current_time = 0

def main():
    player = pygame.Rect(100, 300, SPACESHIP_WITDH, SPACESHIP_HEIGHT)
    #monster = pygame.Rect(150, 950, SPACESHIP_WITDH, SPACESHIP_HEIGHT)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < 5:
                    bullet = pygame.Rect(
                        player.x + player.width - 5, player.y + player.height/2 - 2, 10, 5)
                    bullets.append(bullet)
    
            if event.type == MONSTER_HIT:
                GAME_INFO["SCORE"] += 1
            
            elif event.type == PLAYER_HIT:
                print("hit!")
            
            elif event.type == DIFFICULTY_INCREASE:
                print("hi")
                GAME_INFO["MAX_MONSTERS"] += 5 

        current_time = pygame.time.get_ticks()
        #print(current_time)
        pressed_keys = pygame.key.get_pressed()
        player_movementhandle(pressed_keys, player)
        time_timer = 0
        if current_time > 2000:
            time_timer = pygame.time.get_ticks()

        if current_time - time_timer != 0:
            monsterspawner()

        #pygame.time.set_timer(DIFFICULTY_INCREASE, 10000)
        hitreg(bullets, monsters, player)
        player_bulletshandle(bullets)
        mob_handle(monsters)
        
        draw_window(player, bullets, monsters)

    pygame.quit()

if __name__ == "__main__":
    main()