# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import numpy as np
import classes as directives


def extract_params(element):
    lst = []
    for attribute in element:
        param = directives.Param()
        
        param.val_type = attribute.tag
        
        if param.val_type == 'ref':
            param.name = 'id'    
        else:
            param.name = attribute.attrib.get('name')
        
        if param.val_type == 'point' or param.val_type == 'vector':
            param.value = np.array([attribute.attrib.get('x'), attribute.attrib.get('y'), attribute.attrib.get('z')])
        elif param.val_type == 'ref':
            param.value = attribute.attrib.get('id')
        else:
            param.value = attribute.attrib.get('value')
        
        lst.append(param)

    return lst

def filter_params(list, param_type):
    lst = [x for x in list if not x.val_type == param_type]
    return lst
    
def extract_material(material):
    m = None
    
    #first: check bump map case
    if material.get('type') == 'bumpmap':
        bumpmap = directives.BumpMap()
        
        # texture
        texture_elem = material.find('texture')
        
        if texture_elem is not None:
            texture = directives.Texture()
        
            texture.name = texture_elem.attrib.get('name')
            texture.tex_type = texture_elem.attrib.get('type')
            texture.params = extract_params(texture_elem)
        
            bumpmap.texture = texture
        
        else:
            bumpmap.texture = None
        
        # adapter
        adapter_elem = material.find('bsdf')
        
        
        # check if material is adapter or regular
        adapted_mat_elem = adapter_elem.find('bsdf')
        if adapted_mat_elem is not None:
        
            # material = adapter material (twosided usually)
            adapter = directives.AdapterMaterial()
            adapter.mat_type = adapter_elem.attrib.get('type')
            adapter.mat_id = adapter_elem.attrib.get('id')
            
            # adapted_mat = adapted material (diffuse or wtv)
            adapted_mat = directives.Material()
            adapted_mat.mat_type = adapted_mat_elem.get('type')
                
            # get other material parameters
            adapted_mat.params = extract_params(adapted_mat_elem)
            adapted_mat.params = filter_params(adapted_mat.params, 'texture')
            
            adapter.material = adapted_mat
            bumpmap.adapter = adapter
            m = bumpmap
            
        else:
            mat = directives.Material()
            
            mat.mat_type = material.attrib.get('type')
            mat.mat_id = material.attrib.get('id')

            # get other material parameters
            mat.params = extract_params(material)
            
            bumpmap.adapter = mat
            m = bumpmap
                    
    else:
        # check if material is adapter or regular
        adapted_mat_elem = material.find('bsdf')
        if adapted_mat_elem is not None:
        
            # material = adapter material (twosided usually)
            adapter = directives.AdapterMaterial()
            adapter.mat_type = material.attrib.get('type')
            adapter.mat_id = material.attrib.get('id')
            
            # adapted_mat = adapted material (diffuse or wtv)
            adapted_mat = directives.Material()
            adapted_mat.mat_type = adapted_mat_elem.get('type')
            
            # check texture
            texture_elem = adapted_mat_elem.find('texture')
            if texture_elem is not None:
                texture = directives.Texture()
                
                texture.name = texture_elem.attrib.get('name')
                texture.tex_type = texture_elem.attrib.get('type')
                texture.params = extract_params(texture_elem)
                    
                adapted_mat.texture = texture
                    
            else:
                adapted_mat.texture = None
                
            # get other material parameters
            adapted_mat.params = extract_params(adapted_mat_elem)
            adapted_mat.params = filter_params(adapted_mat.params, 'texture')
            
            adapter.material = adapted_mat
            m = adapter
            
        else:
            mat = directives.Material()
            
            mat.mat_type = material.attrib.get('type')
            mat.mat_id = material.attrib.get('id')

            # check texture
            texture_elem = material.find('texture')
            if texture_elem is not None:
                texture = directives.Texture()
        
                texture.name = texture_elem.attrib.get('name')
                texture.tex_type = texture_elem.attrib.get('type')
                texture.params = extract_params(texture_elem)
                
                mat.texture = texture
            
            else:
                mat.texture = None

            # get other material parameters
            mat.params = extract_params(material)
            mat.params = filter_params(mat.params, 'texture')
            m = mat
                
    return m

def read_from_xml(filename):
    tree = ET.parse(filename)
    scene_element = tree.getroot()

    scene = load_scene(scene_element)

    return scene

def load_scene(scene_element):
    scene = directives.Scene()

    scene.integrator = load_integrator(scene_element)
    scene.sensor = load_sensor(scene_element)
    scene.materials = load_materials(scene_element)
    scene.shapes = load_shapes(scene_element)
    scene.lights = load_lights(scene_element)
    
    return scene
    
