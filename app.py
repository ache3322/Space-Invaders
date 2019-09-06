#====================================================================
# Name: app.py
# Created by: Austin Che
# Created on: Sep 6, 2019
# Modified on: Sep 6, 2019
# 
# Description:
#   Contains common classes used in the project.
#====================================================================
class Singleton(object):
    """
    Singleton implementation.\n
    Created by: Guido van Rossum\n
    https://www.python.org/download/releases/2.2.3/descrintro/
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class ApplicationManager(Singleton):
    """
    The ApplicationManager contains states and behaviours
    to control the game and scenes
    """
    running = True
    paused = False
    scene = None
    sceneLoading = False

    def __init__(self):
        pass

    def load_scene(self, scene):
        self.scene = scene
        self.sceneLoading = True

    def scene_initialized(self):
        self.sceneLoading = False

    def get_scene(self):
        return self.scene