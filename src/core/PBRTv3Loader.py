import PBRTv3Lex
import PBRTv3Yacc
from Directives import *
import sys

class PBRTv3Loader:

    def importFile(self, filename):
        data = open(filename).read()
        sceneStructure = PBRTv3Yacc.parse(data)

        return sceneStructure

    def loadScene(self, sceneStructure):
        scene = Scene()

        if len(sceneStructure) == 1:
            if sceneStructure[0][0] in ['Integrator', 'Sampler', 'Film', 'Filter', 'Camera', 'Transform']:
                scene = self.loadDirectives(sceneStructure[0], scene)
            else:
                scene = self.loadWorld(sceneStructure[0], scene)

        else:
            scene = self.loadDirectives(sceneStructure[0], scene)
            scene = self.loadWorld(sceneStructure[1], scene)

        return scene
        
    def loadDirectives(self, directiveStructure, scene):
        for struct in directiveStructure:
            directive = struct[0]
            print directive

            #integrator
            if directive == 'Integrator':
                scene.integrator = Integrator()
                scene.integrator.type = struct[1]

                if struct[2] is not None:
                    scene.integrator.params = self.loadParams(struct[2][0])

                

    def loadWorld(self, worldStructure, scene):
        pass

    def loadParams(self, paramStructure):
        params = {}

        if paramStructure is not None:
            for struct in paramStructure:
                param = Param(paramStructure[0], paramStructure[1], paramStructure[2])

                params[paramStructure[1]] = param

        return params

    def __init__(self, filename):
        sceneStruct = self.importFile(filename)
        scene = self.loadScene(sceneStruct)

if __name__ == '__main__':
    loader = PBRTv3Loader(sys.argv[1])
    