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

            int_type = mtpbrt.integratorType[scene.integrator.int_type]
            if int_type:
                outfile.write('"' + int_type + '" ')
            else:
                outfile.write('"path" ')

            for param in scene.integrator.params:
                pbrt_param = mtpbrt.integratorParam[param.name]
                if pbrt_param:
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    outfile.write('[' + param.value + ']')

            outfile.write('\n')

        # transform
        if scene.sensor.transform.matrix:
            outfile.write('Transform ')
            outfile.write('[ ')

            # convert transform matrix to inverse transpose (PBRT default)
            m = scene.sensor.transform.matrix
            m_T = np.transpose(m)
            m_IT = np.linalg.inv(m_t)

            for i in range(0,4):
                for j in range(0,4):
                    outfile.write(m_IT[i][j])
                    outfile.write(' ')

            outfile.write(']')
            outfile.write('\n')

        # sampler
        if scene.sensor.sampler:
            outfile.write('Sampler ')

            sampler_type = mtpbrt.samplerType[scene.sensor.sampler.sampler_type]
            if sampler_type
                outfile.write('"' + sampler_type + '" ')
            else:
                outfile.write('"sobol" ')

            for param in scene.sensor.sampler.params:
                pbrt_param = mtpbrt.samplerParam[param.name]
                if pbrt_param:
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    if pbrt_param.val_type is 'string':
                        outfile.write('[ "' + param.value + '" ]')
                    else:
                        outfile.write('[' + param.value + ']')
            
            outfile.write('\n')

        # filter
        if scene.sensor.filter:
            outfile.write('PixelFilter ')

            filter_type = mtpbrt.filterType[scene.sensor.filter.filter_type]
            if filter_type:
                outfile.write('"' + filter_type + '" ')
            else:
                outfile.write('"triangle" ')


            for param in scene.sensor.filter.params:
                pbrt_param = mtpbrt.filterParam[param.name]
                if pbrt_param:
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    if pbrt_param.val_type is 'string':
                        outfile.write('[ "' + param.value + '" ]')
                    else:
                        outfile.write('[' + param.value + ']')
    
            outfile.write('\n')

        # film
        if scene.sensor.film:
            outfile.write('Film ')

            film_type = mtpbrt.filmType[scene.sensor.film.film_type]
            if film_type:
                outfile.write('"' + film_type + '" ')
            else:
                outfile.write('"image" ')


            for param in scene.sensor.film.params:
                pbrt_param = mtpbrt.filmParam[param.name]
                if pbrt_param:
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    if pbrt_param.val_type is 'string':
                        outfile.write('[ "' + param.value + '" ]')
                    else:
                        outfile.write('[' + param.value + ']')
    
            outfile.write('\n')

        # sensor/camera
        if scene.sensor:
            outfile.write('Camera ')

            sensor_type = mtpbrt.sensorType[scene.sensor.sensor_type]
            if sensor_type:
                outfile.write('"' + sensor_type + '" ')
            else:
                outfile.write('"perspective" ')

            for param in scene.sensor.params:
                pbrt_param = mtpbrt.sensorParam[param.name]
                if pbrt_param:
                    outfile.write('"' + param.val_type + ' ' + pbrt_param + '" ')
                    if pbrt_param.val_type is 'string':
                        outfile.write('[ "' + param.value + '" ]')
                    else:
                        outfile.write('[' + param.value + ']')

            outfile.write('\n')

        # scene description
        outfile.write('WorldBegin\n')
        
        # texture declaration



        # end scene description
        outfile.write('WorldEnd\n')














