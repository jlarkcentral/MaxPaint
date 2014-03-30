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
    
        self.font = utils.getFont('Handy00', 44)
        self.infofont = utils.getFont('Handy00', 18)
        self.keyfont = utils.getFont('Handy00', 24)
        self.background = pygame.image.load("../img/backgrounds/options.png").convert()
        self.soundBar = pygame.image.load("../img/backgrounds/soundBar.png")
        self.musicBar = pygame.image.load("../img/backgrounds/soundBar.png")
        self.keyImg = pygame.image.load("../img/backgrounds/key.png")
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
        self.actionKeys = ['slow time','shield','trap','left','jump','right']
        self.keys = ['w','x','c','<','^','>']
        self.actionKeysPos = [(200,450),(330,450),(430,450),(530,450),(630,450),(730,450)]




    def render(self, backgroundScreen):
        backgroundScreen.blit(self.background, (0,0))
        for i in range(len(self.menuEntries)):
            if i == self.menuChoice:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.activeColor), self.menuPositions[i])
            else:
                backgroundScreen.blit(self.font.render(self.menuEntries[i], 1, self.inactiveColor), self.menuPositions[i])
        for i in range(len(self.actionKeys)):
            backgroundScreen.blit(self.infofont.render(self.actionKeys[i],1,self.inactiveColor),(200+(i>0)*(i*100+30),450))
            backgroundScreen.blit(self.keyImg,(200+(i>0)*(i*100+30),380))
            backgroundScreen.blit(self.keyfont.render(self.keys[i],1,self.inactiveColor),(200+(i>0)*(i*100+30)+20,390))
        for i in range(5):
            backgroundScreen.blit(self.soundBar, (400+i*40,120), (0, (self.soundLevel > i)*30, 30, 30))
            backgroundScreen.blit(self.musicBar, (400+i*40,220), (0, (self.musicLevel > i)*30, 30, 30))

      
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