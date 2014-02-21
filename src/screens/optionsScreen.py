'''
OptionsScreen
'''

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
sys.path.append('../lib/')
import pyganim

sys.path.append('../')
import utils
from utils import cycle

import mainMenuScreen
from saveUtil import save,load,exist





def show(width,height,backgroundScreen,dt,screen,clock,fps): #space,
    
    font = utils.getFont('SigmarOne', 44)
    background = pygame.image.load("../img/backgrounds/bgOptions.png").convert()
    infoBar = pygame.image.load("../img/hud/scoreBar.png").convert()
    soundBar = pygame.image.load("../img/backgrounds/soundBar.png")
    musicBar = pygame.image.load("../img/backgrounds/soundBar.png")
    
    volumeTest = pygame.mixer.Sound("../sounds/volumeTest.wav")


    menuEntries = ["Music","Sound","Controls","Back"]
    menuChoice = 0
    activeColor = THECOLORS["black"]
    inactiveColor = THECOLORS["grey29"]
    menuColors = [activeColor,inactiveColor,inactiveColor,inactiveColor]

    
    soundLevel = 0
    if exist('soundLevel'):
        soundLevel = load('soundLevel')
    
    musicLevel = 0
    if exist('musicLevel'):
        musicLevel = load('musicLevel')

    running = True
    frame_number = 0
    while running:
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(infoBar, (0,600))

        backgroundScreen.blit(font.render(menuEntries[0], 1, menuColors[0]), (200,100))
        backgroundScreen.blit(font.render(menuEntries[1], 1, menuColors[1]), (200,200))
        backgroundScreen.blit(font.render(menuEntries[2], 1, menuColors[2]), (200,300))
        backgroundScreen.blit(font.render(menuEntries[3], 1, menuColors[3]), (200,500))
        
        backgroundScreen.blit(soundBar, (400,120), (0, soundLevel*30, 190, 30))
        backgroundScreen.blit(musicBar, (400,220), (0, musicLevel*30, 190, 30))        

        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        clock.tick(fps)
        frame_number += 1

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    save([('soundLevel',soundLevel),('musicLevel',musicLevel)])
                    running = False
                    mainMenuScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                if event.key == K_RETURN:
                    if menuChoice == 3:
                        save([('soundLevel',soundLevel),('musicLevel',musicLevel)])
                        running = False
                        mainMenuScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                if event.key == K_UP:
                    menuChoice = cycle("up",menuColors,menuChoice)
                if event.key == K_DOWN:
                    menuChoice = cycle("down",menuColors,menuChoice)
                if event.key == K_LEFT:
                    if menuChoice == 0:
                        soundLevel = max(0,soundLevel-1)
                        volumeTest.set_volume(soundLevel*0.2)
                        volumeTest.play()
                    if menuChoice == 1:
                        musicLevel = max(0,musicLevel-1)
                        pygame.mixer.music.set_volume(musicLevel*0.2)
                        volumeTest.set_volume(musicLevel*0.2)
                        volumeTest.play()
                if event.key == K_RIGHT:
                    if menuChoice == 0:
                        soundLevel = min(5,soundLevel+1)
                        volumeTest.set_volume(soundLevel*0.2)
                        volumeTest.play()
                    if menuChoice == 1:
                        musicLevel = min(5,musicLevel+1)
                        pygame.mixer.music.set_volume(musicLevel*0.2)
                        volumeTest.set_volume(musicLevel*0.2)
                        volumeTest.play()
            if event.type == QUIT:
                save([('soundLevel',soundLevel),('musicLevel',musicLevel)])
                running = False