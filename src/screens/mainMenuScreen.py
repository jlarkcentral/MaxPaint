'''
MainMenuScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../lib/')
import pyganim

import pgext

sys.path.append('../')
from utils import cycle

import optionsScreen
import startGameScreen
import startScreen




def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("SigmarOne", 44)
    infofont = pygame.font.SysFont("SigmarOne", 18)
    background = pygame.image.load("../img/backgrounds/bgMainMenuBW.png")
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()

    menuEntries = ["Start Game","Options","Quit"] ## add continue -> levelMenuScreen
    menuInfo = ["Start or continue your adventure","Change game and user settings","Exit the game. Goodbye!"]
    menuChoice = 0
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey29"]
    menuColors = [activeColor,inactiveColor,inactiveColor]


    running = True
    frame_number = 0

    while running:
        backgroundScreen.fill((56,56,56))
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        backgroundScreen.blit(infofont.render(menuInfo[menuChoice], 1, THECOLORS["white"]),(200,605))

        backgroundScreen.blit(font.render(menuEntries[0], 1, menuColors[0]), (200,100))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuColors[1]), (200,300))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuColors[2]), (200,500))

        

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    startScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                    running = False
                if event.key == K_RETURN:
                    if menuChoice == 0:
                        startGameScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                        running = False
                    if menuChoice == 1:
                        optionsScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                        running = False
                    if menuChoice == 2:
                        running = False
                if event.key == K_UP:
                    menuChoice = cycle("up",menuColors,menuChoice)
                if event.key == K_DOWN:
                    menuChoice = cycle("down",menuColors,menuChoice)
            if event.type == QUIT:
                running = False


        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1