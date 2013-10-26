'''
MainMenuScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../lib/')
import pyganim

sys.path.append('../')
from utils import cycle

import optionsScreen
import startGameScreen




def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/backgrounds/bgMainMenu.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()

    menuEntries = ["Start Game","Options","Quit"] ## add continue -> levelMenuScreen
    menuChoice = 0
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey"]
    menuColors = [activeColor,inactiveColor,inactiveColor]


    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        backgroundScreen.blit(font.render(menuEntries[0], 1, menuColors[0]), (200,100))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuColors[1]), (200,300))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuColors[2]), (200,500))

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if menuChoice == 0:
                        #game.launchGame(width,height,space,backgroundScreen,dt,screen,clock,fps)
                        startGameScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                        running = False
                    if menuChoice == 1:
                        optionsScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                        running = False
                if event.key == K_UP:
                    menuChoice = cycle("up",menuColors,menuChoice)
                if event.key == K_DOWN:
                    menuChoice = cycle("down",menuColors,menuChoice)
            if event.type == QUIT:
                running = False