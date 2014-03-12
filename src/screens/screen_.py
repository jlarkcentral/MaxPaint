"""
base class for every screen
"""

class Screen_(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        pass

    def handle_events(self, events):
        raise NotImplementedError