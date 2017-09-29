# integrator

integratorType =    {   'path'  : 'path',
                        'volpath_simple': 'path',
                        'volpath' : 'path',
                        'adaptive' : 'path',
                        'ptracer' : ???,
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
                        'hideEmitters' : '',
                        'strictNormals' : '',
                        'rrDepth',
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
                        'photonCount' : '',
                        'initialRadius' : '',
                        'alpha' : '',
                        'maxPasses' : '',
                        #pssmlt, mlt
                        'bidirectional' : '',
                        'luminanceSamples' : '',
                        'twoStage' : '',
                        'pLarge',
                        'bidirectionalMutation' : '',
                        'lambda' : '',
                        #erpt                        
                        'numChains' : '',
                        'maxChains' : '',
                        'chainLength' : '',



                    }

