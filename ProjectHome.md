# The Big Picture #

The Big Picture is an early attempt for a Python library to read and write Exif and IPTC metadata from and to JPEG and TIFF files. It is in a very early stage.

This library is fallout from the [Happy Camel](http://happycamel.sourceforge.net/) project, a tool to correlate GPS data with digital photo's.

## Status ##
Currently, The Big Picture is in a alpha stage, which basically means that _I_ have succesfully used it on a few example pictures. There is a first alpha release, and the bleeding-edge code is in Subversion.

There is support for reading and writing Exif and IPTC metadata in Jpeg and Tiff files, and Jpeg comments.

The basic structure is there, but a lot of work is required to make sure all checks are in place for reading, writing and setting tags. Furthermore, I'm still compiling the tag libraries with all their requirements (luckily I can peek at [Exiftool's documentation](http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/index.html) :)

**If you're interested in using this library, please bear in mind that, currently, it might invalidate your images!** The good news is that the files themselves are untouched, and alterations are only written to copies :)

## Usage ##

Usage and other information may be found in [this project's Wiki](http://code.google.com/p/thebigpicture/wiki/Usage).