def load_integrator(scene):
    integrator = directives.Integrator()
    integrator_element = scene.find('integrator')
    
    # extract integrator type
    integrator.int_type = integrator_element.attrib.get('type')
    
    # extract all aditional parameters
    integrator.params = extract_params(integrator_element)
    
    return integrator

def load_sensor(scene):
    np.set_printoptions(suppress=True)
    
    sensor = directives.Sensor()
    sensor_element = scene.find('sensor')

    # extract sensor type
    sensor.sensor_type = sensor_element.attrib.get('type')

    # sensor has:   parameters
    #               transform, sampler, film

    # transform setup
    sensor.transform.name = sensor_element.find('transform').get('name')
    
    matrix = sensor_element.find('transform').find('matrix').get('value')
    sensor.transform.matrix = map(float, matrix.strip().split(' '))
    # formats matrix into 4x4 pattern
    sensor.transform.matrix = [sensor.transform.matrix[i:i + 4] for i in xrange(0, len(sensor.transform.matrix), 4)]

    # sampler setup
    sampler_element = sensor_element.find('sampler')
    sensor.sampler.sampler_type = sampler_element.get('type')
    sensor.sampler.params = extract_params(sampler_element)
    
    # film setup
    film_element = sensor_element.find('film')
    sensor.film.film_type = film_element.get('type')
    sensor.film.filter_type = film_element.find('rfilter').get('type')

    sensor.film.params = extract_params(film_element)
    sensor.film.params = filter_params(sensor.film.params, 'rfilter')
    
    # other params
    sensor.params = extract_params(sensor_element)
    sensor.params = filter_params(sensor.params, 'transform')
    sensor.params = filter_params(sensor.params, 'film')
    sensor.params = filter_params(sensor.params, 'sampler')

    return sensor

def load_materials(scene):
    material_list = []
    
    for material in scene.findall('bsdf'):
        mat = extract_material(material)
        if mat is not None:
            material_list.append(mat)

    return material_list

def load_shapes(scene):
    shape_list = []
    for shape in scene.findall('shape'):
        type = shape.get('type')
        s = directives.Shape()
        
        if type == 'sphere':
            p = shape.find('point')
            if p is not None:
                s.center = np.array([p.get('x'), p.get('y'), p.get('z')])
                
        s.type = type

        if shape.find('transform') is not None:
            s.transform.name = shape.find('transform').get('name')
            
            matrix = shape.find('transform').find('matrix').get('value')
            s.transform.matrix =  map(float, matrix.strip().split(' '))
            # formats matrix into 4x4 pattern
            s.transform.matrix = [s.transform.matrix[i:i + 4] for i in xrange(0, len(s.transform.matrix), 4)]
            
        if shape.find('emitter') is not None:
            s.emitter = directives.Emitter()
            s.emitter.type = shape.find('emitter').get('type')
            
            if shape.find('emitter').find('transform') is not None:
                s.emitter.transform = directives.Transform()
                matrix = shape.find('emitter').find('transform').find('matrix').get('value')
                s.emitter.transform.matrix =  map(float, matrix.strip().split(' '))
                # formats matrix into 4x4 pattern
                s.emitter.transform.matrix = [s.emitter.transform.matrix[i:i + 4] for i in xrange(0, len(s.emitter.transform.matrix), 4)]
            
            s.emitter.params = extract_params(shape.find('emitter'))
            s.emitter.params = filter_params(s.emitter.params, 'transform')
        
        material_elem = shape.find('bsdf')
        
        if material_elem is not None:
            s.material = extract_material(material_elem)

        s.params = extract_params(shape)
        s.params = filter_params(s.params, 'transform')
        s.params = filter_params(s.params, 'bsdf')
        s.params = filter_params(s.params, 'emitter')
        
        print s.transform.matrix
        
        shape_list.append(s)
        
    for s in shape_list:
        print s.transform.matrix
        
    return shape_list
    
def load_lights(scene):
    light_list = []
    
    for emitter in scene.findall('emitter'):    
        e = directives.Emitter()
        e.type = emitter.get('type')
            
        if emitter.find('transform') is not None:
            e.transform = directives.Transform()
            matrix = emitter.find('transform').find('matrix').get('value')
            e.transform.matrix =  map(float, matrix.strip().split(' '))
            # formats matrix into 4x4 pattern
            e.transform.matrix = [e.transform.matrix[i:i + 4] for i in xrange(0, len(e.transform.matrix), 4)]
            
        e.params = extract_params(emitter)
        e.params = filter_params(e.params, 'transform')
        
        light_list.append(e)
    
    return light_list
          
           
def main():
    scene = read_from_xml('/home/grad/lahagemann/pbr_scene_converter/test_files/mitsuba/staircase.xml')

if  __name__ =='__main__':main()

#def load_world(scene):
#    pass

