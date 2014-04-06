"""

PyGame game test

Game launcher

"""

import sys
import random
import math
import pygame
from pygame.locals import *
from pygame.color import *
from pygame import K_ESCAPE
sys.path.append('../lib/pyganim/')
import pyganim

sys.path.append('gameObjects/')
from player import Player
from camera import Camera
from level import Level
from screen_ import Screen_
from fragment import Fragment
from utils import save,load,exist,to_pygame


class GameScreen(Screen_):
    
    def __init__(self,levelInd):
        super(GameScreen, self).__init__()
        self.fadeScreen = pygame.image.load("../img/backgrounds/blackscreen.png").convert()
        self.font = pygame.font.SysFont("Handy00", 20)
        self.nextColorIcon = pygame.image.load("../img/hud/nextColor23.png").convert_alpha()
        self.progressIcon = pygame.image.load("../img/hud/progress.png").convert_alpha()
        self.timebar = pygame.image.load("../img/hud/timebar.png").convert_alpha()
        self.shieldbar = pygame.image.load("../img/hud/shieldbar.png").convert_alpha()
        self.lifebar_ = pygame.image.load("../img/hud/lifebar_.png").convert()

        self.level = Level(levelInd)
        self.camera = Camera(640, 800, 3200)
        # running = True
        self.retry = False
        self.frame_number = 0
        self.anims = []

        self.stopDelay = 0
        self.stopped = False

        self.killFragments = []
        self.dust = []

        self.starting = True
        self.ending = False
        self.alpha = 255


        # Music load
        # pygame.mixer.music.load("../sounds/piano.wav")
        # pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        # Player
        self.player = Player()
        self.fire = Rect((0,3200),(800,5))
        self.playerDown = False



        


    def killFragmentsUpdate(self):
        for kf in self.killFragments:
            kf.update()
            if kf.kill:
                self.killFragments.remove(kf)


        

    def render(self, backgroundScreen):
        # draw background
        backgroundScreen.blit(self.level.background,(0, 0))
        for d in self.dust:
            backgroundScreen.fill(d.color,d.rect)
        backgroundScreen.blit(self.level.background_alpha,(0,self.camera.apply(Rect(0, 0, 0, 0))[1]/2))


        for e in self.level.enemies:
            e.render(backgroundScreen, self.camera)
        if not self.player.killed:
            self.player.render(backgroundScreen, self.camera)

        for b in self.level.blocks:
            b.render(backgroundScreen,self.camera)

        # Display bottom bar
        backgroundScreen.fill(THECOLORS['black'],Rect((0,600),(800,40)))
        backgroundScreen.blit(self.nextColorIcon, to_pygame((35,35), backgroundScreen), (0, 30, 50, 30))
        backgroundScreen.blit(self.font.render(str(self.player.timePower), 1, (170,174,48)), (50,607))
        backgroundScreen.blit(self.progressIcon, to_pygame((35,5), backgroundScreen), (0, 10, self.player.timePowerCount*10, 10))

        backgroundScreen.blit(self.nextColorIcon, to_pygame((120,35), backgroundScreen), (0, 60, 50, 30))
        backgroundScreen.blit(self.font.render(str(self.player.mines), 1, (131,43,93)), (135,607))
        backgroundScreen.blit(self.progressIcon, to_pygame((120,5), backgroundScreen), (0, 20, self.player.minesCount*10, 10))        

        backgroundScreen.blit(self.nextColorIcon, to_pygame((205,35), backgroundScreen), (0, 0, 50, 30))
        backgroundScreen.blit(self.font.render(str(self.player.shields), 1, (8,108,110)), (220,607))
        backgroundScreen.blit(self.progressIcon, to_pygame((205,5), backgroundScreen), (0, 0, self.player.shieldsCount*10, 10))
        
        backgroundScreen.blit(self.lifebar_, to_pygame((400,40), backgroundScreen))
        if self.player.slomoDelay > 0:
            backgroundScreen.blit(self.timebar, to_pygame((404,31), backgroundScreen), (0, 0, (math.ceil(self.player.slomoDelay*2/20)*20), 22))
        elif self.player.shieldDelay > 0:
            backgroundScreen.blit(self.shieldbar, to_pygame((404,31), backgroundScreen), (0, 0, (math.ceil(self.player.shieldDelay*2/20)*20), 22))


        if self.player.killed:
            for kf in self.killFragments:
                kf.render(backgroundScreen,self.camera)

        # backgroundScreen.blit(self.laserImg, self.camera.apply(self.fire))
        if self.starting:
            self.fadeScreen.set_alpha(self.alpha)
            backgroundScreen.blit(self.fadeScreen,(0,0))
            if self.alpha < 0:
                self.starting = False
                self.alpha = 0
            self.alpha -= 10
        if self.ending:
            # pygame.mixer.music.set_volume(1-self.alpha/255)
            self.fadeScreen.set_alpha(self.alpha)
            backgroundScreen.blit(self.fadeScreen,(0,0))
            if self.alpha > 255:
                self.stopped = True
            self.alpha += 10

        if self.player.finished:
            self.fadeScreen.set_alpha(self.alpha)
            backgroundScreen.blit(self.fadeScreen,(0,0))
            if self.alpha > 255:
                self.stopped = True
            self.alpha += 10
            self.player.render(backgroundScreen, self.camera)
            if self.confirmFinished:
                backgroundScreen.blit(self.font.render("What's your name ?",1,THECOLORS['white']),(500,200))
                backgroundScreen.blit(self.font.render("This is none of your business",1,THECOLORS['white']),(100,300))
                backgroundScreen.blit(self.font.render("Who are YOU ?",1,THECOLORS['white']),(100,400))
                backgroundScreen.blit(self.font.render("I don't remember",1,THECOLORS['white']),(100,500))


    def handle_events(self,events):
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.manager.go_to('levelSelectScreen')
        if self.player.finished:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:



    def update(self):
        # Update blocks
        for b in self.level.blocks:
            b.update(self.player)

        # Update enemies
        for e in self.level.enemies:
            e.update( self.player, self.level.blocks)
            if e.hit:
                self.level.enemies.remove(e)

        # player update
        if not self.player.killed:
            self.player.update(self.level.blocks,self.level.enemies,self.frame_number)
        else:
            if not self.stopped:
                # for _ in range(random.randint(20,40)):
                #     self.killFragments.append(Fragment(self.player.rect.center,THECOLORS['white']))
                # self.stopDelay = 50
                self.stopped = True
                self.ending = True
            else:
                # self.stopDelay -= 1
                # if self.stopDelay == 0:
                    # save([('coins',[self.player.mines,self.player.shields,self.player.timePower])])
                self.manager.go_to_game(self.level.index)
        
        
        self.camera.update((self.player.rect.x, self.player.rect.y, 0, 0))
        self.killFragmentsUpdate()


        if self.player.rect.y + 64 > abs(self.camera.state.y-600):
            self.player.killed = True
        if self.player.killed and not self.playerDown:
            # self.player.hitSound.play()
            self.playerDown = True

        if random.randint(0,10) == 5:
            s = random.randint(2,10)
            self.dust.append(Dust(Rect(random.randint(200,600),700,s,s)))
        if self.player.slomoDelay > 0:
            for d in self.dust:
                d.update(d.speed/5)
        else:
            for d in self.dust:
               d.update(d.speed)



class Dust(object):
    def __init__(self,rect):
        self.rect = rect
        self.color = THECOLORS[random.choice(['grey75','grey59','grey42'])]
        self.speed = random.randint(1,5)
    def update(self, speed):
        self.rect.y -= speed
