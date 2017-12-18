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
                        # photonmapper
                        'globalLookupRadius' : 'radius',
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
                        'chainLength' : 'mutationsperpixel'
                    }
# sampler

samplerType =       {   'independent' : 'random',
                        'stratified' : 'stratified',
                        'ldsampler' : '02sequence',
                        'halton' : 'halton',
                        'hammersley' : 'random',
                        'sobol' : 'sobol'
                    }

samplerParam =      {   'sampleCount' : 'pixelsamples'  }

# film

filmType =          {   'ldrfilm' : 'image',
                        'hdrfilm' : 'image',
                        'tiledhdrfilm' : 'image',
                        'mfilm' : 'image'
                    }

filmParam =         {   'width' : 'xresolution',
                        'height' : 'yresolution'
                    }

#filter

filterType =        {
                        'box' : 'box',
                        'tent' : 'triangle',
                        'gaussian' : 'gaussian',
                        'mitchell' : 'mitchell',
                        'catmullrom' : 'mitchell',
                        'lanczos' : 'sinc'
                    }

# sensor -> camera

sensorType =        {   'perspective' : 'perspective',
                        'thinlens' : 'perspective',
                        'orthographic' : 'orthographic',
                        'telecentric' : 'orthographic',
                        'spherical' : 'environment',
                        'irradiancemeter' : 'realistic',
                        'radiancemeter' : 'realistic',
                        'fluencemeter' : 'realistic',
                        'perspective_rdist' : 'perspective'
                    }

sensorParam =       {   #perspective
                        'fov' : 'fov',
                        'shutterOpen' : 'shutteropen',
                        'shutterClose' : 'shutterclose',
                        # thinlens
                        'apertureRadius' : 'lensradius',
                        'focusDistance' : 'focaldistance'
                    }
                    
textureType =       {
                        '' : 'bilerp',
                        '' : 'checkerboard',
                        '' : 'constant',
                        '' : 'dots',
                        '' : 'fbm',
                        '' : 'marble',
                        '' : 'mix',
                        '' : 'scale',
                        '' : 'uv'
                    }

textureParam =      {
                        'color1' : 'tex1',
                        'color0' : 'tex2',
                        'uscale' : 'uscale',
                        'vscale' : 'vscale'
                    }

material =          {
                        'diffuse'  : 'matte',
                        'diffuseReflectance' : 'matte',
                        'roughconductor' : 'metal',
                        'dielectric' : 'glass',
                        'conductor' : 'metal',
                        'plastic' : 'plastic'
                        'thindielectric' : 'uber'
                    }
