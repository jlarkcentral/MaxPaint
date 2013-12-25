"""

PyGame & PyMunk game test

modified code from platformer example

Game launcher

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
from player import Player
from camera import Camera

sys.path.append('screens/')
import pauseScreen



# INITIALIZATION & CONTENT LOADING
def gameScreenInit(width_,height_,space_,cameraHeight):
    global width
    global height
    global space
    global camera

    width = width_
    height = height_
    space = space_

    camera = Camera(height, width, cameraHeight)
    static_body = pymunk.Body()
    static_lines = [pymunk.Segment(static_body, (0, 0), (0, height), 0.0),
                    pymunk.Segment(static_body, (width, 0), (width, height), 0.0)
                    #pymunk.Segment(static_body, (0, 50), (width, 50), 20.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

def loadResources():
    global font
    global background
    global scoreBar
    global jumpBar
    global nextColorIcon
    global lifeHud
    global color_dict
    global plusOneAnim_dict
    
    font = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl1.png").convert()
    scoreBar = pygame.image.load("../img/hud/scoreBar.png").convert()
    nextColorIcon = pygame.image.load("../img/hud/nextColor23.png").convert()
    lifeHud = pygame.image.load("../img/hud/life.png")
    color_dict = {'blue': 0, 'yellow': 0, 'red': 0}
    
    # TODO modif pyganim to load directly entire anim
    plusOneAnimBlue = pyganim.PygAnimation([('../img/anims/plusOne/plusOneBlue7.png', 0.05),
                                        ('../img/anims/plusOne/plusOneBlue6.png', 0.05),
                                        ('../img/anims/plusOne/plusOneBlue5.png', 0.05),
                                        ('../img/anims/plusOne/plusOneBlue4.png', 0.05),
                                        ('../img/anims/plusOne/plusOneBlue3.png', 0.05),
                                        ('../img/anims/plusOne/plusOneBlue2.png', 0.05),
                                        ('../img/anims/plusOne/plusOneBlue1.png', 0.05)])
    plusOneAnimBlue.loop = False
    
    plusOneAnimYellow = pyganim.PygAnimation([('../img/anims/plusOne/plusOneYellow7.png', 0.05),
                                        ('../img/anims/plusOne/plusOneYellow6.png', 0.05),
                                        ('../img/anims/plusOne/plusOneYellow5.png', 0.05),
                                        ('../img/anims/plusOne/plusOneYellow4.png', 0.05),
                                        ('../img/anims/plusOne/plusOneYellow3.png', 0.05),
                                        ('../img/anims/plusOne/plusOneYellow2.png', 0.05),
                                        ('../img/anims/plusOne/plusOneYellow1.png', 0.05)])
    plusOneAnimYellow.loop = False
    
    plusOneAnimRed = pyganim.PygAnimation([('../img/anims/plusOne/plusOneRed7.png', 0.05),
                                        ('../img/anims/plusOne/plusOneRed6.png', 0.05),
                                        ('../img/anims/plusOne/plusOneRed5.png', 0.05),
                                        ('../img/anims/plusOne/plusOneRed4.png', 0.05),
                                        ('../img/anims/plusOne/plusOneRed3.png', 0.05),
                                        ('../img/anims/plusOne/plusOneRed2.png', 0.05),
                                        ('../img/anims/plusOne/plusOneRed1.png', 0.05)])
    plusOneAnimRed.loop = False
    
    plusOneAnim_dict = {'blue':plusOneAnimBlue, 'yellow':plusOneAnimYellow, 'red':plusOneAnimRed}



def randomColor():
    return random.choice(["blue","red","yellow"])


# LAUNCH GAME SCREEN
def launchGame(width,height,space,backgroundScreen,dt,screen,clock,fps,level):
    
    loadResources()
    gameScreenInit(width,height,space,background.get_size()[1])
    running = True
    retry = False
    frame_number = 0
    anims = []

    bgSurface = pygame.Surface(background.get_size())

    # Music load
    pygame.mixer.music.load("../sounds/music.mp3")
    #pygame.mixer.music.play(-1)

    # Player
    player = Player()
    space.add(player.body, player.hitbox)

    # Level blocks constrution
    blocksPos = level.blocks
    for b in level.blocks:
        space.add(b.hitbox)
    
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
                #running = False
                exit()
            elif event.type == KEYDOWN:
                if event.key in [K_p,K_ESCAPE]:    
                    pauseScreen.show(width,height,space,backgroundScreen,dt,screen,clock,fps)
                elif event.key == K_TAB:
                    retry = True
        
        # draw background
        backgroundScreen.blit(background,to_pygame(camera.apply(Rect(0, background.get_size()[1], 0, 0)), backgroundScreen))
        

        # player update
        player.update(space, dt, events, color_dict, backgroundScreen, camera, enemies)
        
        # TODO manage death
        if player.lives == 0:
            retry = True

        # Update platforms
        for b in level.blocks:
            if abs((b.positionY ) - (player.positionY - 58)) < 5 and \
            b.positionX - 64 + 20 <= player.positionX and \
            (b.positionX + 100 - 20) >= player.positionX:
                if b.active == False and b.color in ['red','blue','yellow']:
                    b.active = True
                    color_dict[b.color] += 1
                    anim = plusOneAnim_dict[b.color].getCopy()
                    anim.play()
                    anims.append((anim, (b.positionX,640-(camera.state.y + b.positionY + 50))))
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen), (0, b.active*50, 100, 50))
            
        
        # Update enemies
        for e in enemies:
            e.update(dt, backgroundScreen, camera, player)
            backgroundScreen.blit(e.img, to_pygame(camera.apply(Rect(e.positionX-70, e.positionY+100, 0, 0)), backgroundScreen))

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
        backgroundScreen.blit(font.render(str(color_dict["yellow"]), 1, THECOLORS["white"]), (100,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((120,35), backgroundScreen), (0, 3*30, 50, 30))
        backgroundScreen.blit(font.render(str(color_dict["red"]), 1, THECOLORS["white"]), (185,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((205,35), backgroundScreen), (0, 4*30, 50, 30))
        
        for i in range(player.lives):
            backgroundScreen.blit(lifeHud, (385+i*40,605))

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
            running = False
            pygame.mixer.music.stop()