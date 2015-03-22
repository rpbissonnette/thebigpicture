# Introduction #

The Big Picture currently handles Exif and IPTC metadata in Jpeg and Tiff files. Additionally, JPEG comments may be read and set.

Exif and IPTC data is stored in the form of tags with a certain tag number, scattered across several segments. Currently, The Big Picture knows of most tag numbers and (shorthand) names and segment numbers and names. To get or set metadata, you need to know the shorthand name or the number of your tag. Only if the tag number can occur in multiple records, a record name or number is known.

# Details #

To use this library, you first need to import The Big Picture:

`import TBP`

The library exports two classes, Jpeg and Tiff. Loading is done by calling these classes with the file name as argument.

## Manipulating the metadata ##

Then you can get, set or delete Exif and IPTC metadata using the following methods:
  * Exif
    * getExifTag(_tag_)
    * setExifTag(_tag_, _payload_)
    * delExifTag(_tag_)
  * IPTC
    * getIPTCTag(_tag_)
    * setIPTCTag(_tag_, _payload_)
    * appendIPTCTag(_tag_, _payload_)
    * delIPTCTag(_tag_, _payload_)
The extra appendTag method in IPTC exists because some tags (like _Keywords_) may occur multiple times.

For Jpeg files, additional methods exist to manipulate the comments:
  * getComments()
  * setComment(_comment_, _append_ = False)
The _append_ parameter determines whether the comment should be appended, or override the existing comments.

## Writing the file ##

There is currently no way to save the data to the image file itself, you have to create a new file for that with the writeFile(_path_) method.

## Example ##

Say you want to embed the some keywords about the location and a description of your in one of your vacation images. This is how you would do it:
```
import TBP

# Load the image
j = TBP.Jpeg('/path/to/image.jpg')

# Get the keywords
iptc_keywords = j.getTag("Keywords")

# Append keywords not currently set
for keyword in ["England", "London", "Big Ben"]:
  if (keyword not in iptc_keywords):
    j.appendIPTCTag("Keywords", keyword)

# Set the comment, ignoring comments already in the image
j.setComment("My holiday at the Big Ben")

# Write the data to the file
j.writeFile('/path/to/copy.jpg')
```

Now you have two files, _image,jpg_ and the manipulated version _copy.jpg_. In its status, it might be a good idea to check if the copy is correct before you replace the original with it.

NOTE: instead of loading the IPTC tags and checking if a tag was already present, you could also simply have done the following:
```
j.delIPTCTag("Keywords")
for keyword in ["England", "London", "Big Ben"]:
  j.appendTag("Keyword", keyword)
```
