'''
level

'''

import pygame
import random
from block import Block
from enemy import Enemy

class Level(object):

	def __init__(self,index):
		self.index = index
		self.blocks = []
		self.enemies = []
		# self.exitPosDict = dict({1:(50,1200),2:(700,1200),3:(400,1250)})
		# self.exitPos = self.exitPosDict[index]
		self.background_img = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl"+str(index)+".jpg").convert()

		self.background = pygame.transform.scale(self.background_img, (800, 3200))
		



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
