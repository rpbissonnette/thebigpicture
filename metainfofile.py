# Copyright 2007 Pieter Edelman (p _dot_ edelman _at_ gmx _dot_ net)
#
# This file is part of The Big Picture.
# 
# The Big Picture is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# The Big Picture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with The Big PictureGe; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# 

import byteform

class Photoshop:
  """ Read and write the photoshop structure. """
  
  def __init__(self, *args, **kwargs):
    """ Initialize the structure. It may be done by passing an open file object,
        offset to the start of the structure, and length, or by passing the
        binary content as string. An optional big_endian argument may be given
        to determine the byte ordering (defaults to big endian). """
        
    if (len(args) == 3):
      self.fp, self.offset, self.length = args
      self.content = None
    else:
      self.fp, self.offset = None
      self.content = args[0]
      self.length = len(self.content)
    
    if ("big_endian" in kwargs):
      self.is_be = kwargs["big_endian"]
    else:
      self.is_be = True
    
    self.tags = {}
    
    # Needed for reading from file or string
    self.byte_pos = 0
    
    self.parse()
    
  def parse(self):
    """ Parse the structure. """
    
    while (self.byte_pos < self.length):
      # The first four bytes of a data structure should always be the ASCII
      # string 8BIM
      data = self.__readBytes__(4)
      if (data != "8BIM"):
        break

      # The next two bytes specify the resource ID (tag number)
      tag_num = byteform.btoi(self.__readBytes__(2), big_endian = self.is_be)
        
      # What then follows is the "Pascal string". The first byte determines its
      # length. If the total is an uneven number, it is padded with a \x00
      # character. We don't need this string, so we step over it. 
      ps_len =  byteform.btoi(self.__readBytes__(1), big_endian = self.is_be)
      if ((ps_len % 2) == 0):
        ps_len += 1
      self.__readBytes__(ps_len)
        
      # Now it's getting interesting; the next four bytes determine the length
      # of the data
      data_len = byteform.btoi(self.__readBytes__(4), big_endian = self.is_be)
       
      # Store the byte position and data length in the tags dict
      self.tags[tag_num] = [self.byte_pos, data_len]
        
  def __readBytes__(self, num_bytes):
    """ Read a number of bytes from either the content or the file, and return
        them. """
    
    data = None
    
    if ((self.byte_pos + num_bytes) > self.length):
      raise "Attempt to read beyond the size of the data block!"
      
    if (self.fp) and (self.offset):
      self.fp.seek(self.offset + self.byte_pos)
      data = self.fp.read(num_bytes)
    elif (self.content):
      data = self.content[byte_pos:byte_pos + num_bytes]
      
    self.byte_pos += num_bytes
    
    return data
        
class MetaInfoFile:
  """The base class for files containing meta information."""
  
  def __init__(self):
    self.ifds = dict.fromkeys(["tiff", "exif", "gps"], None)

  def getExifTagPayload(self, tag):
    """ Return the payload of a tag with the specified name. """
    
    payload = None
    
    # Iterate over all IFD's
    for ifd in ['tiff', 'exif', 'gps']:
      if (self.ifds[ifd]):
        payload = self.ifds[ifd].getTagPayload(tag)
        if payload:
          break

    return payload

  def getExifBlock(self):
    """ Return the encoded Tiff, Exif and GPS IFD's as a block. """
    
    # The exif data can have a different endianness than the JPEG file
    ifd_is_be = self.ifds["tiff"].is_be
          
    # Calculate the different byte offsets (within the segment)
    if "exif" in self.ifds:
      exif_ifd_offset = self.ifds["tiff"].getSize() + 8 # 8 for Tiff header
    else:
      exif_ifd_offset = 0
      
    if "gps" in self.ifds:
      gps_ifd_offset  = exif_ifd_offset + self.ifds["exif"].getSize()
    else:
      gps_ifd_offset = 0

    # Set the offsets to the tiff data
    if (exif_ifd_offset):
      self.ifds["tiff"].setTagPayload("Exif IFD Pointer", exif_ifd_offset)
    if (gps_ifd_offset):
      self.ifds["tiff"].setTagPayload("GPSInfo IFD Pointer", gps_ifd_offset)
          
    # Write the Exif IFD's
    byte_str = self.ifds["tiff"].getByteStream(8)
    if ("exif" in self.ifds):
      byte_str += self.ifds["exif"].getByteStream(exif_ifd_offset)
    if ("gps" in self.ifds):
      byte_str += self.ifds["gps"].getByteStream(gps_ifd_offset)
      
    return byte_str
    
  def getIPTCBlock(self):
    """ Return the encoded IPTC data as a blcok. """
    pass