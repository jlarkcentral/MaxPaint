'''
Created on Aug 8, 2013

@author: primo
'''

import random
import pygame
from pygame.locals import Rect
from pygame.color import THECOLORS
from bullet import Bullet
from utils import vect_sub,vect_mul,vect_norm, distance, interpolate
from fragment import Fragment
from gameObject_ import GameObject_


class Enemy(GameObject_):

    def __init__(self, path, speed):
        super(Enemy, self).__init__()
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.rect = Rect(self.path[0],(64,64))
        self.img = pygame.image.load("../img/enemies/enemy.png").convert_alpha()
        # self.hitSound = pygame.mixer.Sound("../sounds/playerHit.wav")
        self.bullets = []
        self.shootingDelay = 0
        self.shootingDelayMax = 10
        self.waitDelay = 0
        self.lives = 1
        self.hit = False

        self.bulletFragments = []
        

    def shootAtTarget(self,targetPosition):
        # path = [(self.rect.x+20,self.rect.y+20), vect_add(targetPosition,vect_mul(vect_sub(targetPosition, self.rect.topleft),10))]    
        direction_raw = vect_sub(targetPosition,self.rect.topleft)
        direction = vect_mul(direction_raw,1.0/(vect_norm(direction_raw)))
        b = Bullet((self.rect.x+20,self.rect.y+20),direction, 5, 'grey')# random.choice(["blue","red","yellow"]))
        self.bullets.append(b)
        self.shootingDelay = self.shootingDelayMax


    def updateBullets(self, player,blocks):
        for b in self.bullets:
            b.update()
            if b.outOfScreen:
                self.bullets.remove(b)
            else:
                if b.rect.colliderect(player.rect):
                    if player.shieldDelay == 0:
                        # self.hitSound.play()
                        player.hitWithColor(b.color,b.rect.center)
                    for _ in range(random.randint(3,15)):
                        self.bulletFragments.append(Fragment(b.rect.center,THECOLORS[b.color]))
                    self.bullets.remove(b)
                else:
                    for block in blocks:
                        if b.rect.colliderect(block.rect):
                            for _ in range(random.randint(3,15)):
                                self.bulletFragments.append(Fragment(b.rect.center,THECOLORS[b.color]))
                            self.bullets.remove(b)

                            if block.selected:
                                blocks.remove(block)
                                self.hit = True
                            break
    
    def bulletFragmentsUpdate(self):
        for bf in self.bulletFragments:
            bf.update()
            if bf.kill:
                self.bulletFragments.remove(bf)

    def renderBullets(self, displaySurface, camera):
        for b in self.bullets:
            b.render(displaySurface, camera)

    def renderBulletFragments(self, displaySurface, camera):
        for bf in self.bulletFragments:
            bf.render(displaySurface,camera)

    def update(self, player, blocks):
        # movement
        destination = self.path[self.path_index]
        current = self.rect.topleft
        dist = distance(current,destination)
        t = 1
        if dist < self.speed:
            self.path_index += 1
            self.path_index = self.path_index % len(self.path)
            t = 1
        else:
            t = self.speed / dist
        pos = interpolate(current,destination, t)
        self.rect.topleft = pos

        # waiting at block edges
        if self.waitDelay == 0 and (dist < 0 or self.path_index == 0 and dist < 5):
            self.waitDelay = random.randint(1,200)
        elif self.waitDelay > 0:
            self.waitDelay -= 1

        

        # shooting
        if distance(player.rect.center,self.rect.center ) < 300 \
            and self.shootingDelay == 0:
            self.shootAtTarget(player.rect.center)
        if self.shootingDelay > 0:
            self.shootingDelay -= 1



        # bullets
        self.updateBullets( player,blocks)

        self.bulletFragmentsUpdate()


    def render(self, displaySurface,camera):
        displaySurface.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), (0, 64*0*(3-self.lives), 64, 64))
        self.renderBullets(displaySurface,camera)
        self.renderBulletFragments(displaySurface, camera)

