'''
Created on 2 aout 2013

player class

@author: feral
'''
import sys

import math

import pygame
from pygame.locals import *

# import pymunk
# from pymunk.vec2d import Vec2d
# from pymunk.pygame_util import to_pygame

sys.path.append('../')
from utils import to_pygame

sys.path.append('../../lib/pyganim/')
import pyganim
#sys.path.append('../../lib/')
#import PAdLib.particles as particles

from bullet import Bullet


class Player(object):

    def __init__(self):
        
        # img
        self.imgNormal = pygame.image.load("../img/player/kube.png")
        self.img = self.imgNormal
        self.imgHitY = pygame.image.load("../img/player/kubeY.png")
        self.imgHitB = pygame.image.load("../img/player/kubeB.png")
        self.imgHitR = pygame.image.load("../img/player/kubeR.png")

        # sounds
        self.shootSound = pygame.mixer.Sound("../sounds/playerShoot.wav")
        self.shieldSound = pygame.mixer.Sound("../sounds/playerShield.wav")
        self.hitSound = pygame.mixer.Sound("../sounds/enemyHit.wav")
        
        # anims
        self.shieldAnim = pyganim.loadAnim('../img/anims/shield',0.25)

        # behavior variables
        self.PLAYER_VELOCITY = 10
        self.PLAYER_GROUND_ACCEL_TIME = 0.05
        self.PLAYER_GROUND_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_GROUND_ACCEL_TIME)
        self.PLAYER_AIR_ACCEL_TIME = 0.25
        self.PLAYER_AIR_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_AIR_ACCEL_TIME)
        self.JUMP_HEIGHT = 5
        self.JUMP_CUTOFF_VELOCITY = -5
        self.FALL_VELOCITY = 500.
        
        # physics variables
        # self.body = pymunk.Body(2000, pymunk.inf)
        self.position = 10,155
        self.velocity = (0.0, 0.0)  
        # self.hitbox = pymunk.Poly(self.body, [(0,0),(0,64),(64,64),(64,0)],(0,0))
        # #self.hitbox.layers = 0b1000
        # self.hitbox.collision_type = 1
        # self.hitbox.friction = 1.
        # self.hitbox.ignore_draw = True
        self.target_vx = 0
        self.direction = 1

        # self.landing = {'p':Vec2d.zero(), 'n':0}
        # self.landed_previous = False
        self.positionX, self.positionY = self.position
        self.rect = Rect(self.positionX, self.positionY, 64, 64)
        self.rectTop = Rect(self.positionX+2, self.positionY,60,5)
        self.rectBottom = Rect(self.positionX+2, self.positionY+64,60,5)
        self.rectLeft = Rect(self.positionX, self.positionY+2,5,60)
        self.rectRight = Rect(self.positionX+64, self.positionY+2,5,60)
        
        # game variables
        self.bullets = []
        self.shooting = False
        self.shots = 0
        self.shields = 0
        self.shieldDelay = 0
        self.lives = 3
        self.hit = False
        self.hitColorDelay = 0
        self.sunPower = 0
        self.sunPowering = False
        self.originalLight = 0

        self.well_grounded = False


    def changeColor(self,color):
        if color == 'yellow':
            self.img = self.imgHitY
        if color == 'blue':
            self.img = self.imgHitB
        if color == 'red':
            self.img = self.imgHitR
        self.hitColorDelay = 5
        self.hit = True


    def cpfclamp(self, f, min_, max_):
        """Clamp f between min and max"""
        return min(max(f, min_), max_)

    
    def cpflerpconst(self, f1, f2, d):
        """Linearly interpolate from f1 to f2 by no more than d."""
        return f1 + self.cpfclamp(f2 - f1, -d, d)
        
    
    def updateBullets(self,dt, backgroundScreen, camera, enemies):
        for b in self.bullets:
            b.update(dt)
            if b.positionX <= 0 or b.positionX >= 800:
                self.bullets.remove(b)
            else:
                for e in enemies:
                    if abs(b.positionX - e.positionX) < 10 and \
                    abs( (640-(camera.state.y + b.positionY)) - (640-(camera.state.y + e.positionY)) ) < 40:
                        if e.lives == 1:
                            enemies.remove(e)
                        else:
                            e.lives -= 1
                        self.bullets.remove(b)
                        self.hitSound.play()
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen))
    
    
    def shoot(self): #,space
        path = []
        if self.direction == -1:
            path = [(self.position - (0,-20) ),(0, self.positionY+20)]
        elif self.direction == 1:
            path = [(self.position - (-40,-20)),(800, self.positionY+20)]    
        b = Bullet(path, 15, 'red')
        self.bullets.append(b)
        self.shootSound.play()
    

    def shield(self, backgroundScreen, camera):
        self.shieldAnim.blit(backgroundScreen, to_pygame(camera.apply(Rect(self.positionX -20, self.positionY+50, 0, 0)), backgroundScreen))
        self.shieldDelay -= 1
    

    def handleKeyboardEvents(self, events,  color_dict, lightFill): #space,
        for event in events:
            if event.type == KEYDOWN and event.key == K_UP:
                # if self.well_grounded:
                jump_v = math.sqrt(2.0 * self.JUMP_HEIGHT * 100) #abs(space.gravity.y))
                self.velocity = (self.velocity[0], self.ground_velocity[1] + jump_v)
            elif event.type == KEYUP:
                if event.key == K_UP:              
                    self.velocity = (self.velocity[0], min(self.velocity[1], self.JUMP_CUTOFF_VELOCITY))
                if event.key == K_SPACE:
                    self.shooting = False
                    
        # Target horizontal velocity of player
        self.target_vx = 0
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT]):
            self.direction = -1
            self.target_vx -= self.PLAYER_VELOCITY
        if (keys[K_RIGHT]):
            self.direction = 1
            self.target_vx += self.PLAYER_VELOCITY
        if (keys[K_SPACE]) and not self.shooting and self.shots > 0:
            self.shoot(space)
            self.shooting = True
            self.shots -= 1
            color_dict["red"] -= 1
        if (keys[K_LSHIFT]) and self.shields >= 5 and self.shieldDelay == 0:
            self.shieldDelay = 120
            self.shieldAnim.play()
            self.shieldSound.play()
            color_dict["blue"] -= 5
        if (keys[K_LCTRL]) and self.sunPower >= 3  and not self.sunPowering:
            color_dict["yellow"] -= 3
            self.sunPowering = True

            # TODO light sound
            self.originalLight = lightFill['fill']
            lightFill['fill'] = 255



    
        
        
    def update(self,  dt, events, color_dict, backgroundScreen, camera, enemies,frame_number,lightFill): # space,
        # self.grounding = {
        #     'normal' : Vec2d.zero(),
        #     'penetration' : Vec2d.zero(),
        #     'impulse' : Vec2d.zero(),
        #     'position' : Vec2d.zero(),
        #     'body' : None
        # }

        # def f(arbiter):
        #     n = -arbiter.contacts[0].normal
        #     if n.y > self.grounding['normal'].y:
        #         self.grounding['normal'] = n
        #         self.grounding['penetration'] = -arbiter.contacts[0].distance
        #         self.grounding['body'] = arbiter.shapes[1].body
        #         self.grounding['impulse'] = arbiter.total_impulse
        #         self.grounding['position'] = arbiter.contacts[0].position
        # self.body.each_arbiter(f)
            
        # self.well_grounded = False
        # if self.grounding['body'] != None: #and abs(self.grounding['normal'].x/self.grounding['normal'].y) < self.hitbox.friction:
        #     self.well_grounded = True

        print self.rect.topleft

        # keyboard handling
        self.handleKeyboardEvents(events,  color_dict,lightFill) #space,

        self.ground_velocity = (0,0)
        # if self.well_grounded:
        #     self.ground_velocity = self.grounding['body'].velocity

        
        # if self.grounding['body'] != None:
        #     self.hitbox.friction = -self.PLAYER_GROUND_ACCEL/space.gravity.y
        # else:
        #     self.hitbox.friction = 0
        
        if self.positionY < 40:
            self.position = self.positionX, 40
        if self.positionX < 0:
            self.position = 0, self.positionY
        if self.positionX > 770:
            self.position = 770, self.positionY

        # # Air control
        # if self.grounding['body'] == None:
        velocityX = self.cpflerpconst(self.velocity[0], self.target_vx + self.ground_velocity[0], self.PLAYER_AIR_ACCEL*dt)
        
        velocityY = max(self.velocity[1], -self.FALL_VELOCITY) # clamp upwards as well?
        self.velocity = (velocityX,velocityY)

        self.position = (self.positionX + velocityX, self.positionY + velocityY)

        self.positionX, self.positionY = self.position
     
        
        
        #self.hitbox.update(self.body.position,(0,0))

        self.rect = Rect(self.positionX,self.positionY,64,64)


        # powerups update
        self.shots = color_dict["red"]
        self.shields = color_dict["blue"]
        self.sunPower = color_dict["yellow"]

        #print("raw ",self.body.position)
        #print("to_pygame " ,to_pygame(self.body.position,backgroundScreen))











        # bullets update
        self.updateBullets(dt, backgroundScreen, camera, enemies)

        # shield
        if self.shieldDelay > 0:
            self.shield(backgroundScreen, camera)

        # color delay when hit
        if self.hit:
            if self.hitColorDelay == 0:
                self.img = self.imgNormal
                self.hit = False
            else:
                self.hitColorDelay -= 1

        #self.particle_system.update(dt)
        #self.particle_system.draw(backgroundScreen)

        if self.sunPowering and lightFill['fill'] > self.originalLight:
            lightFill['fill'] = max(0,lightFill['fill'] - 1)
        else:
            self.sunPowering = False

        direction_offset = 64+(self.direction+1) / 2 * 64
        if abs(self.target_vx) > 1:
            animation_offset = 64 *(frame_number / 8 % 4)
        # elif self.grounding['body'] is None:
        #     animation_offset = 128
        else:
            animation_offset = 0
        
        backgroundScreen.blit(self.img, to_pygame(camera.apply(Rect(self.positionX ,self.positionY+40, 0, 0)), backgroundScreen) , (animation_offset, direction_offset, 64, 64))