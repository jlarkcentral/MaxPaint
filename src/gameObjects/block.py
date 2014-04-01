'''
Created on 1 aout 2013

@author: feral
'''

import sys
import random
import pygame
sys.path.append('../../lib/pyganim/')
import pyganim
from pygame.locals import Rect
from utils import distance, interpolate, blockPlusOneAnim
from gameObject_ import GameObject_


class Block(GameObject_):
    def __init__(self, startX, startY):
        super(Block, self).__init__()
        self.rect = Rect(startX,startY,100,40)
        self.active = False
        self.selected = False
        self.speed = 1
        color = random.choice(["blue","red","yellow"])
        self.color = color
        self.note = pygame.mixer.Sound('../sounds/notes/plouit_'+self.color+'.wav')
        self.img = pygame.image.load("../img/blocks/block_"+color+"_pix.png").convert_alpha()
        self.anim = blockPlusOneAnim(self.color)
        # self.selectAnim = pyganim.loadAnim('../img/anims/selectedBlock', 0.1,True)
        self.selectedImg = pygame.image.load("../img/blocks/block_"+color+"_selected_pix.png").convert_alpha()
        self.tralala = False
        self.playing = False
        self.addingPower = False


    def update(self,player):
        if self.selected:
            self.img = self.selectedImg
    

    def render(self,displaySurface,camera):
        displaySurface.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), (0, (not self.active)*40, 100, 40))
        # if self.active and not self.playing:
        #     self.note.play()
        #     self.playing = True
        if self.addingPower and not self.anim.isFinished():
            self.anim.play()
            self.anim.blit(displaySurface, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)))
        if self.selected:
            self.img = self.selectedImg
            # self.selectAnim.play()
            # self.selectAnim.blit(displaySurface, camera.apply(Rect(self.rect.x-10, self.rect.y-10, 0, 0)))


