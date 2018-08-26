# PBR Scene Converter

This software can be used to convert scene files between different renderer file formats. Currently, our software supports *Mitsuba*, *PBRT v3* and *LuxRender* file formats.   

We are currently an alpha version. See `Limitations` for further details.

## Requirements

This software requires the installation of:
    - [Python 3](https://www.python.org/download/releases/3.0/)
    - [PLY](https://www.dabeaz.com/ply/)
    - [Numpy 1.14.0 (and up)](https://github.com/numpy/numpy/releases)

## Running

Currently the converter can be run locally downloading the source code or cloning this repository. Conversion to and from renderers can currently only be executed through the command line in the `src` directory of this project.

The command for converting files between renderers is:

`python __init__.py -s [source renderer] -d [destination render] -f [input filename]`

The default option will create a file named `scene` with the extension of the desired renderer. Optionally, the user can specify the name of the output file in the command: `-o [output filename]`

For example, converting a file from `Mitsuba` to `PBRT v3` with the name `lamp` inputs the following command:

`python __init__.py -s mitsuba -d pbrt -f /path/to/lamp.xml -o lamp`

## Limitations

Our converter *currently* does not support:
    - Hair materials
    - Participating Media
    - Animations
    - Converting colored metals to and from LuxRender
