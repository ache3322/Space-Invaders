#====================================================================
# Name: ui.py
# Created by: Austin Che
# Created on: Sep 1, 2019
# Modified on: Sep 6, 2019
# 
# Description:
#   This file contains pygame UI.
#====================================================================
from enum import Enum
import pygame
import colour

class Justify(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


class Text():
    """
    The Text class is used to create and render pygame text.\n
    @attr x [int] - The x position\n
    @attr y [int] - The y position\n
    @attr width [int] - The width of the text\n
    @attr height [int] - The height of the text\n
    @attr fonttype [str] - The type of font\n
    @attr fontsize [int] - The size of the text\n
    @attr text [str] - The text to display\n
    """
    def __init__(self, x, y, fonttype="courier", fontsize=20, text="", colour=(255,255,255), justified=Justify.LEFT):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(fonttype, fontsize)
        self.rerender = False

        self.foreColour = colour
        self.justified = justified
        self.surface = self.__render_font__(self.text)

    def set_colour(self, colour):
        self.foreColour = colour
        self.rerender = True

    def set_justified(self, justified):
        self.justified = justified
    
    def render(self, screen):
        if self.rerender:
            self.surface = self.__render_font__(self.text)

        textRect = self.surface.get_rect()
        pos_x = self.x

        if self.justified == Justify.LEFT:
            pos_x = self.x - textRect.left
        if self.justified == Justify.CENTER:
            pos_x = self.x - textRect.centerx
        if self.justified == Justify.RIGHT:
            pos_x = self.x - textRect.right

        screen.blit(self.surface, (pos_x, self.y))

    def __render_font__(self, text):
        "Wrapper function around font.render() -> Surface"
        self.rerender = False
        return self.font.render(text, False, self.foreColour)


class Button():
    """
    Create a pygame button.\n
    @attr x [int] - The x-position\n
    @attr y [int] - The y-position\n
    @attr width [int] - The width of the button\n
    @attr height [int] - The height of the button\n
    @attr text [int] - The text to display inside the button
    """
    def __init__(self, x, y, width, height, text=""):
        self.text = text
        self.pos = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.w = width
        self.h = height

        self.font = pygame.font.SysFont("courier", 50)

        self.activeColour = colour.GREY        # Button is active
        self.inactiveColour = colour.WHITE     # Button is inactive
        self.pressedColour = None               # Button is pressed

        self.foreColour = colour.BLUE
        self.backColour = colour.BLACK

        self.hasPressed = False

    def set_position(self, x, y):
        """
        Set the position of the button to display on the screen.\n
        @param rect [pygame.Rect]
        """
        self.pos = pygame.Rect(x, y, 0, 0)

    def set_text(self, newText):
        self.text = newText

    def set_button_colour(self, active, inactive=None, pressed=None):
        "Set the colour of the button when active, inactive, and pressed."
        self.activeColour = active
        self.inactiveColour = inactive
        if pressed is not None:
            self.pressedColour = pressed

    def set_font_colour(self, fore, back):
        "Set the colour of the font. Takes in a foreground and background colour (R,G,B)."
        self.foreColour = fore
        self.backColour = back

    def handle_events(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.pos.collidepoint(mouse[0], mouse[1]):
            if click[0] == 1 and self.hasPressed is False:
                self.hasPressed = True

                # Perform action function
                if self.actionFunc != None:
                    self.actionFunc()
            elif click[0] == 0 and self.hasPressed:
                # Prevent accidental second mouse click
                self.hasPressed = False

    def render(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()        

        if self.pos.collidepoint(mouse[0], mouse[1]):
            # Button is active
            if self.activeColour is not None:
                pygame.draw.rect(screen, self.activeColour, self.pos)

            if click[0] == 1:
                # Button is pressed
                if self.pressedColour is not None:
                    pygame.draw.rect(screen, self.pressedColour, self.pos)
        else:
            # Button is inactive
            if self.inactiveColour is not None:
                pygame.draw.rect(screen, self.inactiveColour, self.pos)
         
        surface = self.__renderFont(self.text)
        textRect = surface.get_rect()
        textRect.center = (self.x + (self.w/2), self.y + (self.h/2))
        
        screen.blit(surface, textRect)

    def __renderFont(self, text, highlight=None):
        "Wrapper function around font.render() -> Surface"
        return self.font.render(text, False, self.foreColour)        

    def actionFunc(self): 
        "Event handler function to handle on_click events."
        pass