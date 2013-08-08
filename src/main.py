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
    color_dict = {'blue': 1, 'green': 2, 'yellow': 3, 'red': 4}

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
    
    score = 0
    bestScore = 0
    frame_number = 0
    
    
    # box walls
    static = [
                pymunk.Segment(space.static_body, (800, 40), (800, 640), 10)
                , pymunk.Segment(space.static_body, (0, 640), (0, 40), 10)
                ]
    
    for s in static :
        s.friction = 1.
        s.group = 1
    space.add(static)
    
    
    blocks = []
    blocksPos = [(0,100,100),(100,100,100),(200,100,100),
                 (600,300,100),(700,300,100),
                 (300,500,100),(400,500,100),
                 (200,700,100),
                 (300,900,100),
                 (600,800,100),(700,800,100),
                 (650,1000,100),
                 (750,1200,100),
                 (400,1300,100),(500,1300,100),
                 (300,1500,100),(400,1500,100),
                 (-50,1800,100),(-50,1850,100),(-50,1900,100),
                 (100,2100,100),(400,2100,100),
                 (600,2300,100),(700,2300,100),
                 (200,2500,100),(300,2500,100),
                 (100,2700,100),(0,2900,100),
                 (100,3000,100),(200,3000,100),(300,3000,100),(400,3000,100),(500,3000,100),(600,3000,100),(700,3000,100),
                 ]
    
    for x,y,l in blocksPos:
        b = Block(x,y,l)
        space.add(b.segment)
        blocks.append(b)
    
    # player
    player = Player()
    space.add(player.body, player.head, player.feet, player.head2)
    
    
    
    currentColor = randomColor()
    currentColor2 = randomColor()
    currentColor3 = randomColor()

    
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
            score = 0
            player.remaining_jumps = 4000
        if player.positionY > 8640:
            player.body.position = player.positionX, 8640
            score = 0
            player.remaining_jumps = 4000
        
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
                    #score = 0
                    if score > 0:
                        score -= 1
        
            backgroundScreen.blit(b.img, to_pygame(camera.apply(Rect(b.positionX, b.positionY, 0, 0)), backgroundScreen), (0, b.active*50, 100, 50))
            #backgroundScreen.blit(font.render(b.color + " block there", 1, THECOLORS["black"]), (b.positionX, 640-(camera.state.y + b.positionY)))

            
            
        # randomly add one
        #if blockCreationDelay == 0 and len(blocks) < 5:
        #    block = Block(camera.state.y)
        #    space.add(block.segment)
        #    blocks.append(block)
        #    previousBlockPosition = block.positionX
        #    blockCreationDelay = randint(10,150)
        #elif blockCreationDelay == 0 and len(blocks) == 5:
        #    blockCreationDelay = 0
        #else:
        #    blockCreationDelay -= 1
        
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

            posX, posY = player.body.position +(-16*2,40)
            backgroundScreen.blit(player.img, to_pygame(camera.apply(Rect(posX ,posY, 0, 0)), backgroundScreen) , (animation_offset, direction_offset, 32*2, 32*2))
            
        


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
        
        #backgroundScreen.blit(font.render("Player here", 1, THECOLORS["black"]), (player.positionX,640-(camera.state.y + player.positionY)))
        
        camera.update((player.positionX, player.body.position.y + 28*2 + 16, 32, 48))
        
        # Display objects
        screen.blit(backgroundScreen,(0,0))
        
        pygame.display.flip()
        
        frame_number += 1
        
        
        ### Update physics
        space.step(dt)

        clock.tick(fps)




if __name__ == '__main__':
    sys.exit(main())
