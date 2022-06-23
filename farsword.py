import pygame
import sys
from action import StaticImage
from action import Player
from action import Boss1
from action import AttackEnum

pygame.init()


def saveGame():
    global state
    with open("saveFile", "w") as file:
        file.write(state)

def readSave():
    with open("saveFile", "r") as file:
        return file.readline()

def colisions(player, boss):
    if pygame.sprite.collide_mask(boss.sword, player) and not boss.sword.hasAttacked:
        boss.sword.hasAttacked = True # Stops multiple hit registers per attack

        if not boss.isBlockable: # Unblockable attack
            player.hp -=1
            boss.unblockableHit.play()

        elif player.attackMovement != AttackEnum.PLAYERDEFEND: # Player not defending
            player.hp -= 1
            boss.attackHit.play()

        elif player.attackMovement == AttackEnum.PLAYERDEFEND and boss.isBlockable: # Player defended
            player.deflectedSound.play()

    if pygame.sprite.collide_mask(player.sword, boss) and not player.sword.hasAttacked:
        player.sword.hasAttacked = True # Stops multiple hit registers per attack
        boss.hp -= 1
        player.attackHit.play()

    for i in range(len(boss.waveAttackList[1])): # Projectile
        if pygame.sprite.collide_mask(player, boss.waveAttackList[1][i]):
            boss.waveAttackList[1].pop(i)
            if player.attackMovement != AttackEnum.PLAYERDEFEND: # Player not defending
                player.hp -= 1
                boss.attackHit.play()
            else:
                player.deflectedSound.play()

def menu():
    global state

    # StaticImage Objects
    backgroundImage = StaticImage(screen, "assets\menu\\background.jpg")
    backgroundImage.scale((1280, 720))
    newGameImage = StaticImage(screen, "assets\menu\\New game.png")
    continueImage = StaticImage(screen, "assets\menu\Continue.png")
    titleImage = StaticImage(screen, "assets\menu\\Title.png")
    continueErrorImage = StaticImage(screen, "assets\menu\Save error.png")

    # Static Drawings
    backgroundImage.display(0,0)
    newGameImage.display(screenWidth * 2 / 3 - newGameImage.width / 2 + padding, screenHeight * 2 / 3)
    continueImage.display(screenWidth / 3 - continueImage.width / 2 - padding, screenHeight * 2 / 3)
    titleImage.display(screenWidth / 2 - titleImage.width / 2 + 10, screenHeight / 7)

    # Music
    pygame.mixer.music.load("assets\menu\\backgroundMusic.mp3")
    pygame.mixer.music.play(-1)

    fileFlag = True

    while True:
        clock.tick(FPS)
        pygame.display.update()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:

                    # Left click new game
                    if pygame.Rect.collidepoint(newGameImage.rect, pygame.mouse.get_pos()):
                        state = "Stage 1 Tutorial"
                        pygame.mixer.music.fadeout(3000)
                        return

                    # Left click continue
                    elif pygame.Rect.collidepoint(continueImage.rect, pygame.mouse.get_pos()) and fileFlag:
                        try:
                            state = readSave()
                            pygame.mixer.music.fadeout(3000)
                            return
                        except:
                            continueErrorImage.display(screenWidth/2 - continueErrorImage.width/2, screenHeight - 330)
                            fileFlag = False

