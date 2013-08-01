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

def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)

def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)



width, height = 800,600
fps = 60
dt = 1./fps
PLAYER_VELOCITY = 100. *2.
PLAYER_GROUND_ACCEL_TIME = 0.05
PLAYER_GROUND_ACCEL = (PLAYER_VELOCITY/PLAYER_GROUND_ACCEL_TIME)

PLAYER_AIR_ACCEL_TIME = 0.25
PLAYER_AIR_ACCEL = (PLAYER_VELOCITY/PLAYER_AIR_ACCEL_TIME)

JUMP_HEIGHT = 16.*3
JUMP_BOOST_HEIGHT = 24.
JUMP_CUTOFF_VELOCITY = 100
FALL_VELOCITY = 250.

JUMP_LENIENCY = 0.05

HEAD_FRICTION = 0.7

PLATFORM_SPEED = 1

def main():

    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 

    clock = pygame.time.Clock()
    running = True
    img = pygame.image.load("xmasgirl1.png")
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0,-1000
    
    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 10), (790, 10), 5)
                , pymunk.Segment(space.static_body, (790, 10), (790, 590), 5)
                , pymunk.Segment(space.static_body, (790, 590), (10, 590), 5)
                , pymunk.Segment(space.static_body, (10, 590), (10, 10), 5)
                ]
    #static[1].color = pygame.color.THECOLORS['red']
    #static[2].color = pygame.color.THECOLORS['green']
    #static[3].color = pygame.color.THECOLORS['red']
    
    
    for s in static:
        s.friction = 1.
        s.group = 1
    space.add(static)
    
    blocks = []
    block = Block()    
    space.add(block.segment)
    blocks.append(block)
    
    def passthrough_handler(space, arbiter):
        if arbiter.shapes[0].body.velocity.y < 0:
            return True
        else:
            return False
            
    space.add_collision_handler(1,2, begin=passthrough_handler)
    
    
    # player
    body = pymunk.Body(50, pymunk.inf)
    body.position = 100,100
    
    
    head = pymunk.Circle(body, 10, (0,5))
    head2 = pymunk.Circle(body, 10, (0,13))
    feet = pymunk.Circle(body, 10, (0,-5))

    head.layers = head2.layers = 0b1000
    feet.collision_type = 1
    feet.ignore_draw = head.ignore_draw = head2.ignore_draw = True
    
    space.add(body, head, feet,head2)
    direction = 1
    remaining_jumps = 2
    landing = {'p':Vec2d.zero(), 'n':0}
    frame_number = 0
    
    landed_previous = False
    
    while running:
        
        grounding = {
            'normal' : Vec2d.zero(),
            'penetration' : Vec2d.zero(),
            'impulse' : Vec2d.zero(),
            'position' : Vec2d.zero(),
            'body' : None
        }
        # find out if player is standing on ground
        
                
        def f(arbiter):
            n = -arbiter.contacts[0].normal
            if n.y > grounding['normal'].y:
                grounding['normal'] = n
                grounding['penetration'] = -arbiter.contacts[0].distance
                grounding['body'] = arbiter.shapes[1].body
                grounding['impulse'] = arbiter.total_impulse
                grounding['position'] = arbiter.contacts[0].position
        body.each_arbiter(f)
            
        well_grounded = False
        if grounding['body'] != None and abs(grounding['normal'].x/grounding['normal'].y) < feet.friction:
            well_grounded = True
            remaining_jumps = 2
    
        ground_velocity = Vec2d.zero()
        if well_grounded:
            ground_velocity = grounding['body'].velocity
    
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            elif event.type == KEYDOWN and event.key == K_UP:
                if well_grounded or remaining_jumps > 0:                    
                    jump_v = math.sqrt(2.0 * JUMP_HEIGHT * abs(space.gravity.y))
                    body.velocity.y = ground_velocity.y + jump_v;
                    remaining_jumps -=1
            elif event.type == KEYUP and event.key == K_UP:                
                body.velocity.y = min(body.velocity.y, JUMP_CUTOFF_VELOCITY)
                
        # Target horizontal velocity of player
        target_vx = 0
        
        if body.velocity.x > .01:
            direction = 1
        elif body.velocity.x < -.01:
            direction = -1
        
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT]):
            direction = -1
            target_vx -= PLAYER_VELOCITY
        if (keys[K_RIGHT]):
            direction = 1
            target_vx += PLAYER_VELOCITY
        if (keys[K_DOWN]):
            direction = -3
            
        feet.surface_velocity = target_vx,0

        
        if grounding['body'] != None:
            feet.friction = -PLAYER_GROUND_ACCEL/space.gravity.y
            head.friciton = HEAD_FRICTION
        else:
            feet.friction,head.friction = 0,0
        
        # Air control
        if grounding['body'] == None:
            body.velocity.x = cpflerpconst(body.velocity.x, target_vx + ground_velocity.x, PLAYER_AIR_ACCEL*dt)
        
        body.velocity.y = max(body.velocity.y, -FALL_VELOCITY) # clamp upwards as well?
        
        # Move the moving platform
        for b in blocks:
            destination = b.path[b.path_index]
            current = Vec2d(b.body.position)
            distance = current.get_distance(destination)
            if distance < PLATFORM_SPEED:
                b.path_index += 1
                b.path_index = b.path_index % len(b.path)
                t = 1
            else:
                t = PLATFORM_SPEED / distance
            new = current.interpolate_to(destination, t)
            b.body.position = new
            b.body.velocity = (new - current) / dt
        
        # randomly add one
        randCreate = randint(0,100)
        if randCreate == 5 and len(blocks) < 50:
            block = Block()    
            space.add(block.segment)
            blocks.append(block)
        
        ### Clear screen
        screen.fill(pygame.color.THECOLORS["black"])
        
        ### Helper lines
        #for y in [50,100,150,200,250,300]:
        #    color = pygame.color.THECOLORS['darkgrey']
        #    pygame.draw.line(screen, color, (10,y), (680,y), 1)
        
        ### Draw stuff
        draw_space(screen, space)
        
        if feet.ignore_draw:
            direction_offset = 48+(1*direction+1)/2 * 48
            if grounding['body'] != None and abs(target_vx) > 1:
                animation_offset = 32 * (frame_number / 8 % 4)
            elif grounding['body'] is None:
                animation_offset = 32*1
            else:
                animation_offset = 32*0
            position = body.position +(-16,28)
            screen.blit(img, to_pygame(position, screen), (animation_offset, direction_offset, 32, 48))

        # Did we land?
        if abs(grounding['impulse'].y) / body.mass > 200 and not landed_previous:
            landing = {'p':grounding['position'],'n':5}
            landed_previous = True
        else:
            landed_previous = False
        if landing['n'] > 0:
            pygame.draw.circle(screen, pygame.color.THECOLORS['yellow'], to_pygame(landing['p'], screen), 5)
            landing['n'] -= 1
      
       
        pygame.display.flip()
        frame_number += 1
        ### Update physics
        
        space.step(dt)
        
        clock.tick(fps)

if __name__ == '__main__':
    sys.exit(main())
