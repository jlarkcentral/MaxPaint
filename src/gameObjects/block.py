'''
Created on 1 aout 2013

@author: feral
'''

import sys
import random
import pygame
from pygame.locals import *
sys.path.append('../')
from utils import to_pygame, distance, interpolate
sys.path.append('../../lib/pyganim/')
import pyganim

class Block(object):

    def __init__(self,  backgroundScreen, startX, startY, moving=False, path=[]):
        # self.position = (startX,startY)
        # self.positionX,self.positionY = (startX,startY)
        self.rect = Rect(startX,startY,100,40)
        self.active = False
        self.speed = 1
        self.moving = moving
        self.path = path
        self.path_index = 0

        color = random.choice(["blue","red","yellow"])
        self.color = color
        self.img = pygame.image.load("../img/blocks/block_"+color+".png")
        self.anim = pyganim.PygAnimation([(self.img,0.1)])

    def update(self,player,color_dict,plusOneAnim_dict,backgroundScreen,camera,dt):

        if abs((self.rect.y ) - (player.rect.y + 60)) < 5 and \
        self.rect.x <= player.rect.x <= self.rect.x + 100 - 60:
            if not self.active: # and b.color in ['red','blue','yellow']:
                self.active = True
                color_dict[self.color] += 1
                self.anim = plusOneAnim_dict[self.color].getCopy()
                self.anim.play()
                self.anim.blit(backgroundScreen, camera.apply(Rect(self.rect.x+25, self.rect.y, 0, 0)))
        
        # backgroundScreen.blit(self.img, to_pygame(camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), backgroundScreen), (0, self.active*40, 100, 40))
        backgroundScreen.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), (0, self.active*40, 100, 40))
        # backgroundScreen.blit(self.img, Rect(self.rect.x, self.rect.y, 0, 0), (0, self.active*40, 100, 40))       
        if self.active and not self.anim.isFinished():
            self.anim.blit(backgroundScreen, camera.apply(Rect(self.rect.x+25, self.rect.y, 0, 0)))


        if self.moving:
            destination = self.path[self.path_index]
            current = self.rect.topleft
            dist = distance(current,destination)
            t = 1
            if dist < self.speed:
                self.path_index += 1
                self.path_index = self.path_index % len(self.path)
                t = 1
                #print(self.path[self.path_index])
            else:
                t = self.speed / dist
            #self.rect.x, self.rect.y = 
            #print(self.rect.x, self.rect.y)
            pos = interpolate(current,destination, t)
            self.rect.topleft = pos #camera.apply(Rect(pos[0], pos[1], 0, 0)).topleft
