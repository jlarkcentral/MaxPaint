"""

PyGame game test

modified code from platformer example

Game launcher

"""

import os
import sys
import time

import pygame
from pygame.locals import *
from pygame.color import *

sys.path.append('../lib/pyganim/')
import pyganim
sys.path.append('../lib/')
import PAdLib.shadow as shadow

sys.path.append('gameObjects/')
from player import Player
from camera import Camera
from level import Level

sys.path.append('screens/')
import pauseScreen

from saveUtil import save,load,exist
from utils import to_pygame, distance


# INITIALIZATION & CONTENT LOADING
def gameScreenInit(width_,height_,cameraHeight):

    width = width_
    height = height_
    camera = Camera(height, width, cameraHeight)

# def loadResources():

#     font = pygame.font.SysFont("Impact", 24)
#     scoreBar = pygame.image.load("../img/hud/scoreBar.png").convert()
#     nextColorIcon = pygame.image.load("../img/hud/nextColor23.png").convert()
#     lifeHud = pygame.image.load("../img/hud/life.png")

#     color_dict = {'blue': 0, 'yellow': 0, 'red': 0}
#     if exist('coins'):
#         color_dict = load('coins')
    
#     plusOneAnimBlue = pyganim.loadAnim('../img/anims/plusOne/blue',0.05)
#     plusOneAnimYellow = pyganim.loadAnim('../img/anims/plusOne/yellow',0.05)
#     plusOneAnimRed = pyganim.loadAnim('../img/anims/plusOne/red',0.05)
    
#     plusOneAnim_dict = {'blue':plusOneAnimBlue, 'yellow':plusOneAnimYellow, 'red':plusOneAnimRed}

#     exitAnim = pyganim.loadAnim('../img/anims/exit', 0.1,True)
#     exitAnim.play()

#     lightFill = {'fill':255}

def randomColor():
    return random.choice(["blue","red","yellow"])

def updateShadow(shad,player,surf_lighting,frame_number,backgroundScreen,surf_falloff,camera,lightFill):
    # shad.set_light_position(to_pygame(camera.apply(Rect(player.positionX + 32, player.positionY, 0, 0)), backgroundScreen))
    shad.set_light_position(camera.apply(Rect(player.rect.x + 30, player.rect.y + 30, 0, 0)))
    mask,draw_pos = shad.get_mask_and_position(False)
    mask.blit(surf_falloff,(0,0),special_flags=BLEND_MULT)
    if frame_number % 10 == 0 and lightFill['fill'] > 0 and not player.sunPowering:
        lightFill['fill'] -= 1
    surf_lighting.fill((lightFill['fill'],lightFill['fill'],lightFill['fill']))
    surf_lighting.blit(mask,draw_pos,special_flags=BLEND_MAX)
    backgroundScreen.blit(surf_lighting,(0,0),special_flags=BLEND_MULT)

