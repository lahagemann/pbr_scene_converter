# -*- coding: utf-8 -*-

import mitsuba as mit
import mitsubaToPBRT as mtpbrt
import classes as directives
import numpy as np

def pbrt_writeParams(outfile, paramList, dictionary):
    for param in paramList:
        if param.name in dictionary:
            pbrt_param = dictionary[param.name]
            outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
            if param.val_type is 'string' or param.val_type is 'bool':
                outfile.write('[ "' + param.value + '" ] ')
            else:
                outfile.write('[ ' + param.value + ' ] ')

def pbrt_shapeString(shape):
    s = ''
    
    if shape.type == 'obj' or shape.type == 'ply':
        # if ref != None, set material reference with "NamedMaterial" command
        s = s + 'NamedMaterial "' + shape.material_ref + '"\n'
        s = s + 'Shape "plymesh" "string filename" [ "' + shape.filename + '" ]\n'
            
    elif shape.type == 'cube':
        # cube will be a triangle mesh
        pass
    
    elif shape.type == 'sphere':
        pass
            
    elif shape.type == 'cylinder':
        pass
        
    elif shape.type == 'rectangle':
        # rectangle will be a triangle mesh
        p0 = np.sum(scene.transform.matrix * np.array([-1, -1, 0, 1]), axis = 1)
        p1 = np.sum(scene.transform.matrix * np.array([1, -1, 0, 1]), axis = 1)
        p2 = np.sum(scene.transform.matrix * np.array([1, 1, 0, 1]), axis = 1)
        p3 = np.sum(scene.transform.matrix * np.array([-1, 1, 0, 1]), axis = 1)        

        s = s + 'Shape "trianglemesh" "integer indices" [ 0 1 2 0 2 3 ] "point P" '
        s = s + '[ ' + str(p0[0]) + ' ' + str(p0[1]) + ' ' + str(p0[2]) + ' '
        s = s + str(p1[0]) + ' ' + str(p1[1]) + ' ' + str(p1[2]) + ' '
        s = s + str(p2[0]) + ' ' + str(p2[1]) + ' ' + str(p2[2]) + ' '
        s = s + str(p3[0]) + ' ' + str(p3[1]) + ' ' + str(p3[2]) + ' ] '
                
        # normal for all 4 points in a rectangle is the same as face normal
        normal = np.cross(p2 - p0, p3 - p1)
        s = s + '"normal N" ['
        s = s + str(normal[0] + ' ' + str(normal[1]) + ' ' + str(normal[2]) + ' '
        s = s + str(normal[0] + ' ' + str(normal[1]) + ' ' + str(normal[2]) + ' '
        s = s + str(normal[0] + ' ' + str(normal[1]) + ' ' + str(normal[2]) + ' '
        s = s + str(normal[0] + ' ' + str(normal[1]) + ' ' + str(normal[2]) + ' '

        # float uv for triangle is default
        s = s + '"float uv" [ 0 0 1 0 1 1 0 1 ]\n'
            
    elif shape.type == 'disk':
            
    elif shape.type == 'hair':
            
    elif shape.type == 'heightfield':


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

            pbrt_writeParams(outfile, scene.integrator.params, mtpbrt.integratorParam)
            outfile.write('\n')

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

            pbrt_writeParams(outfile, scene.sensor.sampler.params, mtpbrt.samplerParam)
            outfile.write('\n')

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

            pbrt_writeParams(outfile, scene.sensor.film.params, mtpbrt.filmParam)
            outfile.write('\n')

        # sensor/camera
        if scene.sensor:
            outfile.write('Camera ')

            if scene.sensor.sensor_type in mtpbrt.sensorType:
                sensor_type = mtpbrt.sensorType[scene.sensor.sensor_type]
                outfile.write('"' + sensor_type + '" ')
            else:
                outfile.write('"perspective" ')

            pbrt_writeParams(outfile, scene.sensor.params, mtpbrt.sensorParam)
            outfile.write('\n')

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
                    outfile.write('Texture "' + id + '" "float" ')
                
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        pass #TODO
                
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
                            pass
    
                    tex_count += 1
                    outfile.write('\n')
        
            # case adapter: texture in adapter -> material
            elif isinstance(material, directives.AdapterMaterial):
                tex = material.material.texture
                
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.mat_id] = id
                
                    outfile.write('Texture "' + id + '" "spectrum" ')
                    
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        pass #TODO

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
                            pass
        
                    tex_count += 1
                    outfile.write('\n')
            
            # case material: texture field.
            else:
                tex = material.texture
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.mat_id] = id
                
                    outfile.write('Texture "' + id + '" "spectrum" ')
                
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        pass #TODO
                
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
                            pass

                    tex_count += 1
                    outfile.write('\n')


        # named material declaration
        for material in scene.materials:
            if isinstance(material, directives.BumpMap):
                outfile.write('MakeNamedMaterial "' + material.adapter.mat_id + '" ')
            
                outfile.write('\n')
            elif isinstance(material, directives.AdapterMaterial):
                outfile.write('MakeNamedMaterial "' + material.mat_id + '" ')

                outfile.write('\n')
            else:
                outfile.write('MakeNamedMaterial "' + material.mat_id + '" ')
                    
                outfile.write('\n')
                    
                    
        for shape in scene.shapes:
            if shape.emitter is not None:
                if shape.emitter.type == 'area':
                    outfile.write('AttributeBegin\n')
                    
                    
                
                    outfile.write('AttributeEnd\n')

            
            

        # end scene description
        outfile.write('WorldEnd\n')


def main():
    scene = mit.read_from_xml('/Users/luiza.hagemann/Development/pbr_scene_converter/test_files/mitsuba/staircase.xml')
    toPBRT(scene)

if  __name__ =='__main__': main()











