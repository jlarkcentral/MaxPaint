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

    def __init__(self, startX, startY, randColorIndex):
        
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
        
        if randColorIndex < 5:
            randColorIndex = randint(0,3)
        if(randColorIndex == 0):
            self.color = "blue"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blocks/blockBlue.png")
        elif(randColorIndex == 1):
            self.color = "red"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blocks/blockRed.png")
        elif(randColorIndex == 2):
            self.color = "yellow"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blocks/blockYellow.png")
        elif(randColorIndex == 3):
            self.color = "green"
            self.PLATFORM_SPEED = 0
            self.img = pygame.image.load("../img/blocks/blockGreen.png")
        
        
        
           