"""

PyGame game test

modified code from platformer example

Game launcher

"""

import sys
import pygame
from pygame.locals import *
from pygame.color import *
from pygame import K_ESCAPE
sys.path.append('../lib/pyganim/')
import pyganim
sys.path.append('../lib/')
import PAdLib.shadow as shadow

sys.path.append('gameObjects/')
from player import Player
from camera import Camera
from level import Level
from screen_ import Screen_
from utils import save,load,exist,to_pygame


class GameScreen(Screen_):
    
    def __init__(self,levelInd):
        super(GameScreen, self).__init__()
        self.font = pygame.font.SysFont("Impact", 20)
        self.scoreBar = pygame.image.load("../img/hud/scoreBar.png")
        self.nextColorIcon = pygame.image.load("../img/hud/nextColor23.png")
        # self.lifeHud = pygame.image.load("../img/hud/life.png")
        self.lifebar = pygame.image.load("../img/hud/lifebar.png")
        self.lifebar_ = pygame.image.load("../img/hud/lifebar_.png")
        self.exitAnim = pyganim.loadAnim('../img/anims/exit', 0.1,True)
        self.exitAnim.play()
        self.lightFill = {'fill':255}

        self.level = Level(levelInd)
        self.camera = Camera(640, 800, self.level.background.get_size()[1])
        # running = True
        self.retry = False
        self.frame_number = 0
        self.anims = []
        self.bgSurface = pygame.Surface(self.level.background.get_size())


        # self.surf_lighting = pygame.Surface(screen.get_size())
        # self.shad = shadow.Shadow()
        # self.shad.set_radius(200.0)
        # self.surf_falloff = pygame.image.load("../img/light_falloff100.png").convert()


        # Music load
        #pygame.mixer.music.load("../sounds/music.mp3")
        #pygame.mixer.music.play(-1)

        # Player
        self.player = Player()


        self.background_alpha = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl1_alpha_2.png").convert_alpha()
        self.background_deg = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl1_trees.png").convert()

        if exist('coins'):
            self.coins = load('coins')
            self.player.mines = self.coins[0]
            self.player.shields = self.coins[1]
            self.player.sunPower = self.coins[2]

        # # Level blocks constrution
        # self.blocks = level.blocks

        # # Spawning enemies
        # self.enemies = level.enemies



# def updateShadow(shad,player,surf_lighting,frame_number,backgroundScreen,surf_falloff,camera,lightFill):
#     # shad.set_light_position(to_pygame(camera.apply(Rect(player.positionX + 32, player.positionY, 0, 0)), backgroundScreen))
#     shad.set_light_position(camera.apply(Rect(player.rect.x + 30, player.rect.y + 30, 0, 0)))
#     mask,draw_pos = shad.get_mask_and_position(False)
#     mask.blit(surf_falloff,(0,0),special_flags=BLEND_MULT)
#     if frame_number % 10 == 0 and lightFill['fill'] > 0 and not player.sunPowering:
#         lightFill['fill'] -= 1
#     surf_lighting.fill((lightFill['fill'],lightFill['fill'],lightFill['fill']))
#     surf_lighting.blit(mask,draw_pos,special_flags=BLEND_MAX)
#     backgroundScreen.blit(surf_lighting,(0,0),special_flags=BLEND_MULT)

    def render(self, backgroundScreen):
        # draw background
        # backgroundScreen.blit(self.level.background,self.camera.apply(Rect(0, 0, 0, 0)))
        backgroundScreen.blit(self.background_deg,(0, 0))
        backgroundScreen.blit(self.background_alpha,(0,self.camera.apply(Rect(0, 0, 0, 0))[1]/2))

        for b in self.level.blocks:
            b.render(backgroundScreen,self.camera)

        for e in self.level.enemies:
            e.render(backgroundScreen, self.camera)

        self.player.render(backgroundScreen, self.camera)

        # Display bottom bar
        backgroundScreen.blit(self.scoreBar, (0,600))
        backgroundScreen.blit(self.nextColorIcon, to_pygame((35,35), backgroundScreen), (0, 0, 50, 30))
        backgroundScreen.blit(self.font.render(str(self.player.shields), 1, (8,108,110)), (50,606))
        backgroundScreen.blit(self.nextColorIcon, to_pygame((120,35), backgroundScreen), (0, 30, 50, 30))
        backgroundScreen.blit(self.font.render(str(self.player.sunPower), 1, (170,174,48)), (135,606))
        backgroundScreen.blit(self.nextColorIcon, to_pygame((205,35), backgroundScreen), (0, 60, 50, 30))
        backgroundScreen.blit(self.font.render(str(self.player.mines), 1, (131,43,93)), (220,606))
        # for i in range(self.player.lives):
        #     backgroundScreen.blit(self.lifeHud, (385+i*40,605))
        backgroundScreen.blit(self.lifebar_, to_pygame((400,40), backgroundScreen))
        backgroundScreen.blit(self.lifebar, to_pygame((404,31), backgroundScreen), (0, 0, self.player.life*2, 22))
        
        

    def handle_events(self,events):
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    save(self.coins)
                    self.manager.go_to('levelSelectScreen')


    def update(self):
        # Update blocks
        for b in self.level.blocks:
            b.update(self.player)#,blockimg,False)
        # Update enemies
        for e in self.level.enemies:
            e.update( self.player, self.level.blocks)
            if e.hit:
                self.level.enemies.remove(e)
        # Shadow
        # updateShadow(shad,player,surf_lighting,frame_number,backgroundScreen,surf_falloff,camera,lightFill)

        # player update
        self.player.update(self.level.blocks,self.level.enemies,self.frame_number)

        # TODO manage death
        if self.player.life == 0:
            self.manager.go_to('levelSelectScreen')
        self.camera.update((self.player.rect.x, self.player.rect.y, 0, 0))
