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
		self.exitPosDict = dict({1:(50,1200),2:(700,1200),3:(400,1250)})
		self.exitPos = self.exitPosDict[index]
		self.background_img = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl"+str(index)+".jpg").convert()

		self.background = pygame.transform.scale(self.background_img, (800, 3200))
		self.loadLevel()

	def loadLevel(self):
		with open('../levels/'+str(self.index)+'/staticblocks') as f:
			i = 1
			for line in f:
				blocksTemp = line.split(',')
				currentY = i * 100
				j = 0
				for elem in blocksTemp:
					currentX = j * 100
					if elem[0] == '1':
						self.blocks.append(Block(currentX,currentY))
					j += 1
				i += 1

		# with open('../levels/'+str(self.index)+'/enemies') as f:
		# 	for line in f:
		# 		enemyTemp = line.split(',')
		# 		enemyPath = []
		# 		for i in range(0,len(enemyTemp)-1,2):
		# 			enemyPath.append((int(enemyTemp[i+1])*100,int(enemyTemp[i])*100+36))
		# 			enemyPath.append((int(enemyTemp[i+1])*100 + 60,int(enemyTemp[i])*100+36))
		# 		self.enemies.append(Enemy([enemyPath[0],enemyPath[-1]],int(enemyTemp[-1])))


		for i in range(25):
			pathlength = random.randint(3,6)
			path = [((random.randint(0,8))*100, (i+random.randint(0,3))*100) for _ in range(pathlength)]
			speed = random.randint(1,5)
			self.enemies.append(Enemy(path,speed))