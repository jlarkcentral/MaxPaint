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
    Moving platform class
    '''




    def __init__(self, previousBlockPosition):
        '''
        Constructor
        '''
        
        self.PLATFORM_SPEED = 1
        
        randPosX = 0
        if previousBlockPosition >= 490:
            randPosX = randint(110,previousBlockPosition - 100)
        elif previousBlockPosition <= 210:
            randPosX = randint(previousBlockPosition+100,590)    
        else:    
            randPosBool = random.choice([True, False])
            if randPosBool:
                randPosX = randint(110,previousBlockPosition - 100)
            else:
                randPosX = randint(previousBlockPosition+100,590)    
        self.path = [(randPosX,640),(randPosX,0)]
        self.path_index = 0
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.positionX = randPosX
        self.positionY = 640
        self.body.position = self.positionX, self.positionY
        self.segment = pymunk.Segment(self.body, (0, 0), (100, 0), 10)
        self.segment.friction = 1.
        self.segment.group = 1
        self.segment.ignore_draw = True
        randColorIndex = randint(0,3)
        if(randColorIndex == 0):
            self.color = "blue"
            self.PLATFORM_SPEED = 1.0
            self.img = pygame.image.load("../img/blockBlue.png")
        elif(randColorIndex == 1):
            self.color = "red"
            self.PLATFORM_SPEED = 1.75
            self.img = pygame.image.load("../img/blockRed.png")
        elif(randColorIndex == 2):
            self.color = "yellow"
            self.PLATFORM_SPEED = 1.5
            self.img = pygame.image.load("../img/blockYellow.png")
        elif(randColorIndex == 3):
            self.color = "green"
            self.PLATFORM_SPEED = 1.25
            self.img = pygame.image.load("../img/blockGreen.png")
        else:
            print 'bad color index !'
        #self.segment.color = pygame.color.THECOLORS[self.color]

        
        self.isCurrentBlock = False
        self.active = False
        
        #self.PLATFORM_SPEED = randint(5,20) / 10.0
        
       
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