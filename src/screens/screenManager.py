"""

screen manager
"""

from startScreen import StartScreen
from optionsScreen import OptionsScreen
from mainMenuScreen import MainMenuScreen
from levelSelectScreen import LevelSelectScreen
from gameScreen import GameScreen

class ScreenManager(object):
    def __init__(self):
        self.screen = StartScreen()
        self.screen.manager = self

    def go_to(self, screen):
        if screen == 'levelSelectScreen':
	        self.screen = LevelSelectScreen()
        elif screen == 'mainMenuScreen':
        	self.screen = MainMenuScreen()
        elif screen == 'optionsScreen':
        	self.screen = OptionsScreen()
        elif screen == 'startScreen':
        	self.screen = StartScreen()
        self.screen.manager = self

    def go_to_game(self,index):
        self.screen = GameScreen(index)
        self.screen.manager = self