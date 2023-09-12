import pygame
import random
from pygame import mixer
import os

path = "Alien Assault - Pygame"
os.chdir(path)

# Initialize the pygame
pygame.init()

# Create screen (width, height) in pixels
# Left-To-Right: Width, Top-To-Bottom: Height
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")
startImg = pygame.image.load("start.png")
# Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption("Alien Assault")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

def welcome():
    game_quit = False
    start_font = pygame.font.Font("freesansbold.ttf",32)
    clock = pygame.time.Clock()

    def start():
        start = start_font.render("WELCOME TO ALIEN ASSAULT!!", True, (50,24,71))
        screen.blit(start, (140,230))
        start = start_font.render("PRESS 1 FOR EASY MODE!", True, (255,255,255))
        screen.blit(start, (180,290))
        start = start_font.render("PRESS 2 FOR HARD MODE!", True, (0,0,0))
        screen.blit(start, (180,335))

    while not game_quit:
        screen.fill((133,189,67))
        screen.blit(startImg, (-35,0))
        start()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
        
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()

mode = welcome()

# Player 64 by 60 pixels
PlayerImg = pygame.image.load("player.png")
PlayerX = 370
PlayerY = 480
PlayerX_Change = 0
PlayerX_NewChange1 = -3
PlayerX_NewChange2 = 3

# Enemy 64 by 60 pixels
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_Change = []
EnemyY_Change = []
EnemyX_Change_i = 1
EnemyX_NewChange = 1
num = 2
for i in range(num):
    EnemyImg.append(pygame.image.load("enemy.png"))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_Change.append(EnemyX_Change_i)
    EnemyY_Change.append(40)

# Bullet 32 by 32 pixels
BulletImg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 480
BulletY_Change = 8
BulletY_NewChange = 0
Bullet_State = "Ready"  # Ready - Bullet off screen; Fire - Bullet is moving

# Score
score = 0
highscore = ""
previous_score = 5
font = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 10
scoreY = 10
bullets = 0
with open("highscore.txt") as f:
    highscore = f.read()    

# Clock and fps
Clock = pygame.time.Clock()
fps = 60

# Game Over
Game_Over_font = pygame.font.Font("freesansbold.ttf", 64)

def update(num):
    num += 1
    EnemyImg.append(pygame.image.load("enemy.png"))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_Change.append(EnemyX_Change_i)
    EnemyY_Change.append(40)
    return num


def show_score(x, y):
    Score = font.render("Score: " + str(score) + "  HighScore: " + str(highscore), True, (255, 255, 255))
    screen.blit(Score, (x, y))


def Game_Over_text(score, highscore, bullets):
    if score > int(highscore):
        highscore = score
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))
    
    mixer.music.stop()
    over = mixer.Sound("GameOver.mp3")
    over.play()
    GameOverImg = pygame.image.load("GameOver.png")
    screen.blit(GameOverImg,(-30,0))
    Score = font.render("FINAL SCORE: {}".format(score), True, (120,230,203))
    screen.blit(Score, (290, 80))
    Bullets = font.render("BULLETS SHOT: {}".format(bullets), True, (105,58,192))
    screen.blit(Bullets, (280,500))


def Player(x, y):
    screen.blit(PlayerImg, (x, y))  # blit = draw


def Enemy(x, y):
    screen.blit(EnemyImg[i], (x, y))


def Fire_Bullet(x, y):
    global Bullet_State
    Bullet_State = "Fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(x1, y1, x2, y2):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if distance < 27:
        return True
    else:
        return False


if mode == 1:   # EASY MODE -- Normal controls
    running = True
    while running:  # Game Loop running
        # RGB - Red, Green, Blue
        screen.fill((220, 220, 220))
        # Background Image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # QUIT refers to quitting the game
                running = False

            # If keystroke is pressed check whether left or right or up or down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if score >= previous_score:
                        if score < 40:
                            previous_score += 5
                            PlayerX_NewChange1 += -3
                            PlayerX_NewChange2 += 3
                            EnemyX_NewChange += 0.5
                            num = update(num)
                        EnemyX_Change_i = EnemyX_NewChange
                        PlayerX_Change = PlayerX_NewChange1
                        if BulletY_Change < 15:
                            BulletY_NewChange += 1
                            BulletY_Change += BulletY_NewChange
                    else:
                        PlayerX_Change = PlayerX_NewChange1
                if event.key == pygame.K_RIGHT:
                    if score >= previous_score:
                        if score < 40:
                            previous_score += 5
                            PlayerX_NewChange1 += -3
                            PlayerX_NewChange2 += 3
                            EnemyX_NewChange += 0.5
                            num = update(num)
                        EnemyX_Change_i = EnemyX_NewChange
                        PlayerX_Change = PlayerX_NewChange2
                        if BulletY_Change < 15:
                            BulletY_NewChange += 1
                            BulletY_Change += BulletY_NewChange
                    else:
                        PlayerX_Change = PlayerX_NewChange2
                if event.key == pygame.K_SPACE:
                    if Bullet_State == "Ready" and BulletY != 2000:
                        BulletX = PlayerX  # Current x coordinate of spaceship
                        Fire_Bullet(BulletX, BulletY)
                        Bullet_Sound = mixer.Sound("laser.wav")
                        Bullet_Sound.play()
                        bullets += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    PlayerX_Change = 0

        # Checking Boundary of spaceship - Avoid out of bounds
        PlayerX += PlayerX_Change
        if PlayerX <= 0:
            PlayerX = 0
        elif PlayerX >= 736:
            PlayerX = 736

        # Enemy movements
        for i in range(num):
            # Game Over
            if EnemyY[i] > 450:
                for j in range(num):
                    EnemyY[j] = 2000
                PlayerY = 2000
                BulletY = 2000
                Bullet_State == "Ready"
                Game_Over_text(score, highscore, bullets)
                break

            EnemyX[i] += EnemyX_Change[i]
            if EnemyX[i] <= 0:
                EnemyX_Change[i] = EnemyX_Change_i
                EnemyY[i] += EnemyY_Change[i]
            elif EnemyX[i] >= 736:
                EnemyX_Change[i] = -EnemyX_Change_i
                EnemyY[i] += EnemyY_Change[i]

            # Collision
            Collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
            if Collision:
                Explosion_Sound = mixer.Sound("explosion.wav")
                Explosion_Sound.play()
                BulletY = 480
                Bullet_State = "Ready"
                score += 1
                EnemyX[i] = random.randint(0, 735)
                EnemyY[i] = random.randint(50, 150)

            Enemy(EnemyX[i], EnemyY[i])

        # Bullet Movement
        if BulletY <= 0:
            BulletY = 480
            Bullet_State = "Ready"

        if Bullet_State == "Fire":
            Fire_Bullet(BulletX, BulletY)
            BulletY -= BulletY_Change

        Player(PlayerX, PlayerY)
        if BulletY != 2000:
            show_score(scoreX, scoreY)
        pygame.display.update()
        Clock.tick(fps)

