#====================================================================
# Name: constants.py
# Created by: Austin Che
# Created on: Aug 28, 2019
# Modified on: Sep 6, 2019
# 
# Description:
#   File containing constants used within project.
#====================================================================
import pygame

# Dimensions of window width and height
WIDTH = 800
HEIGHT = 600
FPS = 60

# Max shots that can appear on screen
MAX_SHOT = 1

SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

# Enemy variables
MIN_E_SPEED = 1
MAX_E_SPEED = 5
MAX_SPEED_FACTOR = 4
MIN_E_COL = 6
MAX_E_COL = 10