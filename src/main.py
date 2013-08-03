"""

PyGame & PyMunk game test

modified code from platformer example

img
http://untamed.wild-refuge.net/rmxpresources.php?characters

"""

from random import randint

import sys,math

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

from block import *
from player import *







width, height = 800,600
fps = 60
dt = 1./fps




def main():

    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 

    clock = pygame.time.Clock()
    running = True
    
    font = pygame.font.SysFont("Impact", 24)
    img = pygame.image.load("../img/robot.png")
    #background = pygame.image.load("../img/bg.png")

    
    score = 0
    bestScore = 0
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0,-1000
    
    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 10), (790, 10), 5)
                , pymunk.Segment(space.static_body, (790, 10), (790, 590), 5)
                , pymunk.Segment(space.static_body, (790, 590), (10, 590), 5)
                , pymunk.Segment(space.static_body, (10, 590), (10, 10), 5)
                ## side ladders
                , pymunk.Segment(space.static_body, (10, 200), (100, 200), 5)
                , pymunk.Segment(space.static_body, (10, 400), (100, 400), 5)
                , pymunk.Segment(space.static_body, (790, 200), (690, 200), 5)
                , pymunk.Segment(space.static_body, (790, 400), (690, 400), 5)
                ]
    
    # colored out walls
    outWalls = [pymunk.Segment(space.static_body, (5, 5), (795, 5), 5)
                , pymunk.Segment(space.static_body, (795, 5), (795, 595), 5)
                , pymunk.Segment(space.static_body, (795, 595), (5, 595), 5)
                , pymunk.Segment(space.static_body, (5, 595), (5, 5), 5)
                ]
    
    for w in outWalls:
        w.color = pygame.color.THECOLORS['black']
    
    
    
    for s in static + outWalls:
        s.friction = 1.
        s.group = 1
    space.add(static + outWalls)
    
    blocks = []
    block = Block()
    space.add(block.segment)
    blocks.append(block)
    
    
    
    # player
    player = Player()
    space.add(player.body, player.head, player.feet, player.head2)
    
    frame_number = 0
    
    currentColor = "black"
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
        
        # background
        #screen.blit(background,(0,0))
        
        # player update
        player.update(space, dt, events)
    
        
        # Move the moving platform
        for b in blocks:
            b.update(dt)
            
            if b.positionY == 0:
                blocks.remove(b)
                space.remove(b.segment)
                
            elif abs((b.positionY ) - (player.positionY - 28)) < 5 and \
            b.positionX <= player.positionX and \
            (b.positionX + 100) >= player.positionX:
                print 'player on block' + b.color
                b.isCurrentBlock = True
                if player.landed_previous and b.color == currentColor:
                    score += 1
                    if score > bestScore:
                        bestScore = score
                elif player.landed_previous and b.color != currentColor:
                    score -= 1
                    
        if player.landed_previous and player.positionY < 25:
            score = 0
        
        # randomly add one
        randCreate = randint(0,100)
        if randCreate == 5 and len(blocks) < 20:
            block = Block()
            space.add(block.segment)
            blocks.append(block)
        
        if player.landed_previous:
            randColorIndex = randint(0,3)
            if(randColorIndex == 0):
                currentColor = "blue"
            elif(randColorIndex == 1):
                currentColor = "red"
            elif(randColorIndex == 2):
                currentColor = "yellow"
            elif(randColorIndex == 3):
                currentColor = "green"
            else:
                print 'bad color index !'
            for w in outWalls:
                w.color = pygame.color.THECOLORS[currentColor]
        
        
        
        ### Clear screen
        screen.fill(pygame.color.THECOLORS["black"])
        
        ### Draw stuff
        draw_space(screen, space)
        
        ### Character anim
        if player.feet.ignore_draw:
            direction_offset = 48*2+(1*player.direction+1)/2 * 48 * 2
            if player.grounding['body'] != None and abs(player.target_vx) > 1:
                animation_offset = 32 * 2 *(frame_number / 8 % 4)
            elif player.grounding['body'] is None:
                animation_offset = 32*1 * 2
            else:
                animation_offset = 32*0
            position = player.body.position +(-16*2,28*2 + 16)
            screen.blit(img, to_pygame(position, screen), (animation_offset, direction_offset, 32*2, 48*2))

        # Did we land?
        if abs(player.grounding['impulse'].y) / player.body.mass > 30 and not player.landed_previous: 
            player.landing = {'p':player.grounding['position'],'n':5}
            player.landed_previous = True
        else:
            player.landed_previous = False
        if player.landing['n'] > 0:
            pygame.draw.circle(screen, pygame.color.THECOLORS['yellow'], to_pygame(player.landing['p'], screen), 5)
            player.landing['n'] -= 1
      
      
      
        # Display score
        screen.blit(font.render("Score : " + str(score), 1, THECOLORS["white"]), (15,12))
        screen.blit(font.render("Best : " + str(bestScore), 1, THECOLORS["white"]), (15,42))
        
        
        
        
        pygame.display.flip()
        frame_number += 1
        
        ### Update physics
        space.step(dt)
        
        
        clock.tick(fps)

if __name__ == '__main__':
    sys.exit(main())