else:    # HARD MODE -- Reversed controls
    PlayerX_NewChange1 = 3
    PlayerX_NewChange2 = -3
    running = True
    while running:
        # RGB - Red, Green, Blue
        screen.fill((220, 220, 220))
        # Background Image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # QUIT refers to quitting the game
                running = False

            # If keystroke is pressed check whether left or right or up or down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if score >= previous_score:
                        if score < 40:
                            previous_score += 5
                            PlayerX_NewChange1 += 3
                            PlayerX_NewChange2 += -3
                            EnemyX_NewChange += 0.5
                            num = update(num)
                        EnemyX_Change_i = EnemyX_NewChange
                        PlayerX_Change = PlayerX_NewChange1
                        if BulletY_Change < 15:
                            BulletY_NewChange += 1
                            BulletY_Change += BulletY_NewChange
                    else:
                        PlayerX_Change = PlayerX_NewChange1
                if event.key == pygame.K_RIGHT:
                    if score >= previous_score:
                        if score < 40:
                            previous_score += 5
                            PlayerX_NewChange1 += 3
                            PlayerX_NewChange2 += -3
                            EnemyX_NewChange += 0.5
                            num = update(num)
                        EnemyX_Change_i = EnemyX_NewChange
                        PlayerX_Change = PlayerX_NewChange2
                        if BulletY_Change < 15:
                            BulletY_NewChange += 1
                            BulletY_Change += BulletY_NewChange
                    else:
                        PlayerX_Change = PlayerX_NewChange2
                if event.key == pygame.K_SPACE:
                    if Bullet_State == "Ready" and BulletY != 2000:
                        BulletX = PlayerX  # Current x coordinate of spaceship
                        Fire_Bullet(BulletX, BulletY)
                        Bullet_Sound = mixer.Sound("laser.wav")
                        Bullet_Sound.play()
                        bullets += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    PlayerX_Change = 0

        # Checking Boundary of spaceship - Avoid out of bounds
        PlayerX += PlayerX_Change
        if PlayerX <= 0:
            PlayerX = 0
        elif PlayerX >= 736:
            PlayerX = 736

        # Enemy movements
        for i in range(num):
            # Game Over
            if EnemyY[i] > 450:
                for j in range(num):
                    EnemyY[j] = 2000
                PlayerY = 2000
                BulletY = 2000
                Bullet_State == "Ready"
                Game_Over_text(score, highscore, bullets)
                break

            EnemyX[i] += EnemyX_Change[i]
            if EnemyX[i] <= 0:
                EnemyX_Change[i] = EnemyX_Change_i
                EnemyY[i] += EnemyY_Change[i]
            elif EnemyX[i] >= 736:
                EnemyX_Change[i] = -EnemyX_Change_i
                EnemyY[i] += EnemyY_Change[i]

            # Collision
            Collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
            if Collision:
                Explosion_Sound = mixer.Sound("explosion.wav")
                Explosion_Sound.play()
                BulletY = 480
                Bullet_State = "Ready"
                score += 1
                EnemyX[i] = random.randint(0, 735)
                EnemyY[i] = random.randint(50, 150)

            Enemy(EnemyX[i], EnemyY[i])

        # Bullet Movement
        if BulletY <= 0:
            BulletY = 480
            Bullet_State = "Ready"

        if Bullet_State == "Fire":
            Fire_Bullet(BulletX, BulletY)
            BulletY -= BulletY_Change

        Player(PlayerX, PlayerY)
        if BulletY != 2000:
            show_score(scoreX, scoreY)
        pygame.display.update()
        Clock.tick(fps)
pygame.quit()  # QUIT - type of event & pygame.quit() - function
quit()  # exit() also can be used

# sys.exit() is preferred but you need to import sys module