import numpy as np

# general directives

class Param:
	def __init__(self, type, name, value):
		self.type = type
		self.name = name
		self.value = value

# scene directives

class Integrator:
	def __init__(self, type = 'path'):
		self.type = type
		self.params = {}

class Transform:
	def __init__(self, name = 'toWorld'):
		self.name = name
		self.matrix = []

class Sampler:
	def __init__(self, type = 'sobol'):
		self.type = type
		self.params = {}

class Film:
	def __init__(self, type = 'ldrfilm', filter = ''):
		self.type = type
		self.filter = filter
		self.params = {}

class Sensor:
	def __init__(self, type = 'perspective'):
		self.type = type
		self.transform = Transform()
		self.sampler = Sampler()
		self.film = Film()
		self.params = {}

# world components

class Texture:
	def __init__(self, name, type):
		self.name = name
		self.type = type
		self.params = {}

class Material:
	def __init__(self, type, id):
		self.type = type
		self.id = id
		self.texture = None
		self.params = {}

class BumpMap:
	def __init__(self):
		self.texture = None
		self.material = Material('', '')
		self.params = {}

class Emitter:
	def __init__(self, type):
		self.type = type
		self.transform = Transform()
		self.params = {}

class Shape:
	def __init__(self, type):
		self.type = type
		self.emitter = Emitter('')
		self.material = Material('', '')
		self.params = {}

# global

class Scene:
	def __init__(self):
		self.integrator = Integrator()
		self.sensor = Sensor()
		self.materials = []
		self.shapes = []
		self.lights = []
		self.mediums = []

