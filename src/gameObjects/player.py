'''
Created on 2 aout 2013

player class

@author: feral

modified code from collision example:
python-forum.org/viewtopic.php?f=26&t=1889

'''

import sys
import math
import pygame
from pygame.locals import *
sys.path.append('../')
from utils import to_pygame
sys.path.append('../../lib/pyganim/')
import pyganim
from bullet import Bullet

    

class Player(object):
    """Class representing our player."""
    def __init__(self):
        # physics properties
        self.x_vel = self.y_vel = self.y_vel_i = 0
        self.grav = 20
        self.fall = False
        self.time = 0 # None
        self.image = pygame.image.load("../img/player/kube.png")
        self.speed = 10
        self.jump_power = 10
        self.rect = Rect(0, 0, 60, 60)
        self.rect.topleft = (150,350)
        self.collide_ls = [] #what obstacles does the player collide with
        self.direction = 1
        self.direction_offset = 0
        self.animation_offset = 0
        self.animationTicks = 0
        
        
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

        # anims and sound
        self.shieldAnim = pyganim.loadAnim('../img/anims/shield',0.25)
        self.shootSound = pygame.mixer.Sound("../sounds/playerShoot.wav")
        self.shieldSound = pygame.mixer.Sound("../sounds/playerShield.wav")
        self.hitSound = pygame.mixer.Sound("../sounds/enemyHit.wav")

    def phys_update(self):
        if self.fall:
            self.time += 2 # frame_number # pygame.time.get_ticks()
            self.y_vel = self.grav*((self.time)/100.0) + self.y_vel_i

        else:
            self.time = 0
            self.y_vel = 0

    def get_pos(self,blocks):
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

    

    def controls(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_vel -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_vel += self.speed
            self.direction = 1
        if keys[pygame.K_SPACE]:
            self.y_vel_i = -self.jump_power
            self.fall = True
        if keys[pygame.K_LCTRL]:
            if not self.shooting:
                self.shoot()
                self.shooting = True
        elif not keys[pygame.K_LCTRL]:
            self.shooting = False
        if keys[pygame.K_LSHIFT]:
            if self.shieldDelay == 0:
                self.shieldAnim.play()
                self.shieldDelay = 120



    def powerUpsUpdate(self,color_dict):
        self.shots = color_dict["red"]
        self.shields = color_dict["blue"]
        self.sunPower = color_dict["yellow"]

    def updateBullets(self,dt, backgroundScreen, camera, enemies):
        for b in self.bullets:
            b.update(dt)
            if b.rect.x <= 0 or b.rect.x >= 800:
                self.bullets.remove(b)
            else:
                for e in enemies:
                    # if abs(b.rect.x - e.rect.x) < 10 and \
                    # abs( (640-(camera.state.y + b.rect.y)) - (640-(camera.state.y + e.rect.y)) ) < 40:
                    if b.rect.colliderect(e.rect):    
                        if e.lives == 1:
                            enemies.remove(e)
                        else:
                            e.lives -= 1
                        self.bullets.remove(b)
                        # self.hitSound.play()
            backgroundScreen.blit(b.img, camera.apply(Rect(b.rect.x, b.rect.y, 0, 0)))
    
    
    def shoot(self):
        path = []
        if self.direction == -1:
            path = [(self.rect.x, self.rect.y + 30),(0, self.rect.y+30)]
        elif self.direction == 1:
            path = [(self.rect.x + 60, self.rect.y + 30),(800, self.rect.y+30)]    
        b = Bullet(path, 15, 'red')
        self.bullets.append(b)
        # self.shootSound.play()

    def shield(self, backgroundScreen, camera):
        self.shieldAnim.blit(backgroundScreen, camera.apply(Rect(self.rect.x -20, self.rect.y-15, 0, 0)))
        self.shieldDelay -= 1

    def shieldUpdate(self, backgroundScreen, camera):
        if self.shieldDelay > 0:
            self.shield(backgroundScreen, camera)

    def animationUpdate(self,frame_number):
        self.direction_offset = 64+(self.direction+1) / 2 * 64
        if abs(self.x_vel) > 1:
            # self.animation_offset = 64 *(self.animationTicks % 8)
            self.animation_offset = 64 *int(self.animationTicks / 8 % 4)
        elif self.fall:
            self.animation_offset = 128
        else:
            self.animation_offset = 0
        if self.animationTicks == 32:
            self.animationTicks = 0
        else:
            self.animationTicks += 1 

    def update(self,Surf,blocks,camera,dt,enemies, color_dict,frame_number):
        self.controls()
        self.get_pos(blocks)
        self.phys_update()
        self.powerUpsUpdate(color_dict)
        self.updateBullets(dt, Surf, camera, enemies)
        self.animationUpdate(frame_number)
        self.shieldUpdate(Surf,camera)

        Surf.blit(self.image, camera.apply(self.rect) , (self.animation_offset, self.direction_offset, 64, 64))

# class Player_(object):

#     def __init__(self):
        
#         # img
#         self.imgNormal = pygame.image.load("../img/player/kube.png")
#         self.img = self.imgNormal
#         self.imgHitY = pygame.image.load("../img/player/kubeY.png")
#         self.imgHitB = pygame.image.load("../img/player/kubeB.png")
#         self.imgHitR = pygame.image.load("../img/player/kubeR.png")

#         # sounds
#         self.shootSound = pygame.mixer.Sound("../sounds/playerShoot.wav")
#         self.shieldSound = pygame.mixer.Sound("../sounds/playerShield.wav")
#         self.hitSound = pygame.mixer.Sound("../sounds/enemyHit.wav")
        
#         # anims
#         self.shieldAnim = pyganim.loadAnim('../img/anims/shield',0.25)

#         self.JUMP_HEIGHT = 1
        
#         # physics variables
#         self.position = 10,155
#         self.velocity_x = 0.0
#         self.velocity_y = 0.0
#         self.speed = 5
#         self.direction = 1
#         self.positionX, self.positionY = self.position
#         self.rect = Rect(self.positionX, self.positionY, 64, 64)
        
#         # game variables
#         self.bullets = []
#         self.shooting = False
#         self.shots = 100
#         self.shields = 0
#         self.shieldDelay = 0
#         self.lives = 3
#         self.hit = False
#         self.hitColorDelay = 0
#         self.sunPower = 0
#         self.sunPowering = False
#         self.originalLight = 0

#         self.well_grounded = False


#     def changeColor(self,color):
#         if color == 'yellow':
#             self.img = self.imgHitY
#         if color == 'blue':
#             self.img = self.imgHitB
#         if color == 'red':
#             self.img = self.imgHitR
#         self.hitColorDelay = 5
#         self.hit = True
        
    
    
    

#     def shield(self, backgroundScreen, camera):
#         self.shieldAnim.blit(backgroundScreen, to_pygame(camera.apply(Rect(self.positionX -20, self.positionY+50, 0, 0)), backgroundScreen))
#         self.shieldDelay -= 1
    

#     def handleKeyboardEvents(self, events,  color_dict, lightFill): #space,
#         for event in events:
#             if event.type == KEYDOWN:
#                 jump_v = math.sqrt(2.0 * self.JUMP_HEIGHT * 100)
#                 if event.key == K_UP:
#                     self.velocity_y += jump_v
#                     print "UP : " + str(self.velocity_y)
#                 elif event.key == K_DOWN:
#                     self.velocity_y -= jump_v
#                     print "DOWN : " + str(self.velocity_y)
#                 if event.key == K_LEFT: 
#                     self.velocity_x -= jump_v
#                     print "LEFT : " + str(self.velocity_x)
#                 elif event.key == K_RIGHT:
#                     self.velocity_x += jump_v
#                     print "RIGHT : " + str(self.velocity_x)
#                 print "POSITION : " + str(self.position)
#             elif event.type == KEYUP:
#                 if event.key == K_UP:              
#                     self.velocity_y = 0
#                 elif event.key == K_DOWN:              
#                     self.velocity_y = 0
#                 if event.key == K_LEFT:              
#                     self.velocity_x = 0
#                 elif event.key == K_RIGHT:
#                     self.velocity_x = 0

#             # TODO light sound
#             self.originalLight = lightFill['fill']
#             lightFill['fill'] = 255



    
        
        
#     def update(self, dt, events, color_dict, backgroundScreen, camera, enemies,frame_number,lightFill,blocks):

#         # keyboard handling
#         self.handleKeyboardEvents(events, color_dict, lightFill)
        
        


#         # has a collision happened?
#         # hitX = False
#         # hitY = False

#         for block in blocks:
#             if self.rect.colliderect(block.rect):
#                 # if not too far above or below
#                 if not self.rect.y - 64 <= block.rect.y \
#                 and not self.rect.y >= block.rect.y - 30:
#                     # if left
#                     if self.rect.x + 64 <= block.rect.x:
#                         if self.velocity_x > 0:
#                             self.velocity_x = 0
#                     # if right
#                     elif self.rect.x >= block.rect.x + 100:
#                         if self.velocity_x < 0:
#                             self.velocity_x = 0
#                 # if not too far left or right
#                 if not self.rect.x + 64 <= block.rect.x \
#                 and not self.rect.x >= block.rect.x + 100:
#                     # if above
#                     if self.rect.y + 64 <= block.rect.y:
#                         if self.velocity_y > 0:
#                             self.velocity_y = 0
#                     # if below
#                     elif self.rect.y <= block.rect.y + 30:
#                         if self.velocity_y < 0:
#                             self.velocity_x = 0


#             # if self.velocity[0] > 0:  # moving right
#             #     if x + w < block.rect.x and x_next + w >= block.rect.x:
#             #         # collision!
#             #         x_next =  block.rect.x - w
#             #         hitX = True
#             # elif self.velocity[0] < 0: # moving left
#             #     if x > block.rect.x + block.rect.w and x_next > block.rect.x + block.rect.w:
#             #         # collision!
#             #         x_next = block.rect.x + block.rect.w
#             #         hitX = True

#             # if self.velocity[1] > 0:  # moving up
#             #     if x + w < block.rect.x and x_next + w >= block.rect.x:
#             #         # collision!
#             #         x_next =  block.rect.x - w
#             #         hitY = True
#             # elif self.velocity[1] < 0: # moving down
#             #     if x > block.rect.x + block.rect.w and x_next > block.rect.x + block.rect.w:
#             #         # collision!
#             #         x_next = block.rect.x + block.rect.w
#             #         hitY = True

#         # now update rect to have the new collision fixed positions:

#         # self.rect.x = x_next
#         # self.rect.y = y_next

#         # and if there was a collision, fix the velocity.

#         # if hitX:
#         #     self.velocity = (0,self.velocity_y)  # or 0 - velX to bounce instead of stop
#         # if hitY:
#         #     self.velocity = (self.velocity_x, 0)  # or 0 - velY to bounce instead of stop


#         self.rect.x += self.velocity_x
#         self.rect.y += self.velocity_y
#         self.position = self.rect.topleft
#         self.positionX ,self.positionY = self.position




#         # powerups update
#         self.shots = color_dict["red"]
#         self.shields = color_dict["blue"]
#         self.sunPower = color_dict["yellow"]



#         # bullets update
#         self.updateBullets(dt, backgroundScreen, camera, enemies)

#         # shield
#         if self.shieldDelay > 0:
#             self.shield(backgroundScreen, camera)

#         # color delay when hit
#         if self.hit:
#             if self.hitColorDelay == 0:
#                 self.img = self.imgNormal
#                 self.hit = False
#             else:
#                 self.hitColorDelay -= 1


#         if self.sunPowering and lightFill['fill'] > self.originalLight:
#             lightFill['fill'] = max(0,lightFill['fill'] - 1)
#         else:
#             self.sunPowering = False

#         direction_offset = 64+(self.direction+1) / 2 * 64
#         if abs(self.velocity_x) > 1:
#             animation_offset = 64 *(frame_number / 8 % 4)
#         # elif self.grounding['body'] is None:
#         #     animation_offset = 128
#         else:
#             animation_offset = 0
        
#         backgroundScreen.blit(self.img, to_pygame(camera.apply(self.rect), backgroundScreen) , (animation_offset, direction_offset, 64, 64))