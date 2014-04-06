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
        self.rect = Rect(self.path[0],(64,32))
        self.imgNormal = pygame.image.load("../img/enemies/enemy.png").convert_alpha()
        self.imgRed = pygame.image.load("../img/enemies/enemyRed.png").convert_alpha()
        self.img = self.imgNormal
        # self.hitSound = pygame.mixer.Sound("../sounds/playerHit.wav")
        self.bullets = []
        self.bulletSpeed = 10
        self.shootingDelay = 0
        self.shootingDelayMax = 50
        self.radius = 300
        self.waitDelay = 0
        self.lives = 1
        self.hit = False

        self.bulletFragments = []

        self.shootSound = pygame.mixer.Sound('../sounds/enemyShoot.wav')
        

    def shootAtTarget(self,targetPosition):
        # path = [(self.rect.x+20,self.rect.y+20), vect_add(targetPosition,vect_mul(vect_sub(targetPosition, self.rect.topleft),10))]    
        direction_raw = vect_sub(targetPosition,self.rect.topleft)
        direction = vect_mul(direction_raw,1.0/(vect_norm(direction_raw)))
        b = Bullet((self.rect.x+20,self.rect.y+20),direction, 'grey')# random.choice(["blue","red","yellow"]))
        self.bullets.append(b)
        self.shootingDelay = self.shootingDelayMax
        self.shootSound.play()


    def updateBullets(self, player,blocks):
        for b in self.bullets:
            b.update(self.bulletSpeed)
            if b.outOfScreen:
                self.bullets.remove(b)
            else:
                if b.rect.colliderect(player.rect):
                    # if player.shieldDelay == 0:
                    #     player.killed = True
                    for _ in range(random.randint(3,15)):
                        self.bulletFragments.append(Fragment(b.rect.center,THECOLORS[b.color]))
                    self.bullets.remove(b)
                else:
                    for block in blocks:
                        if b.rect.colliderect(block.rect):
                            # if b.nbCollide == 3:
                            for _ in range(random.randint(3,15)):
                                self.bulletFragments.append(Fragment(b.rect.center,THECOLORS[b.color]))
                            self.bullets.remove(b)
                            
                            if block.selected:
                                self.hit = True
                                blocks.remove(block)
                            # b.nbCollide += 1
                            # b.direction = (b.direction[0],-b.direction[1])
                            break
    
    def bulletFragmentsUpdate(self):
        for bf in self.bulletFragments:
            bf.update()
            if bf.kill:
                self.bulletFragments.remove(bf)

    

    def update(self, player, blocks):
        if player.slomoDelay > 0:
            self.bulletSpeed = 3
            self.shootingDelayMax = 150
        else:
            self.bulletSpeed = 10
            self.shootingDelayMax = 50

        # shooting
        if not player.killed:
            if distance(player.rect.center,self.rect.center ) < self.radius:
                if self.rect.y < player.rect.y:
                    self.img = self.imgRed
                    if self.shootingDelay == 0 \
                    and len(self.bullets) < 3:
                        self.shootAtTarget(player.rect.center)
            else:
                self.img = self.imgNormal
            if self.shootingDelay > 0:
                self.shootingDelay -= 1

        self.updateBullets( player,blocks)
        self.bulletFragmentsUpdate()



    def renderBullets(self, displaySurface, camera):
        for b in self.bullets:
            b.render(displaySurface, camera)

    def renderBulletFragments(self, displaySurface, camera):
        for bf in self.bulletFragments:
            bf.render(displaySurface,camera)


    def render(self, displaySurface,camera):
        displaySurface.blit(self.img, camera.apply(Rect(self.rect.x, self.rect.y, 0, 0)), (0, 64*0*(3-self.lives), 64, 64))
        # displaySurface.fill(THECOLORS['grey'],self.rect)
        self.renderBullets(displaySurface,camera)
        self.renderBulletFragments(displaySurface, camera)

