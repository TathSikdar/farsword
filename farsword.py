import pygame
import sys
import action

pygame.init()


def saveGame():
    global state
    with open("saveFile", "w") as file:
        file.write(state)

def readSave():
    global state

    with open("saveFile", "r") as file:
        return state

def menu():
    global state

    # StaticImage Objects
    backgroundImage = action.StaticImage(screen, "Assets\Start screen background.jpg")
    backgroundImage.scale((1280, 720))
    newGameImage = action.StaticImage(screen, "Assets\\New game.png")
    continueImage = action.StaticImage(screen, "Assets\Continue.png")
    titleImage = action.StaticImage(screen, "Assets\\Title.png")
    continueErrorImage = action.StaticImage(screen, "Assets\Save error.png")

    # Static Drawings
    backgroundImage.display(0,0)
    newGameImage.display(screenWidth * 2 / 3 - newGameImage.width / 2 + padding, screenHeight * 2 / 3)
    continueImage.display(screenWidth / 3 - continueImage.width / 2 - padding, screenHeight * 2 / 3)
    titleImage.display(screenWidth / 2 - titleImage.width / 2 + 10, screenHeight / 7)

    fileFlag = True

    while True:
        clock.tick(fps)
        pygame.display.update()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:

                    # New game button mouse left click
                    if pygame.Rect.collidepoint(newGameImage.rect, pygame.mouse.get_pos()):
                        state = "Stage 1"
                        return

                    # Continue button mouse left click
                    elif pygame.Rect.collidepoint(continueImage.rect, pygame.mouse.get_pos()) and fileFlag:
                        try:
                            state = readSave()
                            return
                        except:
                            continueErrorImage.display(screenWidth/2 - continueErrorImage.width/2, screenHeight - 330)
                            fileFlag = False


def stage1():
    global state

    while True:
        clock.tick(fps)
        pygame.display.update()
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#-----------------------------------------------------VARIABLES---------------------------------------------------------

# Display surface
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Shitkiro: Shadows Die")

# Fonts
# titleFont = pygame.font.SysFont("Roboto Slab", 100)
# subtitleFont = pygame.font.SysFont("Roboto Regular", 20)
# regularFont = pygame.font.SysFont("Roboto Regular", 15)
padding = 50

# Clock
fps = 60
clock = pygame.time.Clock()

state = "Menu"

# -------------------------------------------------------MAIN-----------------------------------------------------------



while True:
    if state == "Menu":
        menu()
    elif state == "Stage 1":
        stage1()