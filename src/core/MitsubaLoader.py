# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import numpy as np
import core

def readFromXML(filename):
    tree = ET.parse(filename)
    element = tree.getroot()

    scene = loadScene(element)

    return scene

def loadScene(element):
    scene = Scene()

    scene.integrator = loadIntegrator(element)
    scene.sensor = loadSensor(element)
    scene.materials = loadMaterials(element)
    scene.shapes = loadShapes(element)
    scene.lights = loadLights(element)
    
    return scene

def loadIntegrator(element):
    integrator_element = element.find('integrator')
    type = integrator_element.attrib.get('type')

    integrator = Integrator(type)
    
    integrator.params = extractParams(integrator_element)
    
    return integrator

def loadSensor(scene):
    np.set_printoptions(suppress=True)
    
    sensor_element = scene.find('sensor')
    type = sensor_element.attrib.get('type')

    sensor = directives.Sensor()

    # transform setup
    name = sensor_element.find('transform').get('name')
    sensor.transform = Transform(name)
    
    matrix = sensor_element.find('transform').find('matrix').get('value')
    sensor.transform.matrix = map(float, matrix.strip().split(' '))
    sensor.transform.matrix = [sensor.transform.matrix[i:i + 4] for i in xrange(0, len(sensor.transform.matrix), 4)]

    # sampler setup
    sampler_element = sensor_element.find('sampler')
    type = sampler_element.get('type')
    sensor.sampler = Sampler(type)
    sensor.sampler.params = extractParams(sampler_element)
    
    # film setup
    film_element = sensor_element.find('film')
    type = film_element.get('type')
    filter = film_element.find('rfilter').get('type')
    sensor.film = Film(type, filter)

    sensor.film.params = extractParams(film_element)
    sensor.film.params.pop('rfilter', None)
    
    # other params
    sensor.params = extractParams(sensor_element)
    sensor.params.pop('transform', None)
    sensor.params.pop('film', None)
    sensor.params.pop('sampler', None)

    return sensor

def loadMaterials(scene):
    materials = []
    
    for material in scene.findall('bsdf'):
        mat = extractMaterial(material)
        if mat is not None:
            material_list.append(mat)

    return materials

def loadShapes(scene):
    shapes = []
    for shape in scene.findall('shape'):
        type = shape.get('type')
        s = directives.Shape()
        
        if type == 'sphere':
            p = shape.find('point')
            if p is not None:
                s.center = np.array([p.get('x'), p.get('y'), p.get('z')])
                
        s.type = type

        if shape.find('transform') is not None:
            s.transform = directives.Transform()
            s.transform.name = shape.find('transform').get('name')
            
            matrix = shape.find('transform').find('matrix').get('value')
            m = map(float, matrix.strip().split(' '))
            s.transform.matrix = [m[i:i + 4] for i in xrange(0, len(m), 4)]
            
        if shape.find('emitter') is not None:
            s.emitter = directives.Emitter()
            s.emitter.type = shape.find('emitter').get('type')
            
            if shape.find('emitter').find('transform') is not None:
                s.emitter.transform = directives.Transform()
                matrix = shape.find('emitter').find('transform').find('matrix').get('value')
                s.emitter.transform.matrix =  cp.deepcopy(map(float, matrix.strip().split(' ')))
                # formats matrix into 4x4 pattern
                s.emitter.transform.matrix = cp.deepcopy([s.emitter.transform.matrix[i:i + 4] for i in xrange(0, len(s.emitter.transform.matrix), 4)])
            
            s.emitter.params = extract_params(shape.find('emitter'))
            s.emitter.params = filter_params(s.emitter.params, 'transform')
        
        material_elem = shape.find('bsdf')
        
        if material_elem is not None:
            s.material = extract_material(material_elem)

        s.params = extract_params(shape)
        s.params = filter_params(s.params, 'transform')
        s.params = filter_params(s.params, 'bsdf')
        s.params = filter_params(s.params, 'emitter')
        
        shape_list.append(s)
        
    return shape_list

