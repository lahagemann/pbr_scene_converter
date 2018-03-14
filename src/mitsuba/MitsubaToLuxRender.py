import numpy as np
import sys

sys.path.insert(0, 'core/')
from Directives import BumpMap as bmap

sys.path.insert(0, 'dictionaries')
from dictionaries import MitsubaLux as mtlux

class MitsubaToLuxRender:
    textureCount = 1
    materialTextureRef = {}

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

                # convert transform matrix to inverse transpose (PBRT/Lux default)
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
        output = ''
        # textures
        for material in scene.materials:
            if material.texture is not None:
                id = 'Texture' + str(self.textureCount).zfill(2)
                
                print material

                if isinstance(material, bmap):
                    print 'bumpmap'
                    self.materialTextureRef[material.material.id] = id
                    output += '\tTexture "' + id + '" "float" '
                else:
                    print 'regularmat'
                    self.materialTextureRef[material.id] = id
                    output += '\tTexture "' + id + '" "spectrum" '

                if material.texture.type == 'bitmap':
                    output += '"imagemap" '
                else:
                    if material.texture.type in mtlux.textureType:
                        type = mtlux.textureType[material.texture.type]
                        output += '"' + type + '" '
            
                for key in material.texture.params:
                    if key == 'filename':
                        output += '"string filename" [ "' + material.texture.params[key].value + '" ] '
                        
                    elif key == 'filterType':
                        if material.texture.params[key] == 'ewa':
                            output += '"bool trilinear" [ "false" ] '
                        else:
                            output += '"bool trilinear" [ "true" ] '
                    else:
                        # search the dictionary
                        if key in mtlux.textureParam:
                            luxParam = mtlux.textureParam[key]
                            mitsubaParam = material.texture.params[key]
                            output += '"' + mitsubaParam.type + ' ' + luxParam + '" '

                            if mitsubaParam.type == 'string' or mitsubaParam.type == 'bool':
                                output += '[ "' + str(mitsubaParam.value) + '" ] '
                            elif mitsubaParam.type == 'rgb' or mitsubaParam.type == 'spectrum':
                                output += '[ ' + str(mitsubaParam.value[0]) + ' ' + str(mitsubaParam.value[1]) + ' ' + str(mitsubaParam.value[2]) + ' ] '
                            else:
                                output += '[ ' + str(mitsubaParam.value) + ' ] '
                    
                output += '\n'

                self.textureCount += 1

        for material in scene.materials:
            if isinstance(material, BumpMap):
                output += '\tMakeNamedMaterial "' + material.material.id + '" '
                id = material.material.id
                params = material.material.params
                mitsubaType = material.material.type
            else:
                output += '\tMakeNamedMaterial "' + material.id + '" '
                id = material.id
                params = material.params
                mitsubaType = material.type

            if mitsubaType in mtlux.materialType:
                luxType = mtlux.materialType[mitsubaType]
                output += '"string type" [ "' + luxType + '" ] '

            if material.texture is not None:
                if isinstance(material, BumpMap):
                    output += '"texture bumpmap" [ "' + self.materialTextureRef[id] + '" ] '
                else:
                    output += '"texture Kd" [ "' + self.materialTextureRef[id] + '" ] '
                
            # special material cases:

            if mitsubaType.endswith('plastic'):
                if 'alpha' in params:
                    alpha = params['alpha']
                    output += '"float uroughness" [ ' + str(alpha.value) + ' ] '
                    output += '"float vroughness" [ ' + str(alpha.value) + ' ] '

                output += self.paramsToLux(params, mtlux.plasticParam)
            
            elif mitsubaType.endswith('conductor'):
                if 'alpha' in params:
                    alpha = params['alpha']
                    output += '"float uroughness" [ ' + str(alpha.value) + ' ] '
                    output += '"float vroughness" [ ' + str(alpha.value) + ' ] '

                output += self.paramsToLux(params, mtlux.conductorParam)

            elif mitsubaType.endswith('electric'):
                if 'alpha' in params:
                    alpha = params['alpha']
                    output += '"float uroughness" [ ' + str(alpha.value) + ' ] '
                    output += '"float vroughness" [ ' + str(alpha.value) + ' ] '

                output += self.paramsToLux(params, mtlux.dielectricParam)

            elif mitsubaType == 'difftrans':
                output += self.paramsToLux(params, mtlux.difftransParam)

            else:
                output += self.paramsToLux(params, mtlux.diffuseParam)

            output += '\n'

        return output

    def worldDescriptionToLux(self, scene):
        return ''

    def paramsToLux(self, params, dictionary):
        output = ''
        for key in params:
            if key in dictionary:
                luxParam = dictionary[key]
                mitsubaParam = params[key]
                if mitsubaParam.type == 'rgb' or mitsubaParam.type == 'srgb':
                    output += '"color ' + luxParam + '" '
                else:
                    output += '"' + mitsubaParam.type + ' ' + luxParam + '" '

                if mitsubaParam.type == 'string' or mitsubaParam.type == 'bool':
                    output += '[ "' + str(mitsubaParam.value) + '" ] '
                elif mitsubaParam.type == 'rgb' or mitsubaParam.type == 'srgb' or mitsubaParam.type == 'spectrum' or mitsubaParam.type == 'point' or mitsubaParam.type == 'vector':
                    output += '[ ' + str(mitsubaParam.value[0]) + ' ' + str(mitsubaParam.value[1]) + ' ' + str(mitsubaParam.value[2]) + ' ] '
                else:
                    output += '[ ' + str(mitsubaParam.value) + ' ] '
                    
        output += '\n'

        return output

    def __init__(self, scene, filename):
        self.copySkydome = False
        self.toLux(scene, filename)