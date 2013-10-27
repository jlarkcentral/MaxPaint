'''
Created on Aug 8, 2013

@author: primo
'''

from pymunk.vec2d import Vec2d

import pygame
from pygame.locals import *

import pymunk
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

from bullet import Bullet

class Enemy(object):

    def __init__(self, path, speed):
                
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.body.position = self.path[0]
        self.positionX, self.positionY = self.body.position
        self.hitbox = pymunk.Poly(self.body, [(0,0),(0,40),(40,40),(40,0)],(0,-40))
        self.hitbox.ignore_draw = False
        self.hitbox.group = 1
        self.hitbox.friction = 100
        self.hitbox.layers = 0b1000
        self.hitbox.collision_type = 1
        self.img = pygame.image.load("../img/enemies/enemy1.png")
        self.bullets = []
        self.shootingDelay = 0
    

    def shootAtTarget(self,targetPosition):
        path = []
        path = [(self.body.position),targetPosition + (targetPosition - self.body.position)*100]    
        b = Bullet(path, 5)
        self.bullets.append(b)


    def updateBullets(self,dt, backgroundScreen, camera, playerPositionX, playerPositionY, color_dict):
        for b in self.bullets:
            b.update(dt)
            if b.positionX < 0 or b.positionX > 800 or b.positionY < 0 or b.positionY > 640:
                self.bullets.remove(b)
            #if abs(b.positionX - playerPositionX + 32) < 10 and \
            #abs( (640-(camera.state.y + b.positionY - 32)) - (640-(camera.state.y + playerPositionY - 32)) ) < 40:
            if Vec2d(playerPositionX + 32,playerPositionY - 32).get_distance((b.positionX + 20,b.positionY-20)) < 40 :
                color_dict["yellow"] -= 1
                self.bullets.remove(b)
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen))


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
