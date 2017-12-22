# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import numpy as np
from Directives import *

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
    integratorElement = element.find('integrator')
    type = integratorElement.attrib.get('type')

    integrator = Integrator(type)
    
    integrator.params = extractParams(integratorElement)
    
    return integrator

def loadSensor(scene):
    np.set_printoptions(suppress=True)
    
    sensorElement = scene.find('sensor')
    type = sensorElement.attrib.get('type')

    sensor = Sensor()

    # transform setup
    name = sensorElement.find('transform').get('name')
    sensor.transform = Transform(name)
    
    matrixElement = sensorElement.find('transform').find('matrix')
    if matrixElement is not None:
        matrix = matrixElement.get('value')
        sensor.transform.matrix = map(float, matrix.strip().split(' '))
        sensor.transform.matrix = [sensor.transform.matrix[i:i + 4] for i in xrange(0, len(sensor.transform.matrix), 4)]
    else:
        #search for lookat translate scale
        pass

    # sampler setup
    samplerElement = sensorElement.find('sampler')
    type = samplerElement.get('type')
    sensor.sampler = Sampler(type)
    sensor.sampler.params = extractParams(samplerElement)
    
    # film setup
    filmElement = sensorElement.find('film')
    type = filmElement.get('type')
    filter = filmElement.find('rfilter').get('type')
    sensor.film = Film(type, filter)

    sensor.film.params = extractParams(filmElement)
    sensor.film.params.pop('rfilter', None)
    
    # other params
    sensor.params = extractParams(sensorElement)
    sensor.params.pop('transform', None)
    sensor.params.pop('film', None)
    sensor.params.pop('sampler', None)

    return sensor

def loadMaterials(scene):
    materials = []
    
    for materialElement in scene.findall('bsdf'):
        material = extractMaterial(materialElement)
        if material is not None:
            materials.append(material)

    return materials

def loadShapes(scene):
    shapes = []
    for shapeElement in scene.findall('shape'):
        type = shapeElement.get('type')
        shape = Shape(type)
        
        # isso tem que morrer
        if type == 'sphere':
            p = shapeElement.find('point')
            if p is not None:
                shape.center = np.array([p.get('x'), p.get('y'), p.get('z')])
                
        if shapeElement.find('transform') is not None:
            name = shapeElement.find('transform').get('name')
            shape.transform = Transform(name)
            
            # checar se não são os outros tipos de transform
            matrix = shapeElement.find('transform').find('matrix').get('value')
            matrix = map(float, matrix.strip().split(' '))
            shape.transform.matrix = [matrix[i:i + 4] for i in xrange(0, len(matrix), 4)]
            
        if shapeElement.find('emitter') is not None:
            type = shapeElement.find('emitter').get('type')
            shape.emitter = Emitter(type)
            
            if shapeElement.find('emitter').find('transform') is not None:
                shape.emitter.transform = Transform()
                matrix = shapeElement.find('emitter').find('transform').find('matrix').get('value')
                matrix =  map(float, matrix.strip().split(' '))
                shape.emitter.transform.matrix = [matrix[i:i + 4] for i in xrange(0, len(matrix), 4)]
            
            shape.emitter.params = extractParams(shapeElement.find('emitter'))
            shape.emitter.params.pop('transform', None)
        
        materialElement = shapeElement.find('bsdf')
        
        if materialElement is not None:
            shape.material = extractMaterial(materialElement)

        shape.params = extractParams(shapeElement)
        shape.params.pop('transform', None)
        shape.params.pop('bsdf', None)
        shape.params.pop('emitter', None)
        
        shapes.append(shape)
        
    return shapes

def loadLights(scene):
    lights = []
    
    for emitterElement in scene.findall('emitter'):    
        type = emitterElement.get('type')
        emitter = Emitter(type)
            
        if emitterElement.find('transform') is not None:
            emitter.transform = Transform()
            matrix = emitterElement.find('transform').find('matrix').get('value')
            emitter.transform.matrix =  map(float, matrix.strip().split(' '))
            emitter.transform.matrix = [emitter.transform.matrix[i:i + 4] for i in xrange(0, len(emitter.transform.matrix), 4)]
            
        emitter.params = extractParams(emitterElement)
        emitter.params.pop('transform', None)
        
        lights.append(emitter)
    
    return lights

def extractParams(element):
    return {}

def extractMaterial(element):
    return None

def main():
    scene = readFromXML('/home/grad/lahagemann/pbr_scene_converter/test_files/mitsuba/teapot.xml')
    print 'Shapes: ' + str(len(scene.shapes))
    print 'Materials: ' + str(len(scene.materials))

if  __name__ =='__main__':main()
