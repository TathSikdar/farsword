import pygame
import random
from enum import Enum


class StaticImage():
    def __init__(self, surface, image):
        self.image = pygame.image.load(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.surface = surface

    def scale(self, resolutionTuple):
        self.image = pygame.transform.scale(self.image, resolutionTuple)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


class AttackEnum(Enum):
    PLAYERNOATTACK = 0
    PLAYERATTACK = 1
    PLAYERDEFEND = 2
    PLAYERDASH = 3


class WaveProjectile(pygame.sprite.Sprite):
    def __init__(self, display, startX, startY, isFacingRight):
        self.x = startX
        self.y = startY
        self.isFacingRight = isFacingRight
        self.vel = 20
        self.display = display
        self.image = pygame.image.load("assets\\boss1\waveAttack\\0.png")
        self.image = pygame.transform.scale(self.image,
                                            (round(self.image.get_width() / 2), round(self.image.get_height() / 2)))
        if not self.isFacingRight:
            self.image = pygame.transform.flip(self.image, True, False)

    def shoot(self):
        if self.isFacingRight:
            self.display.blit(self.image, (self.x, self.y))
            self.x += self.vel
        else:
            self.display.blit(self.image, (self.x, self.y))
            self.x -= self.vel

        # Mask collision stuff
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)

