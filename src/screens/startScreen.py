'''
StartScreen
'''

import sys
import pygame
from pygame import KEYDOWN,K_ESCAPE,Rect
from pygame.color import THECOLORS
sys.path.append('../')
import utils
from screen_ import Screen_

class StartScreen(Screen_):

    def __init__(self):
        super(StartScreen, self).__init__()
        self.enterFont = utils.getFont('Handy00', 40)
        self.infoFont = utils.getFont('Handy00', 18)
        self.background = pygame.image.load("../img/backgrounds/title_pix.png").convert()
        self.running = True
        self.enterColors = (235,246,242)
        self.frameNumber = 0
        self.fade = 1
        self.msg = "A game using pygame and pyganim"

    def update(self):        
        if self.frameNumber % 200 != 0:
            self.enterColors = tuple(map(sum, zip((self.fade, self.fade, self.fade), self.enterColors)))
        else:
            self.fade *= -1
            self.frameNumber = 0
        self.frameNumber += 1
        

    def render(self,displaySurface):
        displaySurface.blit(self.background, (0,0))
        # displaySurface.fill(THECOLORS['black'],Rect(0,600,800,40))
        # displaySurface.blit(self.enterFont.render("Press any key",1,self.enterColors),(200,500))
        # displaySurface.blit(self.infoFont.render(self.msg,1,THECOLORS['white']),(300,600))

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key != K_ESCAPE:
                    self.manager.go_to('mainMenuScreen')
                    # self.manager.go_to_game(2)