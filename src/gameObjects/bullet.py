'''
Created on Aug 9, 2013

@author: primo
'''

import pygame
from pygame.locals import *
from utils import *

class Bullet(object):

    def __init__(self, startPosition ,direction, speed, color):

        self.speed = speed
        self.color = color
        self.direction = direction
        self.rect = Rect(startPosition,(5,5))
        self.img = pygame.image.load("../img/bullets/bullet_"+color+".png")
        self.outOfScreen = False
        
        
    def update(self, dt):
        self.rect.topleft = vect_add(self.rect.topleft,vect_mul(self.direction,self.speed))
        if self.rect.x < 0 or self.rect.x > 800 or self.rect.y < 0 or self.rect.y > 3200:
            self.outOfScreen = True