# LAUNCH GAME SCREEN
def launchGame(width,height,backgroundScreen,dt,screen,clock,fps,levelInd):

    font = pygame.font.SysFont("Impact", 24)
    scoreBar = pygame.image.load("../img/hud/scoreBar.png").convert()
    nextColorIcon = pygame.image.load("../img/hud/nextColor23.png").convert()
    lifeHud = pygame.image.load("../img/hud/life.png")

    color_dict = {'blue': 0, 'yellow': 0, 'red': 0}
    if exist('coins'):
        color_dict = load('coins')
    
    plusOneAnimBlue = pyganim.loadAnim('../img/anims/plusOne/blue',0.05)
    plusOneAnimYellow = pyganim.loadAnim('../img/anims/plusOne/yellow',0.05)
    plusOneAnimRed = pyganim.loadAnim('../img/anims/plusOne/red',0.05)
    
    plusOneAnim_dict = {'blue':plusOneAnimBlue, 'yellow':plusOneAnimYellow, 'red':plusOneAnimRed}

    exitAnim = pyganim.loadAnim('../img/anims/exit', 0.1,True)
    exitAnim.play()

    lightFill = {'fill':255}


    level = Level(backgroundScreen,levelInd)
    camera = Camera(height, width, level.background.get_size()[1])
    running = True
    retry = False
    frame_number = 0
    anims = []
    bgSurface = pygame.Surface(level.background.get_size())


    surf_lighting = pygame.Surface(screen.get_size())
    shad = shadow.Shadow()
    shad.set_radius(200.0)
    surf_falloff = pygame.image.load("../img/light_falloff100.png").convert()


    # Music load
    #pygame.mixer.music.load("../sounds/music.mp3")
    #pygame.mixer.music.play(-1)

    # Player
    player = Player()

    # Level blocks constrution
    blocksPos = level.blocks
    
    # Spawning enemies
    enemies = level.enemies
    # enemies = []
    


    # GAME LOOP
    while running:
        if not retry:
            # keyboard events
            events = pygame.event.get() # try to change to getkeys (-> faster ?)
            for event in events:
                if event.type == QUIT: 
                    #running = False
                    exit()
                elif event.type == KEYDOWN:
                    # if event.key in [K_p,K_ESCAPE]:    
                    #     pauseScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                    if event.key == K_TAB:
                        retry = True
            
            # draw background
            backgroundScreen.blit(level.background,camera.apply(Rect(0, 0, 0, 0)))
            
            # Update blocks
            for b in level.blocks:
                b.update(player,color_dict,plusOneAnim_dict,backgroundScreen,camera,dt)#,blockimg,False)
            # Update enemies
            for e in enemies:
                e.update(dt, backgroundScreen, camera, player, level.blocks)
            # Shadow
            # updateShadow(shad,player,surf_lighting,frame_number,backgroundScreen,surf_falloff,camera,lightFill)
            
            # player update
            player.update(backgroundScreen,level.blocks,camera,dt,enemies,color_dict,frame_number)
            
            # TODO manage death
            if player.lives == 0:
                retry = True
            # level end
            # if distance((player.positionX + 32,player.positionY - 32),(level.exitPos[0] + 20,level.exitPos[1]-20)) < 50:
            #     retry = True

            


            # exit anim
            # exitAnim.blit(backgroundScreen,to_pygame(camera.apply(Rect(level.exitPos[0], level.exitPos[1], 0, 0)), backgroundScreen))
            




            # Display bottom bar
            backgroundScreen.blit(scoreBar, (0,600))
            backgroundScreen.blit(font.render(str(color_dict["blue"]), 1, THECOLORS["white"]), (15,605))
            backgroundScreen.blit(nextColorIcon, to_pygame((35,35), backgroundScreen), (0, 30, 50, 30))
            backgroundScreen.blit(font.render(str(color_dict["yellow"]), 1, THECOLORS["white"]), (100,605))
            backgroundScreen.blit(nextColorIcon, to_pygame((120,35), backgroundScreen), (0, 90, 50, 30))
            backgroundScreen.blit(font.render(str(color_dict["red"]), 1, THECOLORS["white"]), (185,605))
            backgroundScreen.blit(nextColorIcon, to_pygame((205,35), backgroundScreen), (0, 120, 50, 30))
            for i in range(player.lives):
                backgroundScreen.blit(lifeHud, (385+i*40,605))

            # update camera
            camera.update((player.rect.x, player.rect.y, 0, 0))


            

            

        # Display objects
        #draw(backgroundScreen,space)
        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        
        # Update game mechanics
        frame_number += 1
        # space.step(dt)
        clock.tick(fps)

        # quit level ## TODO quit screen, fading...
        if retry:
            # draw background
            # backgroundScreen.blit(level.background,to_pygame(camera.apply(Rect(0, level.background.get_size()[1], 0, 0)), backgroundScreen))
            backgroundScreen.blit(level.background,camera.apply(Rect(0, level.background.get_size()[1], 0, 0)))
            # backgroundScreen.blit(level.background,(Rect(0, level.background.get_size()[1],0,0)))
            # pygame.mixer.music.stop()

            time.sleep(1)
            running = False

    save([('coins',color_dict)])
