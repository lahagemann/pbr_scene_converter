# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import classes as directives

def read_from_xml(filename):
    tree = ET.parse(filename)
    scene_element = tree.getroot()

    scene = load_scene(scene_element)

    return scene

def load_scene(scene_element):
    scene = directives.Scene()

    scene.integrator = load_integrator(scene_element)
    scene.sensor = load_sensor(scene_element)

    #scene.world = load_world(scene_element)

    return scene
    
def load_integrator(scene):
    integrator = directives.Integrator()
    integrator_element = scene.find('integrator')
    
    # extract integrator type
    integrator.int_type = integrator_element.attrib.get('type')
    
    # extract all aditional parameters
    for parameter in integrator_element:
        integrator_param = directives.Param()
        
        integrator_param.val_type = parameter.tag
        integrator_param.name = parameter.attrib.get('name')
        integrator_param.value = parameter.attrib.get('value')
    
        integrator.params.append(integrator_param)
    
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
    
    for parameter in sampler_element:
        sampler_param = directives.Param()
        
        sampler_param.val_type = parameter.tag
        sampler_param.name = parameter.attrib.get('name')
        sampler_param.value = parameter.attrib.get('value')
        
        sensor.sampler.params.append(sampler_param)
        
    # film setup
    film_element = sensor_element.find('film')
    sensor.film.film_type = film_element.get('type')
    
    sensor.film.filter_type = film_element.find('rfilter').get('type')
    
    for parameter in film_element:
        if not parameter.tag == 'rfilter':
            film_param = directives.Param()
            
            film_param.val_type = parameter.tag
            film_param.name = parameter.attrib.get('name')
            film_param.value = parameter.attrib.get('value')
            
            sensor.film.params.append(film_param)
    
    # other params
    for parameter in sensor_element:
        if (not parameter.tag == 'transform') and (not parameter.tag == 'film') and (not parameter.tag == 'sampler'):
            sensor_param = directives.Param()
            
            sensor_param.val_type = parameter.tag
            sensor_param.name = parameter.attrib.get('name')
            sensor_param.value = parameter.attrib.get('value')
            
            sensor.params.append(sensor_param)

    return sensor

#def load_materials(scene):
    #for material_element in scene.findall('bsdf'):
    #    pass

def test_directives():
    scene = read_from_xml('/home/grad/lahagemann/scene_converter/test_files/mitsuba/staircase.xml')

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

def main():
    test_directives()

if  __name__ =='__main__':main()

#def load_world(scene):
#    pass

