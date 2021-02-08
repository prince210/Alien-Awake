import pygame, sys
import random
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))

###################### menu #################################################
isOpen = True
isONorOF = "ON"
blinkCount = 0
isGameOver = False

class Menu:
    def __init__(self):
        self.textMainMenu = pygame.font.Font('Fluo Gums.ttf', 50)
        self.start_game = pygame.font.Font('sewer.ttf', 50)
        self.options = pygame.font.Font('sewer.ttf', 50)
        self.arraow = pygame.image.load("right-arrow.png")
        self.background_img_menu = pygame.image.load('background.png')
        self.arraowX = 160
        self.arraowY = 300
        self.arraowChangeY = 0

    def menuBasics(self):
        pygame.display.set_caption("alien awake")
        icon = pygame.image.load("ufo.png")
        pygame.display.set_icon(icon)

    def drawMainMenu(self,x, y, text):
        renderedText = self.textMainMenu.render(text, True, (255, 255, 255))
        screen.blit(renderedText, (x, y))

    def drawStartGame(self,x, y, text):
        renderedText = self.start_game.render(text, True, (255, 255, 255))
        screen.blit(renderedText, (x, y))

    def drawOptions(self,x, y, text, volume):
        renderedText = self.options.render(text + " : " + volume, True,
                                           (255, 255, 255))
        screen.blit(renderedText, (x, y))

    def displayBackground(self):
        screen.blit(self.background_img_menu, (0, 0))

    def drawArrow(self,x, y):
        screen.blit(self.arraow, (x, y))


###################### menu #################################################

## Title and icon
pygame.display.set_caption("alien awake")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
tillCrossPressed = True

######    creating score    #######
score = 0
high_score = 0
font = pygame.font.Font('freesansbold.ttf',32)
high_score_font = pygame.font.Font('freesansbold.ttf',50)


## adding sounds
mixer.music.load("background_16bit.wav")  ## loading of music file
mixer.music.play(-1)  ## -1 denotes infintie time music will play
isMute = False
missileSound = mixer.Sound("missile_16bit.wav")
ExlplosionSound = mixer.Sound("Explosion_16bit.wav")

## game over display
game_over_text = pygame.font.Font('freesansbold.ttf', 70)

## Adding background
background_img = pygame.image.load("background.png").convert()

def drawText(x=10, y=10):
    renderedText = font.render("Score : " + str(score), True,
                               (255, 255, 255))  ## arg1 = text to display, arg2 = , arg3 = color
    screen.blit(renderedText, (x, y))

