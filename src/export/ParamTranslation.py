class ParamTranslation:
    # getProperty:
    # dictionary: integrator, sampler, film, filter, ...
    # property: type or params (materialParams for materials)
    # renderer: pbrtv3, luxrender or mitsuba
    # name: name of the property
    def getProperty(dictionary, property, inputRenderer, targetRenderer, name):
        if not property in dictionary:
            return None

        propDictionary = dictionary[property]

        for valueDictionary in propDictionary:
            if type(valueDictionary[inputRenderer]) == str:
                if valueDictionary[inputRenderer] == name:
                    prop = valueDictionary[targetRenderer]
                    if type(prop) == list:
                        return prop[0]
                    else:
                        return prop

            elif type(valueDictionary[inputRenderer]) == list:
                if name in valueDictionary[inputRenderer]:
                    prop = valueDictionary[targetRenderer]
                    if type(prop) == list:
                        index = valueDictionary[inputRenderer].index(name)
                        return prop[index]
                    else:
                        return prop

    # initializes all dictionaries needed for param translation between renderers
    # it is not mandatory that this translator be a class,
    # but for organization purposes we thought it best to structure it this way
    def __init__(self):
        self.integrator = {
            'type' : [
                {
                    'pbrtv3' : 'path',
                    'luxrender' : 'path',
                    'mitsuba' : ['path', 'volpath_simple', 'volpath', 'adaptive']
                },
                {
                    'pbrtv3' : 'directlighting',
                    'luxrender' : 'directlighting',
                    'mitsuba' : 'direct'
                },
                {
                    'pbrtv3' : 'bdpt',
                    'luxrender' : 'bidirectional',
                    'mitsuba' : 'bdpt'
                },
                {
                    'pbrtv3' : 'mlt',
                    'luxrender' : None,
                    'mitsuba' : ['mlt', 'pssmlt', 'erpt']
                },
                {
                    'pbrtv3' : 'sppm',
                    'luxrender' : 'sppm',
                    'mitsuba' : ['sppm', 'ppm', 'photonmapper']
                }
            ],
            'params' : [
                {
                    'pbrtv3' : 'maxdepth',
                    'luxrender' : 'maxdepth',
                    'mitsuba' : 'maxDepth'
                },
                {
                    'pbrtv3' : 'rrthreshold',
                    'luxrender' : None,
                    'mitsuba' : 'rrDepth'
                },
                {
                    'pbrtv3' : 'radius',
                    'luxrender' : 'startradius',
                    'mitsuba' : 'globalLookupRadius'
                },
                {
                    'pbrtv3' : 'photonsperiteration',
                    'luxrender' : 'photonperpass',
                    'mitsuba' : 'photonCount'
                },
                {
                    'pbrtv3' : 'iterations',
                    'luxrender' : 'maxphotondepth',
                    'mitsuba' : 'maxPasses'
                },
                {
                    'pbrtv3' : 'radius',
                    'luxrender' : 'startradius',
                    'mitsuba' : 'initialRadius'
                },
                {
                    'pbrtv3' : 'bootstrapsamples',
                    'luxrender' : None,
                    'mitsuba' : 'luminanceSamples'
                },
                {
                    'pbrtv3' : 'largestepprobability',
                    'luxrender' : None,
                    'mitsuba' : 'pLarge'
                },
                {
                    'pbrtv3' : 'sigma',
                    'luxrender' : None,
                    'mitsuba' : 'lambda'
                },
                {
                    'pbrtv3' : 'chains',
                    'luxrender' : None,
                    'mitsuba' : 'numChains'
                },
                {
                    'pbrtv3' : 'mutationsperpixel',
                    'luxrender' : None,
                    'mitsuba' : 'chainLength'
                },
                {
                    'pbrtv3' : None,
                    'luxrender' : 'alpha',
                    'mitsuba' : 'alpha'
                },
                {
                    'pbrtv3' : None,
                    'luxrender' : 'photonperpass',
                    'mitsuba' : 'globalPhotons'
                }
            ]
        }

        self.sampler = {
            'type' : [
                {
                    'pbrtv3' : 'random',
                    'luxrender' : 'random',
                    'mitsuba' : ['independent', 'hammersley']
                },
                {
                    'pbrtv3' : 'stratified',
                    'luxrender' : None,
                    'mitsuba' : 'stratified'
                },
                {
                    'pbrtv3' : '02sequence',
                    'luxrender' : 'lowdiscrepancy',
                    'mitsuba' : 'ldsampler'
                },
                {
                    'pbrtv3' : 'halton',
                    'luxrender' : None,
                    'mitsuba' : 'halton'
                },
                {
                    'pbrtv3' : 'sobol',
                    'luxrender' : 'sobol',
                    'mitsuba' : 'sobol'
                }
            ],
            'params' : [
                {
                    'pbrtv3' : 'pixelsamples',
                    'luxrender' : 'pixelsamples',
                    'mitsuba' : 'sampleCount'
                }
            ]
        }

        self.film = {
            'type' : [
                {
                    'pbrtv3' : 'image',
                    'luxrender' : 'fleximage',
                    'mitsuba' : ['ldrfilm', 'hdrfilm', 'tiledhdrfilm', 'mfilm']
                }
            ],
            'params' : [
                {
                    'pbrtv3' : 'xresolution',
                    'luxrender' : 'xresolution',
                    'mitsuba' : 'width'
                },
                {
                    'pbrtv3' : 'yresolution',
                    'luxrender' : 'yresolution',
                    'mitsuba' : 'height'
                },
                {
                    'pbrtv3' : None,
                    'luxrender' : 'gamma',
                    'mitsuba' : 'gamma'
                },
            ]
        }

        self.filter = {
            'type' : [
                {
                    'pbrtv3' : 'box',
                    'luxrender' : 'box',
                    'mitsuba' : 'box'
                },
                {
                    'pbrtv3' : 'triangle',
                    'luxrender' : 'triangle',
                    'mitsuba' : 'tent'
                },
                {
                    'pbrtv3' : 'gaussian',
                    'luxrender' : 'gaussian',
                    'mitsuba' : 'gaussian'
                },
                {
                    'pbrtv3' : 'mitchell',
                    'luxrender' : ['mitchell', 'catmullrom'],
                    'mitsuba' : ['mitchell', 'catmullrom']
                },
                {
                    'pbrtv3' : 'sinc',
                    'luxrender' : 'sinc',
                    'mitsuba' : 'lanczos'
                }
            ]
        }

        self.sensor = {
            'type' : [
                {
                    'pbrtv3' : 'perspective',
                    'luxrender' : 'perspective',
                    'mitsuba' : ['perspective', 'thinlens', 'perspective_rdist']
                },
                {
                    'pbrtv3' : 'orthographic',
                    'luxrender' : 'orthographic',
                    'mitsuba' : ['orthographic', 'telecentric']
                },
                {
                    'pbrtv3' : 'environment',
                    'luxrender' : 'environment',
                    'mitsuba' : 'spherical'
                },
                {
                    'pbrtv3' : 'realistic',
                    'luxrender' : 'realistic',
                    'mitsuba' : ['irradiancemeter', 'radiancemeter', 'fluencemeter']
                }
            ],
            'params' : [
                {
                    'pbrtv3' : 'shutteropen',
                    'luxrender' : 'shutteropen',
                    'mitsuba' : 'shutterOpen'
                },
                {
                    'pbrtv3' : 'shutterclose',
                    'luxrender' : 'shutterclose',
                    'mitsuba' : 'shutterClose'
                },
                {
                    'pbrtv3' : 'lensradius',
                    'luxrender' : 'lensradius',
                    'mitsuba' : 'apertureRadius'
                },
                {
                    'pbrtv3' : 'focaldistance',
                    'luxrender' : 'focaldistance',
                    'mitsuba' : 'focusDistance'
                }
            ]
        }

        self.texture = {
            'type' : [
                {
                    'pbrtv3' : 'checkerboard',
                    'luxrender' : 'checkerboard',
                    'mitsuba' : 'checkerboard'
                },
                {
                    'pbrtv3' : 'scale',
                    'luxrender' : 'scale',
                    'mitsuba' : 'scale'
                }
            ],
            'params' : [
                {
                    'pbrtv3' : 'tex1',
                    'luxrender' : 'tex1',
                    'mitsuba' : 'color1'
                },
                {
                    'pbrtv3' : 'tex2',
                    'luxrender' : 'tex2',
                    'mitsuba' : 'color0'
                },
                {
                    'pbrtv3' : 'uscale',
                    'luxrender' : 'uscale',
                    'mitsuba' : 'uscale'
                },
                {
                    'pbrtv3' : 'vscale',
                    'luxrender' : 'vscale',
                    'mitsuba' : 'vscale'
                }
            ]
        }

        self.material = {
            'type': [
                {
                    'pbrtv3' : 'matte',
                    'luxrender' : 'matte',
                    'mitsuba' : ['diffuse', 'diffuseReflectance', 'roughdiffuse']
                },
                {
                    'pbrtv3' : 'matte',
                    'luxrender' : 'matte',
                    'mitsuba' : ['diffuse', 'diffuseReflectance', 'roughdiffuse']
                },
                {
                    'pbrtv3' : 'mirror',
                    'luxrender' : 'mirror',
                    'mitsuba' : 'conductor'
                },
                {
                    'pbrtv3' : 'metal',
                    'luxrender' : ['mirror', 'metal2'],
                    'mitsuba' : ['conductor', 'roughconductor']
                },
                {
                    'pbrtv3' : 'glass',
                    'luxrender' : ['glass', 'roughglass'],
                    'mitsuba' : ['dielectric', 'roughdielectric']
                },
                {
                    'pbrtv3' : 'uber',
                    'luxrender' : 'glass',
                    'mitsuba' : 'thindielectric'
                },
                {
                    'pbrtv3' : 'substrate',
                    'luxrender' : 'glossy',
                    'mitsuba' : ['plastic', 'roughplastic']
                },
                {
                    'pbrtv3' : 'translucent',
                    'luxrender' : 'mattetranslucent',
                    'mitsuba' : 'difftrans'
                }
            ],
            'diffuseParams' : [
                {
                    'pbrtv3' : 'Kd',
                    'luxrender' : 'Kd',
                    'mitsuba' : ['diffuseReflectance', 'reflectance']
                }
            ],
            'dielectricParams' : [
                {
                    'pbrtv3' : 'Kr',
                    'luxrender' : 'Kr',
                    'mitsuba' : 'specularReflectance'
                },
                {
                    'pbrtv3' : 'Kt',
                    'luxrender' : 'Kt',
                    'mitsuba' : 'specularTransmittance'
                },
                {
                    'pbrtv3' : 'index',
                    'luxrender' : 'index',
                    'mitsuba' : 'intIOR'
                },
                {
                    'pbrtv3' : 'index',
                    'luxrender' : 'index',
                    'mitsuba' : 'intIOR'
                },
                {
                    'pbrtv3' : 'uroughness',
                    'luxrender' : 'uroughness',
                    'mitsuba' : 'alphaU'
                },
                {
                    'pbrtv3' : 'vroughness',
                    'luxrender' : 'vroughness',
                    'mitsuba' : 'alphaV'
                }
            ],
            'thindielectricParams' : [
                {
                    'pbrtv3' : 'index',
                    'luxrender' : None,
                    'mitsuba' : 'intIOR'
                },
                {
                    'pbrtv3' : 'Kr',
                    'luxrender' : None,
                    'mitsuba' : 'specularReflectance'
                },
                {
                    'pbrtv3' : 'Kt',
                    'luxrender' : None,
                    'mitsuba' : 'specularTransmittance'
                }
            ],
            'plasticParams' : [
                {
                    'pbrtv3' : 'uroughness',
                    'luxrender' : 'uroughness',
                    'mitsuba' : 'alphaU'
                },
                {
                    'pbrtv3' : 'vroughness',
                    'luxrender' : 'vroughness',
                    'mitsuba' : 'alphaV'
                },
                {
                    'pbrtv3' : 'Kd',
                    'luxrender' : 'Kd',
                    'mitsuba' : 'diffuseReflectance'
                },
                {
                    'pbrtv3' : 'Ks',
                    'luxrender' : 'Ks',
                    'mitsuba' : 'specularReflectance'
                }
            ],
            'conductorParams' : [
                {
                    'pbrtv3' : 'uroughness',
                    'luxrender' : 'uroughness',
                    'mitsuba' : 'alphaU'
                },
                {
                    'pbrtv3' : 'vroughness',
                    'luxrender' : 'vroughness',
                    'mitsuba' : 'alphaV'
                },
                {
                    'pbrtv3' : 'eta',
                    'luxrender' : None,
                    'mitsuba' : 'eta'
                },
                {
                    'pbrtv3' : 'k',
                    'luxrender' : None,
                    'mitsuba' : 'k'
                }
            ],
            'difftransParams' : [
                {
                    'pbrtv3' : 'Kt',
                    'luxrender' : 'Kt',
                    'mitsuba' : 'transmittance'
                }
            ]
        }

        self.emitter = {
            'params' : [
                {
                    'pbrtv3' : 'L',
                    'luxrender' : 'L',
                    'mitsuba' : 'radiance'
                },
                {
                    'pbrtv3' : 'I',
                    'luxrender' : None,
                    'mitsuba' : 'intensity'
                },
                {
                    'pbrtv3' : 'from',
                    'luxrender' : 'from',
                    'mitsuba' : 'position'
                },
                {
                    'pbrtv3' : 'samples',
                    'luxrender' : 'nsamples',
                    'mitsuba' : 'samplingWeight'
                },
                {
                    'pbrtv3' : 'conedeltaangle',
                    'luxrender' : None,
                    'mitsuba' : 'cutoffAngle'
                },
                {
                    'pbrtv3' : 'coneangle',
                    'luxrender' : None,
                    'mitsuba' : 'beamWidth'
                },
                {
                    'pbrtv3' : None,
                    'luxrender' : 'turbidity',
                    'mitsuba' : 'turbidity'
                },
                {
                    'pbrtv3' : None,
                    'luxrender' : 'relsize',
                    'mitsuba' : 'sunRadiusScale'
                }
            ]
        }

        self.shape = {
            'params' : [
                {
                    'pbrtv3' : 'radius',
                    'luxrender' : 'radius',
                    'mitsuba' : 'radius'
                }
            ]
        }
