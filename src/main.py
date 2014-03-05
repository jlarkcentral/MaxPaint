"""

PyGame game test

modified code from platformer example

"""

import sys
import pygame
sys.path.append('screens/')
import startScreen



def main():
    # init
    width, height = 800,640
    fps = 50
    dt = 1./fps
    
    pygame.init()
    pygame.mixer.init()

    
    screen = pygame.display.set_mode((width,height))
    backgroundScreen = pygame.Surface(screen.get_size())
    clock = pygame.time.Clock()

    # start
    startScreen.show(width,height,backgroundScreen,dt,screen,clock,fps)
    


if __name__ == '__main__':
    sys.exit(main())