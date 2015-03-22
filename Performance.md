# Introduction #

Operation speed and resource usage are of course quite important for a library. While Python as an interpreted language may be a bit slower than compiled code, it is still possible to achieve quite acceptable results. This library tries its best to be as fast as possible while keeping memory requirements low. There are also some things a user of this library can do to get the best results out of it.

## Specifying a record ##

The nature of both Exif and IPTC data makes it so that everything has to be completely read and rewritten if something changes. This results in a slowdown of writing operations. However, in the case of Exif data it is possible to speed up the _reading_ of metadata by reading only the required record. This is done by specifying the record name or number in the getExifTag() method (for IPTC data, this trick does not work, because IPTC data has to be read entirely no matter what).

For example, if we only want to know the map datum of an image, which is stored in the GPS record, we can do:
```
j = TBP.jpeg("foo.jpg")
datum = j.getExifTag("GPSMapDatum")
```
This will give you the right result, or False if it's not there. However, since we know it's in the GPS block, we can also do:
```
j = TBP.jpeg("foo.jpg")
datum = j.getExifTag("GPSMapDatum", "gps")
```
This will give the result much faster (in my personal test, about three times as fast). If you are working with a handful of images, the results may not be of much importance. However, if that number raises towards the hundreds, this trach may save you a lot of time.

**Warning:** If you specify the record but the tag is for some reason stored in a different record (I don't know if this happens in the wild), it will not be found.