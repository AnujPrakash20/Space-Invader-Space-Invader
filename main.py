import pygame
from pygame import mixer
import random
import math
# initialize the pygame
pygame.init()

# create the screen
display = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

#Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invador")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
player = pygame.image.load('spaceship1.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemyIMG = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
no_of_enemy=6
for i in range(no_of_enemy):
    enemyIMG.append(pygame.image.load("ufo.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# Bullet

bulletIMG = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

#Score
score=0
font=pygame.font.Font("freesansbold.ttf",32)
text_x=10
text_y=10

#Game over
game_over=pygame.font.Font("freesansbold.ttf",64)

def showscore(x,y):
    scor=font.render("Score : "+str(score),True,(255,255,255))
    display.blit(scor,(x,y))

def exit():
    game_ove=game_over.render("GAME OVER",True,(255,255,255))
    display.blit(game_ove,(200,250))


def Player(x, y):
    display.blit(player, (x, y))


def enemy(x, y,i):
    display.blit(enemyIMG[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    display.blit(bulletIMG, (x + 16, y + 10))

# def isCollision(bulletx,bullety,enemyx,enemyy):
#     distance=math.sqrt((math.pow((bulletx-enemyx),2)+(math.pow((bullety-enemyy),2))
#     if distance < 27:
def isCollision(enemyx,enemyy,bulletx,bullety) :
    distance = math.sqrt((math.pow((enemyx-bulletx),2))+(math.pow((enemyy-bullety),2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop

running = True
while running:
    # RGB
    display.fill((0, 0, 0))
    display.blit(background, (0, 0))
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False

        # Pressing/Releasing of key
        if events.type == pygame.KEYDOWN:
            # print("Key pressed")
            if events.key == pygame.K_LEFT:
                player_x_change = -5
            if events.key == pygame.K_RIGHT:
                player_x_change = 5
            if events.key == pygame.K_SPACE:# firing bullet by tapping spacebar
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x=player_x
                    fire(bullet_x, bullet_y)

        if events.type == pygame.KEYUP:
            if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:  # Setting boundaries and movement of the enemy
        player_x = 0
    if player_x >= 736:
        player_x = 736


    for i in range(no_of_enemy):
        if enemy_y[i]>440:
            for j in range(no_of_enemy):
                enemy_y[j]=2000
            exit()
            break
        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:  # Setting boundaries and movement of the enemy
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]
        collision= isCollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            collision_sound=mixer.Sound("laser.wav")
            collision_sound.play()
            bullet_y=480
            bullet_state="ready"
            score +=1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i],i)

    #shooting multiple bullets
    if bullet_y <= 0 :
        bullet_y = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    #collision


    Player(player_x, player_y)
    showscore(text_x,text_y)
    pygame.display.update()
