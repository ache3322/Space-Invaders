#====================================================================
# Name: scenes.py
# Created by: Austin Che
# Created on: Aug 28, 2019
# Modified on: Sep 6, 2019
# 
# Description:
#   This file contains all the scenes (levels).
#====================================================================
import random, math
from abc import ABCMeta

import pygame

import colour
import const
from const import SCREENRECT
from app import ApplicationManager
from utils import load_image, load_sound
from ui import Text, Button, Justify
from gameobjects import Player, Enemy, Laser, Score, Lives


class Scene(metaclass=ABCMeta):

    def initialize(self):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, event):
        raise NotImplementedError


class TitleScene(Scene):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.id = 1
        self.sceneName = "title"

    def initialize(self):
        print(f"Initializing the '{self.sceneName}' level...")

        self.startBtn = Button(310, 250, 160, 50, "START")
        self.infoBtn = Button(200, 350, 370, 50, "INSTRUCTIONS")
        self.quitBtn = Button(325, 450, 135, 50, "QUIT")
        self.backBtn = Button(20, 530, 130, 50, "BACK")

        # assign button colour
        self.startBtn.set_button_colour(colour.LIGHTBLUE, None)
        self.infoBtn.set_button_colour(colour.LIGHTBLUE, None)
        self.quitBtn.set_button_colour(colour.LIGHTBLUE, None)
        self.backBtn.set_button_colour(colour.LIGHTBLUE, None)

        # assign action functions to handle button click events
        self.startBtn.actionFunc = self.__onStartBtnClicked
        self.infoBtn.actionFunc = self.__onInfoBtnClicked
        self.quitBtn.actionFunc = self.__onQuitBtnClicked
        self.backBtn.actionFunc = self.__onBackBtnClicked

        self.background = load_image("intro.png")
        self.instructions = load_image("instructions.png")

        self.startGame = False
        self.quitGame = False
        self.showInstructions = False

    def handle_events(self, event):
        self.startBtn.handle_events()
        self.infoBtn.handle_events()
        self.quitBtn.handle_events()
        self.backBtn.handle_events()

        if self.startGame is True:
            ApplicationManager().load_scene(GameScene())

        if event.type == pygame.MOUSEBUTTONDOWN and self.quitGame:
            # QUIT button clicked, exit the program
            ApplicationManager().running = False

    def render(self, screen):

        if self.showInstructions is False:
            # Draw the title screen
            screen.blit(self.background, (0, 0))
            self.startBtn.render(screen)
            self.infoBtn.render(screen)
            self.quitBtn.render(screen)
        else:
            # Draw the info screen
            screen.blit(self.instructions, (0, 0))
            self.backBtn.render(screen)

    def update(self):
        pygame.display.update()

    def __onStartBtnClicked(self):
        self.startGame = True

    def __onInfoBtnClicked(self):
        self.showInstructions = True

    def __onBackBtnClicked(self):
        self.showInstructions = False        

    def __onQuitBtnClicked(self):
        self.quitGame = True


