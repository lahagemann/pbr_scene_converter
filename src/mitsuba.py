# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import classes as directives

def read_from_xml(filename):
    tree = ET.parse(filename)
    scene_element = tree.getroot()

    scene = load_scene(scene_element)

def load_scene(scene_element):
    scene = Scene()

    scene.integrator = load_integrator(scene_element)
    scene.sensor = load_sensor(scene_element)

    scene.world = load_world(scene_element)

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
    sensor.film.film_type = film.get('type')
    
    sensor.film.filter_type = film.find('rfilter').get('type')
    
    for parameter in film_element:
        if not parameter.tag == 'rfilter':
            film_param = directives.Param()
            
            film_param.val_type = parameter.tag
            film_param.name = parameter.attrib.get('name')
            film_param.value = parameter.attrib.get('value')
            
            sensor.film.params.append(film_param)
    
    # other params
    for parameter in sensor_element:
        if not parameter.tag == 'transform' or not parameter.tag == 'film' or not parameter.tag == 'sampler':
            sensor_param = directives.Param()
            
            sensor_param.val_type = parameter.tag
            sensor_param.name = parameter.attrib.get('name')
            sensor_param.value = parameter.attrib.get('value')
            
            sensor.params.append(sensor_param)
            


def load_world(scene):
    pass

