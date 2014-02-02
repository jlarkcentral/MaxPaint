'''
StartGameScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../../lib/')
import pyganim

sys.path.append('../')
import game
from utils import cycle,letterKeys
from saveUtil import save,load,exist

import mainMenuScreen
import levelSelectScreen
import shopScreen




def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("SigmarOne", 44)
    namefont = pygame.font.SysFont("SigmarOne", 24)
    background = pygame.image.load("../img/backgrounds/BWbg.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()

    profileBackground = pygame.image.load("../img/backgrounds/gameMenuSelect.png")

    profileName = 'New'
    if exist('profileName'):
        profileName = load('profileName')
    profile = []

    menuEntries = ["Back","Shop","Start"]
    menuChoice = 2
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey29"]
    menuEntriesColors = [inactiveColor,inactiveColor,inactiveColor]

    currentMenu = profile
    nameEntering = False
    nameEnteringShowing = False

    def get_key():
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return event.key
                else:
                    pass

    current_string = ""
    


    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        if not nameEntering:
            backgroundScreen.blit(font.render(profileName, 1, THECOLORS["black"]), (330,100))
        backgroundScreen.blit(profileBackground, (300,100))

        backgroundScreen.blit(font.render(menuEntries[0], 1, menuEntriesColors[0]), (50,500))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuEntriesColors[1]), (350,500))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuEntriesColors[2]), (600,500))

        if nameEntering:
            backgroundScreen.blit(namefont.render(current_string, 1, activeColor), (330,100))
            if nameEnteringShowing:
                inkey = get_key()
                if inkey == K_BACKSPACE:
                    current_string = current_string[:-1]
                elif inkey == K_RETURN or inkey == K_KP_ENTER:
                    profileName = current_string
                    save([('profileName',profileName)])
                    nameEntering = False
                    nameEnteringShowing = False
                elif inkey in letterKeys:
                    if len(current_string) < 10:
                        current_string += chr(inkey)
            else:
                nameEnteringShowing = True

        else:
            if currentMenu == profile:
                events = pygame.event.get()
                for event in events:
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            mainMenuScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                            running = False
                        if event.key == K_RETURN:
                            if not exist('profileName'):
                                nameEntering = True
                            currentMenu = menuEntries
                            menuChoice = 2
                            menuEntriesColors = [inactiveColor,inactiveColor,activeColor]
                    if event.type == QUIT:
                        running = False

            elif currentMenu == menuEntries:
                events = pygame.event.get()
                for event in events:
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            mainMenuScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                            running = False
                        if event.key == K_UP:
                            currentMenu = profile
                            menuEntriesColors = [inactiveColor,inactiveColor,inactiveColor]
                        if event.key == K_LEFT:
                            menuChoice = cycle("up",menuEntriesColors,menuChoice)
                        if event.key == K_RIGHT:
                            menuChoice = cycle("down",menuEntriesColors,menuChoice)
                        if event.key == K_RETURN:
                            if menuChoice == 0:
                                mainMenuScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                                running = False
                            if menuChoice == 1:
                                shopScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                                running = False
                            if menuChoice == 2:
                                levelSelectScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                                running = False
                    if event.type == QUIT:
                        running = False


        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1