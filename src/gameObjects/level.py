import sys

from block import Block
from enemy import Enemy

class Level(object):

	def __init__(self,index):
		
		self.blocks = []
		self.enemies = []
		self.loadLevel(index)


	def loadLevel(self,index):
		with open('gameObjects/levels/'+str(index)+'/staticblocks') as f:
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

		with open('gameObjects/levels/'+str(index)+'/enemies') as f:
			for line in f:
				enemyTemp = line.split(',')
				enemyPath = []
				for i in range(0,len(enemyTemp)-1,2):
					enemyPath.append((int(enemyTemp[i+1])*100,int(enemyTemp[i])*100 + 40))
					enemyPath.append((int(enemyTemp[i+1])*100 + 60,int(enemyTemp[i])*100 + 40))
				self.enemies.append(Enemy([enemyPath[0],enemyPath[-1]],int(enemyTemp[-1])))
