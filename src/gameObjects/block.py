'''
Created on 1 aout 2013

@author: feral
'''

import random
import pygame
from pygame.locals import Rect
from utils import distance, interpolate, blockPlusOneAnim
from gameObject_ import GameObject_


class Block(GameObject_):
    def __init__(self, startX, startY, moving=0, path=[]):
        super(Block, self).__init__()
        self.rect = Rect(startX,startY,100,40)
        self.active = False
        self.speed = 1
        self.moving = moving # -1 : horizontal , 1 : vertical
        self.path = path
        self.path_index = 0

        color = random.choice(["blue","red","yellow"])
        self.color = color
        self.img = pygame.image.load("../img/blocks/block_"+color+".png")
        self.anim = blockPlusOneAnim(self.color)

    def update(self,player):

        if abs((self.rect.y ) - (player.rect.y + 60)) < 5 and \
        self.rect.x <= player.rect.x <= self.rect.x + 100 - 60:
            if not self.active:
                self.active = True
                player.addPowerUp(self.color)
        
        if self.moving:
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
    

    def render(self,displaySurface,camera):
        displaySurface.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), (0, self.active*40, 100, 40))
        if self.active and not self.anim.isFinished():
            self.anim.play()
            self.anim.blit(displaySurface, camera.apply(Rect(self.rect.x+25, self.rect.y, 0, 0)))