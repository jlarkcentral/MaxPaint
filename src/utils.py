'''
Utils
'''

import pygame
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