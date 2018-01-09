import numpy as np
import sys

sys.path.insert(0, 'core/')
from Directives import BumpMap

sys.path.insert(0, 'dictionaries')
from dictionaries import MitsubaPBRTv3 as mtpbrt

class MitsubaToPBRTv3:
    def toPBRT(self, scene, filename):
        np.set_printoptions(suppress=True)
        with open(filename, 'w') as outfile:
            sceneDirectives = self.sceneDirectivesToPBRT(scene)
            outfile.write(sceneDirectives)

            worldDescription = self.worldDescriptionToPBRT(scene)
            outfile.write(worldDescription)

        if self.copySkydome:
            pass

    def sceneDirectivesToPBRT(self, scene):
        output = ''

        if scene.integrator is not None:
            output += 'Integrator '

            if scene.integrator.type in mtpbrt.integratorType:
                type = mtpbrt.integratorType[scene.integrator.type]
                output += '"' + type + '" '

            output += self.paramsToPBRT(scene.integrator.params, mtpbrt.integratorParam)

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

            if scene.sensor.sampler.type in mtpbrt.samplerType:
                type = mtpbrt.samplerType[scene.sensor.sampler.type]
                output += '"' + type + '" '

            output += self.paramsToPBRT(scene.sensor.sampler.params, mtpbrt.samplerParam)

        if scene.sensor.film.filter:
            output += 'PixelFilter '

            if scene.sensor.film.filter in mtpbrt.filterType:
                filter = mtpbrt.filterType[scene.sensor.film.filter]
                output += '"' + filter + '" '
            else:
                output += '"triangle" '
    
            output += '\n'


        if scene.sensor.film is not None:
            output += 'Film '

            if scene.sensor.film.type in mtpbrt.filmType:
                type = mtpbrt.filmType[scene.sensor.film.type]
                output += '"' + type + '" '
            else:
                output += '"image" '

            output += self.paramsToPBRT(scene.sensor.film.params, mtpbrt.filmParam)

        if scene.sensor is not None:
            output += 'Camera '

            if scene.sensor.type in mtpbrt.sensorType:
                type = mtpbrt.sensorType[scene.sensor.type]
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

            output += self.paramsToPBRT(scene.sensor.params, mtpbrt.sensorParam)

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
                
                if isinstance(material, BumpMap):
                    materialTextureRef[material.material.id] = id
                    output += '\tTexture "' + id + '" "float" '
                else:
                    materialTextureRef[material.id] = id
                    output += '\tTexture "' + id + '" "spectrum" '

                if material.texture.type == 'bitmap':
                    output += '"imagemap" '
                else:
                    if material.texture.type in mtpbrt.textureType:
                        type = mtpbrt.textureType[material.texture.type]
                        output += '"' + type + '" '
            
                for paramName in material.texture.params:
                    if paramName == 'filename':
                        output += '"string filename" [ "' + material.texture.params[paramName] + '" ] '
                    elif paramName == 'filterType':
                        if material.texture.params[paramName] == 'ewa':
                            output += '"bool trilinear" [ "false" ] '
                        else:
                            output += '"bool trilinear" [ "true" ] '
                    else:
                        # search the dictionary
                        output += self.paramsToPBRT(material.texture.params, mtpbrt.textureParam)

                textureCount += 1

        for material in scene.materials:
            if isinstance(material, BumpMap):
                output += '\tMakeNamedMaterial "' + material.material.id + '" '
                mitsubaType = material.material.type
            else:
                output += '\tMakeNamedMaterial "' + material.id + '" '
                mitsubaType = material.type

            if mitsubaType in mtpbrt.materialType:
                pbrtType = mtpbrt.materialType[mitsubaType]
                output += '"string type" [ "' + pbrtType + '" ] '

            if material.texture is not None:
                if isinstance(material, BumpMap):
                    output += '"texture bumpmap" [ "' + materialTextureRef[material.material.id] + '" ] '
                    output += self.materialParamsToPBRT(material.material.params, mtpbrt.materialParam, pbrtType)
                else:
                    output += '"texture Kd" [ "' + materialTextureRef[material.id] + '" ] '
                    output += self.materialParamsToPBRT(material.params, mtpbrt.materialParam, pbrtType)

        currentRefMaterial = ''
        for shape in scene.shapes:
            if shape.emitter is not None:
                # child emitter will ALWAYS be area emitter
                output += '\tAttributeBegin\n'
                        
                output += '\t\tAreaLightSource "diffuse" '
                output += self.paramsToPBRT(shape.emitter.params, mtpbrt.emitterParam)
                      
                if 'id' in shape.params:        
                    if shape.params['id'] != currentRefMaterial:
                        output += '\t\tNamedMaterial "' + str(shape.params['id'].value) + '"\n'
                        currentRefMaterial = shape.params['id']

                output += self.shapeToPBRT(shape, 2)
                        
                output += '\tAttributeEnd\n'

            else:
                # if shape has ref material, then make reference  
                if 'id' in shape.params:        
                    if shape.params['id'] != currentRefMaterial:
                        output += '\tNamedMaterial "' + ref + '"\n'
                        output += self.shapeToPBRT(shape, 1)
                        currentRefMaterial = shape.params['id']
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
        identity = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        if shape.material is not None:
            output += ('\t' * identation) + 'Material "'

            if isinstance(shape.material, BumpMap):
                output += ('\t' * identation) + 'Material "' + shape.material.material.id + '" '
                mitsubaType = shape.material.material.type
            else:
                output += ('\t' * identation) + 'Material "' + shape.material.id + '" '
                mitsubaType = shape.material.type

            if mitsubaType in mtpbrt.materialType:
                pbrtType = mtpbrt.materialType[mitsubaType]
                output += '"string type" [ "' + pbrtType + '" ] '

        if shape.type == 'obj' or shape.type == 'ply':
            if shape.transform is not None and shape.transform.matrix:
                if not np.array_equal(shape.transform.matrix, identity):
                    output += ('\t' * identation) + 'TransformBegin\n'
                    output += ('\t' * (identation + 1)) + 'Transform [ '
                    
                    m_T = np.transpose(shape.transform.matrix)

                    for i in range(0,4):
                        for j in range(0,4):
                            output += str(m_T[i][j])
                            output += ' '
                        
                    output += ']\n'
                    output += ('\t' * (identation + 1)) + 'Shape "plymesh" "string filename" [ "' + shape.params['filename'].value + '" ]\n'
                    output += ('\t' * identation) + 'TransformEnd\n'
                else:
                    output += ('\t' * identation) + 'Shape "plymesh" "string filename" [ "' + shape.params['filename'].value + '" ]\n'
                
            else:
                output += ('\t' * identation) + 'Shape "plymesh" "string filename" [ "' + shape.params['filename'].value + '" ]\n'
            
        elif shape.type == 'cube':
            # cube will be a triangle mesh (god help me)
            points = []
            
            points.append(np.sum(shape.transform.matrix * np.array([-1, -1, -1, 1]), axis = 1))
            points.append(np.sum(shape.transform.matrix * np.array([1, -1, -1, 1]), axis = 1))
            points.append(np.sum(shape.transform.matrix * np.array([1, 1, -1, 1]), axis = 1))
            points.append(np.sum(shape.transform.matrix * np.array([-1, 1, -1, 1]), axis = 1))
            points.append(np.sum(shape.transform.matrix * np.array([-1, -1, 1, 1]), axis = 1))
            points.append(np.sum(shape.transform.matrix * np.array([1, -1, 1, 1]), axis = 1))
            points.append(np.sum(shape.transform.matrix * np.array([1, 1, 1, 1]), axis = 1))
            points.append(np.sum(shape.transform.matrix * np.array([-1, 1, 1, 1]), axis = 1))
            
            # 8, 9, 10, 11
            points.append(points[1]), points.append(points[2]), points.append(points[6]), points.append(points[5]) 
            # 12, 13, 14, 15
            points.append(points[0]), points.append(points[4]), points.append(points[7]), points.append(points[3])
            # 16, 17, 18, 19 
            points.append(points[3]), points.append(points[2]), points.append(points[6]), points.append(points[7]) 
            # 20, 21, 22, 23
            points.append(points[0]), points.append(points[1]), points.append(points[5]), points.append(points[4]) 
                    
            output += ('\t' * identation) + 'Shape "trianglemesh" '
            output += '"integer indices" [ 0 2 1 0 2 3 4 6 5 4 6 7 8 10 11 8 10 9 12 14 13 12 14 15 16 18 17 16 18 19 20 22 21 20 22 23 ] "point P" [ '
            
            for i in range(0, 24):
                output += str(points[i][0]) + ' ' + str(points[i][1]) + ' ' + str(points[i][2]) + ' '
                
            output += '] '
            
            #normal for all 4 points in a face are the same
            # faces: 1 = 0 1 2 3; 2 = 4 5 6 7; 3 = 8 9 10 11; 4 = 12 13 14 15; 5 = 16 17 18 19; 6 = 20 21 22 23;
            normalFace1 = np.cross((points[2] - points[0])[:3], (points[3] - points[1])[:3])
            normalFace2 = np.cross((points[6] - points[4])[:3], (points[7] - points[5])[:3])
            normalFace3 = np.cross((points[10] - points[8])[:3], (points[9] - points[11])[:3])
            normalFace4 = np.cross((points[14] - points[12])[:3], (points[15] - points[13])[:3])
            normalFace5 = np.cross((points[18] - points[16])[:3], (points[19] - points[17])[:3])
            normalFace6 = np.cross((points[22] - points[20])[:3], (points[23] - points[21])[:3])
            
            output += '"normal N" [ '
            for i in range(0, 4):
                output += str(normalFace1[0]) + ' ' + str(normalFace1[1]) + ' ' + str(normalFace1[2]) + ' '
            for i in range(0, 4):
                output += str(normalFace2[0]) + ' ' + str(normalFace2[1]) + ' ' + str(normalFace2[2]) + ' '
            for i in range(0, 4):
                output += str(normalFace3[0]) + ' ' + str(normalFace3[1]) + ' ' + str(normalFace3[2]) + ' '
            for i in range(0, 4):
                output += str(normalFace4[0]) + ' ' + str(normalFace4[1]) + ' ' + str(normalFace4[2]) + ' '
            for i in range(0, 4):
                output += str(normalFace5[0]) + ' ' + str(normalFace5[1]) + ' ' + str(normalFace5[2]) + ' '
            for i in range(0, 4):
                output += str(normalFace6[0]) + ' ' + str(normalFace6[1]) + ' ' + str(normalFace6[2]) + ' '
            
            output += '] '
            
            # default uv
            output += '"float uv" [ 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 ]\n'
            
        elif shape.type == 'sphere':
            if shape.params['center']:
                center = shape.params['center']
            else:
                center = [0,0,0]

            output += ('\t' * identation) + 'TransformBegin\n'
            output += ('\t' * (identation + 1)) + 'Transform [ 1 0 0 0 0 1 0 0 0 0 1 0 ' + str(center[0]) + ' ' + str(center[1]) + ' ' + str(center[2]) + ' ' + ' 1 ]\n'
            output += ('\t' * (identation + 1)) + 'Shape "sphere" '
            output += self.paramsToPBRT(shape.params, mtpbrt.shapeParam)
            output += '\n'
            output += ('\t' * identation) + 'TransformEnd\n'
        
        elif shape.type == 'cylinder':
            pass
        
        elif shape.type == 'rectangle':
            # rectangle will be a triangle mesh
            p0 = np.sum(shape.transform.matrix * np.array([-1, -1, 0, 1]), axis = 1)
            p1 = np.sum(shape.transform.matrix * np.array([1, -1, 0, 1]), axis = 1)
            p2 = np.sum(shape.transform.matrix * np.array([1, 1, 0, 1]), axis = 1)
            p3 = np.sum(shape.transform.matrix * np.array([-1, 1, 0, 1]), axis = 1)        

            output += ('\t' * identation) + 'Shape "trianglemesh" "integer indices" [ 0 1 2 0 2 3 ] "point P" '
            output += '[ ' + str(p0[0]) + ' ' + str(p0[1]) + ' ' + str(p0[2]) + ' '
            output += str(p1[0]) + ' ' + str(p1[1]) + ' ' + str(p1[2]) + ' '
            output += str(p2[0]) + ' ' + str(p2[1]) + ' ' + str(p2[2]) + ' '
            output += str(p3[0]) + ' ' + str(p3[1]) + ' ' + str(p3[2]) + ' ] '
                    
            # normal for all 4 points in a rectangle is the same as face normal
            normal = np.cross((p2 - p0)[:3], (p3 - p1)[:3])
            output += '"normal N" ['
            for i in range(0,4):
                output += str(normal[0]) + ' ' + str(normal[1]) + ' ' + str(normal[2]) + ' '

            output += '] '

            # default uv
            output += '"float uv" [ 0 0 1 0 1 1 0 1 ]\n'
            
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
                output += ('\t' * (identation + 1)) + 'Transform '
                
                m = emitter.transform.matrix
                m_T = np.transpose(m)

                for i in range(0,4):
                    for j in range(0,4):
                        output += str(m_T[i][j])
                        output += ' '
                        
                output += ']\n'
                
                output += ('\t' * (identation + 1)) + 'LightSource "infinite" '

                if 'filename' in emitter.params:
                    output += '"string mapname" [ "' + emitter.params['filename'].value + '" ] '

                output += self.paramsToPBRT(emitter.params, mtpbrt.emitterParam)
                output += '\n'
                output += ('\t' * identation) + 'TransformEnd\n'
                
            else:
                output += ('\t' * identation) + 'LightSource "infinite" '
                
                if 'filename' in emitter.params:
                    output += '"string mapname" [ "' + emitter.params['filename'].value + '" ] '

                output += self.paramsToPBRT(emitter.params, mtpbrt.emitterParam)
                output += '\n'
        
        elif emitter.type == 'sunsky':
            output += ('\t' * identation) + 'LightSource "distant" '
            
            if 'sunDirection' in emitter.params:    
                output += '"point from" [ ' + str(sunDirection[0]) + ' ' + str(sunDirection[1]) + ' ' + str(sunDirection[2]) + ' ] '
                output += '"point to" [ 0.000000 0.000000 0.000000 ] '
            
            output += self.paramsToPBRT(emitter.params, mtpbrt.emitterParam)
            output += '\n'

            output += ('\t' * identation) + 'TransformBegin\n'
            output += ('\t' * (identation + 1)) + 'Transform [ -1 0 0 0 0 0 -1 0 0 1 0 0 0 0 0 1 ]\n'
            output += ('\t' * (identation + 1)) + 'LightSource "infinite" "string mapname" [ "Skydome.pfm" ]\n'
            output += ('\t' * identation) + 'TransformEnd\n'

            self.copySkydome = True
            
        elif emitter.type == 'sun':
            output += ('\t' * identation) + 'TransformBegin\n'
            output += ('\t' * (identation + 1)) + 'Transform [ -1 0 0 0 0 0 -1 0 0 1 0 0 0 0 0 1 ]\n'
            output += ('\t' * (identation + 1)) + 'LightSource "infinite" "string mapname" [ "Skydome.pfm" ]\n'
            output += ('\t' * identation) + 'TransformEnd\n'

            self.copySkydome = True

        elif emitter.type == 'sky':
            output += ('\t' * identation) + 'LightSource "distant" '
            
            if 'sunDirection' in emitter.params:    
                output += '"point from" [ ' + str(sunDirection[0]) + ' ' + str(sunDirection[1]) + ' ' + str(sunDirection[2]) + ' ] '
                output += '"point to" [ 0.000000 0.000000 0.000000 ] '
            
            output += self.paramsToPBRT(emitter.params, mtpbrt.emitterParam)
            output += '\n'

        elif emitter.type == 'spot':
            pass
        
        elif emitter.type == 'point':
            output += ('\t' * identation) + 'LightSource "point" '

            output += self.paramsToPBRT(emitter.params, mtpbrt.emitterParam)
            output += '\n'
            
        return output

    def paramsToPBRT(self, params, dictionary):
        output = ''
        for key in params:
            if key in dictionary:
                pbrtParam = dictionary[key]
                mitsubaParam = params[key]
                output += '"' + mitsubaParam.type + ' ' + pbrtParam + '" '

                if mitsubaParam.type is 'string' or mitsubaParam.type is 'bool':
                    output += '[ "' + str(mitsubaParam.value) + '" ] '
                elif mitsubaParam.type is 'rgb' or mitsubaParam.type is 'spectrum':
                    output += '[ ' + str(mitsubaParam.value[0]) + ' ' + str(mitsubaParam.value[1]) + ' ' + str(mitsubaParam.value[2]) + ' ] '
                else:
                    output += '[ ' + str(mitsubaParam.value) + ' ] '
                    
        output += '\n'

        return output

    def materialParamsToPBRT(self, params, dictionary, pbrtType):
        output = ''
        for key in params:
            if key == 'alpha':
                if pbrtType == 'metal' or pbrtType == 'substrate' or pbrtType == 'mirror':
                    mitsubaParam = params[key]
                    output += '"float uroughness" [ ' + str(mitsubaParam.value) + '] '
                    output += '"float vroughness" [ ' + str(mitsubaParam.value) + '] '
                    output += '"bool remaproughness" [ "false" ]'
            else:
                print "oi"
                if key in dictionary:
                    pbrtParam = dictionary[key]
                    mitsubaParam = params[key]
                    output += '"' + mitsubaParam.type + ' ' + pbrtParam + '" '

                    if mitsubaParam.type is 'string' or mitsubaParam.type is 'bool':
                        output += '[ "' + str(mitsubaParam.value) + '" ] '
                    elif mitsubaParam.type is 'rgb' or mitsubaParam.type is 'spectrum':
                        output += '[ ' + str(mitsubaParam.value[0]) + ' ' + str(mitsubaParam.value[1]) + ' ' + str(mitsubaParam.value[2]) + ' ] '
                    else:
                        output += '[ ' + str(mitsubaParam.value) + ' ] '
                    
        
        output += '\n'

        return output

    def __init__(self, scene, filename):
        self.copySkydome = False
        self.toPBRT(scene, filename)