'''
Created on 2 aout 2013

player class

@author: feral
'''

import math

import pygame
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d

from bullet import Bullet

class Player(object):
    '''
    classdocs
    '''

    def cpfclamp(self, f, min_, max_):
        """Clamp f between min and max"""
        return min(max(f, min_), max_)

    def cpflerpconst(self, f1, f2, d):
        """Linearly interpolate from f1 to f2 by no more than d."""
        return f1 + self.cpfclamp(f2 - f1, -d, d)
        
        

    def __init__(self):
        '''
        Constructor
        '''
        
        self.img = pygame.image.load("../img/kube.png")
        self.shieldImg = pygame.image.load("../img/shield.png")
        
        self.shielded = False
        
        self.PLAYER_VELOCITY = 100. *2 *2.
        self.PLAYER_GROUND_ACCEL_TIME = 0.05
        self.PLAYER_GROUND_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_GROUND_ACCEL_TIME)
        
        self.PLAYER_AIR_ACCEL_TIME = 0.25
        self.PLAYER_AIR_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_AIR_ACCEL_TIME)
        
        self.JUMP_HEIGHT = 16.*3*2
        self.JUMP_BOOST_HEIGHT = 24.*2
        self.JUMP_CUTOFF_VELOCITY = 100
        self.FALL_VELOCITY = 500.
        
        self.JUMP_LENIENCY = 5
        
        self.HEAD_FRICTION = 0.7
        
        
        
        
        
        self.body = pymunk.Body(2000, pymunk.inf)
        self.body.position = 10,120
        
        self.head = pymunk.Circle(self.body, 20, (0,20))
        self.head2 = pymunk.Circle(self.body, 15, (0,50))
        self.feet = pymunk.Circle(self.body, 10, (0,-5))
    
        self.head.layers = self.head2.layers = 0b1000
        self.feet.collision_type = 1
        self.feet.ignore_draw = self.head.ignore_draw = self.head2.ignore_draw = True
        
        self.direction = 1
        self.remaining_jumps = 0
        self.landing = {'p':Vec2d.zero(), 'n':0}
        
        self.landed_previous = False
        
        self.positionX, self.positionY = self.body.position
        
        self.bullets = []
        
        self.shooting = False
        
        self.shots = 0
        
        self.shields = 0
        
        
    def update(self, space, dt, events, color_dict):
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
        self.body.each_arbiter(f)
            
        self.well_grounded = False
        if self.grounding['body'] != None and abs(self.grounding['normal'].x/self.grounding['normal'].y) < self.feet.friction:
            self.well_grounded = True
            #self.remaining_jumps = 5
    
    
        self.ground_velocity = Vec2d.zero()
        if self.well_grounded:
            self.ground_velocity = self.grounding['body'].velocity
            
        for event in events:
            if event.type == KEYDOWN and event.key == K_UP:
                #if self.well_grounded or 
                if self.remaining_jumps > 0:                    
                    jump_v = math.sqrt(2.0 * self.JUMP_HEIGHT * abs(space.gravity.y))
                    self.body.velocity.y = self.ground_velocity.y + jump_v;
                    self.remaining_jumps -=1
                    color_dict["green"] -= 1
            elif event.type == KEYUP:
                if event.key == K_UP:                
                    self.body.velocity.y = min(self.body.velocity.y, self.JUMP_CUTOFF_VELOCITY)
                if event.key == K_SPACE:
                    self.shooting = False
                    
                
        # Target horizontal velocity of player
        self.target_vx = 0
        
        if self.body.velocity.x > .01:
            self.direction = 1
        elif self.body.velocity.x < -.01:
            self.direction = -1
        
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
        if (keys[K_LSHIFT]) and not self.shielded:
            self.shield()
            self.shields -= 1
            color_dict["blue"] -= 1
            
            
            
        self.feet.surface_velocity = self.target_vx,0

        
        if self.grounding['body'] != None:
            self.feet.friction = -self.PLAYER_GROUND_ACCEL/space.gravity.y
            self.head.friciton = self.HEAD_FRICTION
        else:
            self.feet.friction,self.head.friction = 0,0
        
        # Air control
        if self.grounding['body'] == None:
            self.body.velocity.x = self.cpflerpconst(self.body.velocity.x, self.target_vx + self.ground_velocity.x, self.PLAYER_AIR_ACCEL*dt)
        
        self.body.velocity.y = max(self.body.velocity.y, -self.FALL_VELOCITY) # clamp upwards as well?
        
        
        self.positionX, self.positionY = self.body.position
    
        if self.shielded:
            self.shieldDelay -= 1
            if self.shieldDelay == 0:
                self.shielded = False
        
    
    def shoot(self,space):
        path = []
        if self.direction == -1:
            path = [(self.body.position),(0, self.positionY)]
        elif self.direction == 1:
            path = [(self.body.position),(800, self.positionY)]    
        b = Bullet(path)
        self.bullets.append(b)
        #space.add(b.body,b.hitbox)
        
    def shield(self):
        self.shielded = True
        self.shieldDelay = 100    
    