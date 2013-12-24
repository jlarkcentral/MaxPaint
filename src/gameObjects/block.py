'''
Created on 1 aout 2013

@author: feral
'''

import pygame

import pymunk

import random
from random import randint

class Block(object):

    def __init__(self, startX, startY):
        
        self.body = pymunk.Body()
        self.positionX = startX
        self.positionY = startY
        self.body.position = self.positionX, self.positionY
        self.hitbox = pymunk.Poly(self.body, [(0,0),(0,50),(100,50),(100,0)], (0,-50))
        self.hitbox.collision_type = 1
        self.hitbox.layers = 0b1000
        self.hitbox.friction = 1
        self.hitbox.group = 1
        self.hitbox.ignore_draw = False
        self.active = False
        
        
        randColorIndex = randint(0,2)
        if(randColorIndex == 0):
            self.color = "blue"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blocks/blockBlue_canvas.png")
        elif(randColorIndex == 1):
            self.color = "red"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blocks/blockRed_canvas.png")
        elif(randColorIndex == 2):
            self.color = "yellow"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blocks/blockYellow_canvas.png") 
        
        
           