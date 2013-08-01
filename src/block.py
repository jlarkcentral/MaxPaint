'''
Created on 1 aout 2013

@author: feral
'''

import pygame
import pymunk
from random import randint

class Block(object):
    '''
    Moving platform class
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        randPosX = randint(10,590)
        self.path = [(randPosX,600),(randPosX,0)]
        self.path_index = 0
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.body.position = randPosX, 600
        self.segment = pymunk.Segment(self.body, (-25, 0), (25, 0), 5)
        self.segment.friction = 1.
        self.segment.group = 1
        randColorIndex = randint(0,3)
        if(randColorIndex == 0):
            self.segment.color = pygame.color.THECOLORS["blue"]
        elif(randColorIndex == 1):
            self.segment.color = pygame.color.THECOLORS["red"]
        elif(randColorIndex == 2):
            self.segment.color = pygame.color.THECOLORS["yellow"]
        elif(randColorIndex == 3):
            self.segment.color = pygame.color.THECOLORS["green"]
        else:
            print 'bad color index !'
        
        