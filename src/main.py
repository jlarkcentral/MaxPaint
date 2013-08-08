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
    
    font = pygame.font.SysFont("Impact", 24)
    background = pygame.image.load("../img/bg.png")
    scoreBar = pygame.image.load("../img/scoreBar.png")
    jumpBar = pygame.image.load("../img/jumpBar.png")
    currentColorIcon = pygame.image.load("../img/nextColor1.png")
    nextColorIcon = pygame.image.load("../img/nextColor23.png")
    color_dict = {'blue': 0, 'green': 0, 'yellow': 0, 'red': 0}

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

    loadResources()
    loadPhysics()
    
    frame_number = 0
    
    
    blocks = []
    blocksPos = [(0,100,1),(100,100,1),(200,100,1),
                 (600,300,2),(700,300,2),
                 (300,500,1),(400,500,1),
                 (200,700,3),
                 (300,900,2),
                 (600,800,1),(700,800,1),
                 (650,1000,0),
                 (750,1200,0),
                 (400,1300,1),(500,1300,2),
                 (300,1500,3),(400,1500,3),
                 (-50,1800,2),
                 (100,2100,1),(400,2100,1),
                 (600,2300,0),(700,2300,0),
                 (200,2500,2),(300,2500,2),
                 (100,2700,1),(0,2900,1),
                 (100,3000,0),(200,3000,0),(300,3000,0),(400,3000,0),(500,3000,0),(600,3000,0),(700,3000,0),
                 ]
    
    for x,y,l in blocksPos:
        b = Block(x,y,l)
        space.add(b.segment)
        blocks.append(b)
    
    enemies = [
               Enemy([(600,340),(760,340)], 1),
               Enemy([(300,540),(460,540)], 1),
               Enemy([(200,740),(260,740)], 1),
               Enemy([(300,940),(360,940)], 1),
               ]
    
    # player
    player = Player()
    space.add(player.body, player.head, player.feet, player.head2)


    while running:
        
        #print "player" + str(player.positionY)
        
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            elif event.type == KEYDOWN and event.key == K_d:
                player.feet.ignore_draw = not player.feet.ignore_draw
                player.head.ignore_draw = not player.head.ignore_draw
                player.head2.ignore_draw = not player.head2.ignore_draw    
        
        # draw background
        backgroundScreen.blit(background, (0,0))
       
        
        # player update
        player.update(space, dt, events)
        if player.positionY < 40:
            player.body.position = player.positionX, 40
        if player.positionX < 16:
            player.body.position = 16, player.positionY
        if player.positionX > 770:
            player.body.position = 770, player.positionY
        
        
        # Update platforms
        for b in blocks:
            if b.positionY <= 40:
                blocks.remove(b)
                space.remove(b.segment)
            elif abs((b.positionY ) - (player.positionY - 28)) < 5 and \
            b.positionX <= player.positionX and \
            (b.positionX + 100) >= player.positionX:
                if b.active == False:
                    b.active = True
                    color_dict[b.color] += 1
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen), (0, b.active*50, 100, 50))

        # Update enemies
        for e in enemies:
            e.update(dt)
            backgroundScreen.blit(e.img, to_pygame(camera.apply(Rect(e.positionX, e.positionY, 0, 0)), backgroundScreen))
        
        ### Draw stuff
        draw_space(backgroundScreen, space)
        
        ### Character anim
        if player.feet.ignore_draw:
            direction_offset = 32*2+(1*player.direction+1)/2 * 32 * 2
            if player.grounding['body'] != None and abs(player.target_vx) > 1:
                animation_offset = 32 * 2 *(frame_number / 8 % 4)
            elif player.grounding['body'] is None:
                animation_offset = 32*1 * 2
            else:
                animation_offset = 32*0

            posX, posY = player.body.position +(-16*2,35)
            backgroundScreen.blit(player.img, to_pygame(camera.apply(Rect(posX ,posY, 0, 0)), backgroundScreen) , (animation_offset, direction_offset, 32*2, 32*2))
      
        
        # Display bottom bar
        backgroundScreen.blit(scoreBar, (0,600))
        
        # Display jump state
        backgroundScreen.blit(jumpBar, to_pygame((400,35), backgroundScreen), (0, 150 - player.remaining_jumps*30, 150, 30))
        
        # Display color pick ups
        backgroundScreen.blit(font.render(str(color_dict["blue"]), 1, THECOLORS["white"]), (15,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((30,35), backgroundScreen), (0, 30, 50, 30))
        
        backgroundScreen.blit(font.render(str(color_dict["green"]), 1, THECOLORS["white"]), (100,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((115,35), backgroundScreen), (0, 2*30, 50, 30))
        
        backgroundScreen.blit(font.render(str(color_dict["yellow"]), 1, THECOLORS["white"]), (185,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((200,35), backgroundScreen), (0, 3*30, 50, 30))
        
        backgroundScreen.blit(font.render(str(color_dict["red"]), 1, THECOLORS["white"]), (270,605))
        backgroundScreen.blit(nextColorIcon, to_pygame((285,35), backgroundScreen), (0, 4*30, 50, 30))
        
        
        camera.update((player.positionX, player.body.position.y + 28*2 + 16, 32, 48))
        
        # Display objects
        screen.blit(backgroundScreen,(0,0))
        
        pygame.display.flip()
        frame_number += 1
        
        # Update game mechanics
        space.step(dt)
        clock.tick(fps)




if __name__ == '__main__':
    sys.exit(main())
