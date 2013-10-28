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
from utils import cycle

import mainMenuScreen
import levelSelectScreen
import specialsScreen




def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("Impact", 44)
    background = pygame.image.load("../img/backgrounds/bgGameStart.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()


    gameBackgrounds = [pygame.image.load("../img/backgrounds/gameMenuSelect.png"), \
    pygame.image.load("../img/backgrounds/gameMenuNotSelect.png"), \
    pygame.image.load("../img/backgrounds/gameMenuNotSelect.png") ]

    gameEntries = ["New","New","New"]
    menuEntries = ["Back","Specials","Start"]
    gameChoice = 0
    menuChoice = 2
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey"]
    gameEntriesColors = [activeColor,inactiveColor,inactiveColor]
    menuEntriesColors = [inactiveColor,inactiveColor,inactiveColor]
    
    currentMenu = gameEntries

    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        if gameChoice == 0:
            backgroundScreen.blit(font.render(gameEntries[0], 1, gameEntriesColors[0]), (200,100))
            backgroundScreen.blit(font.render(gameEntries[1], 1, gameEntriesColors[1]), (450,100))
            backgroundScreen.blit(font.render(gameEntries[2], 1, gameEntriesColors[2]), (600,100))

            backgroundScreen.blit(gameBackgrounds[0], (100,100))
            backgroundScreen.blit(gameBackgrounds[1], (400,100))
            backgroundScreen.blit(gameBackgrounds[2], (550,100))

        elif gameChoice == 1:
            backgroundScreen.blit(font.render(gameEntries[0], 1, gameEntriesColors[0]), (150,100))
            backgroundScreen.blit(font.render(gameEntries[1], 1, gameEntriesColors[1]), (350,100))
            backgroundScreen.blit(font.render(gameEntries[2], 1, gameEntriesColors[2]), (600,100))

            backgroundScreen.blit(gameBackgrounds[0], (100,100))
            backgroundScreen.blit(gameBackgrounds[1], (250,100))
            backgroundScreen.blit(gameBackgrounds[2], (550,100))

        elif gameChoice == 2:
            backgroundScreen.blit(font.render(gameEntries[0], 1, gameEntriesColors[0]), (150,100))
            backgroundScreen.blit(font.render(gameEntries[1], 1, gameEntriesColors[1]), (300,100))
            backgroundScreen.blit(font.render(gameEntries[2], 1, gameEntriesColors[2]), (500,100))

            backgroundScreen.blit(gameBackgrounds[0], (100,100))
            backgroundScreen.blit(gameBackgrounds[1], (250,100))
            backgroundScreen.blit(gameBackgrounds[2], (400,100))            

        backgroundScreen.blit(font.render(menuEntries[0], 1, menuEntriesColors[0]), (100,500))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuEntriesColors[1]), (300,500))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuEntriesColors[2]), (600,500))

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        if currentMenu == gameEntries:
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        mainMenuScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                        running = False
                    if event.key == K_RETURN:
                        currentMenu = menuEntries
                        menuChoice = 2
                        menuEntriesColors = [inactiveColor,inactiveColor,activeColor]
                    if event.key == K_LEFT:
                        gameChoice = cycle("up",gameEntriesColors,gameChoice)
                        cycle("up",gameBackgrounds,0)
                    if event.key == K_RIGHT:
                        gameChoice = cycle("down",gameEntriesColors,gameChoice)
                        cycle("down",gameBackgrounds,0)
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
                        currentMenu = gameEntries
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
                            specialsScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                            running = False
                        if menuChoice == 2:
                            #game.launchGame(width,height,space,backgroundScreen,dt,screen,clock,fps)
                            levelSelectScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                            running = False
                if event.type == QUIT:
                    running = False