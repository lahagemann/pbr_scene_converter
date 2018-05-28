import numpy as np
import sys
import copy

sys.path.insert(0, 'core/')
from Directives import BumpMap

sys.path.insert(0, 'dictionaries')
from dictionaries import LuxRenderPBRTv3 as ltpbrt

class LuxRenderToPBRTv3:
    def toPBRT(self, scene, filename):
        np.set_printoptions(suppress=True)
        with open(filename, 'w') as outfile:
            sceneDirectives = self.sceneDirectivesToPBRT(scene)
            outfile.write(sceneDirectives)

            worldDescription = self.worldDescriptionToPBRT(scene)
            outfile.write(worldDescription)

    def sceneDirectivesToPBRT(self, scene):
        output = ''

        if scene.integrator is not None:
            output += 'Integrator '

            if scene.integrator.type in ltpbrt.integratorType:
                type = ltpbrt.integratorType[scene.integrator.type]
                output += '"' + type + '" '

            output += self.paramsToPBRT(scene.integrator.params, ltpbrt.integratorParam)

        if scene.sensor.transform is not None:
            if scene.sensor.transform.matrix:
                output += 'Transform [ '

                for i in range(0,4):
                    for j in range(0,4):
                        output += str(scene.sensor.transform.matrix[i][j]) + ' '
                  
                output += ']\n'

        if scene.sensor.sampler is not None:
            output += 'Sampler '

            if scene.sensor.sampler.type in ltpbrt.samplerType:
                type = ltpbrt.samplerType[scene.sensor.sampler.type]
                output += '"' + type + '" '

            output += self.paramsToPBRT(scene.sensor.sampler.params, ltpbrt.samplerParam)

        if scene.sensor.film.filter:
            output += 'PixelFilter '

            if scene.sensor.film.filter in ltpbrt.filterType:
                filter = ltpbrt.filterType[scene.sensor.film.filter]
                output += '"' + filter + '" '
            else:
                output += '"triangle" '

            output += '"float xwidth" [ 1.000000 ] "float ywidth" [ 1.000000 ]'
            output += '\n'


        if scene.sensor.film is not None:
            output += 'Film '

            if scene.sensor.film.type in ltpbrt.filmType:
                type = ltpbrt.filmType[scene.sensor.film.type]
                output += '"' + type + '" '
            else:
                output += '"image" '

            output += self.paramsToPBRT(scene.sensor.film.params, ltpbrt.filmParam)

        if scene.sensor is not None:
            output += 'Camera '

            if scene.sensor.type in ltpbrt.sensorType:
                type = ltpbrt.sensorType[scene.sensor.type]
                output += '"' + type + '" '
            else:
                output += '"perspective" '

            output += self.paramsToPBRT(scene.sensor.params, ltpbrt.sensorParam)

        return output

    def worldDescriptionToPBRT(self, scene):
        output = ''

        # scene description opener
        output += 'WorldBegin\n'

        # texture declaration
        textureCount = 1
        materialTextureRef = {}

        # textures
        for material in scene.materials:
            if material.texture is not None:
                id = 'Texture' + str(textureCount).zfill(2)
                type = ''
                
                if not hasattr(material, 'id'):
                    materialTextureRef[material.material.id] = id
                    output += '\tTexture "' + id + '" "float" '
                else:
                    materialTextureRef[material.id] = id
                    output += '\tTexture "' + id + '" "spectrum" '

                print material.texture.type

                if material.texture.type in ltpbrt.textureType:
                    print material.texture.type
                    type = ltpbrt.textureType[material.texture.type]
                    output += '"' + type + '" '
            
                for key in material.texture.params:
                    if key in ltpbrt.textureParam:
                        pbrtParam = ltpbrt.textureParam[key]
                        mitsubaParam = material.texture.params[key]
                        output += '"' + mitsubaParam.type + ' ' + pbrtParam + '" '

                        if mitsubaParam.type == 'string' or mitsubaParam.type == 'bool':
                            output += '[ "' + str(mitsubaParam.value) + '" ] '
                        elif mitsubaParam.type == 'color':
                            output += '[ ' + str(mitsubaParam.value[0]) + ' ' + str(mitsubaParam.value[1]) + ' ' + str(mitsubaParam.value[2]) + ' ] '
                        else:
                            output += '[ ' + str(mitsubaParam.value) + ' ] '
                    
                output += '\n'

                textureCount += 1

        for material in scene.materials:
            if not hasattr(material, 'id'):
                output += '\tMakeNamedMaterial "' + material.material.id + '" '
                id = material.material.id
                params = material.material.params
                luxType = material.material.type
            else:
                output += '\tMakeNamedMaterial "' + material.id + '" '
                id = material.id
                params = material.params
                luxType = material.type

            if luxType in ltpbrt.materialType:
                pbrtType = ltpbrt.materialType[luxType]

                output += '"string type" [ "' + pbrtType + '" ] '

            if material.texture is not None:
                if not hasattr(material, 'id'):
                    output += '"texture bumpmap" [ "' + materialTextureRef[id] + '" ] '
                else:
                    output += '"texture Kd" [ "' + materialTextureRef[id] + '" ] '

            if luxType in ltpbrt.materialDict:
                output += self.paramsToPBRT(params, ltpbrt.materialDict[luxType])

        currentRefMaterial = ''
        for shape in scene.shapes:
            if shape.emitter is not None:
                # child emitter will ALWAYS be area emitter
                output += '\tAttributeBegin\n'
                        
                output += '\t\tAreaLightSource "area" '
                output += self.paramsToPBRT(shape.emitter.params, ltpbrt.emitterParam)
                      
                if 'id' in shape.params:        
                    if shape.params['id'].value != currentRefMaterial:
                        output += '\t\tNamedMaterial "' + str(shape.params['id'].value) + '"\n'
                        currentRefMaterial = shape.params['id'].value

                output += self.shapeToPBRT(shape, 2)
                        
                output += '\tAttributeEnd\n'

            else:
                # if shape has ref material, then make reference
                if 'id' in shape.params:
                    if shape.params['id'].value != currentRefMaterial:
                        output += '\tNamedMaterial "' + shape.params['id'].value + '"\n'
                        output += self.shapeToPBRT(shape, 1)
                        currentRefMaterial = shape.params['id'].value
                    else:
                        output += self.shapeToPBRT(shape, 1)
                else:
                    output += self.shapeToPBRT(shape, 1)

        for light in scene.lights:
            output += self.lightToPBRT(light, 1)

        output += 'WorldEnd\n'

        return output

    def shapeToPBRT(self, shape, identation):
        output = ''

        if shape.material is not None:
            output += ('\t' * identation) + 'Material '

            if not hasattr(shape.material, 'id'):
                luxType = shape.material.material.type
            else:
                luxType = shape.material.type

            if luxType in ltpbrt.materialType:
                pbrtType = ltpbrt.materialType[luxType]
                output += '"' + pbrtType + '" '

            params = shape.material.params


            if luxType in ltpbrt.materialDict:
                output += self.paramsToPBRT(params, ltpbrt.materialDict[luxType])

        if shape.type == 'plymesh':
            if shape.transform is not None and shape.transform.matrix:
                if not np.array_equal(shape.transform.matrix, identity):
                    output += ('\t' * identation) + 'TransformBegin\n'
                    output += ('\t' * (identation + 1)) + 'Transform [ '

                    for i in range(0,4):
                        for j in range(0,4):
                            output += str(shape.transform.matrix[i][j])
                            output += ' '
                        
                    output += ']\n'
                    output += ('\t' * (identation + 1)) + 'Shape "plymesh" "string filename" [ "' + shape.params['filename'].value + '" ]\n'
                    output += ('\t' * identation) + 'TransformEnd\n'
                else:
                    output += ('\t' * identation) + 'Shape "plymesh" "string filename" [ "' + shape.params['filename'].value + '" ]\n'
                
            else:
                output += ('\t' * identation) + 'Shape "plymesh" "string filename" [ "' + shape.params['filename'].value + '" ]\n'
            
        elif shape.type == 'trianglemesh':
            output += ('\t' * identation) + 'Shape "trianglemesh" '

            if 'indices' in shape.params:
                indices = shape.params['indices'].value
                output += '"integer indices" [ ' 

                print indices
                for i in range(0, len(indices)):
                    output += str(indices[i])
                    output += ' '
                    
                output += '] '
            
            if 'P' in shape.params:
                P = shape.params['P'].value
                output += '"point P" [ '
                for i in range(0, len(P)):
                    output += str(P[i])
                    output += ' '

                output += '] '
            
            if 'N' in shape.params:
                N = shape.params['N'].value
                output += '"normal N" [ '
                for i in range(0, len(N)):
                    output += str(N[i])
                    output += ' '
                
                output += '] '    

            if 'uv' in shape.params:
                uv = shape.params['uv'].value
                output += '"float uv" [ '
                for i in range(0, len(uv)):
                    output += str(uv[i])
                    output += ' '

                output += ']\n'
                
            
        elif shape.type == 'sphere':
            if shape.transform is not None and shape.transform.matrix:

                output += ('\t' * identation) + 'TransformBegin\n'
                output += ('\t' * (identation + 1)) + 'Transform [ '
                
                for i in range(0,4):
                    for j in range(0,4):
                        output += str(shape.transform.matrix[i][j])
                        output += ' '
  
                output += ']\n'

            output += ('\t' * (identation + 1)) + 'Shape "sphere" '
            output += self.paramsToPBRT(shape.params, ltpbrt.shapeParam)
            output += '\n'
            output += ('\t' * identation) + 'TransformEnd\n'

        elif shape.type == 'cylinder':
            pass
            
        elif shape.type == 'disk':
            pass
            
        elif shape.type == 'hair':
            pass
                
        return output

    def lightToPBRT(self, emitter, identation):
        output = ''
        
        if emitter.type == 'envmap':
            if emitter.transform is not None and emitter.transform.matrix:
                output += ('\t' * identation) + 'TransformBegin\n'
                output += ('\t' * (identation + 1)) + 'Transform [ '

                for i in range(0,4):
                    for j in range(0,4):
                        output += str(emitter.transform.matrix[i][j])
                        output += ' '
                        
                output += ']\n'
                
                output += ('\t' * (identation + 1)) + 'LightSource "infinite" '

                if 'mapname' in emitter.params:
                    output += '"string mapname" [ "' + emitter.params['mapname'].value + '" ] '

                output += self.paramsToPBRT(emitter.params, ltpbrt.emitterParam)
                output += ('\t' * identation) + 'TransformEnd\n'
                
            else:
                output += ('\t' * identation) + 'LightSource "infinite" '
                
                if 'filename' in emitter.params:
                    output += '"string mapname" [ "' + emitter.params['filename'].value + '" ] '

                output += self.paramsToPBRT(emitter.params, ltpbrt.emitterParam)
                output += '\n'
            
        elif emitter.type == 'sun':
            output += ('\t' * identation) + 'TransformBegin\n'
            output += ('\t' * (identation + 1)) + 'Transform [ -1 0 0 0 0 0 -1 0 0 1 0 0 0 0 0 1 ]\n'
            output += ('\t' * (identation + 1)) + 'LightSource "infinite" "string mapname" [ "Skydome.pfm" ]\n'
            output += ('\t' * identation) + 'TransformEnd\n'

            self.copySkydome = True

        elif emitter.type == 'sky2':
            output += ('\t' * identation) + 'LightSource "distant" '
            
            if 'sundir' in emitter.params:
                sundir = emitter.params['sundir'].value                       
                output += '"point from" [ ' + str(sundir[0]) + ' ' + str(sundir[1]) + ' ' + str(sundir[2]) + ' ] '
                output += '"point to" [ 0.000000 0.000000 0.000000 ] '
            
            output += self.paramsToPBRT(emitter.params, ltpbrt.emitterParam)
            output += '\n'

        elif emitter.type == 'infinite':
            if emitter.transform and emitter.transform.matrix:
                output += ('\t' * identation) + 'TransformBegin\n'
                output += ('\t' * (identation + 1)) + 'Transform [ '

                for i in range(0,4):
                    for j in range(0,4):
                        output += str(emitter.transform.matrix[i][j])
                        output += ' '

                output += ']\n'
                output += ('\t' * (identation + 1)) + 'LightSource "infinite" '

                if 'mapname' in emitter.params:
                    output += '"string mapname" [ "' + emitter.params['mapname'].value + '" ] '

                output += self.paramsToPBRT(emitter.params, ltpbrt.emitterParam)
                output += ('\t' * identation) + 'TransformEnd\n'

            else:
                output += ('\t' * identation) + 'LightSource "infinite" '

                if 'mapname' in emitter.params:
                    output += '"string mapname" [ "' + emitter.params['mapname'].value + '" ] '

                output += self.paramsToPBRT(emitter.params, ltpbrt.emitterParam)

        elif emitter.type == 'distant':
            output += ('\t' * identation) + 'LightSource "distant" '
            output += self.paramsToPBRT(emitter.params, ltpbrt.emitterParam)


        elif emitter.type == 'spot':
            pass
        
        elif emitter.type == 'point':
            output += ('\t' * identation) + 'LightSource "point" '

            output += self.paramsToPBRT(emitter.params, ltpbrt.emitterParam)
            output += '\n'
            
        return output

    def paramsToPBRT(self, params, dictionary):
        output = ''
        for key in params:
            if key in dictionary:
                pbrtParam = dictionary[key]
                luxParam = params[key]
                output += '"' + luxParam.type + ' ' + pbrtParam + '" '

                if luxParam.type == 'string' or luxParam.type == 'bool':
                    output += '[ "' + str(luxParam.value) + '" ] '
                elif luxParam.type == 'color':
                    output += '[ ' + str(luxParam.value[0]) + ' ' + str(luxParam.value[1]) + ' ' + str(luxParam.value[2]) + ' ] '
                else:
                    output += '[ ' + str(luxParam.value) + ' ] '
                    
        output += '\n'

        return output
    
    def __init__(self, scene, filename):
        self.toPBRT(scene, filename)