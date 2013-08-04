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
    
    currentColorIcon = pygame.image.load("../img/nextColor1.png")
    nextColorIcon = pygame.image.load("../img/nextColor23.png")
    
    color_dict = {'blue': 1, 'green': 2, 'yellow': 3, 'red': 4}
    
    def randomColor():
        return random.choice(["blue","red","yellow","green"])
        
    score = 0
    bestScore = 0
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0,-1000
    
    # box walls
    static = [
              #pymunk.Segment(space.static_body, (10, 40), (790, 40), 5)
                pymunk.Segment(space.static_body, (800, 40), (800, 640), 10)
                , pymunk.Segment(space.static_body, (800, 640), (0, 640), 10)
                , pymunk.Segment(space.static_body, (0, 640), (0, 40), 10)
                ]
    
    ## side ladders
    side_ladders = [pymunk.Segment(space.static_body, (0, 200), (110, 200), 5)
                , pymunk.Segment(space.static_body, (0, 400), (110, 400), 5)
                , pymunk.Segment(space.static_body, (800, 200), (690, 200), 5)
                , pymunk.Segment(space.static_body, (800, 400), (690, 400), 5)
                ]
    
    # colored out walls
    #outWalls = [pymunk.Segment(space.static_body, (5, 35), (795, 35), 5)
    #            , pymunk.Segment(space.static_body, (795, 35), (795, 635), 5)
    #            , pymunk.Segment(space.static_body, (795, 635), (5, 635), 5)
    #            , pymunk.Segment(space.static_body, (5, 635), (5, 35), 5)
    #            ]
    
    for l in side_ladders:
        l.friction = 1.
        l.collision_type = 2
        l.layers = l.layers ^ 0b1000
        space.add(l)
        
    def passthrough_handler(space, arbiter):
        if arbiter.shapes[0].body.velocity.y < 0:
            return True
        else:
            return False
            
    space.add_collision_handler(1,2, begin=passthrough_handler)
    
    
    for s in static :
        s.friction = 1.
        s.group = 1
    space.add(static)
    
    
    previousBlockPosition = width/2
    
    blocks = []
    block = Block(previousBlockPosition)
    space.add(block.segment)
    blocks.append(block)
    previousBlockPosition = block.positionX
    
    blockCreationDelay = randint(60,150)
    
    # player
    player = Player()
    space.add(player.body, player.head, player.feet, player.head2)
    
    frame_number = 0
    
    
    currentColor = randomColor()
    currentColor2 = randomColor()
    currentColor3 = randomColor()
    
    #for w in outWalls:
    #    w.color = pygame.color.THECOLORS[currentColor]
    
    
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
       
        
        
        # player update
        player.update(space, dt, events)
    
        
        # Move the moving platform
        for b in blocks:
            b.update(dt)
            
            if b.positionY <= 40:
                blocks.remove(b)
                space.remove(b.segment)
                
            elif abs((b.positionY ) - (player.positionY - 28)) < 5 and \
            b.positionX <= player.positionX and \
            (b.positionX + 100) >= player.positionX:
                b.isCurrentBlock = True
                if player.landed_previous and b.color == currentColor and b.active == False:
                    score += 1
                    b.active = True
                    if score > bestScore:
                        bestScore = score
                    
                    currentColor = currentColor2
                    currentColor2 = currentColor3
                    currentColor3 = randomColor()
                        
                    #for w in outWalls:
                    #    w.color = pygame.color.THECOLORS[currentColor]
                            
                elif player.landed_previous and b.color != currentColor and b.active == False:
                    score -= 1
                    
                    currentColor = currentColor2
                    currentColor2 = currentColor3
                    currentColor3 = randomColor()
                                
                    #for w in outWalls:
                    #    w.color = pygame.color.THECOLORS[currentColor]
        
            backgroundScreen.blit(b.img, to_pygame(b.body.position + (0,10), backgroundScreen), (0, b.active*50, 100, 50))
        
        # randomly add one
        if blockCreationDelay == 0 and len(blocks) < 5:
            block = Block(previousBlockPosition)
            space.add(block.segment)
            blocks.append(block)
            previousBlockPosition = block.positionX
            blockCreationDelay = randint(10,150)
        elif blockCreationDelay == 0 and len(blocks) == 5:
            blockCreationDelay = 0
        else:
            blockCreationDelay -= 1
        
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

        


        # Did we land?
        if abs(player.grounding['impulse'].y) / player.body.mass > 30 and not player.landed_previous: 
            player.landing = {'p':player.grounding['position'],'n':5}
            player.landed_previous = True
        else:
            player.landed_previous = False
        if player.landing['n'] > 0:
            pygame.draw.circle(backgroundScreen, pygame.color.THECOLORS['yellow'], to_pygame(player.landing['p'], backgroundScreen), 5)
            player.landing['n'] -= 1
      
      
            
        backgroundScreen.blit(scoreBar, (0,600))
      
        backgroundScreen.blit(jumpBar, to_pygame((300,35), backgroundScreen), (0, 150 - player.remaining_jumps*30, 150, 30))

        backgroundScreen.blit(currentColorIcon, to_pygame((600,35), backgroundScreen), (0, color_dict[currentColor]*30, 75, 30))
        backgroundScreen.blit(nextColorIcon, to_pygame((680,35), backgroundScreen), (0, color_dict[currentColor2]*30, 50, 30))
        backgroundScreen.blit(nextColorIcon, to_pygame((730,35), backgroundScreen), (0, color_dict[currentColor3]*30, 50, 30))
      
        # Display score
        backgroundScreen.blit(font.render("Score : " + str(score), 1, THECOLORS["white"]), (15,605))
        backgroundScreen.blit(font.render("Best : " + str(bestScore), 1, THECOLORS["white"]), (150,605))
        backgroundScreen.blit(font.render("Next : ", 1, THECOLORS["white"]), (520,605))
        
        
        
        # Display objects
        screen.blit(backgroundScreen,(0,0))
        
        pygame.display.flip()
        
        frame_number += 1
        
        
        ### Update physics
        space.step(dt)

        clock.tick(fps)

if __name__ == '__main__':
    sys.exit(main())
