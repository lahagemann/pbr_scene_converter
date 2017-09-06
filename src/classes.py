# -*- coding: utf-8 -*-

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

class Material:
    mat_type = ''
    mat_id = ''
    adapter = False
    params = []
    texture = Texture()

# WORLD DECLARATION

    


