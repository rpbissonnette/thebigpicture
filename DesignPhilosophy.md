# Design philosophy #

The Big Picture doesn't have much of a design philosophy, except for the principle that it does as much on the file reading and deciphering as possible only on request, to have a better performance. For example, Exif tags are not deciphered by the file readers, only when the user specifically asks for it.

I don't know if it actually makes much of a difference, or even if this is always the best approach. For example, it might be faster to read an IFD as a block into memory instead of seeking on disk (but even then, deciphering is not necessary until the user requests it).