import numpy as np
import sys
import copy
import xml.etree.ElementTree as ET

sys.path.insert(0, 'core/')
from Directives import BumpMap

sys.path.insert(0, 'dictionaries')
from dictionaries import PBRTv3Mitsuba as pbrttm

class PBRTv3ToMitsuba:
    

    def toMitsuba(self, scene, filename):
        np.set_printoptions(suppress=True)

        self.sceneDirectivesToMitsuba(scene)
        # self.worldDescriptionToMitsuba(scene)

        tree = ET.ElementTree(self.sceneElement)
        tree.write(filename)

    def sceneDirectivesToMitsuba(self, scene):
        if scene.integrator is not None:
            if scene.integrator.type in pbrttm.integratorType:
                type = pbrttm.integratorType[scene.integrator.type]
                integrator = ET.SubElement(self.sceneElement, 'integrator', type=type)
            else:
                integrator = ET.SubElement(self.sceneElement, 'integrator')

            self.paramsToMitsuba(integrator, scene.integrator.params, pbrttm.integratorParams)

        if scene.sensor is not None:
            if scene.sensor.type in pbrttm.sensorType:
                type = pbrttm.sensorType[scene.sensor.type]
                sensor = ET.SubElement(self.sceneElement, 'sensor', type=type)
            else:
                sensor = ET.SubElement(self.sceneElement, 'sensor')

            if 'fov' in scene.sensor.params:
                if 'width' in scene.sensor.film.params and 'height' in scene.sensor.film.params:
                    width = float(scene.sensor.film.params['width'].value)
                    height = float(scene.sensor.film.params['height'].value)
                    fov = float(scene.sensor.params['fov'].value)

                    if height < width:
                        adjustedFov = (fov * width) / height
                        ET.SubElement(sensor, 'float', name='fov', value=str(adjustedFov))
                    else:
                        ET.SubElement(sensor, 'float', name='fov', value=str(fov))

                else:
                    width = 768
                    height = 576
                    fov = scene.sensor.params['fov']
                    adjustedFov = (fov * height) / width

                    ET.SubElement(sensor, 'float', name='fov', value=str(adjustedFov))

            self.paramsToMitsuba(sensor, scene.sensor.params, pbrttm.sensorParams)

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
            
            self.paramsToMitsuba(sampler, scene.sensor.sampler.params, pbrttm.samplerParams)

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

                self.paramsToMitsuba(film, scene.sensor.film.params, pbrttm.filmParams)

                ET.SubElement(film, 'string', name='pixelFormat', value='rgb')
                ET.SubElement(film, 'float', name='gamma', value='2.2')
                ET.SubElement(film, 'boolean', name='banner', value='false')

        if scene.sensor.film.filter:
            if scene.sensor.film.filter in pbrttm.filterType:
                filter = pbrttm.filterType[scene.sensor.film.filter]
                ET.SubElement(film, 'rfilter', type=filter)
            else:
                ET.SubElement(film, 'rfilter', type='tent')

    # def worldDescriptionToMitsuba(self, scene):


    def paramsToMitsuba(self, rootElement, params, dictionary):
        for key in params:
            if key in dictionary:
                mitsubaParamName = dictionary[key]
                pbrtParam = params[key]
                type = pbrtParam.type

                if type == 'rgb':
                    value = str(pbrtParam.value[0]) + ', ' +  str(pbrtParam.value[1]) + ', ' +  str(pbrtParam.value[2])
                    ET.SubElement(rootElement, type, name=mitsubaParamName, value=value)
                elif type == 'vector' or type == 'point'
                    ET.SubElement(rootElement, type, name=mitsubaParamName, x=str(pbrtParam.value[0]), y=str(pbrtParam.value[1]), z=str(pbrtParam.value[2]))
                else:
                    ET.SubElement(rootElement, type, name=mitsubaParamName, value=str(pbrtParam.value))
            
    def __init__(self, scene, filename):
        self.sceneElement = ET.Element('scene', version='0.5.0')
        self.toMitsuba(scene, filename)

    

