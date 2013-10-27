'''
StartScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../lib/')
import pyganim

import mainMenuScreen




def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/backgrounds/bgStart.png").convert()
    titleG = pygame.image.load("../img/backgrounds/g.png")
    titleL = pygame.image.load("../img/backgrounds/l.png")
    titleO = pygame.image.load("../img/backgrounds/o.png")
    titleX = pygame.image.load("../img/backgrounds/x.png")

    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(titleG, (100,200))
        backgroundScreen.blit(titleL, (250,200))
        backgroundScreen.blit(titleO, (400,200))
        backgroundScreen.blit(titleX, (550,200))
        backgroundScreen.blit(font.render("A python game using pygame, pymunk and pyganim", \
            1, THECOLORS["white"]), (250,605))
    
        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key != K_ESCAPE:
                    mainMenuScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                    running = False
                elif event.key == K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False