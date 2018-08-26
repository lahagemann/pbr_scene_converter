import numpy as np
import sys
import copy

import ParamTranslation as PT

sys.path.insert(0, 'import/')
from Directives import BumpMap

class ToPBRTv3:
    def __init__(self, scene, outputName, inputRenderer):
        np.set_printoptions(suppress=True)

        self.copySkydome = False
        self.export(scene, filename, inputRenderer)

    def export(self, scene, outputName, inputRenderer):
        with open(outputName, 'w') as outfile:
            sceneDirectives = self.exportRenderingOptions(scene, inputRenderer)
            outfile.write(sceneDirectives)

            worldDescription = self.worldDescriptionToPBRT(scene, inputRenderer)
            outfile.write(worldDescription)

        if self.copySkydome:
            pass

    def exportRenderingOptions(self, scene):
        output = ''

        if scene.integrator:
            type = PT.getProperty(PT.integrator, 'type', inputRenderer, 'pbrtv3', scene.integrator.type)
            if type:
                output += 'Integrator "' + type + '" '
                output += self.exportParams(scene.integrator.params, PT.integrator, 'params', inputRenderer)

        if scene.sensor.transform:
            if scene.sensor.transform.matrix:
                output += 'Transform [ '

                for i in range(0,4):
                    for j in range(0,4):
                        output += str(scene.sensor.transform.matrix[i][j]) + ' '

                output += ']\n'

            elif scene.sensor.transform.lookat:
                output += 'LookAt [ '

        return output

    def exportParams(self, params, dictionary, property, inputRenderer):
        output = ''

        for name in params:
            pbrtParam = PT.getProperty(PT.integrator, property, inputRenderer, 'pbrtv3', name)
            inputParam = params[name]

            if pbrtParam:
                output += '"' + inputParam.type + ' ' + pbrtParam + '" '

                if inputParam.type == 'string' or inputParam.type == 'bool':
                    output += '[ "' + str(inputParam.value) + '" ] '
                elif inputParam.type == 'rgb' or inputParam.type == 'color' or inputParam.type == 'spectrum':
                    output += '[ ' + str(inputParam.value[0]) + ' ' + str(inputParam.value[1]) + ' ' + str(inputParam.value[2]) + ' ] '
                else:
                    output += '[ ' + str(inputParam.value) + ' ] '

        output += '\n'
        return output
