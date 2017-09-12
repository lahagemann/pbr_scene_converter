# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import classes as directives

def extract_params(element):
    lst = []
    
    for attribute in element:
        param = directives.Param()
        
        param.val_type = attribute.tag
        param.name = attribute.attrib.get('name')
        param.value = attribute.attrib.get('value')
        
        lst.append(param)

    return lst

def filter_params(list, param_type):
    lst = [x for x in list if not x.val_type == param_type]
    return lst


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

    #scene.world = load_world(scene_element)

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
        
        #first: check bump map case
        if material.get('type') == 'bumpmap':
            pass
            # do some shit
        
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
                material_list.append(adapter)
                
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
                material_list.append(mat)

    return material_list

def test_directives():
    #scene = read_from_xml('/home/grad/lahagemann/scene_converter/test_files/mitsuba/staircase.xml')
    scene = read_from_xml('/Users/luiza.hagemann/Development/pbr_scene_converter/test_files/mitsuba/staircase.xml')
    
    print '---- SCENE DIRECTIVES ----'

    print ('integrator', scene.integrator.int_type)
    print 'params:'
    for param in scene.integrator.params:
        print (param.val_type, param.name, param.value)
    print '-----'

    print ('sensor', scene.sensor.sensor_type)
    print 'params:'
    for param in scene.sensor.params:
        print (param.val_type, param.name, param.value)
    print '-----'

    print ('transform', scene.sensor.transform.name, scene.sensor.transform.matrix)
    print '-----'

    print ('film', scene.sensor.film.film_type, scene.sensor.film.filter_type)
    print 'params:'
    for param in scene.sensor.film.params:
        print (param.val_type, param.name, param.value)
    print '-----'

    print ('sampler', scene.sensor.sampler.sampler_type)
    print 'params:'
    for param in scene.sensor.sampler.params:
        print (param.val_type, param.name, param.value)
    print '-----'

def test_materials():
    scene = read_from_xml('/Users/luiza.hagemann/Development/pbr_scene_converter/test_files/mitsuba/staircase.xml')

    print '---- MATERIALS ----'

    for material in scene.materials:
        if isinstance(material, directives.AdapterMaterial):
            print 'Adapter'
            print (material.mat_type, material.mat_id)
            print 'Adapted Material'
            print (material.material.mat_type, material.material.mat_id)
            print 'params'
            for param in material.material.params:
                print (param.val_type, param.name, param.value)
            if material.material.texture is not None:
                print 'texture'
                print (material.material.texture.name, material.material.texture.tex_type)
                print 'tex params'
                for param in material.material.texture.params:
                    print (param.val_type, param.name, param.value)

        else:
            print 'Material'
            print (material.mat_type, material.mat_id)
            print 'params'
            for param in material.params:
                print (param.val_type, param.name, param.value)
            if material.texture is not None:
                print 'texture'
                print (material.texture.name, material.texture.tex_type)
                print 'tex params'
                for param in material.texture.params:
                    print (param.val_type, param.name, param.value)

        print '-----'

def main():
    test_directives()
    test_materials()

if  __name__ =='__main__':main()

#def load_world(scene):
#    pass

