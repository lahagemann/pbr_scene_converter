# integrator

integratorType =    {   'path'  : 'path',
                        'volpath_simple': 'path',
                        'volpath' : 'path',
                        'adaptive' : 'path',
                        'direct' : 'directlighting',
                        'bdpt' : 'bdpt', 
                        'mlt' : 'mlt',
                        'pssmlt' : 'mlt',
                        'erpt' : 'mlt',
                        'photonmapper' : 'sppm',
                        'ppm' : 'sppm',
                        'sppm' : 'sppm'
                    }

integratorParam =   {   # path, volpath_simple, volpath
                        'maxDepth' : 'maxdepth',
                        'rrDepth' : 'rrthreshold',
                        # bdpt
                        'lightImage' : '',
                        'sampleDirect' : '',
                        # photonmapper
                        'directSamples' : '',
                        'glossySamples' : '',
                        'globalPhotons' : '',
                        'causticPhotons' : '',
                        'volumePhotons' : '',
                        'globalLookupRadius' : '',
                        'causticLookupRadius' : '',
                        'lookupSize' : '',
                        'granularity' : '',
                        # ppm, sppm
                        'photonCount' : 'photonsperiteration',
                        'initialRadius' : 'radius',
                        'maxPasses' : 'iterations',
                        #pssmlt, mlt
                        'luminanceSamples' : 'bootstrapsamples',
                        'pLarge' : 'largestepprobability',
                        'lambda' : 'sigma',
                        #erpt                        
                        'numChains' : 'chains',
                        'maxChains' : '',
                        'chainLength' : '',
                    }

samplerType =       {   'independent' : 'random',
                        'stratified' : 'stratified',
                        'ldsampler' : '02sequence',
                        'halton' : 'halton',
                        'hammersley' : 'random',
                        'sobol' : 'sobol'
                    }

samplerParam =      {   'sampleCount' : 'pixelsamples'  }

filmType =          {   'ldrfilm' : 'image',
                        'hdrfilm' : 'image',
                        'tiledhdrfilm' : 'image',
                        'mfilm' : 'image'
                    }

filmParam =         {   'width' : 'xresolution',
                        'height' : 'yresolution'
                    }

filterType =        {
    
                    }

sensorType =        {   'perspective' : 'perspective',
                        'thinlens' : 'perspective',
                        'orthographic' : 'orthographic',
                        'telecentric' : '',
                        'spherical' : '',
                        'irradiancemeter' : '',
                        'radiancemeter' : '',
                        'fluencemeter' : '',
                        'perspective_rdist' : '',
                    }

sensorParam =       {   #perspective
                        'toWorld' : '',
                        'focalLength' : '',
                        'fov' : 'fov',
                        'fovAxis' : '',
                        'shutterOpen' : 'shutteropen',
                        'shutterClose' : 'shutterclose',
                        'nearClip' : '',
                        'farClip' : '',
                        # thinlens
                        'apertureRadius' : 'lensradius',
                        'focusDistance' : 'focaldistance',
                        # perspective_rdist
                        'kc' : '',
                    }

