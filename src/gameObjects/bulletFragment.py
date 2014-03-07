'''

copy of http://thepythongamebook.com/en:pygame:step015
'''
import random
import pygame
from pygame import Rect


class BulletFragment(object): # pygame.sprite.Sprite):
        """a fragment of an exploding Bird"""
        gravity = True # fragments fall down ?
        def __init__(self, pos, color):
            # pygame.sprite.Sprite.__init__(self, self.groups)
            self.kill = False
            self.pos = [0.0,0.0]
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.image = pygame.Surface((10,10))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, color,(5,5),3)#(random.randint(1,64),0,0), (5,5),random.randint(2,5))
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
            self.lifetime = 50 # max 6 seconds
            self.time = 0.0
            self.fragmentmaxspeed = 5 * 2 # try out other factors !
            self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            
        def update(self, backgroundScreen, camera, seconds=1):
            self.time += seconds
            if self.time > self.lifetime:
                self.kill = True 
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            if BulletFragment.gravity:
                self.dy += 1 # gravity suck fragments down
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            backgroundScreen.blit(self.image, camera.apply(Rect(self.rect.centerx, self.rect.centery, 0, 0)))