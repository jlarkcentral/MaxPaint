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

class MainMenuScreen(Screen_):
    def __init__(self):
        super(MainMenuScreen, self).__init__()
        self.font = utils.getFont('SigmarOne', 44)
        self.infofont = utils.getFont('SigmarOne', 18)
        self.background = pygame.image.load("../img/backgrounds/mainMenu.png")
        self.infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
        self.menuEntries = ["Start Game","Options","Quit"] ## add continue -> levelMenuScreen
        self.menuPositions = [(200,100),(200,300),(200,500)]
        self.menuInfo = ["Start or continue your adventure","Change game and user settings","Exit the game. Goodbye!"]
        self.menuChoice = 0
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey29"]


    def render(self,backgroundScreen):
    
        backgroundScreen.fill((56,56,56))
        backgroundScreen.blit(self.background, (0,0))
        backgroundScreen.blit(self.infoBar, (0,600))
        backgroundScreen.blit(self.infofont.render(self.menuInfo[self.menuChoice], 1, THECOLORS["white"]),(200,605))
        for i in range(len(self.menuEntries)):
            if i == self.menuChoice:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.activeColor), self.menuPositions[i])
            else:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.inactiveColor), self.menuPositions[i])

        
    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.manager.go_to('startScreen')
                elif event.key == K_RETURN:
                    if self.menuChoice == 0:
                        self.manager.go_to('startGameScreen')
                    elif self.menuChoice == 1:
                        self.manager.go_to('optionsScreen')
                    elif self.menuChoice == 2:
                        self.manager.go_to('startScreen')
                elif event.key == K_UP:
                    self.menuChoice = (self.menuChoice - 1) % len(self.menuEntries)
                elif event.key == K_DOWN:
                    self.menuChoice = (self.menuChoice + 1) % len(self.menuEntries)
