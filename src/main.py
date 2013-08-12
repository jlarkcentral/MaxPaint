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

import pyganim

from block import Block
from player import Player
from camera import Camera
from enemy import Enemy


def gameInit():
    global width, height
    global screen
    global fps
    global dt
    global backgroundScreen
    global clock
    global camera
    
    width, height = 800,640
    fps = 60
    dt = 1./fps
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    backgroundScreen = pygame.Surface(screen.get_size())
    clock = pygame.time.Clock()
    camera = Camera(800, 8640)
    



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
    background = pygame.image.load("../img/bg.png").convert()
    scoreBar = pygame.image.load("../img/scoreBar.png").convert()
    jumpBar = pygame.image.load("../img/jumpBar.png").convert()
    currentColorIcon = pygame.image.load("../img/nextColor1.png").convert()
    nextColorIcon = pygame.image.load("../img/nextColor23.png").convert()
    color_dict = {'blue': 5, 'green': 5, 'yellow': 5, 'red': 5}
    
    
    
    plusOneAnimGreen = pyganim.PygAnimation([('../img/anims/plusOneGreen7.png', 0.05),
                                        ('../img/anims/plusOneGreen6.png', 0.05),
                                        ('../img/anims/plusOneGreen5.png', 0.05),
                                        ('../img/anims/plusOneGreen4.png', 0.05),
                                        ('../img/anims/plusOneGreen3.png', 0.05),
                                        ('../img/anims/plusOneGreen2.png', 0.05),
                                        ('../img/anims/plusOneGreen1.png', 0.05)])
    plusOneAnimGreen.loop = False
    
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
    
    plusOneAnim_dict = {'green':plusOneAnimGreen, 'blue':plusOneAnimBlue, 'yellow':plusOneAnimYellow, 'red':plusOneAnimRed}

def loadPhysics():
    global space
    
    space = pymunk.Space()   
    space.gravity = 0,-1000
    
    def passthrough_handler(space, arbiter):
        if arbiter.shapes[0].body.velocity.y < 0:
            return True
        else:
            return False
            
    space.add_collision_handler(1,2, begin=passthrough_handler)


def randomColor():
        return random.choice(["blue","red","yellow","green"])



#####################################################################



#####################################################################



