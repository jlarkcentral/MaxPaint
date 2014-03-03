'''
StartScreen
'''

import sys
import random

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../lib/pyganim')
import pyganim

import utils
import mainMenuScreen




def show(width,height,backgroundScreen,dt,screen,clock,fps): #space,
    enterFont = utils.getFont('SigmarOne', 40)
    background = pygame.image.load("../img/backgrounds/title.png").convert()
    running = True
    enterColors = (235,246,242)
    frameNumber = 0
    fade = 1
    

    while running:
        
        backgroundScreen.blit(background, (0,0))

        backgroundScreen.blit(enterFont.render("Press any key",1,enterColors),(200,400))           
        if frameNumber % 200 != 0:
            enterColors = tuple(map(sum, zip((fade, fade, fade), enterColors)))
        else:
            fade *= -1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key != K_ESCAPE:
                    mainMenuScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                    running = False
                elif event.key == K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frameNumber += 1