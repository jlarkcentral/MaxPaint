'''
LevelSelectScreen
'''

import sys
import os

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../../lib/')
import pyganim

sys.path.append('../')
import utils
from utils import cycle
import game

sys.path.append('../gameObjects/')
from level import Level

import mainMenuScreen
import startGameScreen



def show(width,height,backgroundScreen,dt,screen,clock,fps): # space,
    
    font = utils.getFont('SigmarOne', 44)
    background = pygame.image.load("../img/backgrounds/transition.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()

    levelTitles = ["Tutorial","Green Machine", "Strange Orange", "Purple Trouble"]
    levelBackgrounds = []
    lvlbgsNames = []
    
    currentLevel = 0
    menuEntries = ["Stage 1","Stage 2","Stage 3","Back"]
    
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey29"]
    menuChoice = 0
    menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]

    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        backgroundScreen.blit(font.render(levelTitles[currentLevel], 1, activeColor), (100,50))

        backgroundScreen.blit(font.render(menuEntries[0], 1, menuColors[0]), (200,100))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuColors[1]), (200,200))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuColors[2]), (200,300))
        backgroundScreen.blit(font.render(menuEntries[3], 1, menuColors[3]), (200,500))

        

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    startGameScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                    running = False
                if event.key == K_RETURN:
                    if menuChoice < 3:
                        game.launchGame(width,height,backgroundScreen,dt,screen,clock,fps,currentLevel*3 + (menuChoice + 1)) # space,
                        #running = False
                    elif menuChoice == 3:
                        startGameScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) # space,
                        running = False
                if event.key == K_UP:
                    menuChoice = cycle("up",menuColors,menuChoice)
                if event.key == K_DOWN:
                    menuChoice = cycle("down",menuColors,menuChoice)
                if event.key == K_LEFT:
                    currentLevel = (currentLevel - 1) % len(levelTitles)
                    menuChoice = 0
                    menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]
                if event.key == K_RIGHT:
                    currentLevel = (currentLevel + 1) % len(levelTitles)
                    menuChoice = 0
                    menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]
            if event.type == QUIT:
                running = False

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1