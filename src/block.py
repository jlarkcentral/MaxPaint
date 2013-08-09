'''
Created on 1 aout 2013

@author: feral
'''

import pygame

import pymunk
from pymunk.vec2d import Vec2d

import random
from random import randint

class Block(object):
    '''
    '''


    def __init__(self, startX, startY, randColorIndex):
        '''
        Constructor
        '''
        
        self.body = pymunk.Body()
        self.positionX = startX
        self.positionY = startY
        self.body.position = self.positionX, self.positionY
        self.segment = pymunk.Segment(self.body, (0, 0), (100, 0), 10)
        self.segment.collision_type = 1
        self.segment.layers = self.segment.layers ^ 0b1000
        
        self.segment.friction = 100
        self.segment.group = 1
        self.segment.ignore_draw = True
        
        
        
        randColorIndex = randint(0,3)
        if(randColorIndex == 0):
            self.color = "blue"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blockBlue.png")
        elif(randColorIndex == 1):
            self.color = "red"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blockRed.png")
        elif(randColorIndex == 2):
            self.color = "yellow"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blockYellow.png")
        elif(randColorIndex == 3):
            self.color = "green"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blockGreen.png")
        else:
            self.img = pygame.image.load("../img/tile.png")

        
        self.active = False
           