def gameOverDisplay():
    over_text = game_over_text.render(" GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (150, 150))

def dispUpdateHighScore(score):
    global high_score
    if score > high_score:
        high_score = score

    renderedText = high_score_font.render("High Score : " + str(high_score), True,(255, 255, 255))
    screen.blit(renderedText, (230, 400))

def restartText():
    renderedText = font.render(" PRESS ENTER TO RESTART ", True, (255, 255, 255))
    screen.blit(renderedText, (170, 300))

class Player:
    def __init__(self):
        self.bullet1 = pygame.image.load("bullet.png")
        self.player1 = pygame.image.load("space-invaders.png")
        self.playerX = 370
        self.playerY = 480
        self.changeAcrossAxis = 0  ## change in X axis
        self.bulletX = 0
        self.bulletY = 480
        self.bulletChangeAcrossAxisY = 7  ## change in Y axis
        self.bulletState = "ready"
        self.lock = True

    def drawPlayer(self,playerOnX, playerOnY):
        screen.blit(self.player1, (
            playerOnX, playerOnY))

    def fireBullet(self,x, y):
        self.bulletState = "fire"
        screen.blit(self.bullet1, (x + 16, y + 10))

class Enemy:
    def __init__(self):
        self.num_of_enemies = 6
        self.enemy1 = []
        self.enemyX = []
        self.enemyY = []
        self.enemyChangeAcrossAxisX = []
        self.enemyChangeAcrossAxisY = []
        for i in range(self.num_of_enemies):
            self.enemy1.append(pygame.image.load("ufo.png"))
            self.enemyX.append(random.randint(0, 736))
            self.enemyY.append(random.randint(50, 150))
            self.enemyChangeAcrossAxisX.append(2)  ## change in X axis
            self.enemyChangeAcrossAxisY.append(30)  ## change in Y axis

    def drawEnemy(self,x, y, i):
        screen.blit(self.enemy1[i], (x, y))

    ### collision
    def isCollision(self,enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(
            math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))  ## distance between bullet and enemy
        if distance <= 27:
            return True

newPlayer = Player()
newEnemy = Enemy()
newMenu = Menu()

while tillCrossPressed:
    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))

    while isOpen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isOpen = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    newMenu.arraowY = 400
                if event.key == pygame.K_UP:
                    newMenu.arraowY = 300
                if event.key == pygame.K_RETURN and newMenu.arraowY == 300:
                    isOpen = False
                if event.key == pygame.K_RETURN and newMenu.arraowY == 400:
                    if isONorOF == "ON":
                        isONorOF = "OFF"
                        mixer.music.stop()
                        missileSound.stop()
                        ExlplosionSound.stop()
                    else:
                        isONorOF = "ON"
                        mixer.music.play(-1)
                        missileSound.play()
                        ExlplosionSound.play()

        screen.fill((0, 0, 0))
        newMenu.displayBackground()

        newMenu.drawArrow(newMenu.arraowX, newMenu.arraowY)
        newMenu.drawMainMenu(120, 130, "ALIEN AWAKE")
        newMenu.drawStartGame(200, 300, "START GAME")
        newMenu.drawOptions(200, 400, "SOUND", isONorOF)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tillCrossPressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                newPlayer.changeAcrossAxis = -4
            if event.key == pygame.K_RIGHT:
                newPlayer.changeAcrossAxis = 4
            if event.key == pygame.K_SPACE:
                if newPlayer.bulletState == "ready":
                    if isONorOF == "ON":
                        missileSound.play()
                    newPlayer.bulletX = newPlayer.playerX
                    newPlayer.fireBullet(newPlayer.bulletX, newPlayer.bulletY)
            if event.key == pygame.K_ESCAPE:
                isOpen = True
            if event.key == pygame.K_RETURN and isGameOver == True:
                isOpen = True
                isGameOver = False
                mixer.music.play(-1)
                score = 0
                newPlayer = Player()
                newEnemy = Enemy()
                isONorOF = "ON"
                blinkCount = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                newPlayer.changeAcrossAxis = 0

    ## adding up the change
    newPlayer.playerX += newPlayer.changeAcrossAxis

    ### if player goes out of boundary
    if newPlayer.playerX <= 0:
        newPlayer.playerX = 0
    elif newPlayer.playerX >= 736:
        newPlayer.playerX = 736

    for i in range(newEnemy.num_of_enemies):
        if newEnemy.enemyY[i] >= 440:
            for j in range(newEnemy.num_of_enemies):
                newEnemy.enemyY[j] = 2000
            gameOverDisplay()
            isGameOver = True
            mixer.music.stop()
            dispUpdateHighScore(score)
            if blinkCount < 120:
                restartText()
            break
        newEnemy.enemyX[i] += newEnemy.enemyChangeAcrossAxisX[i]
        if newEnemy.enemyX[i] <= 0:
            newEnemy.enemyChangeAcrossAxisX[i] = 2
            newEnemy.enemyY[i] += newEnemy.enemyChangeAcrossAxisY[i]
        elif newEnemy.enemyX[
            i] >= 736:
            newEnemy.enemyChangeAcrossAxisX[i] = -2
            newEnemy.enemyY[i] += newEnemy.enemyChangeAcrossAxisY[i]

        if newEnemy.isCollision(newEnemy.enemyX[i], newEnemy.enemyY[i], newPlayer.bulletX,
                                newPlayer.bulletY):
            newPlayer.bulletY = 480
            newPlayer.bulletState = "ready"
            score += 1
            newEnemy.enemyX[i] = random.randint(0, 736)
            newEnemy.enemyY[i] = random.randint(50, 150)
            if isONorOF == "ON":
                ExlplosionSound.play()

        newEnemy.drawEnemy(newEnemy.enemyX[i], newEnemy.enemyY[i], i)
        # screen.blit(crossing_line,(0,400))
    ### as soon as bullet reaches crosses the screen we are again ready to fire the bullet and coordinates resets to coordinate of space ship
    if newPlayer.bulletY <= 0:
        newPlayer.bulletY = 480
        newPlayer.bulletState = "ready"

    if newPlayer.bulletState == "fire":
        newPlayer.fireBullet(newPlayer.bulletX, newPlayer.bulletY)
        newPlayer.bulletY -= newPlayer.bulletChangeAcrossAxisY

    blinkCount += 1
    if blinkCount > 240:
        blinkCount = 0

    newPlayer.drawPlayer(newPlayer.playerX, newPlayer.playerY)
    drawText()
    clock.tick(120)
    pygame.display.update()


pygame.quit()
