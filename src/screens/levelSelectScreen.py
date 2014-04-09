'''
LevelSelectScreen
'''

import sys
import pygame
sys.path.append('../')
from pygame.locals import *
import utils
from pygame.color import THECOLORS
from screen_ import Screen_


class LevelSelectScreen(Screen_):

    def __init__(self):
        super(LevelSelectScreen, self).__init__()
        self.font = utils.getFont('VolterGoldfish', 44)
        self.background = pygame.image.load("../img/backgrounds/levelSelect.png").convert()
        self.levelTitles = ["Tutorial","Green Machine", "Strange Orange", "Purple Trouble"]
        self.levelBackgrounds = []
        self.lvlbgsNames = []
        self.currentLevel = 0
        self.menuEntries = ["Stage 1","Stage 2","Stage 3","Back"]
        self.menuPositions = [(200,100),(200,200),(200,300),(200,500)]
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey64"]
        self.menuChoice = 0
        self.running = True
        self.frame_number = 0
        

    def handle_events(self,events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.manager.go_to('mainMenuScreen')
                if event.key == K_RETURN:
                    if self.menuChoice < 3:
                        self.manager.go_to_game(self.menuChoice) # self.currentLevel*3 + (self.menuChoice + 1)
                    elif self.menuChoice == 3:
                        self.manager.go_to('mainMenuScreen')
                if event.key == K_UP:
                    self.menuChoice = (self.menuChoice - 1) % len(self.menuEntries)
                if event.key == K_DOWN:
                    self.menuChoice = (self.menuChoice + 1) % len(self.menuEntries)
                # if event.key == K_LEFT:
                #     currentLevel = (currentLevel - 1) % len(levelTitles)
                #     menuChoice = 0
                #     menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]
                # if event.key == K_RIGHT:
                #     currentLevel = (currentLevel + 1) % len(levelTitles)
                #     menuChoice = 0
                #     menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]

    def render(self, backgroundScreen):
        backgroundScreen.blit(self.background, (0,0))
        backgroundScreen.blit(self.font.render(self.levelTitles[self.currentLevel], 1, self.activeColor), (100,50))
        for i in range(len(self.menuEntries)):
            if i == self.menuChoice:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.activeColor), self.menuPositions[i])
            else:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.inactiveColor), self.menuPositions[i])