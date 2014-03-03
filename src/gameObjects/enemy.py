'''
Created on Aug 8, 2013

@author: primo
'''
import sys
import random
import pygame
from pygame.locals import *
import pyganim
from bullet import Bullet
from utils import *


class Enemy(object):

    def __init__(self, path, speed):
                
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.rect = Rect(self.path[0],(64,64))
        self.img = pygame.image.load("../img/enemies/enemy2.png")
        # self.hitSound = pygame.mixer.Sound("../sounds/playerHit.wav")
        self.bullets = []
        self.shootingDelay = 0
        self.waitDelay = 0
        self.lives = 1
        

    def shootAtTarget(self,targetPosition):
        path = [self.rect.topleft, vect_add(targetPosition,vect_mul(vect_sub(targetPosition, self.rect.topleft),10))]    
        b = Bullet(path, 5, random.choice(["blue","red","yellow"]))
        self.bullets.append(b)


    def updateBullets(self,dt, backgroundScreen, camera, player):
        for b in self.bullets:
            b.update(dt)
            if b.rect.x < 0 or b.rect.x > 800 or b.rect.y < 0 or b.rect.y > camera.maxH:
                self.bullets.remove(b)
            else:
                # if distance((player.rect.x + 32,player.rect.y - 32),(b.rect.x + 20,b.rect.y-20)) < 40 :
                if b.rect.colliderect(player.rect):
                    if player.shieldDelay == 0:
                        # self.hitSound.play()
                        player.lives -= 1
                        # player.changeColor(b.color)
                    self.bullets.remove(b)
            backgroundScreen.blit(b.img, camera.apply(Rect(b.rect.x, b.rect.y, 0, 0)))

    def update(self, dt, backgroundScreen, camera, player, isNight):
        # movement
        destination = self.path[self.path_index]
        current = self.rect.topleft
        dist = distance(current,destination)
        t = 1
        if dist < self.speed:
            self.path_index += 1
            self.path_index = self.path_index % len(self.path)
            t = 1
        else:
            t = self.speed / dist
        pos = interpolate(current,destination, t)
        self.rect.topleft = pos

        # waiting at block edges
        if self.waitDelay == 0 and (dist < 0 or self.path_index == 0 and dist < 5):
            self.waitDelay = random.randint(1,200)
        elif self.waitDelay > 0:
            self.waitDelay -= 1

        

        # shooting
        if distance((player.rect.x + 32,player.rect.y - 32),(self.rect.x + 20,self.rect.y-20)) < 300 \
            and self.shootingDelay == 0:
            self.shootAtTarget((player.rect.x + 32,player.rect.y - 32))
            self.shootingDelay = 30
        if self.shootingDelay > 0:
            self.shootingDelay -= 1

        # display
        backgroundScreen.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), (0, 64*0*(3-self.lives), 64, 64))
        
        # bullets
        self.updateBullets(dt, backgroundScreen, camera, player)