def stage1Tutorial():
    global state

    # Instantiation
    player = Player(screen, FPS, (screenWidth/3 + 10, screenHeight - 250))

    # Static images
    backgroundImage = StaticImage(screen, "assets\stage1\\background.png")
    backgroundImage.scale((1280, 720))
    controlsTutorialImage = StaticImage(screen, "assets\stage1\controlsTutorial.png")
    controlsTutorialImage.scale((round(controlsTutorialImage.width * 1.5), round(controlsTutorialImage.height * 1.5)))
    hudTutorialImage = StaticImage(screen, "assets\stage1\hudTutorial.png")
    pressEnterText = StaticImage(screen, "assets\stage1\pressEnterText.png")



    while True:
        clock.tick(FPS)
        pygame.display.update()

        # Blit static images
        backgroundImage.display(0, 0)
        controlsTutorialImage.display(screenWidth/2 - controlsTutorialImage.width/2, 150)
        hudTutorialImage.display(screenWidth/2 - hudTutorialImage.width/2, player.hudCentreY + 11)
        pressEnterText.display(screenWidth/2 - pressEnterText.width/2, screenHeight/2 + 30)

        # EVENTS
        for event in pygame.event.get():

            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse Downstroke
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Left Click
                if event.button == 1:
                    player.moveAttack()

                # Right Click
                elif event.button == 3:
                    player.moveDefend()

            # Key Downstroke
            elif event.type == pygame.KEYDOWN:

                # A [Left]
                if event.key == pygame.K_a:
                    player.moveLeft()

                # D [Right]
                elif event.key == pygame.K_d:
                    player.moveRight()

                # Space [Dash]
                if event.key == pygame.K_SPACE:
                    player.moveDash()

                # Enter [Continue to Stage 1]
                if event.key == pygame.K_RETURN:
                    screen.blit(pygame.image.load("assets\stage1\\transitionScreen.png"), (0,0))
                    pygame.display.update()
                    state = "Stage 1"
                    pygame.time.delay(1000)
                    return

            # Key Upstroke
            elif event.type == pygame.KEYUP:

                # A [Left]
                if event.key == pygame.K_a:  # and player.aIsPressed:
                    player.moveStopLeft()

                # D [Right]
                if event.key == pygame.K_d:  # and player.dIsPressed:
                    player.moveStopRight()

        player.animate()

def stage1():
    global state

    # Save Game
    saveGame()

    # Instanciation
    player = Player(screen, FPS, (0, screenHeight - 250))
    boss1 = Boss1(screen, FPS, player)

    # Static Images & music
    backgroundImage = StaticImage(screen, "assets\stage1\\background.png")
    backgroundImage.scale((1280, 720))
    pygame.mixer.music.load("assets\stage1\\backgroundMusic.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.8)

    while True:
        clock.tick(FPS)
        pygame.display.update()
        backgroundImage.display(0, 0)

        # EVENTS
        for event in pygame.event.get():

            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse Downstroke
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Left Click
                if event.button == 1:
                    player.moveAttack()

                # Right Click
                elif event.button == 3:
                    player.moveDefend()

            # Key Downstroke
            elif event.type == pygame.KEYDOWN:

                # A [Left]
                if event.key == pygame.K_a:
                    player.moveLeft()

                # D [Right]
                elif event.key == pygame.K_d:
                    player.moveRight()

                # Space [Dash]
                if event.key == pygame.K_SPACE:
                    player.moveDash()

            # Key Upstroke
            elif event.type == pygame.KEYUP:

                # A [Left]
                if event.key == pygame.K_a:
                    player.moveStopLeft()

                # D [Right]
                if event.key == pygame.K_d:
                    player.moveStopRight()

        boss1.animate()
        player.animate()
        if player.hp == 0:
            state = "You died"
            return
        if player.hp != 0 and boss1.hp != 0:
            colisions(player, boss1)

def dead():
    global state

    screen.blit(pygame.image.load("assets\dead\youDied.png"), (0,0))
    pygame.display.update()

    pygame.mixer.music.load("assets\dead\deathSound.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.fadeout(4000)
    pygame.time.delay(3000)
    state = "Menu"


#-----------------------------------------------------VARIABLES---------------------------------------------------------
# Display surface
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Shitkiro: Shadows Die")

padding = 50

# Clock
FPS = 60
clock = pygame.time.Clock()

state = "Menu"

# -------------------------------------------------------MAIN-----------------------------------------------------------
while True:
    if state == "Menu":
        menu()
    elif state == "Stage 1 Tutorial":
        stage1Tutorial()
    elif state == "Stage 1":
        stage1()
    elif state == "You died":
        dead()