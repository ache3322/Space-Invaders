#====================================================================
# Name: gameobjects.py
# Created by: Austin Che
# Created on: Aug 28, 2019
# Modified on: Sep 6, 2019
# 
# Description:
#   This file contains the game objects used in the scenes.
#====================================================================
import pygame

from const import SCREENRECT, WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    """
    The Player class contains the state and behaviour of the movable player.\n
    The player is able to move left and right, and shoot a laser to destroy the Enemy.
    """
    image = None
    shootSound = None
    gun_offset = -25
    lives = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.speed = 7      # The speed the player moves horizontally
        self.bounce = 24    # The bounciness of the player sprite

        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        # Move the player up (y-axis) so as not to be against border
        self.rect.y = self.rect.y - 10
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = 0
        self.firing = 0

    def move(self):
        # Use the "facing" datamember to determine which direction to move sprite
        self.rect.move_ip(self.facing * self.speed, 0)
        # Prevent sprite from moving off screen
        self.rect = self.rect.clamp((0, 0, WIDTH, HEIGHT))
        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

    def gunpos(self):
        pos = self.rect.centerx
        return pos, self.rect.top

    def died(self):
        self.lives -= 1
        self.set_start_position()

    def set_start_position(self):
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.rect.y = self.rect.y - 10        

    def get_direction(self):
        """
        Get the direction of the player.\n
        The direction can be either -1, 0, 1
        """
        return self.facing

    def set_direction(self, direction):
        self.facing = direction

    def get_firing(self):
        return self.firing

    def set_firing(self, firing):
        self.firing = firing


class Enemy(pygame.sprite.Sprite):
    id = -1
    image = None
    startingX = 0
    startingY = 0
    startingDir = 1

    def __init__(self, id=0, speed=7, facing=1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.id = id
        self.speed = speed
        self.facing = facing
        self.startingDir = facing

        self.rect = self.image.get_rect()
        self.changeDirection = False
        self.pixels = 0

    def set_position(self, x, y):
        (width, height) = self.image.get_size()
        self.startingX = x
        self.startingY = y
        self.rect = pygame.Rect(x, y, width, height)
        if self.facing < 0:
            self.rect.right = SCREENRECT.right - x

    def reset_position(self):
        self.increaseSpeed()
        self.set_position(self.startingX, self.startingY)
        if self.startingDir < 0:
            self.rect.right = SCREENRECT.right - self.startingX

    def update(self):
        self.rect.move_ip(self.facing * self.speed, 0)
        if not SCREENRECT.contains(self.rect):
            # Ensure the Enemy sprite is within the boundaries of the screen
            # If the sprite goes over, then make the sprite go down and switch directions
            self.changeDirection = True
        else:
            self.changeDirection = False

    def go_down(self):
        self.calc_leftover_pixels()

        self.facing = -self.facing
        self.rect.top = self.rect.bottom + 1
        self.rect = self.rect.clamp(SCREENRECT)

        if self.changeDirection:
            # Ensure equal distance between sprites. Shift the sprite closest
            # to the screen by a few pixels (LEFT or RIGHT)
            if self.facing < 0: # LEFT
                self.rect.right = SCREENRECT.right + self.pixels
            if self.facing > 0: # RIGHT
                self.rect.left = self.rect.left + self.pixels

    def calc_leftover_pixels(self):
        """
        Calculates the remaining pixels outside the screen. The result ensures,
        the sprite can be positioned to ensure equidistant between other sprites.
        """
        pixels = 0
        if self.facing > 0:
            pixels = (self.rect.x + self.rect.width) - SCREENRECT.width
        elif self.facing < 0:
            pixels = self.rect.x - SCREENRECT.x
        self.pixels = pixels

    def increaseSpeed(self):
        if self.speed < 12:
            self.speed = self.speed + 1


class Laser(pygame.sprite.Sprite):
    image = None

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.speed = -9
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            # Remove laser if past screen
            self.kill()


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Courier", 20)
        self.color = (255, 255, 255)
        self.score = 0
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 10)

    def update(self):
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = "Score: %d" % self.score
            self.image = self.font.render(msg, 0, self.color)

    def increment(self):
        self.score += 1

    def get_score(self):
        return self.score


class Lives(pygame.sprite.Sprite):
    def __init__(self, lives):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Courier", 20)
        self.color = (255, 255, 255)
        self.lives = lives
        self.lastlives = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 30)

    def update(self):
        if self.lives != self.lastlives:
            self.lastlives = self.lives
            msg = "Lives: %d" % self.lives
            self.image = self.font.render(msg, 0, self.color)

    def set_lives(self, lives):
        self.lives = lives