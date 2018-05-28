integratorType =    {   'path'  : 'path',
                        'directlighting' : 'directlighting',
                        'bdpt' : 'bdpt', 
                        'mlt' : 'mlt',
                        'sppm' : 'sppm'
                    }

integratorParam =   {   # path, volpath_simple, volpath
                        'maxdepth' : 'maxdepth',
                        
                        # ppm, sppm
                        'iterations' : 'maxphotondepth',
                        'photonsperiteration' : 'photonperpass',
                        'initialRadius' : 'startradius',
                        'alpha' : 'alpha',
                        'bootstrapsamples' : 'bootstrapsamples',
                        'largestepprobability' : 'largestepprobability',
                        'sigma' : 'sigma'
                    }

samplerType =       {   'random' : 'independent',
                        'stratified' : 'stratified',
                        'lowdiscrepancy' : 'ldsampler',
                        'sobol' : 'sobol'
                    }

samplerParam =      {   'pixelsamples' : 'pixelsamples'  }

filmType =          {   'fleximage' : 'image' }

filmParam =         {   'xresolution' : 'xresolution',
                        'yresolution' : 'yresolution',
                        'filename' : 'filename'
                    }

filterType =        {
                        'box' : 'box',
                        'triangle' : 'triangle',
                        'gaussian' : 'gaussian',
                        'mitchell' : 'mitchell',
                        'sinc' : 'sinc'
                    }
    
sensorType =        {   'perspective' : 'perspective',
                        'orthographic' : 'orthographic',
                        'environment' : 'environment',
                        'realistic' : 'realistic'
                    }

sensorParam =       {   #perspective
                        'fov' : 'fov',
                        'shutteropen' : 'shutteropen',
                        'shutterclose' : 'shutterclose',
                        # thinlens
                        'lensradius' : 'lensradius',
                        'focaldistance' : 'focaldistance'
                    }

textureType =       {
                        'imagemap' : 'imagemap',
                        'checkerboard' : 'checkerboard',
                        'scale' : 'scale'
                    }

textureParam =      {
                        'filename' : 'filename',
                        'trilinear' : 'trilinear',
                        'color1' : 'tex1',
                        'color0' : 'tex2',
                        'uscale' : 'uscale',
                        'vscale' : 'vscale'
                    }

materialType =      {
                        'matte'  : 'matte',
                        'mirror' : 'mirror',
                        'metal2' : 'metal',
                        'glass' : 'glass',
                        'glossy' : 'substrate',
                        'mattetranslucent' : 'translucent'
                    }

matteParam =      {
                        'Kd' : 'Kd'
                    }

glassParam =        {
                        'Kr' : 'Kr',
                        'Kt' : 'Kt',
                        'index' : 'index',
                        'uroughness' : 'uroughness',
                        'vroughness' : 'vroughness',
                        'remaproughness' : 'remaproughness'
                    }
glossyParam =    {
                        'Kd' : 'Kd',
                        'Ks' : 'Ks',
                        'uroughness' : 'uroughness',
                        'vroughness' : 'vroughness',
                        'remaproughness' : 'remaproughness'
                    }

metalParam =        {
                        'eta' : 'eta',
                        'k' : 'k',
                        'uroughness' : 'uroughness',
                        'vroughness' : 'vroughness',
                        'remaproughness' : 'remaproughness'
                    }

translucentParam =  {
                        'Kt' : 'Kt'
                    }

materialDict =      {
                        'matte' : matteParam,
                        'metal2' : metalParam,
                        'glass' : glassParam,
                        'glossy' : glossyParam,
                        'translucent' : translucentParam
                    }

emitterType = {}

emitterParam =      {
                        'L' : 'L',
                        'from' : 'from',
                        'to' : 'to'
                    }