import numpy as np
import sys
import copy
# import xml.etree.ElementTree as ET
from lxml import etree as ET


sys.path.insert(0, 'core/')
from Directives import BumpMap

sys.path.insert(0, 'dictionaries')
from dictionaries import PBRTv3Mitsuba as pbrttm

class PBRTv3ToMitsuba:
    

    def toMitsuba(self, scene, filename):
        np.set_printoptions(suppress=True)

        self.sceneDirectivesToMitsuba(scene)
        self.worldDescriptionToMitsuba(scene)

        tree = ET.ElementTree(self.sceneElement)
        
        # tree.write(filename)
        tree.write(filename, pretty_print=True)

    def sceneDirectivesToMitsuba(self, scene):
        if scene.integrator is not None:
            if scene.integrator.type in pbrttm.integratorType:
                type = pbrttm.integratorType[scene.integrator.type]
                integrator = ET.SubElement(self.sceneElement, 'integrator', type=type)
            else:
                integrator = ET.SubElement(self.sceneElement, 'integrator')

            self.paramsToMitsuba(integrator, scene.integrator.params, pbrttm.integratorParam)

        if scene.sensor is not None:
            if scene.sensor.type in pbrttm.sensorType:
                type = pbrttm.sensorType[scene.sensor.type]
                sensor = ET.SubElement(self.sceneElement, 'sensor', type=type)
            else:
                sensor = ET.SubElement(self.sceneElement, 'sensor')

            if 'fov' in scene.sensor.params:
                if 'xresolution' in scene.sensor.film.params and 'yresolution' in scene.sensor.film.params:
                    width = float(scene.sensor.film.params['xresolution'].value)
                    height = float(scene.sensor.film.params['yresolution'].value)
                    fov = float(scene.sensor.params['fov'].value)

                    if height < width:
                        adjustedFov = fov / height * width
                        ET.SubElement(sensor, 'float', name='fov', value=str(adjustedFov))
                    else:
                        ET.SubElement(sensor, 'float', name='fov', value=str(fov))

                else:
                    width = 768
                    height = 576
                    fov = scene.sensor.params['fov'].value
                    adjustedFov = fov / height * width

                    ET.SubElement(sensor, 'float', name='fov', value=str(adjustedFov))

            self.paramsToMitsuba(sensor, scene.sensor.params, pbrttm.sensorParam)

        if scene.sensor.transform is not None:
            if scene.sensor.transform.matrix:
                matrix = ''

                # convert transform matrix to inverse transpose (PBRT default)
                m = scene.sensor.transform.matrix
                m_T = np.transpose(m)
                m_IT = np.linalg.inv(m_T)

                # left-handed x right-handed
                m_IT[0][0] = -m_IT[0][0]
                m_IT[1][0] = -m_IT[1][0]
                m_IT[2][0] = -m_IT[2][0]
                m_IT[3][0] = -m_IT[3][0]

                for i in range(0,4):
                    for j in range(0,4):
                        matrix += str(m_IT[i][j]) + ' '
                  
                transform = ET.SubElement(sensor, 'transform', name='toWorld')
                ET.SubElement(transform, 'matrix', value=matrix)

        if scene.sensor.sampler is not None:
            if scene.sensor.sampler.type in pbrttm.samplerType:
                type = pbrttm.samplerType[scene.sensor.sampler.type]
                sampler = ET.SubElement(sensor, 'sampler', type=type)
            else:
                sampler = ET.SubElement(sensor, 'sampler')
            
            self.paramsToMitsuba(sampler, scene.sensor.sampler.params, pbrttm.samplerParam)

        if scene.sensor.film is not None:
            if scene.sensor.film.type in pbrttm.filmType:
                type = pbrttm.filmType[scene.sensor.film.type]
                film = ET.SubElement(sensor, 'film', type=type)
            else:
                film = ET.SubElement(sensor, 'film')

            if 'filename' in scene.sensor.film.params:
                filename = scene.sensor.film.params['filename'].value.split('.')
                if len(filename) > 1:
                    ET.SubElement(film, 'string', name='fileFormat', value=filename[1])
                else:
                    ET.SubElement(film, 'string', name='fileFormat', value='png')

                self.paramsToMitsuba(film, scene.sensor.film.params, pbrttm.filmParam)

                ET.SubElement(film, 'string', name='pixelFormat', value='rgb')
                ET.SubElement(film, 'float', name='gamma', value='2.2')
                ET.SubElement(film, 'boolean', name='banner', value='false')

        if scene.sensor.film.filter:
            if scene.sensor.film.filter in pbrttm.filterType:
                filter = pbrttm.filterType[scene.sensor.film.filter]
                ET.SubElement(film, 'rfilter', type=filter)
            else:
                ET.SubElement(film, 'rfilter', type='tent')

    def worldDescriptionToMitsuba(self, scene):
        # materials
        for material in scene.materials:
            self.materialDescriptionToMitsuba(material, self.sceneElement)

        self.shapeDescriptionToMitsuba(scene)
        self.lightDescriptionToMitsuba(scene)
        

    def materialDescriptionToMitsuba(self, material, element):
        # normal material
        if hasattr(material,'id'):
            if material.type in pbrttm.materialType:
                type = pbrttm.materialType[material.type]
            
            alpha = 0.001
            if 'roughness' in material.params:
                alpha = material.params['roughness'].value 
            elif 'uroughness' in material.params or 'vroughness' in material.params:
                alpha = material.params['uroughness'].value

            if alpha > 0.001:
                type = 'rough' + type

            if material.type == 'glass':
                bsdf = ET.SubElement(element, 'bsdf', type=type, id=material.id)

                if 'uroughness' in material.params or 'vroughness' in material.params:
                    if type.startswith('rough'):
                        alpha = material.params['uroughness'].value
                        ET.SubElement(bsdf, 'float', name='alpha', value=str(alpha))

                self.paramsToMitsuba(bsdf, material.params, pbrttm.glassParam)
            else:
                twosided = ET.SubElement(element, 'bsdf', type='twosided', id=material.id)
                bsdf = ET.SubElement(twosided, 'bsdf', type=type)

                if material.type == 'mirror':
                    ET.SubElement(bsdf, 'string', name='material', value='none')

                if 'uroughness' in material.params or 'vroughness' in material.params:
                    if type.startswith('rough'):
                        alpha = material.params['uroughness'].value
                        ET.SubElement(bsdf, 'float', name='alpha', value=str(alpha))

                if material.type in pbrttm.materialDict:
                    dictionary = pbrttm.materialDict[material.type]
                    self.paramsToMitsuba(bsdf, material.params, dictionary)

            if material.texture is not None:
                if material.texture.type in pbrttm.textureType:
                    texType = pbrttm.textureType[material.texture.type]
                    if type == 'diffuse':
                        texture = ET.SubElement(bsdf, 'texture', name='reflectance', type=texType)
                    else:
                        texture = ET.SubElement(bsdf, 'texture', name='diffuseReflectance', type=texType)

                    self.paramsToMitsuba(texture, material.texture.params, pbrttm.textureParam)

                    if 'trilinear' in material.texture.params:
                        if material.texture.params['trilinear'].value == 'true':
                            ET.SubElement(texture, 'string', name='filterType', value='trilinear')
        else:
            bumpmap = ET.SubElement(element, 'bsdf', type='bumpmap')
            if material.texture is not None:
                if material.texture.type in pbrttm.textureType:
                    texType = pbrttm.textureType[material.texture.type]
                    texture = ET.SubElement(bumpmap, 'texture', name='map', type=texType)
                    self.paramsToMitsuba(texture, material.texture.params, pbrttm.textureParam)

                    if 'trilinear' in material.texture.params:
                        if material.texture.params['trilinear'].value == 'true':
                            ET.SubElement(texture, 'string', name='filterType', value='trilinear')

            if material.material is not None:
                if material.material.type in pbrttm.materialType:
                    type = pbrttm.materialType[material.material.type]
            
                alpha = 0.001
                if 'roughness' in material.material.params:
                    alpha = material.material.params['roughness'].value 
                elif 'uroughness' in material.material.params or 'vroughness' in material.material.params:
                    alpha = material.material.params['uroughness'].value

                if alpha > 0.001:
                    type = 'rough' + type

                if material.material.type == 'glass':
                    bsdf = ET.SubElement(bumpmap, 'bsdf', type=type, id=material.id)

                    if 'uroughness' in material.material.params or 'vroughness' in material.material.params:
                        if type.startswith('rough'):
                            alpha = material.material.params['uroughness'].value
                            ET.SubElement(bsdf, 'float', name='alpha', value=str(alpha))

                    self.paramsToMitsuba(bsdf, material.material.params, pbrttm.glassParam)
                else:
                    twosided = ET.SubElement(bumpmap, 'bsdf', type='twosided', id=material.material.id)
                    bsdf = ET.SubElement(twosided, 'bsdf', type=type)

                    if material.material.type == 'mirror':
                        ET.SubElement(bsdf, 'rgb', name='specularReflectance', value='1, 1, 1')

                    if material.material.type == 'substrate':
                        ET.SubElement(bsdf, 'boolean', name='nonlinear', value='true')

                    if 'uroughness' in material.material.params or 'vroughness' in material.material.params:
                        if type.startswith('rough'):
                            alpha = material.material.params['uroughness'].value
                            ET.SubElement(bsdf, 'float', name='alpha', value=str(alpha))

                    if material.material.type in pbrttm.materialDict:
                        dictionary = pbrttm.materialDict[material.material.type]
                        self.paramsToMitsuba(bsdf, material.material.params, dictionary)
                
                if material.material.texture is not None:
                    if material.material.texture.type in pbrttm.textureType:
                        texType = pbrttm.textureType[material.material.texture.type]
                        
                        if type == 'diffuse':
                            texture = ET.SubElement(bsdf, 'texture', name='reflectance', type=texType)
                        else:
                            texture = ET.SubElement(bsdf, 'texture', name='diffuseReflectance', type=texType)

                        self.paramsToMitsuba(texture, material.material.texture.params, pbrttm.textureParam)

                        if 'trilinear' in material.texture.params:
                            if material.material.texture.params['trilinear'].value == 'true':
                                ET.SubElement(texture, 'string', name='filterType', value='trilinear')

    def shapeDescriptionToMitsuba(self, scene):
        for shape in scene.shapes:
            if shape.type == 'plymesh':
                type = 'ply'

                s = ET.SubElement(self.sceneElement, 'shape', type=type)

                filename = shape.params['filename'].value
                ET.SubElement(s, 'string', name='filename', value=filename)

                if shape.transform is not None and shape.transform.matrix:
                    matrix = ''
                    for i in range(0,4):
                        for j in range(0,4):
                            matrix += str(np.array(shape.transform.matrix).T[i][j])
                else:
                    matrix = '1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1'

                transform = ET.SubElement(s, 'transform', name='toWorld')
                ET.SubElement(transform, 'matrix', value=matrix)

                if shape.material is not None:
                    self.materialDescriptionToMitsuba(shape.material, s)

                if shape.emitter is not None:
                    emitter = ET.SubElement(s, 'emitter', type='area')
                    self.paramsToMitsuba(emitter, shape.emitter.params, pbrttm.emitterParam)

                if 'id' in shape.params:
                    ref = shape.params['id'].value
                    ET.SubElement(s, 'ref', id=ref)

            elif shape.type == 'cylinder':
                pass
            elif shape.type == 'sphere':
                type = 'sphere'

                s = ET.SubElement(self.sceneElement, 'shape', type=type)

                if shape.transform is not None and shape.transform.matrix:
                    center = [shape.transform.matrix[3][0], shape.transform.matrix[3][1], shape.transform.matrix[3][2]]
                    ET.SubElement(s, 'point', name='center', x=str(center[0]), y=str(center[1]), z=str(center[2]))

                self.paramsToMitsuba(s, shape.params, pbrttm.shapeParam)

                if shape.emitter is not None:
                    emitter = ET.SubElement(s, 'emitter', type='area')
                    self.paramsToMitsuba(emitter, shape.emitter.params, pbrttm.emitterParam)

                if 'id' in shape.params:
                    ref = shape.params['id']
                    ET.SubElement(s, 'ref', id=ref)

            elif shape.type == 'trianglemesh':
                if 'indices' in shape.params:
                    indices = shape.params['indices'].value
                    if max(indices) == 3:
                        type = 'rectangle'
                        if 'P' in shape.params:
                            p = shape.params['P'].value
                            p0 = [p[0], p[1], p[2]]
                            p1 = [p[3], p[4], p[5]]
                            p2 = [p[6], p[7], p[8]]
                            p3 = [p[9], p[10], p[11]]

                            points = np.array([[p0[0], p1[0], p2[0], p3[0]],
                                               [p0[1], p1[1], p2[1], p3[1]],
                                               [p0[2], p1[2], p2[2], p3[2]],
                                               [1, 1, 1, 1]])

                            canonical = np.array([[-1, 1, 1, -1], [-1, -1, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1]])
                            toWorld = np.matmul(points, np.linalg.pinv(canonical))

                            # put cushion on z axis so matrix stays invertible. figure out later
                            for i in range(0,3):
                                toWorld[i][2] = -0.01

                            matrix = ''
                            for i in range(0,4):
                                for j in range(0,4):
                                    matrix += str(toWorld[i][j]) + ' '

                            s = ET.SubElement(self.sceneElement, 'shape', type=type)
                            transform = ET.SubElement(s, 'transform', name='toWorld')
                            ET.SubElement(transform, 'matrix', value=matrix)

                            if shape.material is not None:
                                self.materialDescriptionToMitsuba(shape.material, s)

                            if shape.emitter is not None:
                                emitter = ET.SubElement(s, 'emitter', type='area')
                                self.paramsToMitsuba(emitter, shape.emitter.params, pbrttm.emitterParam)

                            if 'id' in shape.params:
                                ref = shape.params['id'].value
                                ET.SubElement(s, 'ref', id=ref)

                    elif max(indices) == 23:
                        type = 'cube'
                        pass

    def lightDescriptionToMitsuba(self, scene):

        print scene.lights
        for light in scene.lights:
            if light.type == 'distant':
                emitter = ET.SubElement(self.sceneElement, 'emitter', type='sun')

                if 'from' in light.params:
                    f = light.params['from'].value
                    ET.SubElement(emitter, 'vector', name='sunDirection', x=str(f[0]), y=str(f[1]), z=str(f[2]))
                
                if 'L' in light.params:
                    scale = light.params['L'].value
                    ET.SubElement(emitter, 'float', name='sunScale', value=str(scale[0]))
            
            elif light.type == 'infinite':
                emitter = ET.SubElement(self.sceneElement, 'emitter', type='envmap')

                if light.transform and light.transform.matrix:
                    m = copy.deepcopy(light.transform.matrix)
                    m_rot = np.zeros((4,4))
                    
                    m_rot[2] = copy.deepcopy(m[0])
                    m_rot[0] = copy.deepcopy(m[1])
                    m_rot[1] = copy.deepcopy(m[2])

                    m_rot[0][2] = -m_rot[0][2]
                    m_rot[1][2] = -m_rot[1][2]
                    m_rot[2][2] = -m_rot[2][2]
                    m_rot[3][3] = 1

                    matrix = ''

                    for i in range(0,4):
                        for j in range(0,4):
                            matrix += str(m_rot[i][j])
                            matrix += ' '
                    
                    transform = ET.SubElement(emitter, 'transform', name='toWorld')
                    ET.SubElement(transform, 'matrix', value=matrix)

                self.paramsToMitsuba(emitter, light.params, pbrttm.emitterParam)
                        
            elif light.type == 'spot':
                pass
            
            elif light.type == 'point':
                pass

            
    def paramsToMitsuba(self, rootElement, params, dictionary):
        for key in params:
            if key in dictionary:
                mitsubaParamName = dictionary[key]
                pbrtParam = params[key]
                type = pbrtParam.type

                if type == 'rgb':
                    value = str(pbrtParam.value[0]) + ', ' +  str(pbrtParam.value[1]) + ', ' +  str(pbrtParam.value[2])
                    ET.SubElement(rootElement, type, name=mitsubaParamName, value=value)
                elif type == 'vector' or type == 'point':
                    ET.SubElement(rootElement, type, name=mitsubaParamName, x=str(pbrtParam.value[0]), y=str(pbrtParam.value[1]), z=str(pbrtParam.value[2]))
                else:
                    ET.SubElement(rootElement, type, name=mitsubaParamName, value=str(pbrtParam.value))
            
    def __init__(self, scene, filename):
        self.sceneElement = ET.Element('scene', version='0.5.0')
        self.toMitsuba(scene, filename)

    

