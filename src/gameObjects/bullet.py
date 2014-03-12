'''
Created on Aug 9, 2013

@author: primo
'''
import sys
import pygame
from pygame.locals import Rect
sys.path.append('../')
from utils import vect_add, vect_mul
from gameObject_ import GameObject_

class Bullet(GameObject_):
    
    def __init__(self, startPosition ,direction, speed, color):
        super(Bullet, self).__init__()
        self.speed = speed
        self.color = color
        self.direction = direction
        self.rect = Rect(startPosition,(30,30))
        self.img = pygame.image.load("../img/bullets/bullet_"+color+".png")
        self.outOfScreen = False

    def update(self):
        self.rect.topleft = vect_add(self.rect.topleft,vect_mul(self.direction,self.speed))
        if self.rect.x < 0 or self.rect.x > 800 or self.rect.y < 0 or self.rect.y > 3200:
            self.outOfScreen = True
    
    def render(self,displaySurface, camera):
        displaySurface.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)))