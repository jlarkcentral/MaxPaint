"""

game objects base class

"""

class GameObject_(object):
	def __init__(self):
		pass

	def render(self, screen, camera=None):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError