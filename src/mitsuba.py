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
    # sensor.transform.name = sensor_element.attrib.get('transform')


def load_world(scene):
    pass

