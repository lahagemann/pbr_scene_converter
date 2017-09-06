%start scene 
%%

scene			: directives world
				;

directives		: integrator transform sampler filter film camera
				;

integrator		: "Integrator" integrator_type integrator_parameter_list
				;

transform		:
				| "Transform" transform_matrix
				;

sampler			: 
				| "Sampler" sampler_type sampler_parameter_list
				;
	
filter			: 
				| "PixelFilter" filter_type filter_parameter_list
				;

film			:
				| "Film" "image" film_parameter_list
				;

camera			: 
				| "Camera" camera_type camera_parameter_list
				;

integrator_type	: "bdpt"
				| "directlighting"
				| "mlt"
				| "path"
				| "sppm"
				| "whitted"
				;


http://www.cs.man.ac.uk/~pjj/cs212/ex5_hint.html
http://www.cs.man.ac.uk/~pjj/cs212/ho/node4.html#SECTION00046000000000000000
https://ds9a.nl/lex-yacc/cvs/lex-yacc-howto.html

