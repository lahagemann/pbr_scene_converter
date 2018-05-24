import sys
import glob
import LuxLex
import LuxYacc

class PBRTv3Loader:
    def assembleSingleFile(directory):
        if directory.endswith('/'):
            directory = directory.replace('/','')

        lxs = ''

        for file in glob.glob(directory + '/*.lxs'):
            with open(file) as infile:
                for line in infile:
                    if 'Include' in line.strip():
                        filename = line.replace('\n','').replace('"','').split(' ')[1]
                        lxs += open(directory + '/' + filename).read()
                    else:
                        lxs += line
                
        return lxs
    
    def importFile(self, filename):
        data = open(filename).read()
        sceneStructure = PBRTv3Yacc.parse(data)

        return sceneStructure