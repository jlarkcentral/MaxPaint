'''
StartScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../lib/pyganim')
import pyganim

import mainMenuScreen




def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("SigmarOne", 18)
    background = pygame.image.load("../img/backgrounds/startScreenBG_withcanvas_withtaches.png").convert()
    hudbar = pygame.image.load("../img/hud/scoreBar.png").convert()

    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(hudbar,(0,605))
        backgroundScreen.blit(font.render("A python game using pygame, pymunk and pyganim", \
            1, THECOLORS["white"]), (230,605))
    
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