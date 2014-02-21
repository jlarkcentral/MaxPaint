'''
Created on 1 aout 2013

@author: feral
'''

import sys
import random

import pygame
from pygame.locals import *
# import pymunk
# from pymunk.vec2d import Vec2d
# from pymunk.pygame_util
sys.path.append('../')
from utils import to_pygame

sys.path.append('../../lib/pyganim/')
import pyganim

class Block(object):

    def __init__(self,  backgroundScreen, startX, startY, moving=False, path=[]): #space,

        # self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.position = (startX,startY)
        self.positionX,self.positionY = (startX,startY) #self.body.position
        #self.hitbox = pymunk.Segment(space.static_body, (startX,startY), (startX+100,startY), 30 )
        # self.hitbox = pymunk.Poly(self.body,[(0,0),(0,20),(100,20),(100,0)])
        #print(startX,startY)
        #print(self.body.position)
        #print() 
        # self.hitbox.collision_type = 1
        #self.hitbox.layers = 0b1000
        # self.hitbox.friction = 100
        # self.hitbox.group = 1
        # self.hitbox.ignore_draw = True

        self.rect = Rect(self.positionX,self.positionY,100,30)

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
        #self.body.position = to_pygame(camera.apply(Rect(self.positionX, self.positionY, 0, 0)),backgroundScreen)
        #self.positionX, self.positionY = self.body.position

        

        if abs((self.positionY ) - (player.positionY - 20)) < 5 and \
        self.positionX - 44 <= player.positionX and (self.positionX + 80) >= player.positionX:
            if not self.active: # and b.color in ['red','blue','yellow']:
                self.active = True
                color_dict[self.color] += 1
                self.anim = plusOneAnim_dict[self.color].getCopy()
                self.anim.play()
                #self.anim.blit(backgroundScreen, (self.positionX+25,self.positionY))
        backgroundScreen.blit(self.img, to_pygame(camera.apply(Rect(self.positionX, self.positionY, 0, 0)), backgroundScreen), (0, self.active*40, 100, 40))
        if self.active and not self.anim.isFinished():
            self.anim.blit(backgroundScreen, to_pygame(camera.apply(Rect(self.positionX+25, self.positionY, 0, 0)), backgroundScreen))

        #if self.rect.colliderect(player.rect):
        #    if player
        #     player.positionY = self.positionY + 64
        #     print 'collide bottom'
        # elif self.rect.colliderect(player.rectTop):
        #     player.positionY = self.positionY - 30
        #     print 'collide top'
        # elif self.rect.colliderect(player.rectLeft):
        #     player.positionX = self.positionX + 64
        #     print 'collide left'
        # elif self.rect.colliderect(player.rectRight):
        #     player.positionX = self.positionX + 100
        #     print 'collide right'

        # if self.moving:
        #     destination = self.path[self.path_index]
        #     current = Vec2d(self.body.position)
        #     distance = current.get_distance(destination)
        #     t = 1
        #     if distance < self.speed:
        #         self.path_index += 1
        #         self.path_index = self.path_index % len(self.path)
        #         t = 1
        #         #print(self.path[self.path_index])
        #     else:
        #         t = self.speed / distance
        #     #self.positionX, self.positionY = 
        #     #print(self.positionX, self.positionY)
        #     pos = current.interpolate_to(destination, t)
        #     self.body.position = pos #camera.apply(Rect(pos[0], pos[1], 0, 0)).topleft
        #     self.positionX, self.positionY = pos
        #     self.body.velocity = (self.body.position - current) / dt
