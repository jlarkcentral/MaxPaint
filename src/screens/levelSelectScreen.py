'''
LevelSelectScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../../lib/')
import pyganim

sys.path.append('../')
from utils import cycle
import game

import mainMenuScreen





def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("Impact", 44)
    #background = pygame.image.load("../img/backgrounds/bgOptions.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()

    levelTitles = ["Initial Friction", "Hot Lift", "Magma Chamber",\
     "Lava Rush", "Volcano Explosion", "Big Smoke", "Clear Sky"]
    levelBackgrounds = [pygame.image.load("../img/backgrounds/1_InitialFriction_menu.png").convert(),\
                        pygame.image.load("../img/backgrounds/2_HotLift_menu.png").convert(),\
                        pygame.image.load("../img/backgrounds/3_MagmaChamber_menu.png").convert(),\
                        pygame.image.load("../img/backgrounds/4_lavaRush_menu.png").convert(),\
                        pygame.image.load("../img/backgrounds/5_volcanoExplosion_menu.png").convert(),\
                        pygame.image.load("../img/backgrounds/6_BigSmoke_menu.png").convert(),\
                        pygame.image.load("../img/backgrounds/bg_menu.png").convert()]
    currentLevel = 0
    menuEntries = ["Stage 1","Stage 2","Stage 3","Back"]
    menuChoice = 0
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey"]
    menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]


    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(levelBackgrounds[currentLevel], (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        backgroundScreen.blit(font.render(levelTitles[currentLevel], 1, activeColor), (100,50))

        backgroundScreen.blit(font.render(menuEntries[0], 1, menuColors[0]), (200,100))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuColors[1]), (200,200))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuColors[2]), (200,300))
        backgroundScreen.blit(font.render(menuEntries[3], 1, menuColors[3]), (200,500))

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenuScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                    running = False
                if event.key == K_RETURN:
                    if menuChoice < 3:
                        game.launchGame(width,height,space,backgroundScreen,dt,screen,clock,fps)
                        running = False
                    #elif menuChoice == 3:

                if event.key == K_UP:
                    menuChoice = cycle("up",menuColors,menuChoice)
                if event.key == K_DOWN:
                    menuChoice = cycle("down",menuColors,menuChoice)
                if event.key == K_LEFT:
                    currentLevel = (currentLevel - 1) % len(levelTitles)
                if event.key == K_RIGHT:
                    currentLevel = (currentLevel + 1) % len(levelTitles)
            if event.type == QUIT:
                running = False