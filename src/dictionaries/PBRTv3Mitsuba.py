integratorType =    {   'path'  : 'path',
                        'directlighting' : 'direct',
                        'bdpt' : 'bdpt', 
                        'mlt' : 'mlt',
                        'sppm' : 'sppm'
                    }

integratorParam =   {   # path, volpath_simple, volpath
                        'maxdepth' : 'maxDepth',
                        'rrthreshold' : 'rrDepth',
                        # ppm, sppm
                        'photonsperiteration' : 'photonCount',
                        'radius' : 'initialRadius',
                        'iterations' : 'maxPasses',
                        #pssmlt, mlt
                        'bootstrapsamples' : 'luminanceSamples',
                        'largestepprobability' : 'pLarge',
                        'sigma' : 'lambda'
                    }
# sampler

samplerType =       {   'random' : 'independent',
                        'stratified' : 'stratified',
                        '02sequence' : 'ldsampler',
                        'halton' : 'halton',
                        'sobol' : 'sobol'
                    }

samplerParam =      {   'sampleCount' : 'pixelsamples'  }

# film

filmType =          {   'image' : 'ldrfilm' }

filmParam =         {   'xresolution' : 'width',
                        'yresolution' : 'height'
                    }

#filter

filterType =        {
                        'box' : 'box',
                        'triangle' : 'tent',
                        'gaussian' : 'gaussian',
                        'mitchell' : 'mitchell',
                        'sinc' : 'lanczos'
                    }

# sensor -> camera

sensorType =        {   'perspective' : 'perspective',
                        'orthographic' : 'orthographic',
                        'environment' : 'spherical',
                        'realistic' : 'radiancemeter'
                    }

sensorParam =       {   #perspective
                        'shutteropen' : 'shutterOpen',
                        'shutterclose' : 'shutterClose',
                        # thinlens
                        'lensradius' : 'apertureRadius',
                        'focaldistance' : 'focusDistance'
                    }

textureType =       {
                        'checkerboard' : 'checkerboard',
                        'scale' : 'scale',
                        'imagemap' : 'bitmap'
                    }

textureParam =      {
                        'tex1' : 'color1',
                        'tex2' : 'color0',
                        'uscale' : 'uscale',
                        'vscale' : 'vscale'
                    }

# in pbrt, plastic doesn't respond well to roughness params
materialType =      {
                        'matte' : 'diffuse',
                        'metal' : 'conductor',
                        'mirror' : 'conductor',
                        'glass' : 'dielectric',
                        'uber' : 'thindielectric',
                        'substrate' : 'plastic',
                        'translucent' : 'difftrans'
                    }

matteParam =        {
                        'Kd' : 'reflectance'
                    }

glassParam =        {
                        'Kr' : 'specularReflectance',
                        'Kt' : 'specularTransmittance',
                        'index' : 'intIOR'
                    }

uberParam =         {
                        'intIOR' : 'index',
                        'specularReflectance' : 'Kr',
                        'specularTransmittance' : 'Kt'
                    }

substrateParam =    {
                        'alphaU' : 'uroughness',
                        'alphaV' : 'vroughness',
                        'diffuseReflectance' : 'Kd',
                        'specularReflectance' : 'Ks'
                    }

metalParam =        {
                        'eta' : 'eta',
                        'k' : 'k',
                        #'specularReflectance' : 'Kr',
                        'alphaU' : 'uroughness',
                        'alphaV' : 'vroughness'
                    }

translucentParam =  {
                        'transmittance' : 'Kt'
                    }

materialDict =      {
                        'matte' : matteParam,
                        'metal' : metalParam,
                        'mirror' : metalParam,
                        'glass' : glassParam,
                        'uber' : uberParam,
                        'substrate' : substrateParam,
                        'translucent' : translucentParam
                    }