class GameScene(Scene):

    def __init__(self):
        super(GameScene, self).__init__()
        self.id = 2
        self.sceneName = "game"

        self.spawnFactor = 0
        self.speedFactor = 0
        self.resetEnemy = False

    def initialize(self):
        print(f"Initializing the '{self.sceneName}' level...")

        # Loading resources (images, audio, etc.) before beginning scene
        Player.image = load_image("player.gif")
        Player.shootSound = load_sound("laser.ogg")
        Laser.image = load_image("laser.gif")
        Enemy.image = load_image("spider.gif")
        self.background = load_image("background2.gif").convert()

        # Initialize sprite group
        self.lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.all = pygame.sprite.RenderUpdates()

        # Assign groups to sprites
        Laser.containers = self.lasers, self.all
        Enemy.containers = self.aliens, self.all
        Player.containers = self.all
        Score.containers = self.all
        Lives.containers = self.all

        self.player = Player()
        self.score = Score()
        self.lives = Lives(self.player.lives)
        self.all.add(self.score)
        self.all.add(self.lives)
        self.generate_enemies()

    def handle_events(self, event):
        keystate = pygame.key.get_pressed()

        # Player using LEFT & RIGHT ARROWS to move
        direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
        self.player.set_direction(direction)

        # Player presses SPACE to shoot
        self.player.firing = keystate[pygame.K_SPACE]

    def render(self, screen):
        screen.blit(self.background, (0,0))
        self.all.clear(screen, self.background)
        self.all.update()
        self.all.draw(screen)

    def update(self):
        if self.player.alive():
            self.player.move()

            # Prevent overfiring/spamming lasers over max limit
            if not self.player.reloading and self.player.firing and len(self.lasers) < const.MAX_SHOT:
                Laser(self.player.gunpos())
                Player.shootSound.play()
            self.player.reloading = self.player.firing
        else:
            # Player has died (lost all lives)
            self.go_to_gameover()

        # Enemy (group) direction change check
        for e1 in self.aliens:
            # An enemy reaches the edge of the screen,
            # then change all enemy's direction
            if e1.changeDirection:
                for e2 in self.aliens:
                    e2.go_down()
                break

        #===-------------------
        # Collision detection
        for alien in pygame.sprite.spritecollide(self.player, self.aliens, 1):
            self.resetEnemy = True
            self.player.died()
            self.lives.set_lives(self.player.lives)
            if self.player.lives <= 0:
                self.player.kill()
            break

        for alien in pygame.sprite.groupcollide(self.lasers, self.aliens, 1, 1).keys():
            self.score.increment()
        #===-------------------

        # Reset position of enemies
        if self.resetEnemy:
            self.resetEnemy = False
            for e in self.aliens:
                e.reset_position()

        if len(self.aliens) == 0:
            if self.speedFactor < const.MAX_SPEED_FACTOR:
                self.speedFactor += 1
            self.generate_enemies()

        pygame.display.update()

    def generate_enemies(self):
        rows = random.randrange(2, 5)
        cols = random.randrange(5, 11)
        speed = random.randrange(const.MIN_E_SPEED + self.speedFactor, const.MAX_E_SPEED + self.speedFactor)
        facing = random.choice((-1, 1))

        count = 0
        offset_x = offset_y = 16
        x_pos = y_pos = 0

        for row in range(rows):
            for col in range(cols):
                count = count + 1
                e = Enemy(count, speed, facing)
                e.set_position(x_pos, y_pos)
                x_pos = 32 + x_pos + offset_x
            x_pos = 0
            y_pos = 32 + y_pos + offset_y

    def go_to_gameover(self):
        ApplicationManager().load_scene(GameOverScene(self.score.get_score()))


class GameOverScene(Scene):
    def __init__(self, score=0):
        super(GameOverScene, self).__init__()
        self.id = 3
        self.sceneName = "gameover"
        self.score = score
    
    def initialize(self):
        print(f"Initializing the '{self.sceneName}' level...")

        self.gameOverTxt = Text(400, 100, "courier new", 100, "GAME OVER!", colour.LORANGE, Justify.CENTER)
        self.scoreTxt = Text(400, 200, "courier new", 50, f"SCORE: {self.score}", colour.RED, Justify.CENTER)        

        self.againBtn = Button(225, 370, 350, 50, "PLAY AGAIN?")
        self.quitBtn = Button(330, 450, 140, 50, "QUIT")

        # assign button colour
        self.againBtn.set_button_colour(colour.LIGHTBLUE, None)
        self.quitBtn.set_button_colour(colour.LIGHTBLUE, None)

        # assign action functions to handle button click events
        self.againBtn.actionFunc = self.__onAgainBtnClicked__
        self.quitBtn.actionFunc = self.__onQuitBtnClicked__

        self.background = load_image("background1.gif")

        self.playAgain = False
        self.quitGame = False

    def handle_events(self, event):
        self.againBtn.handle_events()
        self.quitBtn.handle_events()

        if self.playAgain:
            ApplicationManager().load_scene(GameScene())

        if event.type == pygame.MOUSEBUTTONDOWN and self.quitGame:
            ApplicationManager().running = False

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        self.gameOverTxt.render(screen)
        self.scoreTxt.render(screen)
        self.againBtn.render(screen)
        self.quitBtn.render(screen)

    def update(self):
        pygame.display.update()

    def __onAgainBtnClicked__(self):
        self.playAgain = True

    def __onQuitBtnClicked__(self):
        self.quitGame = True
