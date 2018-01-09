from mitsuba import MitsubaToPBRTv3 as mp
from core import MitsubaLoader as mit

if __name__ == '__main__':
	loader = mit.MitsubaLoader('/Users/luiza.hagemann/Development/pbr_scene_converter/test_files/mitsuba/teapot.xml')
	mp.MitsubaToPBRTv3(loader.scene, "scene.pbrt")

