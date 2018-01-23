from mitsuba import MitsubaToPBRTv3 as mp
from core import MitsubaLoader as mit

import sys

if __name__ == '__main__':
	filename = ''
	source = ''
	destination = ''
	output = 'scene'

	if len(sys.argv) <= 1:
		print 'Please call PBR Scene converter using the following parameters: -s [source renderer] -d [destination render] -f [input filename] <option: -o [output filename]>'
	elif not '-f' in sys.argv:
		print 'No input file specified. Please call PBR Scene converter using the following parameters: -s [source renderer] -d [destination render] -f [input filename] -o [output filename]'
	elif not '-s'in sys.argv:
		print 'No source renderer specified. Please call PBR Scene Converter with the following parameters: -s [source renderer] -d [destination render] -f [input filename] -o [output filename]'
	
	else:
		for i in range(1,len(sys.argv)):
			if sys.argv[i] == '-s':
				source = sys.argv[i+1]

			elif sys.argv[i] == '-d':
				destination = sys.argv[i+1]

			elif sys.argv[i] == '-f':
				filename = sys.argv[i+1]

			elif sys.argv[i] == '-o':
				output = sys.argv[i+1]

		# load scene from file
		if source == 'mitsuba':
			loader = mit.MitsubaLoader(filename)

		else:
			loader = mit.MitsubaLoader(filename)

		# convert
		if destination == 'pbrt':
			mp.MitsubaToPBRTv3(loader.scene, output)
			if not output.endswith('.pbrt'):
				output += '.pbrt'
		else:
			mp.MitsubaToPBRTv3(loader.scene, output)
			if not output.endswith('.pbrt'):
				output += '.pbrt'

