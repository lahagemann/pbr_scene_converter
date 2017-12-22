# -*- coding: utf-8 -*-

import mitsuba as mit
import mitsubaToPBRT as mtpbrt
import classes as directives
import numpy as np

def pbrt_writeParams(paramList, dictionary):
    s = ''
    for param in paramList:
        if param.name in dictionary:
            pbrt_param = dictionary[param.name]
            s += '"' + param.val_type + ' ' + pbrt_param + '" '
            if param.val_type is 'string' or param.val_type is 'bool':
                s += '[ "' + param.value + '" ] '
            else:
                s += '[ ' + param.value + ' ] '
                
    return s

def pbrt_shapeString(shape, numberOfTabs):
    autoTab = '\t'
    s = ''
    identity = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    if shape.type == 'obj' or shape.type == 'ply':
        if shape.transform is not None:
            if not np.array_equal(shape.transform.matrix, identity):
                s += (autoTab * numberOfTabs) + 'TransformBegin\n'
                s += (autoTab * (numberOfTabs + 1)) + 'Transform [ '
                
                m = shape.transform.matrix
                m_T = np.transpose(m)

                for i in range(0,4):
                    for j in range(0,4):
                        s += str(m_T[i][j])
                        s += ' '
                    
                s += ']\n'
                s += (autoTab * (numberOfTabs + 1)) + 'Shape "plymesh" "string filename" [ "' + shape.getParam('filename') + '" ]\n'
                s += (autoTab * numberOfTabs) + 'TransformEnd\n'
            else:
                s += (autoTab * numberOfTabs) + 'Shape "plymesh" "string filename" [ "' + shape.getParam('filename') + '" ]\n'
                
        else:
            s += (autoTab * numberOfTabs) + 'Shape "plymesh" "string filename" [ "' + shape.getParam('filename') + '" ]\n'
            
    elif shape.type == 'cube':
        # cube will be a triangle mesh (god help me)
        points = []
        
        points.append(np.sum(shape.transform.matrix * np.array([-1, -1, -1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([-1, 1, 1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([1, 1, -1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([1, -1, 1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([-1, 1, -1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([-1, -1, 1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([1, -1, -1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([1, 1, 1, 1]), axis = 1))
        
        points.append(points[5]), points.append(points[0]), points.append(points[3]), points.append(points[6]) # 8, 9, 10, 11
        points.append(points[7]), points.append(points[2]), points.append(points[1]), points.append(points[4]) # 12, 13, 14, 15
        points.append(points[4]), points.append(points[1]), points.append(points[0]), points.append(points[5]) # 16, 17, 18, 19
        points.append(points[6]), points.append(points[3]), points.append(points[2]), points.append(points[7]) # 20, 21, 22, 23
                
        s += (autoTab * numberOfTabs) + 'Shape "trianglemesh" '
        s += '"integer indices" [ 0 2 1 0 3 2 4 6 5 4 7 6 8 10 9 8 11 10 12 14 13 12 15 14 16 18 17 16 19 18 20 22 21 20 23 22 ] "point P" [ '
        
        for i in range(0, 24):
            s += str(points[i][0]) + ' ' + str(points[i][1]) + ' ' + str(points[i][2]) + ' '
            
        s += '] '
        
        #normal for all 4 points in a face are the same
        # faces: 1 = 0 1 2 3; 2 = 4 5 6 7; 3 = 8 9 10 11; 4 = 12 13 14 15; 5 = 16 17 18 19; 6 = 20 21 22 23;
        normalFace1 = np.cross((points[2] - points[0])[:3], (points[3] - points[1])[:3])
        normalFace2 = np.cross((points[6] - points[4])[:3], (points[7] - points[5])[:3])
        normalFace3 = np.cross((points[10] - points[8])[:3], (points[11] - points[9])[:3])
        normalFace4 = np.cross((points[14] - points[12])[:3], (points[15] - points[13])[:3])
        normalFace5 = np.cross((points[18] - points[16])[:3], (points[19] - points[17])[:3])
        normalFace6 = np.cross((points[22] - points[20])[:3], (points[23] - points[21])[:3])
        
        s += '"normal N" [ '
        for i in range(0, 4):
            s += str(normalFace1[0]) + ' ' + str(normalFace1[1]) + ' ' + str(normalFace1[2]) + ' '
        for i in range(0, 4):
            s += str(normalFace2[0]) + ' ' + str(normalFace2[1]) + ' ' + str(normalFace2[2]) + ' '
        for i in range(0, 4):
            s += str(normalFace3[0]) + ' ' + str(normalFace3[1]) + ' ' + str(normalFace3[2]) + ' '
        for i in range(0, 4):
            s += str(normalFace4[0]) + ' ' + str(normalFace4[1]) + ' ' + str(normalFace4[2]) + ' '
        for i in range(0, 4):
            s += str(normalFace5[0]) + ' ' + str(normalFace5[1]) + ' ' + str(normalFace5[2]) + ' '
        for i in range(0, 4):
            s += str(normalFace6[0]) + ' ' + str(normalFace6[1]) + ' ' + str(normalFace6[2]) + ' '
        
        s += '] '
        
        # default uv
        s += '"float uv" [ 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 ]\n'
            
    elif shape.type == 'sphere':
        s += (autoTab * numberOfTabs) + 'TransformBegin\n'
        s += (autoTab * (numberOfTabs + 1)) + 'Transform [ 1 0 0 0 0 1 0 0 0 0 1 0 ' + str(shape.center[0]) + ' ' + str(shape.center[1]) + ' ' + str(shape.center[2]) + ' ' + ' 1 ]\n'
        s += (autoTab * (numberOfTabs + 1)) + 'Shape "sphere" '
        #s += pbrt_writeParams(shape.params, mtpbrt.shapeParam)
        s += '\n'
        s += (autoTab * numberOfTabs) + 'TransformEnd\n'
        
    elif shape.type == 'cylinder':
        pass
        
    elif shape.type == 'rectangle':
        # rectangle will be a triangle mesh
        p0 = np.sum(shape.transform.matrix * np.array([-1, -1, 0, 1]), axis = 1)
        p1 = np.sum(shape.transform.matrix * np.array([1, -1, 0, 1]), axis = 1)
        p2 = np.sum(shape.transform.matrix * np.array([1, 1, 0, 1]), axis = 1)
        p3 = np.sum(shape.transform.matrix * np.array([-1, 1, 0, 1]), axis = 1)        

        s += (autoTab * numberOfTabs) + 'Shape "trianglemesh" "integer indices" [ 0 1 2 0 2 3 ] "point P" '
        s += '[ ' + str(p0[0]) + ' ' + str(p0[1]) + ' ' + str(p0[2]) + ' '
        s += str(p1[0]) + ' ' + str(p1[1]) + ' ' + str(p1[2]) + ' '
        s += str(p2[0]) + ' ' + str(p2[1]) + ' ' + str(p2[2]) + ' '
        s += str(p3[0]) + ' ' + str(p3[1]) + ' ' + str(p3[2]) + ' ] '
                
        # normal for all 4 points in a rectangle is the same as face normal
        normal = np.cross((p2 - p0)[:3], (p3 - p1)[:3])
        s += '"normal N" ['
        for i in range(0,4):
            s += str(normal[0]) + ' ' + str(normal[1]) + ' ' + str(normal[2]) + ' '

        # default uv
        s += '"float uv" [ 0 0 1 0 1 1 0 1 ]\n'
            
    elif shape.type == 'disk':
        pass
            
    elif shape.type == 'hair':
        pass
                        
    if shape.material is not None:
        s += (autoTab * numberOfTabs) + 'Material "'
                        
        if isinstance(shape.material, directives.AdapterMaterial):
            # convert material type
                        
            s += '" '
            params = pbrt_writeParams(shape.material.material.params, mtpbrt.materialParam)
            s += params + '\n'
                        
                        
        elif isinstance(shape.material, directives.Material):
            # convert material type
                        
            s += '" '
            params = pbrt_writeParams(shape.material.params, mtpbrt.materialParam)
            s += params + '\n'
                
    return s

def pbrt_lightString(emitter, numberOfTabs):
    s = ''
    autoTab = '\t'
    
    if emitter.type == 'envmap':
        if emitter.transform is not None:
            s += (autoTab * numberOfTabs) + 'TransformBegin\n'
            s += (autoTab * (numberOfTabs + 1)) + 'Transform '
            
            m = emitter.transform.matrix
            m_T = np.transpose(m)

            for i in range(0,4):
                for j in range(0,4):
                    s += str(m_T[i][j])
                    s += ' '
                    
            s += ']\n'
            
            s += (autoTab * (numberOfTabs + 1)) + 'LightSource "infinite" '
            s += pbrt_writeParams(emitter.params, mtpbrt.emitterParam)
            s += '\n'
            s += (autoTab * numberOfTabs) + 'TransformEnd\n'
            
        else:
            s += (autoTab * numberOfTabs) + 'LightSource "infinite" '
            s += pbrt_writeParams(emitter.params, mtpbrt.emitterParam)
            s += '\n'
    
    elif emitter.type == 'sunsky':
        s += (autoTab * numberOfTabs) + 'LightSource "distant" '
        
        sunDirection = emitter.getParam('sunDirection')
        
        s += '"point from" [ ' + str(sunDirection[0]) + ' ' + str(sunDirection[1]) + ' ' + str(sunDirection[2]) + ' ] '
        s += '"point to" [ 0.000000 0.000000 0.000000 ] '
        
        s += pbrt_writeParams(emitter.params, mtpbrt.emitterParam)
        s += '\n'
        
    elif emitter.type == 'spot':
        pass
    
    elif emitter.type == 'point':
        pass
        
    return s
    
def toPBRT(scene):
    np.set_printoptions(suppress=True)
    textures = {} # texture dictionary. entries are 'material_name' : 'texture_id'
    
    with open("scene.pbrt", 'w') as outfile:
        # scene directives
        # integrator
        if scene.integrator:
            outfile.write('Integrator ')

            if scene.integrator.int_type in mtpbrt.integratorType:
                int_type = mtpbrt.integratorType[scene.integrator.int_type]
                outfile.write('"' + int_type + '" ')
            else:
                outfile.write('"path" ')

            p = pbrt_writeParams(scene.integrator.params, mtpbrt.integratorParam)
            outfile.write(p + '\n')

        # transform
        if scene.sensor.transform.matrix:
            outfile.write('Transform ')
            outfile.write('[ ')

            # convert transform matrix to inverse transpose (PBRT default)
            m = scene.sensor.transform.matrix
            m_T = np.transpose(m)
            m_IT = np.linalg.inv(m_T)

            for i in range(0,4):
                for j in range(0,4):
                    outfile.write(str(m_IT[i][j]))
                    outfile.write(' ')

            outfile.write(']')
            outfile.write('\n')

        # sampler
        if scene.sensor.sampler:
            outfile.write('Sampler ')

            if scene.sensor.sampler.sampler_type in mtpbrt.samplerType:
                sampler_type = mtpbrt.samplerType[scene.sensor.sampler.sampler_type]
                outfile.write('"' + sampler_type + '" ')
            else:
                outfile.write('"sobol" ')

            p = pbrt_writeParams(scene.sensor.sampler.params, mtpbrt.samplerParam)
            outfile.write(p + '\n')

        # filter
        if scene.sensor.film.filter_type:
            outfile.write('PixelFilter ')

            if scene.sensor.film.filter_type in mtpbrt.filterType:
                filter_type = mtpbrt.filterType[scene.sensor.film.filter_type]
                outfile.write('"' + filter_type + '" ')
            else:
                outfile.write('"triangle" ')
    
            outfile.write('\n')

        # film
        if scene.sensor.film:
            outfile.write('Film ')

            if scene.sensor.film.film_type in mtpbrt.filmType:
                film_type = mtpbrt.filmType[scene.sensor.film.film_type]
                outfile.write('"' + film_type + '" ')
            else:
                outfile.write('"image" ')

            p = pbrt_writeParams(scene.sensor.film.params, mtpbrt.filmParam)
            outfile.write(p + '\n')

        # sensor/camera
        if scene.sensor:
            outfile.write('Camera ')

            if scene.sensor.sensor_type in mtpbrt.sensorType:
                sensor_type = mtpbrt.sensorType[scene.sensor.sensor_type]
                outfile.write('"' + sensor_type + '" ')
            else:
                outfile.write('"perspective" ')

            p = pbrt_writeParams(scene.sensor.params, mtpbrt.sensorParam)
            outfile.write(p + '\n')

        # scene description
        outfile.write('WorldBegin\n')
        
        # texture declaration
        tex_count = 1
        
        for material in scene.materials:
            # case bumpmap: texture with adapter texture
            if isinstance(material, directives.BumpMap):
                tex = material.texture
                
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.adapter.mat_id] = id
                
                    # outer texture for bumpmap is float. otherwise, spectrum
                    outfile.write('\tTexture "' + id + '" "float" ')
                
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        if tex.tex_type in mtpbrt.textureType:
                            tex_type = mtpbrt.textureType[tex.tex_type]
                            outfile.write('"' + tex_type + '" ')
                
                    for param in tex.params:
                        if param.name == 'filename':
                            outfile.write('"string filename" [ "' + param.value + '" ] ')
                        elif param.name == 'filterType':
                            if param.value == 'ewa':
                                outfile.write('"bool trilinear" [ "false" ] ')
                            else:
                                outfile.write('"bool trilinear" [ "true" ] ')
                        else:
                            # search the dictionary
                            p = pbrt_writeParams(tex.params, mtpbrt.textureParam)
                            outfile.write(p + '\n')
        
    
                    tex_count += 1
                    outfile.write('\n')
        
            # case adapter: texture in adapter -> material
            elif isinstance(material, directives.AdapterMaterial):
                tex = material.material.texture
                
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.mat_id] = id
                
                    outfile.write('\tTexture "' + id + '" "spectrum" ')
                    
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        if tex.tex_type in mtpbrt.textureType:
                            tex_type = mtpbrt.textureType[tex.tex_type]
                            outfile.write('"' + tex_type + '" ')

                    for param in tex.params:
                        if param.name == 'filename':
                            outfile.write('"string filename" [ "' + param.value + '" ] ')
                        elif param.name == 'filterType':
                            if param.value == 'ewa':
                                outfile.write('"bool trilinear" [ "false" ] ')
                            else:
                                outfile.write('"bool trilinear" [ "true" ] ')
                        else:
                            # search the dictionary
                            p = pbrt_writeParams(tex.params, mtpbrt.textureParam)
                            outfile.write(p + '\n')
        
                    tex_count += 1
                    outfile.write('\n')
            
            # case material: texture field.
            else:
                tex = material.texture
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.mat_id] = id
                
                    outfile.write('\tTexture "' + id + '" "spectrum" ')
                
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        if tex.tex_type in mtpbrt.textureType:
                            tex_type = mtpbrt.textureType[tex.tex_type]
                            outfile.write('"' + tex_type + '" ')
                
                    for param in tex.params:
                        if param.name == 'filename':
                            outfile.write('"string filename" [ "' + param.value + '" ] ')
                        elif param.name == 'filterType':
                            if param.value == 'ewa':
                                outfile.write('"bool trilinear" [ "false" ] ')
                            else:
                                outfile.write('"bool trilinear" [ "true" ] ')
                        else:
                            # search the dictionary
                            p = pbrt_writeParams(tex.params, mtpbrt.textureParam)
                            outfile.write(p + '\n')
        

                    tex_count += 1
                    outfile.write('\n')


        # named material declaration
        for material in scene.materials:
            if isinstance(material, directives.BumpMap):
                outfile.write('\tMakeNamedMaterial "' + material.adapter.mat_id + '" ')
                # convert material type
                mitsubaType = material.adapter.material.mat_type
                if mitsubaType in mtpbrt.materialType:
                    pbrtType = mtpbrt.materialType[mitsubaType]
                    outfile.write('"string type" [ "' + pbrtType + '" ] ')
                else:  
                    outfile.write('"string type" [ "matte" ] ')

            
                # if material has texture, put param "texture Kd" + reference
                if material.texture is not None:
                    outfile.write('"texture bumpmap" [ "' + textures[material.adapter.mat_id] + '" ] ')

                # convert all other params
                p = pbrt_writeParams(material.adapter.material.params, mtpbrt.materialParam)
                outfile.write(p + '\n')
            
            elif isinstance(material, directives.AdapterMaterial):
                outfile.write('\tMakeNamedMaterial "' + material.mat_id + '" ')
                
                # convert material type
                mitsubaType = material.material.mat_type
                if mitsubaType in mtpbrt.materialType:
                    pbrtType = mtpbrt.materialType[mitsubaType]
                    outfile.write('"string type" [ "' + pbrtType + '" ] ')
                else:  
                    outfile.write('"string type" [ "matte" ] ')
            
                # if material has texture, put param "texture Kd" + reference
                if material.material.texture is not None: 
                    outfile.write('"texture Kd" [ "' + textures[material.mat_id] + '" ] ')

                # convert all other params
                p = pbrt_writeParams(material.material.params, mtpbrt.materialParam)
                outfile.write(p + '\n')

            else:
                outfile.write('\tMakeNamedMaterial "' + material.mat_id + '" ')

                # convert material type
                mitsubaType = material.mat_type
                if mitsubaType in mtpbrt.materialType:
                    pbrtType = mtpbrt.materialType[mitsubaType]
                    outfile.write('"string type" [ "' + pbrtType + '" ] ')
                else:  
                    outfile.write('"string type" [ "matte" ] ')
            
                # if material has texture, put param "texture Kd" + reference
                if material.texture is not None: 
                    outfile.write('"texture Kd" [ "' + textures[material.mat_id] + '" ] ')

                # convert all other params
                p = pbrt_writeParams(material.params, mtpbrt.materialParam)
                outfile.write(p + '\n')
                    
                outfile.write('\n')
                    
                    
        currentRefMaterial = ''
        for shape in scene.shapes:
            if shape.emitter is not None:
                # child emitter will ALWAYS be area emitter
                outfile.write('AttributeBegin\n')
                        
                outfile.write('\tAreaLightSource "diffuse" ')
                p = pbrt_writeParams(shape.emitter.params, mtpbrt.emitterParam)
                outfile.write(p + '\n')
                        
                shapeString = pbrt_shapeString(shape, 2)
                outfile.write(shapeString)
                        
                ref = shape.getParam('id')
                print ref
                        
                if not ref == '':
                    if ref != currentRefMaterial:
                        outfile.write('\tNamedMaterial "' + ref + '"\n')
                        currentRefMaterial = ref
                        
                outfile.write('AttributeEnd\n')
                        
            else:
                # if shape has ref material, then make reference
                shapeString = pbrt_shapeString(shape,1)
                
                ref = shape.getParam('id')
                        
                if not ref == '':
                    if ref != currentRefMaterial:
                        outfile.write('\tNamedMaterial "' + ref + '"\n')
                        outfile.write(shapeString)
                        currentRefMaterial = ref
                    else:
                        outfile.write(shapeString)
                else:
                    outfile.write(shapeString)
                    
                    
        for light in scene.lights:
            l = pbrt_lightString(light, 1)
            outfile.write(l)
            
        # end scene description
        outfile.write('WorldEnd\n')


def main():
    scene = mit.read_from_xml('/Users/luiza.hagemann/Development/pbr_scene_converter/test_files/mitsuba/dining-room.xml')
    toPBRT(scene)

if  __name__ =='__main__': main()











