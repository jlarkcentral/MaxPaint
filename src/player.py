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
        self.PLAYER_VELOCITY = 100. *2.
        self.PLAYER_GROUND_ACCEL_TIME = 0.05
        self.PLAYER_GROUND_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_GROUND_ACCEL_TIME)
        
        self.PLAYER_AIR_ACCEL_TIME = 0.25
        self.PLAYER_AIR_ACCEL = (self.PLAYER_VELOCITY/self.PLAYER_AIR_ACCEL_TIME)
        
        self.JUMP_HEIGHT = 16.*3
        self.JUMP_BOOST_HEIGHT = 24.
        self.JUMP_CUTOFF_VELOCITY = 100
        self.FALL_VELOCITY = 250.
        
        self.JUMP_LENIENCY = 0.05
        
        self.HEAD_FRICTION = 0.7
        
        
        
        
        
        self.body = pymunk.Body(50, pymunk.inf)
        self.body.position = 100,100
        
        self.head = pymunk.Circle(self.body, 10, (0,5))
        self.head2 = pymunk.Circle(self.body, 10, (0,13))
        self.feet = pymunk.Circle(self.body, 10, (0,-5))
    
        self.head.layers = self.head2.layers = 0b1000
        self.feet.collision_type = 1
        self.feet.ignore_draw = self.head.ignore_draw = self.head2.ignore_draw = True
        
        self.direction = 1
        self.remaining_jumps = 2
        self.landing = {'p':Vec2d.zero(), 'n':0}
        
        self.landed_previous = False
        
        
        
        
    def update(self, space, dt, events):
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
            self.remaining_jumps = 2
    
    
        self.ground_velocity = Vec2d.zero()
        if self.well_grounded:
            self.ground_velocity = self.grounding['body'].velocity
            
        for event in events:
            if event.type == KEYDOWN and event.key == K_UP:
                if self.well_grounded or self.remaining_jumps > 0:                    
                    jump_v = math.sqrt(2.0 * self.JUMP_HEIGHT * abs(space.gravity.y))
                    self.body.velocity.y = self.ground_velocity.y + jump_v;
                    self.remaining_jumps -=1
            elif event.type == KEYUP and event.key == K_UP:                
                self.body.velocity.y = min(self.body.velocity.y, self.JUMP_CUTOFF_VELOCITY)
                
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
        if (keys[K_DOWN]):
            self.direction = -3
        #if (keys[K_UP]):
        #    if self.well_grounded or self.remaining_jumps > 0:                    
        #            jump_v = math.sqrt(2.0 * self.JUMP_HEIGHT * abs(space.gravity.y))
        #            self.body.velocity.y = self.ground_velocity.y + jump_v;
        #            self.remaining_jumps -=1
        #else :                
        #    self.body.velocity.y = min(self.body.velocity.y, self.JUMP_CUTOFF_VELOCITY)
        
        
            
            
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
        
        
    
    
        
    
    
    