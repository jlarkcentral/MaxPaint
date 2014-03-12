'''
StartGameScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *

sys.path.append('../')
import utils
from utils import cycle,save,load,exist
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
        self.profile = []

        self.menuEntries = ["Back","Shop","Start"]
        self.menuChoice = 2
        self.activeColor = THECOLORS["black"]
        self.inactiveColor = THECOLORS["grey29"]
        self.menuEntriesColors = [self.inactiveColor,self.inactiveColor,self.inactiveColor]

        self.currentMenu = self.profile
        self.nameEntering = False
        self.nameEnteringShowing = False

    def render(self, backgroundScreen):
        backgroundScreen.blit(self.background, (0,0))
        backgroundScreen.blit(self.infoBar, (0,600))        
        backgroundScreen.blit(self.profileBackground, (300,100))
        backgroundScreen.blit(self.font.render(self.menuEntries[0], 1, self.menuEntriesColors[0]), (50,500))
        backgroundScreen.blit(self.font.render(self.menuEntries[1], 1, self.menuEntriesColors[1]), (350,500))
        backgroundScreen.blit(self.font.render(self.menuEntries[2], 1, self.menuEntriesColors[2]), (600,500))

        # if nameEntering:
        #     backgroundScreen.blit(namefont.render(current_string, 1, activeColor), (330,100))
        #     if nameEnteringShowing:
        #         inkey = get_key()
        #         if inkey == K_BACKSPACE:
        #             current_string = current_string[:-1]
        #         elif inkey == K_RETURN or inkey == K_KP_ENTER:
        #             profileName = current_string
        #             save([('profileName',profileName)])
        #             nameEntering = False
        #             nameEnteringShowing = False
        #         elif inkey in letterKeys:
        #             if len(current_string) < 10:
        #                 current_string += chr(inkey)
        #     else:
        #         nameEnteringShowing = True

        # else:

    def handle_events(self, events):
        if self.currentMenu == self.profile:
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # mainMenuScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                        self.screenManager
                    if event.key == K_RETURN:
                        if not exist('profileName'):
                            self.nameEntering = True
                        self.currentMenu = self.menuEntries
                        self.menuChoice = 2
                        self.menuEntriesColors = [self.inactiveColor,self.inactiveColor,self.activeColor]

        elif self.currentMenu == self.menuEntries:
            # events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # mainMenuScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) # space,
                        self.manager.go_to('mainMenuScreen')
                    if event.key == K_UP:
                        self.currentMenu = self.profile
                        self.menuEntriesColors = [self.inactiveColor,self.inactiveColor,self.inactiveColor]
                    if event.key == K_LEFT:
                        self.menuChoice = cycle("up",self.menuEntriesColors,self.menuChoice)
                    if event.key == K_RIGHT:
                        self.menuChoice = cycle("down",self.menuEntriesColors,self.menuChoice)
                    if event.key == K_RETURN:
                        if self.menuChoice == 0:
                            # mainMenuScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #,space
                            self.manager.go_to('mainMenuScreen')
                        if self.menuChoice == 1:
                            # shopScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                            self.manager.go_to('shopScreen')
                        if self.menuChoice == 2:
                            # levelSelectScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) # space
                            self.manager.go_to('levelSelectScreen')

