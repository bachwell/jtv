#!/usr/bin/python

import sys
import jtv


print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
print "Preferred encoding: ",jtv.preferredEncoding

zipPath = u'/home/bocha/Downloads/jtv'
zipFileName = u'jtv.zip'
zipEncode = u'cp866'



objJtv = jtv.JTV(zipPath, zipFileName, zipEncode)
objJtv.execute()

objJtv.printInfo()


print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"



