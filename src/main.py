"""

PyGame & PyMunk game test

modified code from platformer example


"""

import random
from random import randint

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

sys.path.append('../lib/')
import pyganim

sys.path.append('screens/')
import startScreen


# INITIALIZATION

def gameGlobalInit():
    global width, height
    global screen
    global fps
    global dt
    global backgroundScreen
    global clock
    width, height = 800,640
    fps = 50
    dt = 1./fps
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    backgroundScreen = pygame.Surface(screen.get_size())
    clock = pygame.time.Clock()
    

def loadPhysics():
    global space
    space = pymunk.Space()
    space.gravity = 0,-1000
    
    def passthrough_handler(space, arbiter):
        if arbiter.shapes[0].body.velocity.y < 0:
            return True
        else:
            return False
            
    space.add_collision_handler(1,2, begin=passthrough_handler)






# MAIN PROGRAM


def main():
    gameGlobalInit()
    loadPhysics()
    startScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
    


if __name__ == '__main__':
    sys.exit(main())
