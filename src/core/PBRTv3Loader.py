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

        print scene.lights

        return scene
        
    def loadDirectives(self, directiveStructure, scene):
        scene.sensor = Sensor()
        for struct in directiveStructure:
            directive = struct[0]

            if directive == 'Integrator':
                scene.integrator.type = struct[1]

                if struct[2] is not None:
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

                texture = Texture(name, type)
                texture.params = params

                textures[name] = texture

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
                
                else:
                    material = Material(type, id)
                    material.params = params

                    if 'Kd' in params:
                        kd = params['Kd']
                        if kd.type == 'texture':
                            material.texture = textures[kd.value]
                            material.params.pop('Kd')

                    materials.append(material)

            elif directive == 'NamedMaterial':
                currentRefMaterial = struct[1]

            elif directive == 'Shape':
                # simple shape, no emitter, embed material or transform
                shape = Shape(struct[1])
                shape.params = self.loadParams(struct[2])

                # add reference material
                if currentRefMaterial:
                    shape.params['id'] = Param('string', 'id', currentRefMaterial)

                shapes.append(shape)

            elif directive == 'LightSource':
                # simple emitters, no transform or shape involved. they go into lights list
                emitter = Emitter(struct[1])
                emitter.transform = None
                emitter.params = self.loadParams(struct[2])

                lights.append(emitter)

            elif directive == 'AttributeBegin':
                material = None
                emitter = None
                transform = None

                for modifiedStruct in struct[1]:
                    modifiedDirective = modifiedStruct[0]

                    if modifiedDirective == 'AreaLightSource':
                        emitter = Emitter(modifiedStruct[1])
                        emitter.params = self.loadParams(modifiedStruct[2])

                    elif modifiedDirective == 'Transform':
                        transform = Transform()
                        transform.matrix = modifiedStruct[2]

                    elif modifiedDirective == 'Material':
                        type = ''
                        id = modifiedStruct[1]
                        params = self.loadParams(modifiedStruct[2])

                        if 'type' in params:
                            type = params['type'].value
                            params.pop('type')

                        material = Material(type, id)
                        material.params = params

                        if 'Kd' in params:
                            kd = params['Kd']
                            if kd.type == 'texture':
                                material.texture = textures[kd.value]
                                material.params.pop('Kd')

                    elif modifiedDirective == 'Shape':
                        # simple shape, no emitter, embed material or transform
                        shape = Shape(modifiedStruct[1])
                        shape.params = self.loadParams(modifiedStruct[2])

                        # add reference material
                        if currentRefMaterial:
                            shape.params['id'] = Param('string', 'id', currentRefMaterial)

                        shape.emitter = emitter
                        shape.material = material
                        shape.transform = transform

                        shapes.append(shape)

            elif directive == 'TransformBegin':
                transform = None
                for modifiedStruct in struct[1]:
                    modifiedDirective = modifiedStruct[0]

                    if modifiedDirective == 'Transform':
                        transform = Transform()
                        transform.matrix = modifiedStruct[2]

                    elif modifiedDirective == 'Shape':
                        # simple shape, no emitter, embed material or transform
                        shape = Shape(modifiedStruct[1])
                        shape.params = self.loadParams(modifiedStruct[2])

                        # add reference material
                        if currentRefMaterial:
                            shape.params['id'] = Param('string', 'id', currentRefMaterial)

                        shape.transform = transform

                        shapes.append(shape)
        
        scene.materials = materials
        scene.lights = lights
        scene.shapes = shapes

        return scene

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
    