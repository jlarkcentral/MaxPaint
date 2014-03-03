'''
Created on Aug 9, 2013

@author: primo
'''

import pygame
from pygame.locals import *
from utils import distance,interpolate

class Bullet(object):

    def __init__(self, path, speed, color):

        self.speed = speed
        self.color = color
        self.path = path
        self.path_index = 0
        self.rect = Rect(self.path[0],(5,5))
        self.img = pygame.image.load("../img/bullets/bullet_"+color+".png")
        
        
    def update(self, dt):

        destination = self.path[self.path_index]
        current = self.rect.topleft
        distance_ = distance(current,destination)
        if distance_ < self.speed:
            self.path_index += 1
            self.path_index = self.path_index % len(self.path)
            t = 1        
        else:
            t = self.speed / distance_
        self.rect.topleft = interpolate(current, destination, t)
        self.velocity = ((self.rect.x - current[0])/dt, (self.rect.y - current[1])/dt)   
        