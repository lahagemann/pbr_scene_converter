# -*- coding: utf-8 -*-

import mitsuba as mit
import mitsubaToPBRT as mtpbrt
import numpy as np

def toPBRT(scene):
    np.set_printoptions(suppress=True)
    
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

            for param in scene.integrator.params:
                if param.name in mtpbrt.integratorParam:
                    pbrt_param = mtpbrt.integratorParam[param.name]
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    outfile.write('[ ' + param.value + ' ]')

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

            for param in scene.sensor.sampler.params:
                if param.name in mtpbrt.samplerParam:
                    pbrt_param = mtpbrt.samplerParam[param.name]
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    if param.val_type is 'string':
                        outfile.write('[ "' + param.value + '" ]')
                    else:
                        outfile.write('[ ' + param.value + ' ]')
            
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


            for param in scene.sensor.film.params:
                if param.name == 'fileFormat':
                    outfile.write('"string filename" [ "scene.' + param.value + '" ]' )
                elif param.name in mtpbrt.filmParam:
                    pbrt_param = mtpbrt.filmParam[param.name]
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    if param.val_type is 'string':
                        outfile.write('[ "' + param.value + '" ] ')
                    else:
                        outfile.write('[ ' + param.value + ' ] ')

            outfile.write('\n')

        # sensor/camera
        if scene.sensor:
            outfile.write('Camera ')

            if scene.sensor.sensor_type in mtpbrt.sensorType:
                sensor_type = mtpbrt.sensorType[scene.sensor.sensor_type]
                outfile.write('"' + sensor_type + '" ')
            else:
                outfile.write('"perspective" ')

            for param in scene.sensor.params:
                if param.name in mtpbrt.sensorParam:
                    pbrt_param = mtpbrt.sensorParam[param.name]
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    if param.val_type is 'string':
                        outfile.write('[ "' + param.value + '" ]')
                    else:
                        outfile.write('[ ' + param.value + ' ]')

            outfile.write('\n')

        # scene description
        outfile.write('WorldBegin\n')
        
        # texture declaration



        # end scene description
        outfile.write('WorldEnd\n')


def main():
    scene = mit.read_from_xml('/Users/luiza.hagemann/Development/pbr_scene_converter/test_files/mitsuba/classroom.xml')
    toPBRT(scene)

if  __name__ =='__main__': main()











