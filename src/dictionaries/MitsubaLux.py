integratorType =    {   'path'  : 'path',
                        'volpath_simple': 'path',
                        'volpath' : 'path',
                        'adaptive' : 'path',
                        'direct' : 'directlighting',
                        'bdpt' : 'bidirectional', 
                        'photonmapper' : 'sppm',
                        'ppm' : 'sppm',
                        'sppm' : 'sppm'
                    }

integratorParam =   {   # path, volpath_simple, volpath
                        'maxDepth' : 'maxdepth',
                        
                        # ppm, sppm
                        'maxPasses' : 'maxphotondepth',
                        'photonCount' : 'photonperpass',
                        'initialRadius' : 'startradius',
                        'alpha' : 'alpha',
                        'globalPhotons' : 'photonperpass',
                        'globalLookupRadius' : 'startradius'
                    }


samplerType =       {   'independent' : 'random',
                        'ldsampler' : 'lowdiscrepancy',
                        'hammersley' : 'random',
                        'sobol' : 'sobol'
                    }

samplerParam =      {   'sampleCount' : 'pixelsamples'  }

filmType =          {   'ldrfilm' : 'fleximage',
                        'hdrfilm' : 'fleximage',
                        'tiledhdrfilm' : 'fleximage',
                        'mfilm' : 'fleximage'
                    }

filmParam =         {   'width' : 'xresolution',
                        'height' : 'yresolution',
                        'gamma' : 'gamma'
                    }
                
filterType =        {
                        'box' : 'box',
                        'tent' : 'triangle',
                        'gaussian' : 'gaussian',
                        'mitchell' : 'mitchell',
                        'catmullrom' : 'catmullrom',
                        'lanczos' : 'sinc'
                    }

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

materialType =      {
                        'diffuse'  : 'matte',
                        'diffuseReflectance' : 'matte',
                        'roughdiffuse' : 'matte',
                        'conductor' : 'mirror',
                        'roughconductor' : 'metal2',
                        'dielectric' : 'glass',
                        'roughdielectric' : 'roughglass',
                        'thindielectric' : 'glass',
                        'plastic' : 'glossy',
                        'roughplastic' : 'glossy',
                        'difftrans' : 'mattetranslucent'
                    }
diffuseParam =     {
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

plasticParam =      {
                        #'intIOR' : 'index',
                        'alphaU' : 'uroughness',
                        'alphaV' : 'vroughness',
                        'diffuseReflectance' : 'Kd',
                        'specularReflectance' : 'Ks'
                    }

conductorParam =    {
                        #'eta' : 'eta',
                        #'k' : 'k',
                        #'specularReflectance' : 'Kr',
                        #'extEta' : 'filmindex',
                        'alphaU' : 'uroughness',
                        'alphaV' : 'vroughness'
                    }

difftransParam =    {
                        'transmittance' : 'Kt'
                    }
emitterType = {}

emitterParam =      {
                        'turbidity' : 'turbidity',
                        'sunRadiusScale' : 'relsize',
                        'samplingWeight' : 'nsamples',
                        'radiance' : 'L'
                    }