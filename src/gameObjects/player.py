'''
Created on 2 aout 2013

player class

@author: feral

modified code from collision example:
python-forum.org/viewtopic.php?f=26&t=1889

'''

import sys
import random
import pygame
from pygame.locals import Rect
from pygame.color import THECOLORS
sys.path.append('../../lib/pyganim/')
import pyganim
from bullet import Bullet
from gameObject_ import GameObject_
from fragment import Fragment
import utils

    

class Player(GameObject_):
    def __init__(self):
        super(Player, self).__init__()
        # physics properties
        self.x_vel = self.y_vel = self.y_vel_i = 0
        self.grav = 20
        self.fall = False
        self.time = 0 # None
        self.speed = 10
        self.jump_power = 10
        self.rect = Rect(0, 0, 60, 60)
        self.rect.topleft = (150,3000)
        self.collide_ls = [] #what obstacles does the player collide with
        self.direction = 1
        self.direction_offset = 0
        self.animation_offset = 0
        self.animationTicks = 0
        self.spidering = False
        self.onBlock = None
        self.finished = False
        
        # game properties
        self.bullets = []
        self.mines = 0
        self.minesCount = 0
        self.mining = False
        self.slomoDelay = 0
        self.shields = 0
        self.shieldsCount = 0
        self.shieldDelay = 0
        self.killed = False
        self.timePower = 0
        self.timePowerCount = 0


        # pics, anims and sound
        self.shieldAnim = pyganim.loadAnim('../img/anims/shield',0.1,True)
        self.timeAnim = pyganim.loadAnim('../img/anims/time',0.1,True)
        self.shootSound = pygame.mixer.Sound("../sounds/playerShoot.wav")
        self.shieldSound = pygame.mixer.Sound("../sounds/playerShield.wav")
        self.hitSound = pygame.mixer.Sound("../sounds/playerHit.wav")
        self.noteRed = pygame.mixer.Sound('../sounds/notes/plouit_red.wav')
        self.noteBlue = pygame.mixer.Sound('../sounds/notes/plouit_blue.wav')
        self.noteYellow = pygame.mixer.Sound('../sounds/notes/plouit_yellow.wav')


        self.img = pygame.image.load("../img/player/kube_new_pix.png").convert_alpha()



    def physicsUpdate(self):
        if self.fall:
            self.time += 2 # frame_number # pygame.time.get_ticks()
            self.y_vel = self.grav*((self.time)/100.0) + self.y_vel_i
        else:
            self.time = 0
            self.y_vel = 0

    def positionUpdate(self,blocks):
        """Calculate where our player will end up this frame including collissions."""
        #Has the player walked off an edge?
        if not self.fall and not self.collide_with(blocks,[0,1]):
            self.fall = True
        #Has the player landed from a fall or jumped into an object above them?
        elif self.fall and self.collide_with(blocks,[0,int(self.y_vel)]):
            self.y_vel = self.adjust_pos(self.collide_ls,[0,int(self.y_vel)],1)
            self.y_vel_i = 0
            self.fall = False
        self.rect.y += int(self.y_vel) #Update y position before testing x.
        #Is the player running into a wall?.
        if self.collide_with(blocks,(int(self.x_vel),0)):
            self.x_vel = self.adjust_pos(self.collide_ls,[int(self.x_vel),0],0)
        self.rect.x += int(self.x_vel)
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 740:
            self.rect.x = 740
        if self.rect.y < 40:
            self.rect.y = 40
        elif self.rect.y > 3160:
            self.rect.y = 3200
        # if not self.collide_ls:
        #     self.onBlock = None
        if self.rect.y < 300:
            self.finished = True
    
    def adjust_pos(self,blocks,offset,off_ind):
        offset[off_ind] += (1 if offset[off_ind]<0 else -1)
        while 1:
            if any(self.collide_with(self.collide_ls,offset)):
                offset[off_ind] += (1 if offset[off_ind]<0 else -1)
            else:
                return offset[off_ind]

    def collide_with(self,blocks,offset):
        test = ((self.rect.x+offset[0],self.rect.y+offset[1]),self.rect.size)
        self.collide_ls = []
        for block in blocks:
            if pygame.Rect(test).colliderect(block.rect):
                if self.rect.y > block.rect.y and block.rect.x-60 < self.rect.x < block.rect.x+100:
                    self.spidering = True
                elif self.rect.y < block.rect.y:
                    self.spidering = False
                self.collide_ls.append(block)
                self.onBlock = block
                if not block.active:
                    block.active = True
                    self.addPowerUp(block)
        return self.collide_ls

    def addPowerUp(self,block):
        if block.color == "red":
            self.minesCount += 1
            if self.minesCount == 5:
                self.minesCount = 0
                self.mines += 1
                self.noteRed.play()
                block.addingPower = True
        if block.color == "blue":
            self.shieldsCount += 1
            if self.shieldsCount == 5:
                self.shieldsCount = 0
                self.shields += 1
                self.noteBlue.play()
                block.addingPower = True
        if block.color == "yellow":
            self.timePowerCount += 1
            if self.timePowerCount == 5:
                self.timePowerCount = 0
                self.timePower += 1
                self.noteYellow.play()
                block.addingPower = True

    def shieldUpdate(self):
        if self.shieldDelay > 0:
            self.shieldDelay -= 1

    def slomoUpdate(self):
        if self.slomoDelay > 0:
            self.slomoDelay -= 1

    def animationUpdate(self,frame_number):
        self.direction_offset = self.spidering*128 + (self.direction==-1) * 64
        if abs(self.x_vel) > 1:
            self.animation_offset = 64 *int(self.animationTicks / 8 % 4)
        elif self.fall and not self.spidering:
            self.animation_offset = 128
        else:
            self.animation_offset = 0
        if self.animationTicks == 32:
            self.animationTicks = 0
        else:
            self.animationTicks += 1

    def controlsUpdate(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0
        if not self.finished:
            if keys[pygame.K_LEFT]:
                self.x_vel -= self.speed
                self.direction = -1
            if keys[pygame.K_RIGHT]:
                self.x_vel += self.speed
                self.direction = 1
            if keys[pygame.K_UP]:
                self.y_vel_i = -self.jump_power
                self.fall = True
            if keys[pygame.K_x]:
                if self.onBlock and self.onBlock.active and not self.onBlock.selected \
                and not self.mining and self.mines > 0:
                    self.onBlock.selected = True
                    self.mines -= 1
                    self.mining = True
            elif not keys[pygame.K_x]:
                self.mining = False
            if keys[pygame.K_z]:
                if self.slomoDelay == 0 and self.timePower > 0 and self.shieldDelay == 0:
                    self.timePower -= 1
                    self.timeAnim.play()
                    self.slomoDelay = 100
            if keys[pygame.K_c]:
                if self.shieldDelay == 0 and self.shields > 0 and self.slomoDelay == 0:
                    self.shields -= 1
                    self.shieldAnim.play()
                    self.shieldDelay = 100




    def update(self, blocks,enemies,frame_number):
        self.controlsUpdate()
        self.positionUpdate(blocks)
        self.physicsUpdate()
        self.shieldUpdate()
        self.slomoUpdate()
        self.animationUpdate(frame_number)

    def render(self, displaySurface,camera):
        displaySurface.blit(self.img, camera.apply(self.rect) , (self.animation_offset, self.direction_offset, 64, 64))
        if self.shieldDelay > 0:
            self.shieldAnim.blit(displaySurface, camera.apply(Rect(self.rect.x -20, self.rect.y-15, 0, 0)))
        if self.slomoDelay > 0:
            self.timeAnim.blit(displaySurface, camera.apply(Rect(self.rect.x +16+16*(self.direction == 1), self.rect.y+16+16*self.spidering, 0, 0)))










