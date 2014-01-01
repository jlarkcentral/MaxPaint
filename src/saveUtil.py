'''
Save util


'''
import shelve

def save(objectList):
	shelfFile = shelve.open('savegame')
	for name,obj in objectList:
		shelfFile[name] = obj
	shelfFile.close()

def exist(name):
	shelfFile = shelve.open('savegame')
	return (name in shelfFile)

def load(name):
	shelfFile = shelve.open('savegame')
	obj = shelfFile[name]
	shelfFile.close()
	return obj