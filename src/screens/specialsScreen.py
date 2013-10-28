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
    
    font = pygame.font.SysFont("Impact", 44)
    fontDesc = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/backgrounds/bgGameStart.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
    nextColorIcon = pygame.image.load("../img/hud/nextColor23.png").convert()

    specialsColumns = ["Defender","Aggressor","Believer"]
    specialsBackground = pygame.image.load("../img/backgrounds/specialsBG.png")
    specialsIconsDef = [pygame.image.load("../img/backgrounds/sp_shield_1.png"),
                        pygame.image.load("../img/backgrounds/sp_shield_2.png"),
                        pygame.image.load("../img/backgrounds/sp_shield_3.png")]
    specialsIconsAtt = [pygame.image.load("../img/backgrounds/sp_shoot_1.png"),
                        pygame.image.load("../img/backgrounds/sp_shoot_2.png"),
                        pygame.image.load("../img/backgrounds/sp_shoot_3.png")]
    specialsIconsBel = [pygame.image.load("../img/backgrounds/sp_bel_1.png"),
                        pygame.image.load("../img/backgrounds/sp_bel_2.png"),
                        pygame.image.load("../img/backgrounds/sp_bel_3.png")]
    specialsDescriptions = [["The shield protects all sides",
                             "The shield has 2 layers",
                             "The shield destroys enemies"],
                            ["Shoot 2 bullets at a time",
                             "50"+'%'+" chance of homing bullets",
                             "Infinite ammo for 10 sec. (1/stage)",],
                            ["50"+'%'+" chance that enemies ignore you",
                             "Freeze all enemies for 10 sec. (1/stage)",
                             "50"+'%'+" chance that you reflect bullets"]]
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
        backgroundScreen.blit(specialsBackground, (100,150))

        backgroundScreen.blit(font.render(specialsColumns[0], 1, columnTitleColors[0]), (120,50))
        backgroundScreen.blit(font.render(specialsColumns[1], 1, columnTitleColors[1]), (310,50))
        backgroundScreen.blit(font.render(specialsColumns[2], 1, columnTitleColors[2]), (520,50))

        backgroundScreen.blit(specialsIconsDef[0], (150,180))
        backgroundScreen.blit(specialsIconsDef[1], (150,300))
        backgroundScreen.blit(specialsIconsDef[2], (150,420))

        backgroundScreen.blit(specialsIconsAtt[0], (350,180))
        backgroundScreen.blit(specialsIconsAtt[1], (350,300))
        backgroundScreen.blit(specialsIconsAtt[2], (350,420))

        backgroundScreen.blit(specialsIconsBel[0], (550,180))
        backgroundScreen.blit(specialsIconsBel[1], (550,300))
        backgroundScreen.blit(specialsIconsBel[2], (550,420))

        backgroundScreen.blit(selectionTool, selectionPositions[selectedIcon[0]][selectedIcon[1]])        
        backgroundScreen.blit(fontDesc.render(specialsDescriptions[selectedIcon[0]][selectedIcon[1]], \
            1, THECOLORS["white"]), (50,605))
        backgroundScreen.blit(fontDesc.render("Costs", 1, THECOLORS["white"]), (550,605))

        if activeColumn == 0:
            costColor = [3,4]
        if activeColumn == 1:
            costColor = [1,3]
        if activeColumn == 2:
            costColor = [4,1]

        backgroundScreen.blit(nextColorIcon, to_pygame((650,35), backgroundScreen), (0, costColor[0]*30, 50, 30))
        backgroundScreen.blit(nextColorIcon, to_pygame((750,35), backgroundScreen), (0, costColor[1]*30, 50, 30))


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
                #if event.key == K_RETURN:

                if event.key == K_LEFT:
                    activeColumn = cycle("up",columnTitleColors,activeColumn)
                    selectedIcon = [activeColumn ,iconIndex]
                if event.key == K_RIGHT:
                    activeColumn = cycle("down",columnTitleColors,activeColumn)
                    selectedIcon = [activeColumn ,iconIndex]
                if event.key == K_UP:
                    iconIndex = cycle("up",[0,1,2],iconIndex)
                    selectedIcon = [activeColumn ,iconIndex]
                if event.key == K_DOWN:
                    iconIndex = cycle("down",[0,1,2],iconIndex)
                    selectedIcon = [activeColumn ,iconIndex]
            if event.type == QUIT:
                running = False