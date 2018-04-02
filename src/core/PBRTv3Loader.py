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
        scene.sensor = Sensor()
        for struct in directiveStructure:
            directive = struct[0]

            if directive == 'Integrator':
                scene.integrator.type = struct[1]

                if struct[2] is not None:
                    print 'AAAAAA'
                    print struct[2]
                    scene.integrator.params = self.loadParams(struct[2])
            
            elif directive == 'Camera':
                scene.sensor.type = struct[1]

                if struct[2] is not None:
                   scene.sensor.params = self.loadParams(struct[2]) 
            
            elif directive == 'Sampler':
                scene.sensor.sampler.type = struct[1]

                if struct[2] is not None:
                    scene.sensor.sampler.params = self.loadParams(struct[2])

            elif directive == 'Film':
                scene.sensor.film.type = struct[1]

                if struct[2] is not None:
                    scene.sensor.film.params = self.loadParams(struct[2])

            elif directive == 'PixelFilter':
                scene.sensor.film.filter = struct[1]

            elif directive == 'Transform':
                scene.sensor.transform = Transform()
                
                if struct[2] is not None:
                    scene.sensor.transform.matrix = struct[2]

        # debug
        # print 'integrator: ' + scene.integrator.type
        # print 'sensor: ' + scene.sensor.type
        # print 'sensor.sampler: ' + scene.sensor.sampler.type
        # print 'sensor.film: ' + scene.sensor.film.type
        # print 'sensor.film.filter: ' + scene.sensor.film.filter
        # print 'sensor.transform: ' + str(scene.sensor.transform.matrix)

        return scene

    def loadWorld(self, worldStructure, scene):
        materials = []
        shapes = []
        lights = []
        textures = {}

        currentRefMaterial = ''

        for struct in worldStructure:
            directive = struct[0]

            if directive == 'Texture':
                name = struct[1]
                type = struct[3]

                params = self.loadParams(struct[4])

                # COMPLETE HERE

            elif directive == 'MakeNamedMaterial':
                id = struct[1]
                type = ''
                material = None

                if struct[2] is not None:
                    params = self.loadParams(struct[2])

                # actually there's little need to check if type is specified, but for the sake of properness...
                if 'type' in params:
                    type = params['type'].value
                    params.pop('type')

                # I'M NOT SURE
                if 'bumpmap' in params:
                    bumpTextureName = params['bumpmap'].value

                    material = BumpMap()
                    material.texture = textures[bumpTextureName]

                    material.material = Material(type, id)
                    material.material.params = params

                    materials.append(material)
                    print material
                
                else:
                    material = Material(type, id)
                    material.params = params

                    if 'Kd' in params:
                        kd = params['Kd']
                        if kd.type == 'texture':
                            material.texture = textures[kd.value]
                            material.params.pop('Kd')

                    materials.append(material)
                    print material

            elif directive == 'NamedMaterial':
                currentRefMaterial = struct[1]

            elif directive == 'Shape':
                pass
            elif directive == 'LightSource':
                pass
            elif directive == 'AttributeBegin':
                pass
            elif directive == 'TransformBegin':
                pass


    def loadParams(self, paramStructure):
        params = {}

        for tuple in paramStructure:
            param = Param(tuple[0], tuple[1], tuple[2])
            params[tuple[1]] = param

        return params

    def __init__(self, filename):
        sceneStruct = self.importFile(filename)
        scene = self.loadScene(sceneStruct)

if __name__ == '__main__':
    loader = PBRTv3Loader(sys.argv[1])
    