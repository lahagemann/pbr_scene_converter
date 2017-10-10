# -*- coding: utf-8 -*-

import mitsuba as mit
import mitsubaToPBRT as mtpbrt


def toPBRT(scene):
    with open("scene.pbrt", 'w') as outfile:
        # scene directives
        # integrator
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



