'''
Created on Aug 8, 2013

@author: primo
'''
import sys
import random
import pygame
from pygame.locals import *
from pygame.color import *
import pyganim
from bullet import Bullet
from utils import *
from bulletFragment import *


class Enemy(object):

    def __init__(self, path, speed):
                
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.rect = Rect(self.path[0],(64,64))
        self.img = pygame.image.load("../img/enemies/enemy.png")
        # self.hitSound = pygame.mixer.Sound("../sounds/playerHit.wav")
        self.bullets = []
        self.shootingDelay = 0
        self.waitDelay = 0
        self.lives = 1

        self.bulletFragments = []
        

    def shootAtTarget(self,targetPosition):
        # path = [(self.rect.x+20,self.rect.y+20), vect_add(targetPosition,vect_mul(vect_sub(targetPosition, self.rect.topleft),10))]    
        direction_raw = vect_sub(targetPosition,self.rect.topleft)
        direction = vect_mul(direction_raw,1.0/(vect_norm(direction_raw)))
        b = Bullet((self.rect.x+20,self.rect.y+20),direction, 5, random.choice(["blue","red","yellow"]))
        self.bullets.append(b)


    def updateBullets(self,dt, backgroundScreen, camera, player,blocks):
        for b in self.bullets:
            b.update(dt,backgroundScreen, camera)
            if b.outOfScreen:
                self.bullets.remove(b)
            else:
                if b.rect.colliderect(player.rect):
                    if player.shieldDelay == 0:
                        # self.hitSound.play()
                        player.hitWithColor(b.color)
                    for _ in range(random.randint(3,15)):
                        self.bulletFragments.append(BulletFragment(b.rect.center,THECOLORS[b.color]))
                    self.bullets.remove(b)
                else:
                    for block in blocks:
                        if b.rect.colliderect(block.rect):
                            for _ in range(random.randint(3,15)):
                                self.bulletFragments.append(BulletFragment(b.rect.center,THECOLORS[b.color]))
                            self.bullets.remove(b)
                            break
        for bf in self.bulletFragments:
            bf.update(backgroundScreen, camera)
            if bf.kill:
                self.bulletFragments.remove(bf)

    def update(self, dt, backgroundScreen, camera, player, blocks):
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
        if distance(player.rect.center,self.rect.center ) < 300 \
            and self.shootingDelay == 0:
            self.shootAtTarget(player.rect.center)
            self.shootingDelay = 30
        if self.shootingDelay > 0:
            self.shootingDelay -= 1



        # bullets
        self.updateBullets(dt, backgroundScreen, camera, player,blocks)


        # display
        backgroundScreen.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), (0, 64*0*(3-self.lives), 64, 64))
        

