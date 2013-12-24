'''
Created on Aug 8, 2013

@author: primo
'''
import sys
import random

import pygame
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

sys.path.append('../../lib/PAdLib')
import PAdLib.particles as particles

from bullet import Bullet


class Enemy(object):

    def __init__(self, path, speed):
                
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.body.position = self.path[0]
        self.positionX, self.positionY = self.body.position
        self.hitbox = pymunk.Poly(self.body, [(0,0),(0,40),(40,40),(40,0)],(0,-40))
        self.hitbox.ignore_draw = False
        self.hitbox.group = 1
        self.hitbox.friction = 100
        self.hitbox.layers = 0b1000
        self.hitbox.collision_type = 1
        self.img = pygame.image.load("../img/enemies/enemy1.png")
        self.bullets = []
        self.shootingDelay = 0

        #shooting
        self.particle_system = particles.ParticleSystem()
        self.particle_system.set_particle_acceleration([0.0,500.0])
        

        

    def shootAtTarget(self,targetPosition):
        path = []
        path = [(Vec2d(self.body.position)),targetPosition + (targetPosition - self.body.position)*10]    
        b = Bullet(path, 5, random.choice(["blue","red","yellow"]))
        self.bullets.append(b)

        #emitter = particles.Emitter()
        #emitter.set_density(200)
        #ang = particles.angle((0.1,0.0),self.body.position - targetPosition)
        #emitter.set_angle(ang,10.0)
        #emitter.set_speed([350.0,150.0])
        #emitter.set_life([1.0,1.0])
        #emitter.set_colors([(255,0,0)])
        #self.particle_system.add_emitter(emitter,str(id(b)))


    def updateBullets(self,dt, backgroundScreen, camera, player):
        playerHit = False
        for b in self.bullets:
            b.update(dt)
            if b.positionX < 0 or b.positionX > 800 or b.positionY < 0 or b.positionY > camera.maxH:
                self.bullets.remove(b)
                #del(self.particle_system.emitters[str(id(b))])
            #if abs(b.positionX - playerPositionX + 32) < 10 and \
            #abs( (640-(camera.state.y + b.positionY - 32)) - (640-(camera.state.y + playerPositionY - 32)) ) < 40:
            else:
                #self.particle_system.emitters[str(id(b))].set_position([b.positionX,(640-(camera.state.y + b.positionY))])
                if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((b.positionX + 20,b.positionY-20)) < 40 :
                    if player.shieldDelay == 0:
                        player.lives -= 1
                    self.bullets.remove(b)
                    #del(self.particle_system.emitters[str(id(b))])
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen))
        return playerHit

    def update(self, dt, backgroundScreen, camera, player):
        
        destination = self.path[self.path_index]
        current = Vec2d(self.body.position)
        distance = current.get_distance(destination)
        if distance < self.speed:
            self.path_index += 1
            self.path_index = self.path_index % len(self.path)
            t = 1
        else:
            t = self.speed / distance
        self.positionX, self.positionY = current.interpolate_to(destination, t)
        self.body.position = self.positionX, self.positionY
        self.body.velocity = (self.body.position - current) / dt

        self.updateBullets(dt, backgroundScreen, camera, player)

        if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((self.positionX + 20,self.positionY-20)) < 250 \
            and self.shootingDelay == 0:
            self.shootAtTarget((player.positionX + 32,player.positionY - 32))
            self.shootingDelay = 30
        if self.shootingDelay > 0:
            self.shootingDelay -= 1

        #self.particle_system.update(dt)
        #self.particle_system.draw(backgroundScreen)

        if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((self.positionX + 20,self.positionY-20)) < 50 :
            return True
        return False
