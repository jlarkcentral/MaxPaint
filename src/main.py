"""

PyGame game test

modified code from platformer example

"""

import sys
import pygame
sys.path.append('screens/')
from screenManager import ScreenManager


def main():
    width, height = 800,640
    fps = 50
    pygame.init()
    pygame.mixer.init()
    display = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    manager = ScreenManager()
    running = True
    while running:
        if pygame.event.get(pygame.QUIT):
            running = False
        manager.screen.handle_events(pygame.event.get())
        manager.screen.update()
        manager.screen.render(display)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    sys.exit(main())
