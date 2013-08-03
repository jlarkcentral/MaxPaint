'''
Created on 1 aout 2013

@author: feral
'''

import pygame

import pymunk
from pymunk.vec2d import Vec2d

from random import randint

class Block(object):
    '''
    Moving platform class
    '''




    def __init__(self):
        '''
        Constructor
        '''
        
        self.PLATFORM_SPEED = 1

        
        randPosX = randint(10,590)
        self.path = [(randPosX,600),(randPosX,0)]
        self.path_index = 0
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.positionX = randPosX
        self.positionY = 600
        self.body.position = self.positionX, self.positionY
        self.segment = pymunk.Segment(self.body, (0, 0), (100, 0), 10)
        self.segment.friction = 1.
        self.segment.group = 1
        randColorIndex = randint(0,3)
        if(randColorIndex == 0):
            self.color = "blue"
            #self.imgActive = pygame.image.load("../img/blockBlueActive.png")
            #self.imgInactive = pygame.image.load("../img/blockBlueInactive.png")
        elif(randColorIndex == 1):
            self.color = "red"
        elif(randColorIndex == 2):
            self.color = "yellow"
        elif(randColorIndex == 3):
            self.color = "green"
        else:
            print 'bad color index !'
        self.segment.color = pygame.color.THECOLORS[self.color]
        
        self.isCurrentBlock = False
        self.active = False
       
    def update(self, dt):
        destination = self.path[self.path_index]
        current = Vec2d(self.body.position)
        distance = current.get_distance(destination)
        if distance < self.PLATFORM_SPEED:
            self.path_index += 1
            self.path_index = self.path_index % len(self.path)
            t = 1
        else:
            t = self.PLATFORM_SPEED / distance
        self.positionX, self.positionY = current.interpolate_to(destination, t)
        self.body.position = self.positionX, self.positionY
        self.body.velocity = (self.body.position - current) / dt
        
        self.isCurrentBlock = False    