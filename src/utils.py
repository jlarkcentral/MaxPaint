'''
Utils
'''

import pygame
import math
from pygame.locals import *

# cycle through an array, return the new position : should be used in menus
def cycle(direc,menu,choice):
    if direc == "up":
        temp = menu[0]
        for i in range(len(menu) - 1):
            menu[i] = menu[i+1]
        menu[len(menu)-1] = temp
        choice = (choice - 1) % len(menu)
    elif direc == "down":
        temp = menu[len(menu)-1]
        for i in range(len(menu)-1,0,-1):
            menu[i] = menu[i-1]
        menu[0] = temp
        choice = (choice + 1) % len(menu)
    return choice

letterKeys = [K_a,K_b,K_c,K_d,K_e,K_f,K_g,K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_q,K_r,K_s,K_t,K_u,K_v,K_w,K_x,K_y,K_z]

def getFont(fontName, fontSize):
    return pygame.font.Font('../fonts/'+fontName+'.otf', fontSize)

# copied from pymunk
def to_pygame(p, surface):
    """Convenience method to convert pymunk coordinates to pygame surface 
    local coordinates
    """
    return int(p[0]), surface.get_height()-int(p[1])

def distance(v1,v2):
    return math.sqrt( math.pow(v2[0]-v1[0],2) + math.pow(v2[1]-v1[1],2) )

def interpolate(v1, v2, r):
        return (v1[0] + (v2[0] - v1[0])*r, v1[1] + (v2[1] - v1[1])*r)

def vect_add(v1,v2):
    return (v1[0]+v2[0],v1[1]+v2[1])

def vect_sub(v1,v2):
    return (v1[0]-v2[0],v1[1]-v2[1])

def vect_mul(v,coeff):
    return (v[0]*coeff,v[1]*coeff)

def vect_norm(v):
    return math.sqrt( math.pow(v[0],2) + math.pow(v[1],2) )