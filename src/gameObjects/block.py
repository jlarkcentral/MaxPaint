'''
Created on 1 aout 2013

@author: feral
'''

import sys
import random

import pygame
from pygame.locals import *
import pymunk
from pymunk.pygame_util import to_pygame

sys.path.append('../../lib/pyganim/')
import pyganim

class Block(object):

    def __init__(self, startX, startY):
        
        self.body = pymunk.Body()
        self.positionX = startX
        self.positionY = startY
        self.body.position = self.positionX, self.positionY
        self.hitbox = pymunk.Poly(self.body, [(0,0),(0,50),(100,50),(100,0)], (0,-50))
        self.hitbox.collision_type = 1
        self.hitbox.layers = 0b1000
        self.hitbox.friction = 1
        self.hitbox.group = 1
        self.hitbox.ignore_draw = False
        self.active = False
        self.speed = 0
        
        
        color = random.choice(["blue","red","yellow"])
        self.color = color
        self.img = pygame.image.load("../img/blocks/block_"+color+"_canvas.png")
        self.anim = pyganim.PygAnimation([(self.img,0.1)])

    def update(self,player,color_dict,plusOneAnim_dict,backgroundScreen,camera):
        if abs((self.positionY ) - (player.positionY - 58)) < 5 and \
        self.positionX - 44 <= player.positionX and (self.positionX + 80) >= player.positionX:
            if not self.active: # and b.color in ['red','blue','yellow']:
                self.active = True
                color_dict[self.color] += 1
                self.anim = plusOneAnim_dict[self.color].getCopy()
                self.anim.play()
                self.anim.blit(backgroundScreen, to_pygame(camera.apply(Rect(self.positionX+25, self.positionY, 0, 0)), backgroundScreen))
        backgroundScreen.blit(self.img, to_pygame(camera.apply(Rect(self.positionX, self.positionY, 0, 0)), backgroundScreen), (0, self.active*50, 100, 50))
        if self.active and not self.anim.isFinished():
            self.anim.blit(backgroundScreen, to_pygame(camera.apply(Rect(self.positionX+25, self.positionY, 0, 0)), backgroundScreen))
