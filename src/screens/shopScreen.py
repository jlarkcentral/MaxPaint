'''
SpecialsScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

sys.path.append('../lib/')
import pyganim

sys.path.append('../')
from utils import cycle

import optionsScreen
import startGameScreen





def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    font = pygame.font.SysFont("SigmarOne", 44)
    fontDesc = pygame.font.SysFont("SigmarOne", 24)
    background = pygame.image.load("../img/backgrounds/levelSelect.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()

    
    selectionTool = pygame.image.load("../img/backgrounds/sp_select.png")
    selectionPositions = [[(145,175),(145,295),(145,415)],
                            [(345,175),(345,295),(345,415)],
                            [(545,175),(545,295),(545,415)]]
    
    activeColumn = 0
    iconIndex = 0
    selectedIcon = [activeColumn,iconIndex]
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey"]
    columnTitleColors = [activeColor,inactiveColor,inactiveColor]
    costColor = [3,4]


    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    startGameScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                    running = False
            if event.type == QUIT:
                running = False