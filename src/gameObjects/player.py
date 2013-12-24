'''
Created on 2 aout 2013

player class

@author: feral
'''
import sys

import math

import pygame
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import to_pygame

sys.path.append('../lib/pyganim')
import pyganim
sys.path.append('../lib/PAdLib')
import PAdLib.particles as particles

from bullet import Bullet


class Player(object):

    def __init__(self):
        
        # sprites & sounds
        self.img = pygame.image.load("../img/player/kube.png")
        self.shieldImg = pygame.image.load("../img/player/shield.png")
        self.shootSound = pygame.mixer.Sound("../sounds/playerShoot.wav")
        self.shieldSound = pygame.mixer.Sound("../sounds/playerShield.wav")
        self.hitSound = pygame.mixer.Sound("../sounds/enemyHit.wav")
        
        # behavior variables
        self.PLAYER_VELOCITY = 400
        self.PLAYER_GROUND_ACCEL_TIME = 0.05
        self.PLAYER_GROUND_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_GROUND_ACCEL_TIME)
        self.PLAYER_AIR_ACCEL_TIME = 0.25
        self.PLAYER_AIR_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_AIR_ACCEL_TIME)
        self.JUMP_HEIGHT = 120
        self.JUMP_CUTOFF_VELOCITY = 200
        self.FALL_VELOCITY = 500.
        
        # physics variables
        self.body = pymunk.Body(2000, pymunk.inf)
        self.body.position = 10,220
        self.body.velocity = (0.0, 0.0)  
        self.hitbox = pymunk.Poly(self.body, [(0,0),(0,50),(50,50),(50,0)],(10,-60))
        self.hitbox.layers = 0b1000
        self.hitbox.collision_type = 1
        self.hitbox.ignore_draw = False
        self.target_vx = 0
        self.direction = 1
        self.landing = {'p':Vec2d.zero(), 'n':0}
        self.landed_previous = False
        self.positionX, self.positionY = self.body.position
        
        # game variables
        self.bullets = []
        self.shooting = False
        self.shots = 0
        self.shields = 0
        self.shieldDelay = 0
        self.lives = 3

        #shooting
        self.particle_system = particles.ParticleSystem()
        self.particle_system.set_particle_acceleration([0.0,500.0])



        

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
                del(self.particle_system.emitters[str(id(b))])
            else:
                self.particle_system.emitters[str(id(b))].set_position([b.positionX,(640-(camera.state.y + b.positionY))])
                for e in enemies:
                    if abs(b.positionX - e.positionX) < 10 and \
                    abs( (640-(camera.state.y + b.positionY)) - (640-(camera.state.y + e.positionY)) ) < 40:
                        enemies.remove(e)
                        del(self.particle_system.emitters[str(id(b))])
                        self.bullets.remove(b)
                        self.hitSound.play()
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen))
    
    
    def shoot(self,space):
        path = []
        if self.direction == -1:
            path = [(self.body.position - (0,20) ),(0, self.positionY)]
        elif self.direction == 1:
            path = [(self.body.position - (-40,20)),(800, self.positionY)]    
        b = Bullet(path, 15, 'red')
        self.bullets.append(b)

        emitter = particles.Emitter()
        emitter.set_density(200)
        emitter.set_angle(self.direction*180,10.0)
        emitter.set_speed([350.0,150.0])
        emitter.set_life([1.0,1.0])
        emitter.set_colors([(255,0,0)])
        self.particle_system.add_emitter(emitter,str(id(b)))
        
        self.shootSound.play()
    

    def shield(self, backgroundScreen, camera):
        backgroundScreen.blit(self.shieldImg, to_pygame(camera.apply(Rect(self.positionX - 7,self.positionY + 5, 0, 0)), backgroundScreen))
        self.shieldDelay -= 1
    

    def handleKeyboardEvents(self, events, space, color_dict):
        for event in events:
            if event.type == KEYDOWN and event.key == K_UP:
                if self.well_grounded:
                    jump_v = math.sqrt(2.0 * self.JUMP_HEIGHT * abs(space.gravity.y))
                    self.body.velocity.y = self.ground_velocity.y + jump_v;
            elif event.type == KEYUP:
                if event.key == K_UP:              
                    self.body.velocity.y = min(self.body.velocity.y, self.JUMP_CUTOFF_VELOCITY)
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
        if (keys[K_LSHIFT]) and self.shields > 0 and self.shieldDelay == 0:
            self.shieldDelay = 120
            self.shieldSound.play()
            color_dict["blue"] -= 1

        self.hitbox.surface_velocity = self.target_vx,0


    
        
        
    def update(self, space, dt, events, color_dict, backgroundScreen, camera, enemies):
        self.grounding = {
            'normal' : Vec2d.zero(),
            'penetration' : Vec2d.zero(),
            'impulse' : Vec2d.zero(),
            'position' : Vec2d.zero(),
            'body' : None
        }
        
        # find out if player is standing on ground
        def f(arbiter):
            n = -arbiter.contacts[0].normal
            if n.y > self.grounding['normal'].y:
                self.grounding['normal'] = n
                self.grounding['penetration'] = -arbiter.contacts[0].distance
                self.grounding['body'] = arbiter.shapes[1].body
                self.grounding['impulse'] = arbiter.total_impulse
                self.grounding['position'] = arbiter.contacts[0].position
        #if self.
        self.body.each_arbiter(f)
        self.well_grounded = False
        if self.grounding['body'] != None and \
        abs(self.grounding['normal'].x/self.grounding['normal'].y) < 0.7:
            self.well_grounded = True

        if abs(self.body.velocity.y) < 0.01:
            self.well_grounded = True
            # Avoid being blocked when going right
            self.grounding['body'] = None

        self.ground_velocity = Vec2d.zero()
        if self.well_grounded and self.grounding['body'] != None:
            self.ground_velocity = self.grounding['body'].velocity
        
        if self.grounding['body'] != None:
            self.hitbox.friction = -self.PLAYER_GROUND_ACCEL/space.gravity.y
        else:
            self.hitbox.friction = 0
        
        # Air control
        if self.grounding['body'] == None:
            self.body.velocity.x = self.cpflerpconst(self.body.velocity.x, self.target_vx + self.ground_velocity.x, self.PLAYER_AIR_ACCEL*dt)
        
        self.body.velocity.y = max(self.body.velocity.y, -self.FALL_VELOCITY) # clamp upwards as well?
        self.positionX, self.positionY = self.body.position
     
        if self.positionY < 40:
            self.body.position = self.positionX, 40
        if self.positionX < 0:
            self.body.position = 0, self.positionY
        if self.positionX > 770:
            self.body.position = 770, self.positionY
        

        # keyboard handling
        self.handleKeyboardEvents(events, space, color_dict)

        # powerups update
        self.shots = color_dict["red"]
        self.shields = color_dict["blue"]

        # bullets update
        self.updateBullets(dt, backgroundScreen, camera, enemies)

        # shield
        if self.shieldDelay > 0:
            self.shield(backgroundScreen, camera)

        self.particle_system.update(dt)
        self.particle_system.draw(backgroundScreen)
            