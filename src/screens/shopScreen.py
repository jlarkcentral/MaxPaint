'''
SpecialsScreen
'''

import sys
import pygame
from pygame.locals import *
from pygame.color import THECOLORS
sys.path.append('../')
import utils



class ShopScreen(object):
    """docstring for ShopScreen"""
    def __init__(self):
        super(ShopScreen, self).__init__()
        self.sectionFont = utils.getFont('SigmarOne', 44)
        self.font = utils.getFont('SigmarOne', 34)
        self.fontDesc = utils.getFont('SigmarOne', 24)
        self.background = pygame.image.load("../img/backgrounds/transition.png").convert()
        self.infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
        self.shopBar = pygame.image.load("../img/hud/shopBar.png")

        self.shopSections = ["Blocks","Shield", "Bullets", "Misc"]
        
        self.shopItems = [
                        [
                            ['double red block',20,5,0],\
                            ['double blue block',20,5,0],\
                            ['double yellow block',20,5,0],\
                        ],
                        [
                            ['shield something',20,5,0],\
                            ['shield something',20,5,0],\
                            ['shield something',20,5,0],\
                        ],
                        [
                            ['bullets blabla',20,5,0],\
                            ['bullets blabla',20,5,0],\
                        ],
                        [
                            ['misc item 1',20,5,0],\
                            ['misc item 2',20,5,0],\
                        ]
                    ]


        self.choice = 0
        self.currentSection = 0
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey"]


        
    def render(self, backgroundScreen):
        backgroundScreen.blit(self.background, (0,0))
        backgroundScreen.blit(self.infoBar, (0,600))

        backgroundScreen.blit(self.sectionFont.render(self.shopSections[self.currentSection], 1, THECOLORS["black"]), (100,50))
        for i in range(len(self.shopItems[self.currentSection])):
            if choice != i:
                backgroundScreen.blit(self.font.render(self.shopItems[self.currentSection][i][0], 1, self.inactiveColor), (100,i*50+200))
                backgroundScreen.blit(self.fontDesc.render(str(self.shopItems[self.currentSection][i][1]), 1, THECOLORS["blue4"]), (600,i*50+200))
                backgroundScreen.blit(self.fontDesc.render(str(self.shopItems[self.currentSection][i][2]), 1, THECOLORS["yellow3"]), (670,i*50+200))
                backgroundScreen.blit(self.fontDesc.render(str(self.shopItems[self.currentSection][i][3]), 1, THECOLORS["red3"]), (740,i*50+200))
            else:
                backgroundScreen.blit(self.shopBar,(580,self.choice*50+200))        
                backgroundScreen.blit(self.font.render(self.shopItems[self.currentSection][self.choice][0], 1, self.activeColor), (100,self.choice*50+200))
                backgroundScreen.blit(self.fontDesc.render(str(self.shopItems[self.currentSection][self.choice][1]), 1, THECOLORS["blue"]), (600,self.choice*50+200))
                backgroundScreen.blit(self.fontDesc.render(str(self.shopItems[self.currentSection][self.choice][2]), 1, THECOLORS["yellow"]), (670,self.choice*50+200))
                backgroundScreen.blit(self.fontDesc.render(str(self.shopItems[self.currentSection][self.choice][3]), 1, THECOLORS["red"]), (740,self.choice*50+200))


      
    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # startGameScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                    self.screenManager.go_to('startGameScreen')
                if event.key == K_UP:
                    self.choice = (self.choice - 1) % len(self.shopItems[self.currentSection])
                if event.key == K_DOWN:
                    self.choice = (self.choice + 1) % len(self.shopItems[self.currentSection])
                if event.key == K_RIGHT:
                    self.currentSection = (self.currentSection + 1) % len(self.shopItems)
                    self.choice = 0
                if event.key == K_LEFT:
                    self.currentSection = (self.currentSection - 1) % len(self.shopItems)
                    self.choice = 0