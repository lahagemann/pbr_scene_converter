import numpy as np
import sys

sys.path.insert(0, 'core/')
from Directives import BumpMap

sys.path.insert(0, 'dictionaries')
from dictionaries import MitsubaLux as mtlux

class MitsubaToLuxRender:
    def toLux(self, scene, filename):
        np.set_printoptions(suppress=True)
        with open(filename + '.lxs', 'w') as scenefile:
            sceneDirectives = self.sceneDirectivesToLux(scene)
            scenefile.write(sceneDirectives)

            scenefile.write('WorldBegin\n\n')
            scenefile.write('Include "'+ filename + '.lxm"\n')
            scenefile.write('Include "'+ filename + '.lxo"\n\n')

            scenefile.write('WorldEnd\n')

        with open(filename + '.lxm', 'w') as materialfile:
            materialDescription = self.materialDescriptionToLux(scene)
            materialfile.write(materialDescription)

        with open(filename + '.lxo', 'w') as worldfile:
            worldDescription = self.worldDescriptionToLux(scene)
            worldfile.write(worldDescription)


    def sceneDirectivesToLux(self, scene):
        output = ''

        if scene.integrator is not None:
            output += 'SurfaceIntegrator '

            if scene.integrator.type in mtlux.integratorType:
                type = mtlux.integratorType[scene.integrator.type]
                output += '"' + type + '" '

            output += self.paramsToLux(scene.integrator.params, mtlux.integratorParam)

        if scene.sensor.transform is not None:
            if scene.sensor.transform.matrix:
                output += 'Transform [ '

                # convert transform matrix to inverse transpose (PBRT default)
                m = scene.sensor.transform.matrix
                m_T = np.transpose(m)
                m_IT = np.linalg.inv(m_T)

                for i in range(0,4):
                    for j in range(0,4):
                        output += str(m_IT[i][j]) + ' '
                  
                output += ']\n'

        if scene.sensor.sampler is not None:
            output += 'Sampler '

            if scene.sensor.sampler.type in mtlux.samplerType:
                type = mtlux.samplerType[scene.sensor.sampler.type]
                output += '"' + type + '" '

            output += self.paramsToLux(scene.sensor.sampler.params, mtlux.samplerParam)

        if scene.sensor.film.filter:
            output += 'PixelFilter '

            if scene.sensor.film.filter in mtlux.filterType:
                filter = mtlux.filterType[scene.sensor.film.filter]
                output += '"' + filter + '" '
            else:
                output += '"triangle" '
    
            output += '\n'


        if scene.sensor.film is not None:
            output += 'Film '

            if scene.sensor.film.type in mtlux.filmType:
                type = mtlux.filmType[scene.sensor.film.type]
                output += '"' + type + '" '
            else:
                output += '"image" '

            if 'fileFormat' in scene.sensor.film.params:
                extension = scene.sensor.film.params['fileFormat'].value

                output += '"string filename" [ "scene.' + extension + '" ] '

            output += self.paramsToLux(scene.sensor.film.params, mtlux.filmParam)

        if scene.sensor is not None:
            output += 'Camera '

            if scene.sensor.type in mtlux.sensorType:
                type = mtlux.sensorType[scene.sensor.type]
                output += '"' + type + '" '
            else:
                output += '"perspective" '

            if 'fov' in scene.sensor.params:
                if 'width' in scene.sensor.film.params and 'height' in scene.sensor.film.params:
                    width = float(scene.sensor.film.params['width'].value)
                    height = float(scene.sensor.film.params['height'].value)
                    fov = float(scene.sensor.params['fov'].value)

                    if height < width:
                        adjustedFov = (fov * height) / width
                        output += '"float fov" [ ' + str(adjustedFov) + ' ] '
                    else:
                        output += '"float fov" [ ' + str(fov) + ' ] '

                else:
                    width = 768
                    height = 576
                    fov = scene.sensor.params['fov']
                    adjustedFov = (fov * height) / width

                    output += '"float fov" [ ' + adjustedFov + ' ] '

            output += self.paramsToLux(scene.sensor.params, mtlux.sensorParam)

        return output

    def materialDescriptionToLux(self, scene):
        pass

    def worldDescriptionToLux(self, scene):
        pass

    def paramsToLux(self, params, dictionary):
        output = ''
        for key in params:
            if key in dictionary:
                pbrtParam = dictionary[key]
                mitsubaParam = params[key]
                if mitsubaParam.type == 'rgb':
                    output += '"color ' + pbrtParam + '" '
                else:
                    output += '"' + mitsubaParam.type + ' ' + pbrtParam + '" '

                if mitsubaParam.type == 'string' or mitsubaParam.type == 'bool':
                    output += '[ "' + str(mitsubaParam.value) + '" ] '
                elif mitsubaParam.type == 'rgb' or mitsubaParam.type == 'spectrum':
                    output += '[ ' + str(mitsubaParam.value[0]) + ' ' + str(mitsubaParam.value[1]) + ' ' + str(mitsubaParam.value[2]) + ' ] '
                else:
                    output += '[ ' + str(mitsubaParam.value) + ' ] '
                    
        output += '\n'

        return output