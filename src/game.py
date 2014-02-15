"""

PyGame & PyMunk game test

modified code from platformer example

Game launcher

"""

import os
import sys
import time

import pygame
from pygame.locals import *
from pygame.color import *
    
# import pymunk
# from pymunk.vec2d import Vec2d
# from pymunk.pygame_util import draw, from_pygame, to_pygame

sys.path.append('../lib/pyganim/')
import pyganim
sys.path.append('../lib/')
import PAdLib.shadow as shadow

#import pgext

sys.path.append('gameObjects/')
from player import Player
from camera import Camera
from level import Level

sys.path.append('screens/')
import pauseScreen

from saveUtil import save,load,exist
from utils import to_pygame,distance


# INITIALIZATION & CONTENT LOADING
def gameScreenInit(width_,height_,cameraHeight): #space_
    global width
    global height
    # global space
    global camera

    width = width_
    height = height_
    # space = space_
    camera = Camera(height, width, cameraHeight)
    # static_body = pymunk.Body()
    # static_lines = [pymunk.Segment(static_body, (0, 0), (0, height), 0.0),
    #                 pymunk.Segment(static_body, (width, 0), (width, height), 0.0)
    #                 ]
    # for l in static_lines:
    #     l.friction = 0.5
    # space.add(static_lines)


def loadResources():
    global font
    global scoreBar
    global jumpBar
    global nextColorIcon
    global lifeHud
    global color_dict
    global plusOneAnim_dict
    global exitAnim
    global lightFill


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

def randomColor():
    return random.choice(["blue","red","yellow"])

def updateShadow(shad,player,surf_lighting,frame_number,backgroundScreen,surf_falloff):
    shad.set_light_position(to_pygame(camera.apply(Rect(player.positionX + 32, player.positionY, 0, 0)), backgroundScreen))
    mask,draw_pos = shad.get_mask_and_position(False)
    mask.blit(surf_falloff,(0,0),special_flags=BLEND_MULT)
    if frame_number % 10 == 0 and lightFill['fill'] > 0 and not player.sunPowering:
        lightFill['fill'] -= 1
    surf_lighting.fill((lightFill['fill'],lightFill['fill'],lightFill['fill']))
    surf_lighting.blit(mask,draw_pos,special_flags=BLEND_MAX)
    backgroundScreen.blit(surf_lighting,(0,0),special_flags=BLEND_MULT)

# LAUNCH GAME SCREEN
def launchGame(width,height,backgroundScreen,dt,screen,clock,fps,levelInd): # space,

    loadResources()
    level = Level(backgroundScreen,levelInd) #space,
    gameScreenInit(width,height,level.background.get_size()[1]) #space,
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
    #space.add(player.body, player.hitbox)

    # Level blocks constrution
    blocksPos = level.blocks
    # for b in level.blocks:
    #     space.add(b.hitbox)
    
    # Spawning enemies
    # enemies = level.enemies
    enemies = []
    # for e in enemies:
    #     space.add(e.body)#,e.hitbox)
    
    



    # GAME LOOP
    while running:
        if not retry:
            # keyboard events
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT: 
                    #running = False
                    exit()
                elif event.type == KEYDOWN:
                    if event.key in [K_p,K_ESCAPE]:    
                        pauseScreen.show(width,height,backgroundScreen,dt,screen,clock,fps) #space,
                    elif event.key == K_TAB:
                        retry = True
            
            # draw background
            backgroundScreen.blit(level.background,to_pygame(camera.apply(Rect(0, level.background.get_size()[1], 0, 0)), backgroundScreen))
            #backgroundScreen.fill(pygame.color.THECOLORS["white"])
            #for y in [50,100,150,200,250,300,500,600,700,800,1000,1200,-100,-500]:
            #    color = pygame.color.THECOLORS['darkgrey']
            #    pygame.draw.line(backgroundScreen, color, (0,y), (800,y), 1)

            # Update blocks
            for b in level.blocks:
                b.update(player,color_dict,plusOneAnim_dict,backgroundScreen,camera,dt)#,blockimg,False)
            # Update enemies
            # for e in enemies:
            #     e.update(dt, backgroundScreen, camera, player,False)
            # Shadow
            #updateShadow(shad,player,surf_lighting,frame_number,backgroundScreen,surf_falloff)
            
            # player update
            player.update(dt, events, color_dict, backgroundScreen, camera, enemies,frame_number,lightFill) #space, 
            # TODO manage death
            if player.lives == 0:
                retry = True
            # level end
            if distance((player.positionX + 32,player.positionY - 32),(level.exitPos[0] + 20,level.exitPos[1]-20)) < 50:
                retry = True

            


            # exit anim
            exitAnim.blit(backgroundScreen,to_pygame(camera.apply(Rect(level.exitPos[0], level.exitPos[1], 0, 0)), backgroundScreen))
            
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
            camera.update((player.positionX, player.positionY, 0, 0))


            

            

        # Display objects
        #draw(backgroundScreen,space)
        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        
        # Update game mechanics
        frame_number += 1
        #space.step(dt)
        clock.tick(fps)

        # quit level ## TODO quit screen, fading...
        if retry:
            # draw background
            backgroundScreen.blit(level.background,to_pygame(camera.apply(Rect(0, level.background.get_size()[1], 0, 0)), backgroundScreen))
            # space.remove(player.body)
            # space.remove(player.hitbox)
            # for b in level.blocks:
            #     space.remove(b.hitbox)
            # for e in enemies:
            #     space.remove(e.body)
                #space.remove(e.hitbox)
            #pygame.mixer.music.stop()

            time.sleep(1)
            running = False

    save([('coins',color_dict)])
