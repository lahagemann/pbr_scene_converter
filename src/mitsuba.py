# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import classes as directives



def read_from_xml(filename):
    tree = ET.parse(filename)
    scene_element = tree.getroot()

    scene = load_scene(scene_element)


    
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


