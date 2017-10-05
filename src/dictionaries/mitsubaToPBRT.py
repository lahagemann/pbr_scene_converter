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
                        'hdrfilm' : 'image'
                    }

filmParam =         {   'width' : 'xresolution',
                        'height' : 'yresolution'
                    }

filterType =        {
    
                    }

