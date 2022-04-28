import pygame
import random
import math

from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background Image
# Background Source(download and use illustrator) : https://www.freepik.com/
bgImg = pygame.image.load("background.png")

# Background music
# Sound file Source : https://pixabay.com/
mixer.music.load("retro-wave-melodie-128-bpm-8970.mp3")
mixer.music.play(-1)

# Title and Icon
# Icon source : https://www.flaticon.com/
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Score
# Font Source : https://www.dafont.com/
score_value = 0
# font = pygame.font.Font("freesansbold.ttf", 32)
font = pygame.font.Font("crackvetica.ttf", 32)
textX = 10
textY = 10


def showScore(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over text
over = pygame.font.Font("Bad Signal.otf", 64)


def game_over_text():
    over_text = over.render("GAME OVER !!", True, (255, 255, 255))
    screen.blit(over_text, (240, 250))


# Player (size-64pixel)
playerImg = pygame.image.load("player.png")
playerX = 380
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    # Enemy (size-64pixel)
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(40, 160))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet (size-32pixel)
# state-ready : can't see the bullet on the screen
# state-fire : bullet is moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB value for screen background
    screen.fill((100, 100, 100))

    # Background
    screen.blit(bgImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound("mixkit-game-whip-shot-1512.wav")
                bullet_sound.play()
                # fire bullet from current x coordinate(centre) of spaceship
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change

    # setting boundaries for player
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # sound file bitrate conversion Source : https://online-audio-converter.com/
            explosion_sound = mixer.Sound("explosion-6055-bitrate128.mp3")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 25
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(40, 160)

        # putting enemy on the screen
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # putting player/score on the screen
    player(playerX, playerY)
    showScore(textX, textY)

    pygame.display.update()
