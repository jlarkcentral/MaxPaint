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
        self.font = utils.getFont('SigmarOne', 44)
        self.background = pygame.image.load("../img/backgrounds/transition.png").convert()
        self.infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
        self.levelTitles = ["Tutorial","Green Machine", "Strange Orange", "Purple Trouble"]
        self.levelBackgrounds = []
        self.lvlbgsNames = []
        self.currentLevel = 0
        self.menuEntries = ["Stage 1","Stage 2","Stage 3","Back"]
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey29"]
        self.menuChoice = 0
        self.menuColors = [self.activeColor,self.inactiveColor,self.inactiveColor,self.inactiveColor]
        self.running = True
        self.frame_number = 0
        

    # def update(self,width,height,backgroundScreen,dt,screen,clock,fps):
    def handle_events(self,events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # startGameScreen.show(width,height,backgroundScreen,dt,screen,clock,fps)
                    self.screenManager.go_to('startGameScreen')
                if event.key == K_RETURN:
                    if self.menuChoice < 3:
                        # Game.launchGame(width,height,backgroundScreen,dt,screen,clock,fps,self.currentLevel*3 + (self.menuChoice + 1))
                        #running = False
                        self.manager.go_to_game(1) # self.currentLevel*3 + (self.menuChoice + 1)
                    elif self.menuChoice == 3:
                        # startGameScreen.show(width,height,backgroundScreen,dt,screen,clock,fps)
                        self.screenManager.go_to('startGameScreen')
                # if event.key == K_UP:
                #     menuChoice = cycle("up",menuColors,menuChoice)
                # if event.key == K_DOWN:
                #     menuChoice = cycle("down",menuColors,menuChoice)
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
        backgroundScreen.blit(self.infoBar, (0,600))
        backgroundScreen.blit(self.font.render(self.levelTitles[self.currentLevel], 1, self.activeColor), (100,50))
        backgroundScreen.blit(self.font.render(self.menuEntries[0], 1, self.menuColors[0]), (200,100))
        backgroundScreen.blit(self.font.render(self.menuEntries[1], 1, self.menuColors[1]), (200,200))
        backgroundScreen.blit(self.font.render(self.menuEntries[2], 1, self.menuColors[2]), (200,300))
        backgroundScreen.blit(self.font.render(self.menuEntries[3], 1, self.menuColors[3]), (200,500))