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
        
        
        # game properties
        self.bullets = []
        self.shooting = True # weird shoot at startup TOFIX
        self.shots = 100
        self.shields = 0
        self.shieldDelay = 0
        self.lives = 3
        self.hit = False
        self.hitColorDelay = 0
        self.sunPower = 0
        self.sunPowering = False
        self.originalLight = 0


        # pics, anims and sound
        self.shieldAnim = pyganim.loadAnim('../img/anims/shield',0.25)
        self.shootSound = pygame.mixer.Sound("../sounds/playerShoot.wav")
        self.shieldSound = pygame.mixer.Sound("../sounds/playerShield.wav")
        self.hitSound = pygame.mixer.Sound("../sounds/enemyHit.wav")
        self.imgNormal = pygame.image.load("../img/player/kube.png")
        self.img = self.imgNormal
        self.imgHitY = pygame.image.load("../img/player/kubeY.png")
        self.imgHitB = pygame.image.load("../img/player/kubeB.png")
        self.imgHitR = pygame.image.load("../img/player/kubeR.png")
        self.bulletFragments = []





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
        elif self.rect.y > 3200:
            self.rect.y = 0
    
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
                if not block.moving:
                    self.collide_ls.append(block)
                # else :
                # # if block.moving:
                #     if block.moving == 1:
                #         self.rect.y = block.rect.y - 60
                #         self.fall = False
                #     if block.moving == -1:
                #         self.rect.x = block.rect.x
                #         self.rect.y = block.rect.y - 60
                    # self.fall = False
        return self.collide_ls

    

    def controlsUpdate(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_vel -= self.speed
            self.direction = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_vel += self.speed
            self.direction = 1
        if keys[pygame.K_SPACE]:
            self.y_vel_i = -self.jump_power
            self.fall = True
        elif keys[pygame.K_LCTRL]:
            if not self.shooting and self.shots > 0:
                self.shots -= 1
                self.shoot()
                self.shooting = True
            # else shoot icon blink; warn sound
        elif not keys[pygame.K_LCTRL]:
            self.shooting = False
        if keys[pygame.K_LSHIFT]:
            if self.shieldDelay == 0 and self.shields > 4:
                self.shields -= 5
                self.shieldAnim.play()
                self.shieldDelay = 120

    def addPowerUp(self,color):
        if color == "red":
            self.shots += 1
        if color == "blue":
            self.shields += 1
        if color == "yellow":
            self.sunPower += 1

    def bulletsUpdate(self, enemies, blocks):
        for b in self.bullets:
            b_hit = False
            b.update()
            if b.outOfScreen:
                self.bullets.remove(b)
            else:
                for e in enemies:
                    if b.rect.colliderect(e.rect):    
                        if e.lives == 1:
                            enemies.remove(e)
                        else:
                            e.lives -= 1
                        self.bullets.remove(b)
                        # self.hitSound.play()
                        b_hit = True
                        break
                if not b_hit:
                    for block in blocks:
                        if b.rect.colliderect(block.rect):
                            for _ in range(random.randint(3,15)):
                                self.bulletFragments.append(Fragment(b.rect.center,THECOLORS['red']))
                            self.bullets.remove(b)
                            break
    
    def bulletFragmentsUpdate(self):
        for bf in self.bulletFragments:
            bf.update()
            if bf.kill:
                self.bulletFragments.remove(bf)

    def shoot(self):
        startpos = (self.rect.x, self.rect.y + 20)
        direction = (-1, 0)
        if self.direction == 1:
            startpos = (self.rect.x + 60, self.rect.y + 20)    
            direction = (1, 0)
        b = Bullet(startpos, direction, 15, 'red')
        self.bullets.append(b)
        # self.shootSound.play()

    def shieldUpdate(self):
        if self.shieldDelay > 0:
            self.shieldDelay -= 1

    def changeColor(self,color):
        if color == 'yellow':
            self.img = self.imgHitY
        if color == 'blue':
            self.img = self.imgHitB
        if color == 'red':
            self.img = self.imgHitR
        self.hitColorDelay = 5

    def hitWithColor(self,color):
        self.hit = True
        self.lives -= 1
        self.changeColor(color)

    def colorUpdate(self):
        if self.hit:
            if self.hitColorDelay == 0:
                self.img = self.imgNormal
                self.hit = False
            else:
                self.hitColorDelay -= 1

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

    def update(self, blocks,enemies,frame_number):
        self.controlsUpdate()
        self.positionUpdate(blocks)
        self.physicsUpdate()
        self.bulletsUpdate(enemies, blocks)
        self.bulletFragmentsUpdate()
        self.shieldUpdate()
        self.colorUpdate()
        self.animationUpdate(frame_number)

    def render(self, displaySurface,camera):
        displaySurface.blit(self.img, camera.apply(self.rect) , (self.animation_offset, self.direction_offset, 64, 64))
        if self.shieldDelay > 0:
            self.shieldAnim.blit(displaySurface, camera.apply(Rect(self.rect.x -20, self.rect.y-15, 0, 0)))
        for b in self.bullets:
            b.render(displaySurface,camera)
        for bf in self.bulletFragments:
            bf.render(displaySurface,camera)