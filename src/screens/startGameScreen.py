'''
StartGameScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *

sys.path.append('../')
import utils
from utils import load,exist
from screen_ import Screen_

class StartGameScreen(Screen_):
    """docstring for StartGameScreen"""
    def __init__(self):
        super(StartGameScreen, self).__init__()
        
        self.font = utils.getFont('SigmarOne', 44)
        self.namefont = utils.getFont('SigmarOne', 24)
        self.background = pygame.image.load("../img/backgrounds/transition.png").convert()
        self.infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()

        self.profileBackground = pygame.image.load("../img/backgrounds/gameMenuSelect.png")

        self.profileName = 'New'
        if exist('profileName'):
            self.profileName = load('profileName')

        self.menuEntries = ["Back","Shop","Start"]
        self.menuPositions = [(50,500),(350,500),(600,500)]
        self.menuChoice = 2
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey29"]

    def render(self, backgroundScreen):
        backgroundScreen.blit(self.background, (0,0))
        backgroundScreen.blit(self.infoBar, (0,600))        
        backgroundScreen.blit(self.profileBackground, (300,100))
        for i in range(len(self.menuEntries)):
            if i == self.menuChoice:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.activeColor), self.menuPositions[i])
            else:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.inactiveColor), self.menuPositions[i])

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.manager.go_to('mainMenuScreen')
                if event.key == K_LEFT:
                    self.menuChoice = (self.menuChoice - 1) % len(self.menuEntries)
                if event.key == K_RIGHT:
                    self.menuChoice = (self.menuChoice + 1) % len(self.menuEntries)
                if event.key == K_RETURN:
                    if self.menuChoice == 0:
                        self.manager.go_to('mainMenuScreen')
                    if self.menuChoice == 1:
                        self.manager.go_to('shopScreen')
                    if self.menuChoice == 2:
                        self.manager.go_to('levelSelectScreen')

