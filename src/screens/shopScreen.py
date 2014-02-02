'''
SpecialsScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import from_pygame, to_pygame

sys.path.append('../lib/')
import pyganim

sys.path.append('../')
from utils import cycle

import optionsScreen
import startGameScreen





def show(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    sectionFont = pygame.font.SysFont("SigmarOne", 44)
    font = pygame.font.SysFont("SigmarOne", 34)
    fontDesc = pygame.font.SysFont("SigmarOne", 24)
    background = pygame.image.load("../img/backgrounds/levelSelect.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
    shopBar = pygame.image.load("../img/hud/shopBar.png")

    shopSections = ["Blocks","Shield", "Bullets", "Misc"]
    
    shopItems = [
                    [
                        ['double red block',20,5,0],\
                        ['double blue block',20,5,0],\
                        ['double yellow block',20,5,0],\
                    ],
                    [
                        ['shield something',20,5,0],\
                        ['shield something',20,5,0],\
                        ['shield something',20,5,0],\
                    ],
                    [
                        ['bullets blabla',20,5,0],\
                        ['bullets blabla',20,5,0],\
                    ],
                    [
                        ['misc item 1',20,5,0],\
                        ['misc item 2',20,5,0],\
                    ]
                ]


    choice = 0
    currentSection = 0
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey"]


    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        backgroundScreen.blit(sectionFont.render(shopSections[currentSection], 1, THECOLORS["black"]), (100,50))
        for i in range(len(shopItems[currentSection])):
            if choice != i:
                backgroundScreen.blit(font.render(shopItems[currentSection][i][0], 1, inactiveColor), (100,i*50+200))
                backgroundScreen.blit(fontDesc.render(str(shopItems[currentSection][i][1]), 1, THECOLORS["blue4"]), (600,i*50+200))
                backgroundScreen.blit(fontDesc.render(str(shopItems[currentSection][i][2]), 1, THECOLORS["yellow3"]), (670,i*50+200))
                backgroundScreen.blit(fontDesc.render(str(shopItems[currentSection][i][3]), 1, THECOLORS["red3"]), (740,i*50+200))
            else:
                backgroundScreen.blit(shopBar,(580,choice*50+200))        
                backgroundScreen.blit(font.render(shopItems[currentSection][choice][0], 1, activeColor), (100,choice*50+200))
                backgroundScreen.blit(fontDesc.render(str(shopItems[currentSection][choice][1]), 1, THECOLORS["blue"]), (600,choice*50+200))
                backgroundScreen.blit(fontDesc.render(str(shopItems[currentSection][choice][2]), 1, THECOLORS["yellow"]), (670,choice*50+200))
                backgroundScreen.blit(fontDesc.render(str(shopItems[currentSection][choice][3]), 1, THECOLORS["red"]), (740,choice*50+200))


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
                if event.key == K_UP:
                    choice = (choice - 1) % len(shopItems[currentSection])
                if event.key == K_DOWN:
                    choice = (choice + 1) % len(shopItems[currentSection])
                if event.key == K_RIGHT:
                    currentSection = (currentSection + 1) % len(shopItems)
                    choice = 0
                if event.key == K_LEFT:
                    currentSection = (currentSection - 1) % len(shopItems)
                    choice = 0
            if event.type == QUIT:
                running = False