'''
level

'''
import sys

import pygame

from block import Block
from enemy import Enemy

class Level(object):

	def __init__(self,backgroundScreen,index):
		
		self.index = index
		self.blocks = []
		self.enemies = []
		self.exitPosDict = dict({1:(50,1200),2:(700,1200),3:(400,1250)})
		self.exitPos = self.exitPosDict[index]
		self.background_img = pygame.image.load("../img/backgrounds/levelBackgrounds/lvl"+str(index)+".jpg").convert()
		self.background = pygame.transform.scale(self.background_img, (800, 3200))
		self.loadLevel(backgroundScreen)


	def loadLevel(self,backgroundScreen):
		with open('gameObjects/levels/'+str(self.index)+'/staticblocks') as f:
			i = 31
			for line in f:
				blocksTemp = line.split(',')
				currentY = i * 100
				j = 0
				for elem in blocksTemp:
					currentX = j * 100
					if elem[0] == '1':
						self.blocks.append(Block(backgroundScreen,currentX,currentY))
					j += 1
				i -= 1

		with open('gameObjects/levels/'+str(self.index)+'/enemies') as f:
			for line in f:
				enemyTemp = line.split(',')
				enemyPath = []
				for i in range(0,len(enemyTemp)-1,2):
					enemyPath.append((int(enemyTemp[i+1])*100,int(enemyTemp[i])*100+36))
					enemyPath.append((int(enemyTemp[i+1])*100 + 60,int(enemyTemp[i])*100+36))
				self.enemies.append(Enemy([enemyPath[0],enemyPath[-1]],int(enemyTemp[-1])))

		with open('gameObjects/levels/'+str(self.index)+'/movingBlocks') as f:
			for line in f:
				mvBlocksTemp = line.split((','))
				path = []
				for i in range(0,len(mvBlocksTemp)-1,2):
					path.append((int(mvBlocksTemp[i])*100,int(mvBlocksTemp[i+1])*100))
				#print(path)
				moving = 1 if mvBlocksTemp[0] == mvBlocksTemp[2] else -1
				self.blocks.append(Block(backgroundScreen,int(mvBlocksTemp[0])*100,int(mvBlocksTemp[1])*100,moving,path))