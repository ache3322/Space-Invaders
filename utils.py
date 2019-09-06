#====================================================================
# Name: game_manager.py
# Created by: Austin Che
# Created on: Aug 28, 2019
# Modified on: Sep 6, 2019
# 
# Description:
#   The utils file contains functions to help load resources from
#   the file system (image files, sound files, etc.)
#====================================================================
import os.path
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file, directory="sprites"):
    """Load an image"""

    file = os.path.join(main_dir, directory, file)

    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))

    return surface.convert()


def load_images(*files):
    """Load multiple image files."""
    images = []
    for file in files:
        images.append(file)
    return images


def load_sound(file, directory="assets"):
    """Load audio file"""
    file = os.path.join(main_dir, directory, file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
