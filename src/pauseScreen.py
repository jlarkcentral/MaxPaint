'''
StartScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *

sys.path.append('../lib/')
import pyganim

import game



def pauseScreen(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/backgrounds/bgStart.png").convert()
    scoreBar = pygame.image.load("../img/hud/scoreBar.png").convert()


    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(scoreBar, (0,600))
        backgroundScreen.blit(font.render("Press [Enter] to resume game", \
            1, THECOLORS["white"]), (250,605))
    
        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN and event.key == K_RETURN:
                #game.launchGame(width,height,space,backgroundScreen,dt,screen,clock,fps)
                running = False
            if event.type == QUIT:
                running = False