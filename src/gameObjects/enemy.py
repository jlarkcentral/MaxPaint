'''
Created on Aug 8, 2013

@author: primo
'''
import sys
import random

import pygame
from pygame.locals import *

import pyganim

import pymunk
from pymunk.vec2d import Vec2d
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
        self.hitbox = pymunk.Circle(self.body, 50, offset=(0,0))#[(0,0),(0,30),(70,160),(130,160),(30,0),(0,0)])
        self.hitbox.ignore_draw = False
        self.hitbox.group = 1
        self.hitbox.friction = 100
        self.hitbox.layers = 0b1000
        self.hitbox.collision_type = 1
        self.img = pygame.image.load("../img/enemies/enemy2_cvs.png")
        self.hitSound = pygame.mixer.Sound("../sounds/playerHit.wav")
        self.bullets = []
        self.shootingDelay = 0
        self.waitDelay = 0
        self.lives = 3
        #self.killAnim = pyganim.loadAnim('../img/anims/enemyKill',0.05)

        

    def shootAtTarget(self,targetPosition):
        path = [(Vec2d((self.positionX+15,self.positionY))),targetPosition + (targetPosition - self.body.position)*10]    
        b = Bullet(path, 5, random.choice(["blue","red","yellow"]))
        self.bullets.append(b)


    def updateBullets(self,dt, backgroundScreen, camera, player):
        playerHit = False
        for b in self.bullets:
            b.update(dt)
            if b.positionX < 0 or b.positionX > 800 or b.positionY < 0 or b.positionY > camera.maxH:
                self.bullets.remove(b)
            else:
                if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((b.positionX + 20,b.positionY-20)) < 40 :
                    if player.shieldDelay == 0:
                        self.hitSound.play()
                        player.lives -= 1
                        player.changeColor(b.color)
                    self.bullets.remove(b)
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen))
        return playerHit

    def update(self, dt, backgroundScreen, camera, player):
        # movement
        destination = self.path[self.path_index]
        current = Vec2d(self.body.position)
        distance = current.get_distance(destination)
        toEdge = self.positionX - self.path[self.path_index][0]
        t = 1
        if distance < self.speed:
            if self.waitDelay == 0:
                self.path_index += 1
                self.path_index = self.path_index % len(self.path)
                t = 1
        else:
            t = self.speed / distance
        self.positionX, self.positionY = current.interpolate_to(destination, t)
        self.body.position = self.positionX, self.positionY
        self.body.velocity = (self.body.position - current) / dt

        # waiting at block edges
        if self.waitDelay == 0 and (toEdge < 0 or self.path_index == 0 and toEdge < 5):
            self.waitDelay = random.randint(1,200)
        elif self.waitDelay > 0:
            self.waitDelay -= 1

        

        # shooting
        if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((self.positionX + 20,self.positionY-20)) < 300 \
            and self.shootingDelay == 0:
            self.shootAtTarget((player.positionX + 32,player.positionY - 32))
            self.shootingDelay = 30
        if self.shootingDelay > 0:
            self.shootingDelay -= 1

        # display
        backgroundScreen.blit(self.img,to_pygame(camera.apply(Rect(self.positionX, self.positionY+18, 0, 0)), backgroundScreen),(0, 64*(3-self.lives), 64, 64))
        
        # bullets
        self.updateBullets(dt, backgroundScreen, camera, player)



        # colliding ?
        if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((self.positionX + 20,self.positionY-20)) < 50 :
            return True
        return False
