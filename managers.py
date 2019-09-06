#====================================================================
# Name: managers.py
# Created by: Austin Che
# Created on: Aug 28, 2019
# 
# Description:
#   The GameManger class controls the entire game.
#====================================================================
#pylint: disable=no-name-in-module
import pygame
from pygame.constants import (
    K_ESCAPE, MOUSEBUTTONDOWN, QUIT, MOUSEMOTION, KEYDOWN, K_p
)

from const import SCREENRECT
from app import ApplicationManager, Singleton
from utils import load_image
from scenes import TitleScene


class GameManager(Singleton):

    # Boolean flag representing if application is finished
    def init(self):
        self.title = "Jets and Aliens, IN SPACE!"
        self.currentScene = None

    def initialize(self):
        "Initializes the pygame game engine"
        #pylint: disable=no-member 
        pygame.init()
        #pylint: enable=no-member 

        # Set the display mode        
        self.screen = pygame.display.set_mode(SCREENRECT.size)

        # Decorate the window
        icon = load_image("icon.gif")
        pygame.display.set_icon(icon)
        pygame.display.set_caption(self.title)
        
        self.fpsClock = pygame.time.Clock()

        # Load the scene
        ApplicationManager().load_scene(TitleScene())
        self.load_scene(ApplicationManager().get_scene())
        self.initialize_scene()

    def load_scene(self, scene=None):
        self.currentScene = scene
        if scene is None:
            self.currentScene = ApplicationManager().get_scene()

    def initialize_scene(self):
        "Initialize the scene that is currently loaded"
        self.currentScene.initialize()
        ApplicationManager().scene_initialized()

    def tick(self, fps):
        self.fpsClock.tick(fps)

    def input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                ApplicationManager().running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                ApplicationManager().running = False
            if event.type == KEYDOWN and event.key == K_p:
                ApplicationManager().paused = not ApplicationManager().paused

            self.currentScene.handle_events(event)

    def render(self):
        self.currentScene.render(self.screen)

    def update(self):
        self.currentScene.update()

    def is_running(self):
        return ApplicationManager().running

    def is_paused(self):
        return ApplicationManager().paused

    def is_scene_loading(self):
        return ApplicationManager().sceneLoading

    def quit(self):
        print("Ending the program...")
        #pylint: disable=no-member
        pygame.quit()
        #pylint: enable=no-member
