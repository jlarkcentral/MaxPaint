'''
Created on Aug 7, 2013

@author: primo

from
http://stackoverflow.com/questions/14354171/how-to-add-scrolling-to-a-platformer-in-pygame

'''
from pygame import Rect

class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, -8640, width, height)

    def apply(self, rect):
        return rect.move(self.state.topleft)

    def update(self, rect):
        self.state = self.complex_camera(self.state, rect)

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect    
        _, _, w, h = camera
        l, t, _, _ = l, -t+320, w, h
    
        l = min(0, l)                           # stop scrolling at the left edge
        l = max((camera.width-800), l)   # stop scrolling at the right edge
    
        t = min((camera.height), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)