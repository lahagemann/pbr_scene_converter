# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import numpy as np
from Directives import *

class MitsubaLoader:

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
            shape.transform = extractTransform(shapeElement)
                
            if shapeElement.find('emitter') is not None:
                type = shapeElement.find('emitter').get('type')
                shape.emitter = Emitter(type)
                shape.emitter.transform = extractTransform(shapeElement.find('emitter'))
                
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
            emitter.transform = extractTransform(emitterElement)
                
            emitter.params = extractParams(emitterElement)
            emitter.params.pop('transform', None)
            
            lights.append(emitter)
        
        return lights

    def extractParams(element):
        params = {}

        for attribute in element:
            type = attribute.tag
            if type == 'ref':
                name = 'id'
            else:
                name = attribute.attrib.get('name')

            if type == 'point' or type == 'vector':
                value = np.array([attribute.attrib.get('x'), attribute.attrib.get('y'), attribute.attrib.get('z')])
            elif type == 'rgb':
                value = attribute.attrib.get('value').split(',')
                [x.strip() for x in value]
            else:
                value = attribute.attrib.get('value')

            param = Param(type, name, value)
            params[name] = param

        return params

    def extractMaterial(materialElement):
        materialType = materialElement.get('type')
        if materialType == 'bumpmap':
            bumpmap = BumpMap()

            textureElement = materialElement.find('texture')

            if textureElement is not None:
                name = textureElement.attrib.get('name')
                type = textureElement.attrib.get('type')
                
                bumpmap.texture = Texture(name, type)
                bumpmap.texture.params = extractParams(textureElement)

            else:
                bumpmap.texture = None

            # extract material

            # check for nested material within material element
            nestedMaterialElement = materialElement.find('bsdf')

            # has nested material: pick inner
            if nestedMaterialElement is not None:
                matType = nestedMaterialElement.attrib.get('type')
                matId = materialElement.attrib.get('id')
                material = Material(matType, matId)

                textureElement = nestedMaterialElement.find('texture')

                if textureElement is not None:
                    name = textureElement.attrib.get('name')
                    type = textureElement.attrib.get('type')
                
                    material.texture = Texture(name, type)
                    material.texture.params = extractParams(textureElement)

                else:
                    material.texture = None

                # get other material parameters
                material.params = extractParams(nestedMaterialElement)
                material.params.pop('texture', None)

                bumpmap.material = material

            # just pick the material
            else:
                matType = materialElement.attrib.get('type')
                matId = materialElement.attrib.get('id')
                material = Material(matType, matId)

                textureElement = materialElement.find('texture')

                if textureElement is not None:
                    name = textureElement.attrib.get('name')
                    type = textureElement.attrib.get('type')
                
                    material.texture = Texture(name, type)
                    material.texture.params = extractParams(textureElement)

                else:
                    material.texture = None

                # get other material parameters
                material.params = extractParams(materialElement)
                material.params.pop('texture', None)

                bumpmap.material = material

            return bumpmap

        else:
            # check for nested material within material element
            nestedMaterialElement = materialElement.find('bsdf')

            # has nested material: pick inner
            if nestedMaterialElement is not None:
                matType = nestedMaterialElement.attrib.get('type')
                matId = materialElement.attrib.get('id')
                material = Material(matType, matId)

                textureElement = nestedMaterialElement.find('texture')

                if textureElement is not None:
                    name = textureElement.attrib.get('name')
                    type = textureElement.attrib.get('type')
                
                    material.texture = Texture(name, type)
                    material.texture.params = extractParams(textureElement)

                else:
                    material.texture = None

                # get other material parameters
                material.params = extractParams(nestedMaterialElement)
                material.params.pop('texture', None)

            # just pick the material
            else:
                matType = materialElement.attrib.get('type')
                matId = materialElement.attrib.get('id')
                material = Material(matType, matId)

                textureElement = materialElement.find('texture')

                if textureElement is not None:
                    name = textureElement.attrib.get('name')
                    type = textureElement.attrib.get('type')
                
                    material.texture = Texture(name, type)
                    material.texture.params = extractParams(textureElement)

                else:
                    material.texture = None

                # get other material parameters
                material.params = extractParams(materialElement)
                material.params.pop('texture', None)
            
            return material

    def extractTransform(element):
        transform = None

        if element.find('transform') is not None:
            transformElement = element.find('transform')
            name = transformElement.get('name')
            transform = Transform(name)

            if transformElement.find('matrix') is not None:
                matrix = transformElement.find('matrix').get('value')
                matrix =  map(float, matrix.strip().split(' '))
                transform.matrix = [matrix[i:i + 4] for i in xrange(0, len(matrix), 4)]

            else:
                # extract other elements
                pass

        return transform

    def __init__(filename):
        self.scene = readFromXML(filename)