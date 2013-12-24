"""

PyGame & PyMunk game test

modified code from platformer example

Main program

"""

import random
from random import randint
import sys
import pygame
from pygame.locals import *
import pymunk
sys.path.append('screens/')
import startScreen


# Initialization
def gameGlobalInit():
    global width, height
    global screen
    global fps
    global dt
    global backgroundScreen
    global clock
    global space
    width, height = 800,640
    fps = 50
    dt = 1./fps
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width,height))
    backgroundScreen = pygame.Surface(screen.get_size())
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = 0,-1000


#################################################


def main():
    gameGlobalInit()
    startScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
    


if __name__ == '__main__':
    sys.exit(main())