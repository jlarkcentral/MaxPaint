"""

PyGame & PyMunk game test

modified code from platformer example


"""

import random
from random import randint

import sys

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

sys.path.append('../lib/')
import pyganim

sys.path.append('gameObjects/')
from block import Block
from player import Player
from camera import Camera
from enemy import Enemy
from level import Level

sys.path.append('screens/')
import pauseScreen



# INITIALIZATION & CONTENT LOADING


def gameScreenInit(width_,height_,space_):
    global width
    global height
    global space
    global camera

    width = width_
    height = height_
    space = space_

    cameraHeight = 8640
    camera = Camera(width, cameraHeight)
    static_body = pymunk.Body()
    static_lines = [pymunk.Segment(static_body, (0, 0), (0, height), 0.0)
                    ,pymunk.Segment(static_body, (width, 0), (width, width), 0.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

def loadResources():
    global font
    global background
    global scoreBar
    global jumpBar
    global currentColorIcon
    global nextColorIcon
    global color_dict
    global plusOneAnim_dict
    
    font = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/backgrounds/bg.png").convert()
    scoreBar = pygame.image.load("../img/hud/scoreBar.png").convert()
    jumpBar = pygame.image.load("../img/hud/jumpBar.png").convert()
    currentColorIcon = pygame.image.load("../img/hud/nextColor1.png").convert()
    nextColorIcon = pygame.image.load("../img/hud/nextColor23.png").convert()
    color_dict = {'blue': 0, 'yellow': 0, 'red': 0}
    
    #plusOneAnimGreen = pyganim.PygAnimation([('../img/anims/plusOneGreen7.png', 0.05),
    #                                    ('../img/anims/plusOneGreen6.png', 0.05),
    #                                    ('../img/anims/plusOneGreen5.png', 0.05),
    #                                    ('../img/anims/plusOneGreen4.png', 0.05),
    #                                    ('../img/anims/plusOneGreen3.png', 0.05),
    #                                    ('../img/anims/plusOneGreen2.png', 0.05),
    #                                    ('../img/anims/plusOneGreen1.png', 0.05)])
    #plusOneAnimGreen.loop = False
    
    plusOneAnimBlue = pyganim.PygAnimation([('../img/anims/plusOneBlue7.png', 0.05),
                                        ('../img/anims/plusOneBlue6.png', 0.05),
                                        ('../img/anims/plusOneBlue5.png', 0.05),
                                        ('../img/anims/plusOneBlue4.png', 0.05),
                                        ('../img/anims/plusOneBlue3.png', 0.05),
                                        ('../img/anims/plusOneBlue2.png', 0.05),
                                        ('../img/anims/plusOneBlue1.png', 0.05)])
    plusOneAnimBlue.loop = False
    
    plusOneAnimYellow = pyganim.PygAnimation([('../img/anims/plusOneYellow7.png', 0.05),
                                        ('../img/anims/plusOneYellow6.png', 0.05),
                                        ('../img/anims/plusOneYellow5.png', 0.05),
                                        ('../img/anims/plusOneYellow4.png', 0.05),
                                        ('../img/anims/plusOneYellow3.png', 0.05),
                                        ('../img/anims/plusOneYellow2.png', 0.05),
                                        ('../img/anims/plusOneYellow1.png', 0.05)])
    plusOneAnimYellow.loop = False
    
    plusOneAnimRed = pyganim.PygAnimation([('../img/anims/plusOneRed7.png', 0.05),
                                        ('../img/anims/plusOneRed6.png', 0.05),
                                        ('../img/anims/plusOneRed5.png', 0.05),
                                        ('../img/anims/plusOneRed4.png', 0.05),
                                        ('../img/anims/plusOneRed3.png', 0.05),
                                        ('../img/anims/plusOneRed2.png', 0.05),
                                        ('../img/anims/plusOneRed1.png', 0.05)])
    plusOneAnimRed.loop = False
    
    plusOneAnim_dict = {'blue':plusOneAnimBlue, 'yellow':plusOneAnimYellow, 'red':plusOneAnimRed}



def randomColor():
    return random.choice(["blue","red","yellow"])


def showPauseMenu(backgroundScreen):
    pauseBackground = pygame.image.load("../img/backgrounds/pauseBG.png").convert()
    backgroundScreen.blit(pauseBackground,(200,200))






# LAUNCH GAME SCREEN


def launchGame(width,height,space,backgroundScreen,dt,screen,clock,fps):
    
    gameScreenInit(width,height,space)
    loadResources()
    running = True
    pause = False
    retry = False
    frame_number = 0
    anims = []

    
    # Player
    player = Player()
    space.add(player.body, player.hitbox)


    # Level choice
    level = Level(1)


    # Level blocks constrution
    blocks = []
    blocksPos = level.blocks
    for x,y,l in blocksPos:
        b = Block(x,y,l)
        space.add(b.hitbox)
        blocks.append(b)
    

    # Spawning enemies
    enemies = level.enemies
    for e in enemies:
        space.add(e.body,e.hitbox)
    
    

    # GAME LOOP
    while running:

        # keyboard events
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT: 
                running = False
            elif event.type == KEYDOWN:
                if event.key in [K_p,K_ESCAPE]:    
                    pauseScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)

                elif event.key == K_TAB:
                    retry = True
                    running = False
        
        # draw background
        backgroundScreen.blit(background, (0,0))
        
        # player update
        player.update(space, dt, events, color_dict, backgroundScreen, camera, enemies)
        
        if color_dict["yellow"] < 0:
            retry = True

        # Update platforms
        for b in blocks:
            if abs((b.positionY ) - (player.positionY - 58)) < 5 and \
            b.positionX - 64 + 20 <= player.positionX and \
            (b.positionX + 100 - 20) >= player.positionX:
                if b.active == False:
                    b.active = True
                    color_dict[b.color] += 1
                    anim = plusOneAnim_dict[b.color].getCopy()
                    anim.play()
                    anims.append((anim, (b.positionX,640-(camera.state.y + b.positionY + 50))))
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen), (0, b.active*50, 100, 50))
            
        
        # Update enemies
        for e in enemies:
            e.update(dt)
            e.updateBullets(dt, backgroundScreen, camera, player.positionX, player.positionY, color_dict)
            backgroundScreen.blit(e.img, to_pygame(camera.apply(Rect(e.positionX, e.positionY, 0, 0)), backgroundScreen))
            if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((e.positionX + 20,e.positionY-20)) < 50 :
                retry = True
                running = False
                backgroundScreen.fill(pygame.color.THECOLORS['red'])
            if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((e.positionX + 20,e.positionY-20)) < 250 \
            and e.shootingDelay == 0:
                e.shootAtTarget((player.positionX + 32,player.positionY - 32))
                e.shootingDelay = 30
            if e.shootingDelay > 0:
                e.shootingDelay -= 1

        # show anims
        for anim,pos in anims:
            if anim.isFinished():
                anims.remove((anim,pos))
            else:
                anim.blit(backgroundScreen, pos)

        # Character anim
        direction_offset = 32*2+(1*player.direction+1)/2 * 32 * 2
        if abs(player.target_vx) > 1: #player.grounding['body'] != None and 
            animation_offset = 32 * 2 *(frame_number / 8 % 4)
        elif player.grounding['body'] is None:
            animation_offset = 32*1 * 4
        else:
            animation_offset = 32*0
        posX, posY = player.body.position # +(-16*2*0,-10)
        backgroundScreen.blit(player.img, to_pygame(camera.apply(Rect(posX ,posY, 0, 0)), backgroundScreen) , (animation_offset, direction_offset, 32*2, 32*2))
        
        
        # Display bottom bar
        backgroundScreen.blit(scoreBar, (0,600))
        
        
        # Display color pick ups
        backgroundScreen.blit(font.render(str(color_dict["blue"]), 1, THECOLORS["white"]), (15,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((35,35), backgroundScreen), (0, 30, 50, 30))
        #backgroundScreen.blit(font.render(str(color_dict["green"]), 1, THECOLORS["white"]), (100,605))
        #backgroundScreen.blit(nextColorIcon, to_pygame((120,35), backgroundScreen), (0, 2*30, 50, 30))
        backgroundScreen.blit(font.render(str(color_dict["yellow"]), 1, THECOLORS["white"]), (100,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((120,35), backgroundScreen), (0, 3*30, 50, 30))
        backgroundScreen.blit(font.render(str(color_dict["red"]), 1, THECOLORS["white"]), (185,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((205,35), backgroundScreen), (0, 4*30, 50, 30))
        

        # update camera
        camera.update((player.positionX, player.body.position.y + 28*2 + 16, 32, 48))
            
        # Display objects
        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        
        # Update game mechanics
        frame_number += 1
        space.step(dt)
        clock.tick(fps)

        if retry:
            space.remove(player.body)
            space.remove(player.hitbox)
            launchGame(width,height,space,backgroundScreen,dt,screen,clock,fps)