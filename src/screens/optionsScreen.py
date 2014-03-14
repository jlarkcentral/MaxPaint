'''
OptionsScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
from screen_ import Screen_

sys.path.append('../')
import utils
from utils import save,load,exist


class OptionsScreen(Screen_):
    def __init__(self):
        super(OptionsScreen, self).__init__()
    
        self.font = utils.getFont('SigmarOne', 44)
        self.background = pygame.image.load("../img/backgrounds/options.png").convert()
        self.infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
        self.soundBar = pygame.image.load("../img/backgrounds/soundBar.png")
        self.musicBar = pygame.image.load("../img/backgrounds/soundBar.png")
        self.volumeTest = pygame.mixer.Sound("../sounds/volumeTest.wav")
        self.menuEntries = ["Music","Sound","Controls","Back"]
        self.menuPositions = [(200,100),(200,200),(200,300),(200,500)]
        self.menuChoice = 0
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey29"]
        self.soundLevel = 0
        if exist('soundLevel'):
            self.soundLevel = load('soundLevel')
        self.musicLevel = 0
        if exist('musicLevel'):
           self.musicLevel = load('musicLevel')



    def render(self, backgroundScreen):
        backgroundScreen.blit(self.background, (0,0))
        backgroundScreen.blit(self.infoBar, (0,600))
        for i in range(len(self.menuEntries)):
            if i == self.menuChoice:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.activeColor), self.menuPositions[i])
            else:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.inactiveColor), self.menuPositions[i])
        backgroundScreen.blit(self.soundBar, (400,120), (0, self.soundLevel*30, 190, 30))
        backgroundScreen.blit(self.musicBar, (400,220), (0, self.musicLevel*30, 190, 30))        


      
    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    save([('soundLevel',self.soundLevel),('musicLevel',self.musicLevel)])
                    self.manager.go_to('mainMenuScreen')
                if event.key == K_RETURN:
                    if self.menuChoice == 3:
                        save([('soundLevel',self.soundLevel),('musicLevel',self.musicLevel)])
                        self.manager.go_to('mainMenuScreen')
                if event.key == K_UP:
                    self.menuChoice = (self.menuChoice - 1) % len(self.menuEntries)
                if event.key == K_DOWN:
                    self.menuChoice = (self.menuChoice + 1) % len(self.menuEntries)
                if event.key == K_LEFT:
                    if self.menuChoice == 0:
                        self.soundLevel = max(0,self.soundLevel-1)
                        self.volumeTest.set_volume(self.soundLevel*0.2)
                        self.volumeTest.play()
                    if self.menuChoice == 1:
                        self.musicLevel = max(0,self.musicLevel-1)
                        pygame.mixer.music.set_volume(self.musicLevel*0.2)
                        self.volumeTest.set_volume(self.musicLevel*0.2)
                        self.volumeTest.play()
                if event.key == K_RIGHT:
                    if self.menuChoice == 0:
                        self.soundLevel = min(5,self.soundLevel+1)
                        self.volumeTest.set_volume(self.soundLevel*0.2)
                        self.volumeTest.play()
                    if self.menuChoice == 1:
                        self.musicLevel = min(5,self.musicLevel+1)
                        pygame.mixer.music.set_volume(self.musicLevel*0.2)
                        self.volumeTest.set_volume(self.musicLevel*0.2)
                        self.volumeTest.play()
            if event.type == QUIT:
                save([('soundLevel',self.soundLevel),('musicLevel',self.musicLevel)])