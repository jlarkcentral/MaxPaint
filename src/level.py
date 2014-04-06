'''
level

'''

import pygame
import random
from block import Block
from enemy import Enemy
import utils

class Level(object):

	def __init__(self,index):
		self.index = index
		self.blocks = []
		self.enemies = []
		self.background = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl.jpg").convert()
		self.background_alpha = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl"+str(index)+"_alpha.png").convert_alpha()
		self.loadLevel()

	def loadLevel(self):
		with open('../levels/'+str(self.index)+'/levelmatrix') as f:
			i = 1
			for line in f:
				blocksTemp = line.split(',')
				currentY = i * 100
				j = 0
				for elem in blocksTemp:
					currentX = j * 100
					if elem == '1':
						self.blocks.append(Block(currentX,currentY))
					elif elem == '2':
						self.blocks.append(Block(currentX,currentY))
						self.enemies.append(Enemy([(currentX+18,currentY+40)],random.randint(2,5)))
					j += 1
				i += 1
		self.question = utils.getQuestion(self.index)
		self.answers = utils.getAnswers(self.index)
