# -*- coding: utf-8 -*-

import numpy as np

# GENERIC

class Param:
    val_type = ''    
    name = ''
    value = 0

# SCENE DIRECTIVES

class Integrator:
    int_type = ''
    params = []

class Transform:
    name = ''
    matrix = []

class Sampler:
    sampler_type = ''
    params = []

class Film:
    film_type = ''
    filter_type = ''
    params = []

class Sensor:
    sensor_type = ''
    transform = Transform()
    sampler = Sampler()
    film = Film()
    params = []

class Texture:
    name = ''
    tex_type = ''
    params = []

class WrapperTexture:
    tex_type = ''
    texture = Texture()
    
class Material:
    mat_type = ''
    mat_id = ''    
    params = []
    texture = Texture()
    
class AdapterMaterial:
    mat_type = ''
    mat_id = ''
    material = Material()

class BumpMap:
    texture = Texture()
    adapter = AdapterMaterial()

# WORLD DECLARATION
class Emitter:
    type = ''
    transform = None
    params = []
    
    def getParam(self, paramName):
        p = [x for x in self.params if not x.name != paramName]
        if len(p) == 1:
            return p[0].value
        else:
            return ''

class Shape:
    type = '' 
    center = np.array([0,0,0])
    transform = None#Transform()
    emitter = None
    material = None
    params = []

    def getRefMaterial(self):
        ref = [x for x in self.params if not x.name != 'id']
        if len(ref) == 1:
            return ref[0].value
        else:
            return ''
            
    def getFile(self):
        f = [x for x in self.params if not x.name != 'filename']
        if len(f) == 1:
            return f[0].value
        else:
            return ''
            
    def getParam(self, paramName):
        p = [x for x in self.params if not x.name != paramName]
        if len(p) == 1:
            return p[0].value
        else:
            return ''

# GLOBAL
class Scene:
    integrator = Integrator()
    sensor = Sensor()
    materials = []
    shapes = []
    lights = []
