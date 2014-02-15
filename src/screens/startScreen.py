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
    
    titleFont = utils.getFont('SigmarOne',150)
    enterFont = utils.getFont('SigmarOne', 40)
    noteFont = utils.getFont('SigmarOne', 18)

    background = pygame.image.load("../img/backgrounds/startScreenBGBW.png")

    running = True
    frame_number = 0

    lightFill = 0
    surf_lighting = pygame.Surface(screen.get_size())
    bing = False
    enter = True#False

    dropDelay = 40
    dropx = dropy = 0
    drop = False

    while running:
        
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(titleFont.render("NIGHT",1,(56,56,56)),(100,0))
        backgroundScreen.blit(titleFont.render("TIME",1,(56,56,56)),(150,200))
        backgroundScreen.blit(noteFont.render("A python game using pygame, pymunk and pyganim", \
            1, (56,56,56)), (230,605))

        if enter:
            backgroundScreen.blit(enterFont.render("Press any key",1,(156,156,156)),(200,500))           

        if lightFill < 255 and not bing:
            lightFill += 1
            if lightFill == 255:
                bing = True
                enter = True
        elif lightFill > 50:
            lightFill -= 1
            if lightFill == 50:
                bing = False
        surf_lighting.fill((lightFill,lightFill,lightFill))
        backgroundScreen.blit(surf_lighting,(0,0),special_flags=BLEND_MULT)

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key != K_ESCAPE and enter:
                    mainMenuScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                    running = False
                elif event.key == K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1