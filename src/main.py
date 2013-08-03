"""

PyGame & PyMunk game test

modified code from platformer example


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







width, height = 800,640
fps = 60
dt = 1./fps




def main():

    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 
    
    backgroundScreen = pygame.Surface(screen.get_size())
    

    clock = pygame.time.Clock()
    running = True
    
    font = pygame.font.SysFont("Impact", 24)
    
    background = pygame.image.load("../img/bg.png")
    scoreBar = pygame.image.load("../img/scoreBar.png")
    jumpBar = pygame.image.load("../img/jumpBar.png")

    
    score = 0
    bestScore = 0
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0,-1000
    
    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 40), (790, 40), 5)
                , pymunk.Segment(space.static_body, (790, 40), (790, 630), 5)
                , pymunk.Segment(space.static_body, (790, 630), (10, 630), 5)
                , pymunk.Segment(space.static_body, (10, 630), (10, 40), 5)
                ## side ladders
                , pymunk.Segment(space.static_body, (10, 200), (100, 200), 5)
                , pymunk.Segment(space.static_body, (10, 400), (100, 400), 5)
                , pymunk.Segment(space.static_body, (790, 200), (690, 200), 5)
                , pymunk.Segment(space.static_body, (790, 400), (690, 400), 5)
                ]
    
    # colored out walls
    outWalls = [pymunk.Segment(space.static_body, (5, 35), (795, 35), 5)
                , pymunk.Segment(space.static_body, (795, 35), (795, 635), 5)
                , pymunk.Segment(space.static_body, (795, 635), (5, 635), 5)
                , pymunk.Segment(space.static_body, (5, 635), (5, 35), 5)
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
            elif event.type == KEYDOWN and event.key == K_d:
                player.feet.ignore_draw = not player.feet.ignore_draw
                player.head.ignore_draw = not player.head.ignore_draw
                player.head2.ignore_draw = not player.head2.ignore_draw    
        
        # draw background
        backgroundScreen.blit(background, (0,0))
        backgroundScreen.blit(scoreBar, (0,610))
        
        
        # player update
        player.update(space, dt, events)
    
        
        # Move the moving platform
        for b in blocks:
            b.update(dt)
            
            if b.positionY == 40:
                blocks.remove(b)
                space.remove(b.segment)
                
            elif abs((b.positionY ) - (player.positionY - 28)) < 5 and \
            b.positionX <= player.positionX and \
            (b.positionX + 100) >= player.positionX:
                print 'player on block' + b.color
                b.isCurrentBlock = True
                if player.landed_previous and b.color == currentColor:
                    score += 1
                    b.active = True
                    if score > bestScore:
                        bestScore = score
                elif player.landed_previous and b.color != currentColor:
                    score -= 1
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
        
        # randomly add one
        randCreate = randint(0,100)
        if randCreate == 5 and len(blocks) < 20:
            block = Block()
            space.add(block.segment)
            blocks.append(block)
        
        
        
        
        
        ### Draw stuff
        draw_space(backgroundScreen, space)
        
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
            backgroundScreen.blit(player.img, to_pygame(position, backgroundScreen), (animation_offset, direction_offset, 32*2, 48*2))

        backgroundScreen.blit(jumpBar, to_pygame((300,30), backgroundScreen), (0, 150 - player.remaining_jumps*30, 150, 30))


        # Did we land?
        if abs(player.grounding['impulse'].y) / player.body.mass > 30 and not player.landed_previous: 
            player.landing = {'p':player.grounding['position'],'n':5}
            player.landed_previous = True
        else:
            player.landed_previous = False
        if player.landing['n'] > 0:
            pygame.draw.circle(backgroundScreen, pygame.color.THECOLORS['yellow'], to_pygame(player.landing['p'], backgroundScreen), 5)
            player.landing['n'] -= 1
      
      
      
        # Display score
        backgroundScreen.blit(font.render("Score : " + str(score), 1, THECOLORS["white"]), (15,610))
        backgroundScreen.blit(font.render("Best : " + str(bestScore), 1, THECOLORS["white"]), (150,610))
        
        # Display objects
        screen.blit(backgroundScreen,(0,0))
        pygame.display.flip()
        
        frame_number += 1
        
        ### Update physics
        space.step(dt)

        clock.tick(fps)

if __name__ == '__main__':
    sys.exit(main())
