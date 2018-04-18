from mitsuba import MitsubaToPBRTv3 as mp
from mitsuba import MitsubaToLuxRender as ml
from core import MitsubaLoader as mit
from core import PBRTv3Loader as pbrt
from pbrt import PBRTv3ToMitsuba as pm

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

			if destination == 'pbrt':
				if not output.endswith('.pbrt'):
					output += '.pbrt'
				mp.MitsubaToPBRTv3(loader.scene, output)
				
			elif destination == 'lux' or destination == 'luxrender':
				ml.MitsubaToLuxRender(loader.scene, output)

			else:
				print 'The output renderer informed is not valid. For a mitsuba input file, please type -d pbrt or -d lux.\n'

		elif source == 'pbrt':
			loader = pbrt.PBRTv3Loader(filename)

			if destination == 'mitsuba':
				pm.PBRTv3ToMitsuba(loader.scene, output)
				
			# elif destination == 'lux' or destination == 'luxrender':
			# 	pl.PBRTv3ToLuxRender(loader.scene, output)

			else:
				print 'The output renderer informed is not valid. For a mitsuba input file, please type -d pbrt or -d lux.\n'
		else:
			print 'The source renderer informed is not valid. Current valid source renderers are: pbrt, mitsuba. \n'

		# convert
		

