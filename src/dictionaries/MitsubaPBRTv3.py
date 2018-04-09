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
                        'shutterOpen' : 'shutteropen',
                        'shutterClose' : 'shutterclose',
                        # thinlens
                        'apertureRadius' : 'lensradius',
                        'focusDistance' : 'focaldistance'
                    }
                    
textureType =       {
                        'checkerboard' : 'checkerboard',
                        'scale' : 'scale'
                    }

textureParam =      {
                        'color1' : 'tex1',
                        'color0' : 'tex2',
                        'uscale' : 'uscale',
                        'vscale' : 'vscale'
                    }

# in pbrt, plastic doesn't respond well to roughness params
materialType =      {
                        'diffuse'  : 'matte',
                        'diffuseReflectance' : 'matte',
                        'roughdiffuse' : 'matte',
                        'conductor' : 'metal',
                        'roughconductor' : 'metal',
                        'dielectric' : 'glass',
                        'roughdielectric' : 'glass',
                        'thindielectric' : 'uber',
                        'plastic' : 'substrate',
                        'roughplastic' : 'substrate',
                        'difftrans' : 'translucent'
                    }

diffuseParam =      {
                        'diffuseReflectance' : 'Kd',
                        'reflectance' : 'Kd'
                    }

dielectricParam =   {
                        'specularReflectance' : 'Kr',
                        'specularTransmittance' : 'Kt',
                        'intIOR' : 'index',
                        'alphaU' : 'uroughness',
                        'alphaV' : 'vroughness'
                    }

thindielecParam =   {
                        'intIOR' : 'index',
                        'specularReflectance' : 'Kr',
                        'specularTransmittance' : 'Kt'
                    }

plasticParam =      {
                        'alphaU' : 'uroughness',
                        'alphaV' : 'vroughness',
                        'diffuseReflectance' : 'Kd',
                        'specularReflectance' : 'Ks'
                    }

conductorParam =    {
                        'eta' : 'eta',
                        'k' : 'k',
                        #'specularReflectance' : 'Kr',
                        'alphaU' : 'uroughness',
                        'alphaV' : 'vroughness'
                    }

difftransParam =    {
                        'transmittance' : 'Kt'
                    }

emitterType =       {
                        'point' : 'point',
                        'spot' : 'spot',
                        'envmap' : 'infinite',
                        'sunsky' : 'distant'
                    }
                    
emitterParam =      {
                        'radiance' : 'L',
                        'intensity' : 'I',
                        'position' : 'from',
                        'samplingWeight' : 'samples',
                        'cutoffAngle' : 'conedeltaangle',
                        'beamWidth' : 'coneangle'
                    }
    
shapeParam =        {
                        'radius' : 'radius'
                    }