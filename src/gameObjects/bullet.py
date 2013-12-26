'''
Created on Aug 9, 2013

@author: primo
'''

import pygame

import pymunk
from pymunk.vec2d import Vec2d

class Bullet(object):

    def __init__(self, path, speed, color):

        self.speed = speed
        self.color = color
        self.path = path
        self.path_index = 0
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.body.position = self.path[0]
        self.positionX, self.positionY = self.body.position
        self.hitbox = pymunk.Circle(self.body, 5, (5,-5))
        self.hitbox.ignore_draw = False
        self.hitbox.group = 1
        self.hitbox.friction = 100
        self.hitbox.layers = 0b1000
        self.hitbox.collision_type = 1
        self.img = pygame.image.load("../img/bullets/bullet_"+color+".png")
        
        
    def update(self, dt):

        destination = self.path[self.path_index]
        current = Vec2d(self.body.position)
        distance = current.get_distance(destination)
        if distance < self.speed:
            self.path_index += 1
            self.path_index = self.path_index % len(self.path)
            t = 1        
        else:
            t = self.speed / distance
        self.positionX, self.positionY = current.interpolate_to(destination, t)
        self.body.position = self.positionX, self.positionY
        self.body.velocity = (self.body.position - current) / dt    
        