def main():
    
    gameInit()
    running = True
    retry = False

    loadResources()
    loadPhysics()
    
    frame_number = 0
    
    static_body = pymunk.Body()
    static_lines = [pymunk.Segment(static_body, (0, 0), (0, 640), 0.0)
                    ,pymunk.Segment(static_body, (800, 0), (800, 800), 0.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)
    
    blocks = []
    blocksPos = [(0,100,0),(100,100,0),(200,100,0),(300,100,0),(400,100,0),(500,100,0),(600,100,0),(700,100,0),
                 (500,200,1),
                 (600,300,2),(700,300,2),
                 (300,400,1),(400,400,1),
                 (200,500,3),
                 (300,600,2),
                 (600,700,1),(700,700,1),
                 (650,800,0),
                 (700,900,0),
                 (400,1000,1),(500,1000,2),
                 (300,1100,3),(400,1100,3),
                 (0,1200,2),
                 (200,1300,1),(400,1300,1),
                 (600,1400,0),(700,1400,0),
                 (200,1500,2),(300,1500,2),
                 (100,1600,1),(0,1600,1),
                 (100,3000,0),(200,3000,0),(300,3000,0),(400,3000,0),(500,3000,0),(600,3000,0),(700,3000,0),
                 ]
    
    for x,y,l in blocksPos:
        b = Block(x,y,l)
        space.add(b.hitbox)
        blocks.append(b)
    
    enemies = [
               Enemy([(600,340),(760,340)], 1),
               Enemy([(300,440),(460,440)], 1),
               Enemy([(200,540),(260,540)], 1),
               Enemy([(300,640),(360,640)], 1),
               ]

    for e in enemies:
        space.add(e.body,e.hitbox)
    
    # player
    player = Player()
    space.add(player.body, player.hitbox) # player.head, player.feet, player.head2)


    anims = []

    while running:
        
        #print "player" + str(player.positionY)
        #print "green: " + str(color_dict["green"]) + " blue: " + str(color_dict["blue"]) \
        #+ " yellow: " + str(color_dict["yellow"]) + " red: " + str(color_dict["red"])
        
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            elif event.type == KEYDOWN and event.key == K_TAB:
                retry = True
                running = False
        
        # draw background
        backgroundScreen.blit(background, (0,0))
       
        
        # player update
        player.update(space, dt, events, color_dict)
        if player.positionY < 40:
            player.body.position = player.positionX, 40
        if player.positionX < 30:
            player.body.position = 30, player.positionY
        if player.positionX > 770:
            player.body.position = 770, player.positionY
        player.remaining_jumps = color_dict["green"]
        player.shots = color_dict["red"]
        player.swords = color_dict["blue"]
        
        if player.swording:
            player.swordAnim.play()
            anims.append((player.swordAnim, (player.positionX, 640-(camera.state.y + player.positionY))))
            if player.swordAnim.isFinished():
                player.swording = False
            
        
        for b in player.bullets:
            b.update(dt)
            if b.positionX == 0 or b.positionX == 800:
                player.bullets.remove(b)
            for e in enemies:
                if abs(b.positionX - e.positionX) < 10 and \
                abs( (640-(camera.state.y + b.positionY)) - (640-(camera.state.y + e.positionY)) ) < 40:
                    enemies.remove(e)
                    player.bullets.remove(b)
            
            #backgroundScreen.blit(font.render(".", 1, THECOLORS["black"]), (b.positionX,640-(camera.state.y + b.positionY + 10)))
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen))
            
                
        
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
            
        
        # show anims
        for anim,pos in anims:
            if anim.isFinished():
                anims.remove((anim,pos))
            else:
                anim.blit(backgroundScreen, pos)
        
 
        # Update enemies
        for e in enemies:
            e.update(dt)
            backgroundScreen.blit(e.img, to_pygame(camera.apply(Rect(e.positionX, e.positionY, 0, 0)), backgroundScreen))
            #print str(player.body.position.get_distance((e.positionX,e.positionY)))
            if Vec2d(player.positionX + 32,player.positionY - 32).get_distance((e.positionX + 20,e.positionY-20)) < 50 :
                retry = True
                running = False
                backgroundScreen.fill(pygame.color.THECOLORS['red'])
            
        ### Draw stuff
        #draw_space(backgroundScreen, space)
        
        ### Character anim
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
        
        # Display jump state
        #backgroundScreen.blit(jumpBar, to_pygame((400,35), backgroundScreen), (0, 150 - player.remaining_jumps*30, 150, 30))
        
        # Display color pick ups
        backgroundScreen.blit(font.render(str(color_dict["blue"]), 1, THECOLORS["white"]), (15,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((35,35), backgroundScreen), (0, 30, 50, 30))
        
        backgroundScreen.blit(font.render(str(color_dict["green"]), 1, THECOLORS["white"]), (100,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((120,35), backgroundScreen), (0, 2*30, 50, 30))
        
        backgroundScreen.blit(font.render(str(color_dict["yellow"]), 1, THECOLORS["white"]), (185,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((205,35), backgroundScreen), (0, 3*30, 50, 30))
        
        backgroundScreen.blit(font.render(str(color_dict["red"]), 1, THECOLORS["white"]), (270,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((290,35), backgroundScreen), (0, 4*30, 50, 30))
        
        
        camera.update((player.positionX, player.body.position.y + 28*2 + 16, 32, 48))
        
        # Display objects
        screen.blit(backgroundScreen,(0,0))
        
        pygame.display.flip()
        frame_number += 1
        
        # Update game mechanics
        space.step(dt)
        clock.tick(fps)

    if retry:
        main()


if __name__ == '__main__':
    sys.exit(main())
