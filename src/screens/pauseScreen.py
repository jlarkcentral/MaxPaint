'''
StartScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *

sys.path.append('../lib/')
import pyganim

sys.path.append('../')
from utils import cycle

import game



def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/backgrounds/pauseBG.png").convert()
    scoreBar = pygame.image.load("../img/hud/scoreBar.png").convert()

    menuEntries = ["Resume Game", "Retry Level", "Options", "Quit Level"]
    menuChoice = 0
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey"]
    menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]

    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (250,100))
        backgroundScreen.blit(scoreBar, (0,600))
        backgroundScreen.blit(font.render("Press [Enter] to resume game", \
            1, THECOLORS["white"]), (250,605))

        backgroundScreen.blit(font.render("P A U S E", \
            1, THECOLORS["white"]), (350,130))


        backgroundScreen.blit(font.render(menuEntries[0], 1, menuColors[0]), (350,200))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuColors[1]), (350,250))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuColors[2]), (350,300))
        backgroundScreen.blit(font.render(menuEntries[3], 1, menuColors[3]), (350,350))

    
        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    if menuChoice == 0:
                        running = False
                if event.key == K_UP:
                    menuChoice = cycle("up",menuColors,menuChoice)
                if event.key == K_DOWN:
                    menuChoice = cycle("down",menuColors,menuChoice)
            if event.type == QUIT:
                running = False