# For attack masks
class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, classType):
        super().__init__()

        self.hasAttacked = False

        self.x = x
        self.y = y

        self.playerAttackList = [[],[]]  # [Attack1], [Attack2]
        self.playerAttackReversedList = [[],[]]

        self.playerIdleList = []  # Blank
        self.playerMoveList = []  # Blank
        self.playerDefendList = []  # Blank
        self.playerDash = None

        #-----------------------------------------------------------

        self.boss1NormalAttackList = [[],[]]  # [Attack1],[Attack2]
        self.boss1NormalAttackReversedList = [[],[]]

        self.boss1DashList = []  # Full image
        self.boss1DashReversedList = []

        self.boss1UnblockableStrikeList = []
        self.boss1UnblockableStrikeReversedList = []

        self.boss1MoveList = []  # Blank
        self.boss1WaveAttackList = []  # Blank
        self.boss1DeathList = []  # Blank

        # Images in each animation/file
        PLAYERIDLEFRAMES = 2
        PLAYERATTACKFRAMES = 6
        PLAYERMOVEFRAMES = 10
        PLAYERDEFENDFRAMES = 12
        # DASH only has one frame

        BOSS1MOVEFRAMES = 10
        BOSS1ATTACK1FRAMES = 15
        BOSS1ATTACK2FRAMES = 17
        BOSS1WAVEATTACKFRAMES = 11
        BOSS1UNBLOCKABLESTRIKEFRAMES = 12
        BOSS1DASHFRAMES = 2

    # ----------------------------------------------------IMPORT ASSETS-------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
        # Player idle
        for i in range(1, PLAYERIDLEFRAMES + 1):
            image = pygame.image.load("assets\player\idle\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))

            self.playerIdleList.append(image)

        #---------------------------------------------------------------------------------------------------------------

        # Player attack
        for i in range(1, PLAYERATTACKFRAMES + 1):
            image = pygame.image.load("assets\player\\attack1\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.playerAttackList[0].append(image)
            self.playerAttackReversedList[0].append(reversedImage)

            image = pygame.image.load("assets\player\\attack2\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.playerAttackList[1].append(image)
            self.playerAttackReversedList[1].append(reversedImage)

        #---------------------------------------------------------------------------------------------------------------

        # Player move
        for i in range(1, PLAYERMOVEFRAMES + 1):
            image = pygame.image.load("assets\player\move\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))

            self.playerMoveList.append(image)

        #---------------------------------------------------------------------------------------------------------------

        # Player defend
        for i in range(1, PLAYERDEFENDFRAMES +1):
            image = pygame.image.load("assets\player\defend\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))

            self.playerDefendList.append(image)

        #---------------------------------------------------------------------------------------------------------------

        # Dash
        image = pygame.image.load("assets\player\dash\sword\\1.png")
        self.playerDash = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))

        #---------------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------

        # Boss1 normal attack 1
        for i in range(1, BOSS1ATTACK1FRAMES + 1):
            image = pygame.image.load("assets\\boss1\\attack1\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.boss1NormalAttackList[0].append(image)
            self.boss1NormalAttackReversedList[0].append(reversedImage)

        # Normal attack 2
        for i in range(1, BOSS1ATTACK2FRAMES + 1):
            image = pygame.image.load("assets\\boss1\\attack2\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.boss1NormalAttackList[1].append(image)
            self.boss1NormalAttackReversedList[1].append(reversedImage)

        #---------------------------------------------------------------------------------------------------------------

        # Boss1 dash
        for i in range(1, BOSS1DASHFRAMES + 1):
            image = pygame.image.load("assets\\boss1\dash\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.boss1DashList.append(image)
            self.boss1DashReversedList.append(reversedImage)

        #---------------------------------------------------------------------------------------------------------------

        # Boss1 unblockable
        for i in range(1, BOSS1UNBLOCKABLESTRIKEFRAMES + 1):
            image = pygame.image.load("assets\\boss1\\unblockableStrike\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.boss1UnblockableStrikeList.append(image)
            self.boss1UnblockableStrikeReversedList.append(reversedImage)

        #---------------------------------------------------------------------------------------------------------------

        # Boss1 move
        for i in range(1, BOSS1MOVEFRAMES + 1):
            image = pygame.image.load("assets\\boss1\move\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))

            self.boss1MoveList.append(image)

        #---------------------------------------------------------------------------------------------------------------

        # Boss1 wave attack
        for i in range(1, BOSS1WAVEATTACKFRAMES +1):
            image = pygame.image.load("assets\\boss1\waveAttack\sword\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))

            self.boss1WaveAttackList.append(image)

        #---------------------------------------------------------------------------------------------------------------
        if classType == "Player":
            self.image = self.playerIdleList[1]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        elif classType == "Boss1":
            self.image = self.boss1MoveList[1]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    def getMask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Character(pygame.sprite.Sprite):
    def __init__(self, display, fps, initialPositionTuple, hp, ms):
        super().__init__()

        # Display surface
        self.display = display
        self.displayWidth = self.display.get_width()
        self.displayHeight = self.display.get_height()
        self.DISPLAYFPS = fps

        # Position
        self.x = initialPositionTuple[0]
        self.y = initialPositionTuple[1]

        # Character traits
        self.hp = hp
        self.MS = ms

class Player(Character):
    def __init__(self, display, fps, initialPositionTuple):
        super().__init__(display, fps, initialPositionTuple, 8, 8)

        self.sword = Sword(self.x, self.y, "Player")

        self.width = 384
        self.height = 216

        # Sounds
        self.deflectedSound = pygame.mixer.Sound("assets\player\defend\deflect.mp3")
        self.defendingSound = pygame.mixer.Sound("assets\player\\defend\defending.mp3")
        self.attackHit = pygame.mixer.Sound("assets\player\\attack1\\attackHit.mp3")
        self.attack1Sound = pygame.mixer.Sound("assets\player\\attack1\\attack1.mp3")

        # -----------------------METHOD VARIABLES---------------------
        self.attackMovement = AttackEnum.PLAYERNOATTACK

        # Idle
        self.IDLEWAITFRAMES = self.DISPLAYFPS // 3
        self.idleCurrentWait = 0
        self.idleCurrentFrame = 0
        self.isIdle = True

        # Move Right/Left
        self.MOVEWAITFRAMES = self.DISPLAYFPS // 20
        self.moveCurrentWait = 0
        self.moveCurrentFrame = 0
        self.dIsPressed = False
        self.aIsPressed = False
        self.isFacingRight = True

        # Attack
        self.ATTACKWAITFRAMES = self.DISPLAYFPS // 60
        self.currentWait = 0
        self.currentFrame = 0
        self.attackSwitch = 0  # For rotating between attack 1 and 2

        # Block [same currentWait and currentFrame as attack]
        self.DEFENDWAITFRAMES = self.DISPLAYFPS // 120

        # Dash
        self.dashed = False
        self.DASHCOOLDOWN = 800
        self.DASHDISTANCE = 300
        self.currentTime = 0
        self.lastDashTime = 0

        # HUD
        self.hudCentreX = self.displayWidth / 2
        self.hudCentreY = 45
        # -----------------------------------------------------

        # Sprite Lists [To be filled in]
        # Default: Facing Left
        self.idleList = []
        self.idleReversedList = []

        self.moveList = []
        self.moveReversedList = []

        self.attackList = [[], []]
        self.attackReversedList = [[], []]

        self.defendList = []
        self.defendReversedList = []

        self.dashImage = None
        self.dashReversedImage = None

        self.hpBarList = []  # HUD
        self.dashCooldownList = []  # HUD radial cooldown indicator

        # Images in each animation/file
        IDLEFRAMES = 2
        MOVEFRAMES = 10
        ATTACKFRAMES = 6
        DEFENDFRAMES = 12
        DASHCOOLDOWNFRAMES = 4

        # --------------------------------------------------IMPORTING ASSETS---------------------------------------------
        # ---------------------------------------------------------------------------------------------------------------
        # Idle
        for i in range(1, IDLEFRAMES + 1):
            image = pygame.image.load("assets\player\idle\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.idleList.append(image)
            self.idleReversedList.append(reversedImage)

            # ----------------------------------------------------------------------------------------------------------

            # Move right/left
        for i in range(1, MOVEFRAMES + 1):
            image = pygame.image.load("assets\player\move\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.moveList.append(image)
            self.moveReversedList.append(reversedImage)

            # -----------------------------------------------------------------------------------------------------------

            # Dash
        self.dashImage = pygame.image.load("assets\player\dash\\1.png").convert_alpha()
        self.dashImage = pygame.transform.scale(self.dashImage, (
        round(self.dashImage.get_width() / 5), round(self.dashImage.get_height() / 5)))
        self.dashReversedImage = pygame.transform.flip(self.dashImage, True, False)

        # -----------------------------------------------------------------------------------------------------------

        # Attack
        for i in range(1, ATTACKFRAMES + 1):
            image = pygame.image.load("assets\player\\attack1\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.attackList[0].append(image)
            self.attackReversedList[0].append(reversedImage)

            image = pygame.image.load("assets\player\\attack2\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.attackList[1].append(image)
            self.attackReversedList[1].append(reversedImage)

            # ----------------------------------------------------------------------------------------------------------

            # Defend
        for i in range(1, DEFENDFRAMES + 1):
            image = pygame.image.load("assets\player\defend\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 5), round(image.get_height() / 5)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.defendList.append(image)
            self.defendReversedList.append(reversedImage)

            # -----------------------------------------------------------------------------------------------------------

            # HUD
            # HP bar
        for i in range(self.hp + 1):
            self.hpBarList.append(pygame.image.load("assets\player\hud\healthbar\\" + str(i) + ".png"))

            # Dash cooldown indicator
        for i in range(1, DASHCOOLDOWNFRAMES + 1):
            image = pygame.image.load("assets\player\hud\dashCooldown\\" + str(i) + ".png")
            self.dashCooldownList.append(
                pygame.transform.scale(image, (round(image.get_width() / 4), round(image.get_height() / 4))))
        # -------------------------------------------------------

        self.image = self.idleList[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # -----------------------------------------------------ANIMATION-----------------------------------------------
    def _hudAnimate(self):

        # Hp bar
        hpBarImage = self.hpBarList[self.hp]
        self.display.blit(hpBarImage, (self.hudCentreX - hpBarImage.get_width() / 2, self.hudCentreY))

        # Dash Cooldown
        self.currentTime = pygame.time.get_ticks()
        dashCooldownImage = None

        if self.currentTime - self.lastDashTime <= self.DASHCOOLDOWN / 4:
            dashCooldownImage = self.dashCooldownList[0]
        elif self.currentTime - self.lastDashTime <= self.DASHCOOLDOWN / 2:
            dashCooldownImage = self.dashCooldownList[1]
        elif self.currentTime - self.lastDashTime <= self.DASHCOOLDOWN * 3 / 4:
            dashCooldownImage = self.dashCooldownList[2]
        else:
            dashCooldownImage = self.dashCooldownList[3]

        self.display.blit(dashCooldownImage, (
        self.hudCentreX - dashCooldownImage.get_width() / 2, self.hudCentreY + hpBarImage.get_height() + 5))

    def _idleAnimate(self):
        if self.idleCurrentWait > self.IDLEWAITFRAMES:
            self.idleCurrentFrame += 1
            self.idleCurrentWait = 0
            if self.idleCurrentFrame == len(self.idleList):
                self.idleCurrentFrame = 0
        else:
            self.idleCurrentWait += 1
        self.image = self.idleList[self.idleCurrentFrame]
        self.sword.image = self.sword.playerIdleList[self.idleCurrentFrame]
        if self.isFacingRight:
            self.image = self.idleReversedList[self.idleCurrentFrame]
            self.sword.image = self.sword.playerIdleList[self.idleCurrentFrame]

    def _moveRightAnimate(self):
        if self.moveCurrentWait > self.MOVEWAITFRAMES:
            self.moveCurrentFrame += 1
            self.moveCurrentWait = 0
            if self.moveCurrentFrame == len(self.moveList):
                self.moveCurrentFrame = 0
        else:
            self.moveCurrentWait += 1
        if self.x < self.displayWidth - self.width:
            self.x += self.MS
        self.image = self.moveReversedList[self.moveCurrentFrame]
        self.sword.image = self.sword.playerMoveList[self.moveCurrentFrame]
        self.sword.x =  self.x

    def _moveLeftAnimate(self):
        if self.moveCurrentWait > self.MOVEWAITFRAMES:
            self.moveCurrentFrame += 1
            self.moveCurrentWait = 0
            if self.moveCurrentFrame == len(self.moveList):
                self.moveCurrentFrame = 0
        else:
            self.moveCurrentWait += 1
        if self.x > 0:
            self.x -= self.MS
        self.image = self.moveList[self.moveCurrentFrame]
        self.sword.image = self.sword.playerMoveList[self.moveCurrentFrame]
        self.sword.x = self.x

    def _dashAnimate(self):

        if self.isFacingRight:
            self.image = self.dashReversedImage
            self.sword.image = self.sword.playerDash
            self.sword.x = self.x
        else:
            self.image = self.dashImage
            self.sword.image = self.sword.playerDash
            self.sword.x = self.x
        if self.dashed:
            self.attackMovement = AttackEnum.PLAYERNOATTACK
            if self.isFacingRight:
                if self.x + self.DASHDISTANCE > self.displayWidth - self.width:
                    self.x = self.displayWidth - self.width
                    self.sword.x = self.x
                else:
                    self.x += self.DASHDISTANCE
                    self.sword.x = self.x
            else:
                if self.x - self.DASHDISTANCE < 0:
                    self.x = 0
                    self.sword.x = self.x
                else:
                    self.x -= self.DASHDISTANCE
                    self.sword.x = self.x
        self.dashed = not self.dashed

    def _attackAnimate(self):
        if self.currentWait > self.ATTACKWAITFRAMES:
            self.currentFrame += 1
            self.currentWait = 0
            if self.currentFrame == len(self.attackList[self.attackSwitch]):
                self.currentFrame = 0
                self.attackMovement = AttackEnum.PLAYERNOATTACK
                self.attackSwitch = not self.attackSwitch
                self.sword.hasAttacked = False
                return

        else:
            self.currentWait += 1
        if self.isFacingRight:
            self.image = self.attackReversedList[self.attackSwitch][self.currentFrame]
            self.sword.image = self.sword.playerAttackReversedList[self.attackSwitch][self.currentFrame]
        else:
            self.image = self.attackList[self.attackSwitch][self.currentFrame]
            self.sword.image = self.sword.playerAttackList[self.attackSwitch][self.currentFrame]

    def _defendAnimate(self):
        if self.currentWait > self.DEFENDWAITFRAMES:
            self.currentFrame += 1
            self.currentWait = 0
            if self.currentFrame == len(self.defendList):
                self.currentFrame = 0
                self.attackMovement = AttackEnum.PLAYERNOATTACK
                return
        else:
            self.currentWait += 1
        if self.isFacingRight:
            self.image = self.defendReversedList[self.currentFrame]
            self.sword.image = self.sword.playerDefendList[self.currentFrame]
        else:
            self.image = self.defendList[self.currentFrame]
            self.sword.image = self.sword.playerDefendList[self.currentFrame]

    def _getMask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # -----------------------------------------------------------------------------------------------------------------------

    # Calls animate functions

    def animate(self):
        if self.isIdle:
            self._idleAnimate()
        else:
            if self.attackMovement == AttackEnum.PLAYERATTACK:
                self._attackAnimate()
            elif self.attackMovement == AttackEnum.PLAYERDEFEND:
                self._defendAnimate()
            elif self.attackMovement == AttackEnum.PLAYERDASH:
                self._dashAnimate()
            elif self.attackMovement == AttackEnum.PLAYERNOATTACK:
                if self.isFacingRight:
                    self._moveRightAnimate()
                else:
                    self._moveLeftAnimate()

        self.checkForIdle()
        self.checkForKeyDown()
        self._hudAnimate()
        self._getMask()
        self.sword.getMask()
        self.display.blit(self.image, (self.x, self.y))

    # -----------------------------------------------------SET BOOLS-----------------------------------------------------

    def checkForIdle(self):
        if not self.aIsPressed and not self.dIsPressed:
            if self.attackMovement == AttackEnum.PLAYERNOATTACK:
                self.isIdle = True

    def checkForKeyDown(self):
        if self.attackMovement == AttackEnum.PLAYERNOATTACK:
            if self.dIsPressed:
                self.isFacingRight = True
                self.isIdle = False
                return
            if self.aIsPressed:
                self.isFacingRight = False
                self.isIdle = False
                return

    def moveStopRight(self):
        self.dIsPressed = False
        if self.aIsPressed:
            self.isFacingRight = False
        self.checkForIdle()

    def moveStopLeft(self):
        self.aIsPressed = False
        if self.dIsPressed:
            self.isFacingRight = True
        self.checkForIdle()

    def moveLeft(self):
        self.aIsPressed = True

    def moveRight(self):
        self.dIsPressed = True

    def moveDash(self):
        self.currentTime = pygame.time.get_ticks()
        if self.currentTime - self.DASHCOOLDOWN >= self.lastDashTime:
            if self.attackMovement == AttackEnum.PLAYERNOATTACK:
                self.isIdle = False
                self.attackMovement = AttackEnum.PLAYERDASH
                self.lastDashTime = self.currentTime

    def moveAttack(self):
        if self.attackMovement == AttackEnum.PLAYERNOATTACK:
            self.isIdle = False
            self.attackMovement = AttackEnum.PLAYERATTACK

    def moveDefend(self):
        if self.attackMovement == AttackEnum.PLAYERNOATTACK:
            self.isIdle = False
            self.attackMovement = AttackEnum.PLAYERDEFEND
            self.defendingSound.play()
    # -------------------------------------------------------------------------------------------------------------------


class Boss1(Character):
    def __init__(self, display, fps, player):
        super().__init__(display, fps, (600, 220), 56, 10)

        self.sword = Sword(self.x, self.y, "Boss1")

        self.name = pygame.image.load("assets\\boss1\\name.png")

        # Sounds
        self.unblockableHit = pygame.mixer.Sound("assets\\boss1\\unblockableStrike\\unblockableHit.mp3")
        self.attackHit = pygame.mixer.Sound("assets\\boss1\\attackHit.mp3")

        # ---------------------------METHOD VARIABLES------------------------
        self.player = player
        self.currentWait = 0
        self.currentFrame = 0
        self.MAXHP = self.hp
        self.attackPattern = -1  # Sets up which attack to do in attack list

        # Move
        self.MOVEWAITFRAMES = self.DISPLAYFPS // 30
        self.moveCurrentWait = 0
        self.moveCurrentFrame = 0
        self.MOVETHRESHOLD = 100
        self.isFacingRight = False

        # Normal Attack
        self.NORMALATTACKWAITFRAMES = self.DISPLAYFPS // 120
        self.normalAttackSwitch = 0

        # Wave Attack
        self.WAVEATTACKWAITFRAMES = self.DISPLAYFPS // 60
        self.currentRepetition = 1  # Used in dash as well

        # Unblockable Strike
        self.UNBLOCKABLESTRIKEWAITFRAMES = self.DISPLAYFPS // 60
        self.isBlockable = True
        self.soundIsPlayed = False
        self.UNBLOCKABLESOUND = pygame.mixer.Sound("assets\\boss1\\unblockableStrike\\unblockableSound.mp3")

        # Dash
        self.DASHWAITFRAMES = self.DISPLAYFPS // 120
        self.DASHXSPEED = 50
        self.dashStartingX = 0
        self.isDashing = False

        # Death
        self.DEATHWAITFRAMES = self.DISPLAYFPS // 30
        self.deathCurrentFrame = 0
        self.deathCurrentWait = 0

        # Sprite Lists [To be filled in]
        # Default: Facing Right
        self.moveList = []
        self.moveReversedList = []

        self.normalAttackList = [[], []]
        self.normalAttackReversedList = [[], []]

        self.unblockableStrikeList = [[], []]  # [attack sprite], [unblockable HUD text]
        self.unblockableStrikeReversedList = []

        self.waveAttackList = [[], []]  # [attack sprite], [projectile objects]
        self.waveAttackReversedList = []

        self.dashAttackList = []
        self.dashAttackReversedList = []

        self.deathList = []
        self.deathReversedList = []

        self.hpBarList = []  # HUD

        # Images in each animation/file
        MOVEFRAMES = 10
        ATTACK1FRAMES = 15
        ATTACK2FRAMES = 17
        WAVEATTACKFRAMES = 11
        UNBLOCKABLESTRIKEFRAMES = 12
        DASHFRAMES = 2
        DEATHFRAMES = 14

        # -----------------------------------------------IMPORTING ASSETS------------------------------------------------
        # ---------------------------------------------------------------------------------------------------------------

        # Move
        for i in range(1, MOVEFRAMES + 1):
            image = pygame.image.load("assets\\boss1\move\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.moveList.append(image)
            self.moveReversedList.append(reversedImage)

            # ----------------------------------------------------------------------------------------------------------

            # Normal Attack 1
        for i in range(1, ATTACK1FRAMES + 1):
            image = pygame.image.load("assets\\boss1\\attack1\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.normalAttackList[0].append(image)
            self.normalAttackReversedList[0].append(reversedImage)

            # ----------------------------------------------------------------------------------------------------------

            # Normal Attack 2
        for i in range(1, ATTACK2FRAMES + 1):
            image = pygame.image.load("assets\\boss1\\attack2\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.normalAttackList[1].append(image)
            self.normalAttackReversedList[1].append(reversedImage)

            # ----------------------------------------------------------------------------------------------------------

            # Wave Attack
        for i in range(1, WAVEATTACKFRAMES + 1):
            image = pygame.image.load("assets\\boss1\waveAttack\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.waveAttackList[0].append(image)
            self.waveAttackReversedList.append(reversedImage)

            # ----------------------------------------------------------------------------------------------------------

            # Unblockable Strike
        for i in range(1, UNBLOCKABLESTRIKEFRAMES + 1):
            image = pygame.image.load("assets\\boss1\\unblockableStrike\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.unblockableStrikeList[0].append(image)
            self.unblockableStrikeReversedList.append(reversedImage)

        # HUD unblockableStrike text
        self.unblockableStrikeList[1].append(pygame.image.load("assets\\boss1\\unblockableStrike\\0.png"))

        # ----------------------------------------------------------------------------------------------------------

        # Dash
        for i in range(1, DASHFRAMES + 1):
            image = pygame.image.load("assets\\boss1\dash\\" + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.dashAttackList.append(image)
            self.dashAttackReversedList.append(reversedImage)

            # ----------------------------------------------------------------------------------------------------------

            # Death
        for i in range(1, DEATHFRAMES + 1):
            image = pygame.image.load("assets\\boss1\death\\" + str(i) + ".png")
            image = pygame.transform.scale(image, (round(image.get_width() / 2), round(image.get_height() / 2)))
            reversedImage = pygame.transform.flip(image, True, False)

            self.deathList.append(image)
            self.deathReversedList.append(reversedImage)

            # -----------------------------------------------------------------------------------------------------------

            # HP bar
        for i in range(int(self.hp / 2) + 1):
            self.hpBarList.append(pygame.image.load("assets\\boss1\healthbar\\" + str(i) + ".png"))

        # ---------------------------------------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------------------------

        # Attack Sequences
        self.ATTACKPATTERNLIST = [
            # Above half health
            [self._moveToPlayer, self._normalAttackAnimate, self._moveToPlayer, self._normalAttackAnimate,
             self._moveToPlayer, self._unblockableStrikeAnimate],
            [self._dashAttackAnimate, self._moveToPlayer, self._normalAttackAnimate, self._moveToPlayer,
             self._unblockableStrikeAnimate],
            [self._moveToPlayer, self._unblockableStrikeAnimate, self._blinkToOppositeEdgeFromPlayer, self._dashAttackAnimate],
            [self._blinkToOppositeEdgeFromPlayer, self._dashAttackAnimate, self._waveAttackAnimate],

            # Below half health
            [self._blinkToOppositeEdgeFromPlayer, self._dashAttackAnimate, self._blinkBehindPlayer, self._unblockableStrikeAnimate],
            [self._blinkToOppositeEdgeFromPlayer, self._waveAttackAnimate, self._blinkToOppositeEdge,
             self._waveAttackAnimate, self._blinkToOppositeEdge, self._waveAttackAnimate],
            [self._blinkBehindPlayer, self._unblockableStrikeAnimate],
            [self._blinkBehindPlayer, self._blinkBehindPlayer, self._unblockableStrikeAnimate,
             self._blinkToOppositeEdgeFromPlayer, self._dashAttackAnimate],
        ]

        # Image for first frame
        self.image = self.moveList[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # ---------------------------------------------------------------------------------------------------------------

    def _hudAnimate(self):

        # Hp bar
        hpBarImage = self.hpBarList[self.hp // 2]
        self.display.blit(hpBarImage, (
        self.player.hudCentreX - hpBarImage.get_width() / 2, self.player.hudCentreY - hpBarImage.get_height() - 10))

        # Name
        self.display.blit(self.name, (
        self.player.hudCentreX - self.name.get_width() / 2, self.player.hudCentreY - hpBarImage.get_height() - 10))

        # Unblockable sound effect
        if not self.isBlockable and not self.soundIsPlayed:
            self.UNBLOCKABLESOUND.play()
            self.soundIsPlayed = True

        # Unblockable text
        if not self.isBlockable:
            self.display.blit(self.unblockableStrikeList[1][0], (50, 50))

        else:
            self.soundIsPlayed = False

    def _moveRightAnimate(self):
        # Increment current frame
        if self.moveCurrentWait > self.MOVEWAITFRAMES:
            self.moveCurrentFrame += 1
            self.moveCurrentWait = 0

            # Last frame
            if self.moveCurrentFrame == len(self.moveList):
                self.moveCurrentFrame = 0
        else:
            self.moveCurrentWait += 1

        # Set x coordinate, sprite, and orientation
        self.x += self.MS
        self.image = self.moveList[self.moveCurrentFrame]
        self.sword.image = self.sword.boss1MoveList[self.moveCurrentFrame]
        self.sword.x = self.x

    def _moveLeftAnimate(self):
        # Increment current frame
        if self.moveCurrentWait > self.MOVEWAITFRAMES:
            self.moveCurrentFrame += 1
            self.moveCurrentWait = 0

            # Last frame
            if self.moveCurrentFrame == len(self.moveList):
                self.moveCurrentFrame = 0
        else:
            self.moveCurrentWait += 1

        # Set x coordinate, sprite, and orientation
        self.x -= self.MS
        self.image = self.moveReversedList[self.moveCurrentFrame]
        self.sword.image = self.sword.boss1MoveList[self.moveCurrentFrame]
        self.sword.x = self.x

    def _normalAttackAnimate(self):
        # Increment current frame
        if self.currentWait > self.NORMALATTACKWAITFRAMES:
            self.currentFrame += 1
            self.currentWait = 0

            # Last frame
            if self.currentFrame == len(self.normalAttackList[self.normalAttackSwitch]):
                self.currentFrame = 0
                self.normalAttackSwitch = not self.normalAttackSwitch
                self.sword.hasAttacked = False
                return 1

        # Set sprite and orientation
        else:
            self.currentWait += 1
        if not self.isFacingRight:
            self.image = self.normalAttackReversedList[self.normalAttackSwitch][self.currentFrame]
            self.sword.image = self.sword.boss1NormalAttackReversedList[self.normalAttackSwitch][self.currentFrame]
        else:
            self.image = self.normalAttackList[self.normalAttackSwitch][self.currentFrame]
            self.sword.image = self.sword.boss1NormalAttackList[self.normalAttackSwitch][self.currentFrame]

    def _unblockableStrikeAnimate(self):
        if self.isBlockable:
            self.isBlockable = False

        # Increment current frame
        if self.currentWait > self.UNBLOCKABLESTRIKEWAITFRAMES:
            self.currentFrame += 1
            self.currentWait = 0

            # Last frame
            if self.currentFrame == len(self.unblockableStrikeList[0]):
                self.currentFrame = 0
                self.isBlockable = True
                self.sword.hasAttacked = False
                return 1
        else:
            self.currentWait += 1

        # Set sprite and orientation
        if not self.isFacingRight:
            self.image = self.unblockableStrikeReversedList[self.currentFrame]
            self.sword.image = self.sword.boss1UnblockableStrikeReversedList[self.currentFrame]
        else:
            self.image = self.unblockableStrikeList[0][self.currentFrame]
            self.sword.image = self.sword.boss1UnblockableStrikeList[self.currentFrame]

    def _dashAttackAnimate(self, numberOfRepetitions):
        if self.currentRepetition <= numberOfRepetitions:

            # Returns back to starting dash position
            if self.isDashing and self.dashStartingX - self.DASHXSPEED < self.x < self.dashStartingX + self.DASHXSPEED:
                self.isDashing = False
                self.sword.hasAttacked = False
                self.currentRepetition += 1
                return
            # Sets starting x position
            elif not self.isDashing:
                self.dashStartingX = self.x
                self.isDashing = True

            # Increment current frame
            if self.currentWait > self.DASHWAITFRAMES and self.currentFrame < len(self.dashAttackList) - 1:
                self.currentFrame += 1
                self.currentWait = 0
            else:
                self.currentWait += 1

            # Set x coordinate, sprite, and orientation
            if not self.isFacingRight:
                self.image = self.dashAttackReversedList[self.currentFrame]
                self.sword.image = self.sword.boss1DashReversedList[self.currentFrame]
                self.sword.x = self.x
                if self.x < - self.image.get_width():
                    self.x = self.displayWidth
                else:
                    self.x -= self.DASHXSPEED
            else:
                self.image = self.dashAttackList[self.currentFrame]
                self.sword.image = self.sword.boss1DashList[self.currentFrame]
                self.sword.x = self.x
                if self.x > self.displayWidth:
                    self.x = - self.image.get_width()
                else:
                    self.x += self.DASHXSPEED
        # Attack finished
        else:
            self.currentRepetition = 1
            return 1

    def _waveAttackAnimate(self, numberOfRepetitions):
        if self.currentRepetition <= numberOfRepetitions:

            # Increment current frame
            if self.currentWait > self.WAVEATTACKWAITFRAMES:
                self.currentFrame += 1
                self.currentWait = 0
                # Last frame
                if self.currentFrame == len(self.waveAttackList[0]):
                    self.currentFrame = 0
                    self.currentRepetition += 1
                    return
                # Create projectile object
                elif self.currentFrame == 6:
                    if self.isFacingRight:
                        self.waveAttackList[1].append(
                            WaveProjectile(self.display, self.x + 750, self.y + 340, self.isFacingRight))
                    else:
                        self.waveAttackList[1].append(
                            WaveProjectile(self.display, self.x + 210, self.y + 340, self.isFacingRight))
            else:
                self.currentWait += 1

            # Set sprite and orientation
            if not self.isFacingRight:
                self.image = self.waveAttackReversedList[self.currentFrame]
                self.sword.image = self.sword.boss1WaveAttackList[self.currentFrame]
            else:
                self.image = self.waveAttackList[0][self.currentFrame]
                self.sword.image = self.sword.boss1WaveAttackList[self.currentFrame]

        # Attack finished
        else:
            self.currentRepetition = 1
            return 1

    def _activeProjectileAnimate(self):
        if len(self.waveAttackList[1]) != 0:
            for i in range(len(self.waveAttackList[1]) - 1, -1, -1):
                if -self.waveAttackList[1][i].image.get_width() < self.waveAttackList[1][i].x < self.displayWidth:
                    self.waveAttackList[1][i].shoot()
                else:
                    self.waveAttackList[1].pop(i)

    def _deathAnimate(self):
        if self.deathCurrentFrame < len(self.deathList) - 1:

            # Increment current frame
            if self.deathCurrentWait > self.DEATHWAITFRAMES:
                self.deathCurrentFrame += 1
                self.deathCurrentWait = 0
            else:
                self.deathCurrentWait += 1
        if self.isFacingRight:
            self.image = self.deathList[self.deathCurrentFrame]
        else:
            self.image = self.deathReversedList[self.deathCurrentFrame]

    def _blinkBehindPlayer(self):
        # Blink to the left of player
        if self.player.x + self.player.image.get_width() / 2 < self.x + self.image.get_width() / 2:
            self.x = self.player.x - self.image.get_width() / 2 + 30
            self.sword.x = self.x
            self.isFacingRight = True
        # Blink to the right of player
        else:
            self.x = self.player.x - self.image.get_width() / 4 + 100
            self.sword.x = self.x
            self.isFacingRight = False
        return 1

    def _blinkToOppositeEdgeFromPlayer(self):
        # Player closer to left edge
        if self.player.x + self.player.image.get_width() / 2 < self.displayWidth / 2:
            self.x = self.displayWidth - self.image.get_width() * 2 / 3
            self.sword.x = self.x
            self.isFacingRight = False
        # Player closer to right edge
        else:
            self.x = 0 - self.image.get_width() / 3
            self.sword.x = self.x
            self.isFacingRight = True
        return 1

    def _blinkToOppositeEdge(self):
        # Boss closer to left edge
        if self.x + self.image.get_width() / 3 < self.displayWidth / 2:
            self.x = self.displayWidth - self.image.get_width() * 2 / 3
            self.isFacingRight = False
        # Boss closer to right edge
        else:
            self.x = 0 - self.image.get_width() / 3
            self.sword.x = self.x
            self.isFacingRight = True
        return 1

    def _moveToPlayer(self):
        # Player is left of boss
        if self.player.x + self.player.image.get_width() / 2 < self.x + self.image.get_width() / 2 - self.MOVETHRESHOLD:
            self.isFacingRight = False
            self._moveLeftAnimate()
        elif self.player.x + self.player.image.get_width() / 2 > self.x + self.image.get_width() / 2 + self.MOVETHRESHOLD:
            self.isFacingRight = True
            self._moveRightAnimate()
        else:
            return 1

    def _getMask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def animate(self):
        if self.hp > 0: # Alive
            if self.attackPattern == -1:
                # Pick random attack sequence | attack 0-4 above half health, attack 0-9 for below half health
                self.attackPattern = random.randint(0, (len(self.ATTACKPATTERNLIST) - 1) // 2 if self.hp > (
                            self.MAXHP / 2) else len(self.ATTACKPATTERNLIST) - 1)
                self.attackPatternState = 0  # start with the 0th function in the attack sequence
                self.temp = None  # Reset temp var to use inside attacks
            else:
                # If the attack pattern list has more attack functions to do
                if self.attackPatternState < len(self.ATTACKPATTERNLIST[self.attackPattern]):
                    # pick the attackFunction that needs to be done this loop
                    self.currentAttackFunction = self.ATTACKPATTERNLIST[self.attackPattern][self.attackPatternState]

                    # Special case for functions that need a numberOfRepetitions
                    if self.currentAttackFunction == self._waveAttackAnimate or self.currentAttackFunction == self._dashAttackAnimate:
                        self.temp = random.randint(1, 3) if not self.temp else self.temp
                        self.attackPatternState += 1 if self.currentAttackFunction(self.temp) else 0
                    else:  # Normally execute attack functions
                        self.attackPatternState += 1 if self.currentAttackFunction() else 0

                else:
                    self.attackPattern = -1

            self._activeProjectileAnimate()
            self._hudAnimate()
            self._getMask()
            self.sword.getMask()

        else: # Dead
            self._deathAnimate()

        self.display.blit(self.image, (self.x, self.y))
