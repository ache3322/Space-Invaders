#====================================================================
# Name: main.py
# Created by: Austin Che
# Created on: Aug 28, 2019
#====================================================================
from managers import GameManager


def __main__():

    manager = GameManager()
    manager.initialize()

    # Main game loop
    while manager.is_running():
        manager.tick(60)

        if manager.is_scene_loading():
            manager.load_scene()
            manager.initialize_scene()

        manager.input()

        if not manager.is_paused():
            manager.render()
            manager.update()

    manager.quit()
    return 0

if __name__ == "__main__": __main__()
