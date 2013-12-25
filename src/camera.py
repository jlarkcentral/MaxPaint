'''
Created on Aug 7, 2013


from
http://stackoverflow.com/questions/14354171/how-to-add-scrolling-to-a-platformer-in-pygame

'''
from pygame import Rect

class Camera(object):
    def __init__(self, screen_h, width, height):
        self.state = Rect(0, height, width, height)
        self.maxH = height
        self.screen_height = screen_h

    def apply(self, rect):
        return rect.move(self.state.topleft)

    def update(self, rect):
        self.state = self.complex_camera(self.state, rect)

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect    
        _, _, w, h = camera
        l, t, _, _ = l, -t+(self.screen_height/2), w, h

        # stop scrolling at the left edge
        l = min(0, l)
        # stop scrolling at the right edge 
        l = max(0, l)
        # stop scrolling at the bottom
        t = max(-(camera.height-self.screen_height), t)
        # stop scrolling at the top
        t = min(0, t)
        
        return Rect(l, t, w, h)