'''
MainMenuScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from screen_ import Screen_

#import pgext

sys.path.append('../')
import utils
from utils import cycle

class MainMenuScreen(Screen_):
    def __init__(self):
        super(MainMenuScreen, self).__init__()
        self.font = utils.getFont('SigmarOne', 44)
        self.infofont = utils.getFont('SigmarOne', 18)
        self.background = pygame.image.load("../img/backgrounds/mainMenu.png")
        self.infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
        self.menuEntries = ["Start Game","Options","Quit"] ## add continue -> levelMenuScreen
        self.menuInfo = ["Start or continue your adventure","Change game and user settings","Exit the game. Goodbye!"]
        self.menuChoice = 0
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey29"]
        self.menuColors = [self.activeColor,self.inactiveColor,self.inactiveColor]

    def update(self):
        pass

    def render(self,backgroundScreen):
    
        backgroundScreen.fill((56,56,56))
        backgroundScreen.blit(self.background, (0,0))
        backgroundScreen.blit(self.infoBar, (0,600))
        backgroundScreen.blit(self.infofont.render(self.menuInfo[self.menuChoice], 1, THECOLORS["white"]),(200,605))
        backgroundScreen.blit(self.font.render(self.menuEntries[0], 1, self.menuColors[0]), (200,100))
        backgroundScreen.blit(self.font.render(self.menuEntries[1], 1, self.menuColors[1]), (200,300))
        backgroundScreen.blit(self.font.render(self.menuEntries[2], 1, self.menuColors[2]), (200,500))

        
    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
#                     startScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #,space
                    self.screenManager.go_to('startScreen')
                elif event.key == K_RETURN:
                    if self.menuChoice == 0:
                        self.manager.go_to('startGameScreen')
                        # startGameScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                    elif self.menuChoice == 1:
                        self.manager.go_to('optionsScreen')
                    elif self.menuChoice == 2:
                        self.manager.go_to('startScreen')
                elif event.key == K_UP:
                    self.menuChoice = cycle("up",self.menuColors,self.menuChoice)
                elif event.key == K_DOWN:
                    self.menuChoice = cycle("down",self.menuColors,self.menuChoice)
