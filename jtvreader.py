#!/usr/bin/python

import sys
import jtv
from jtvdb import JtvDB


print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
print "Preferred encoding: ",jtv.preferredEncoding

zipPath = u'/home/bocha/Downloads/jtv'
zipFileName = u'jtv.zip'




jtvDb = JtvDB()

try:
#    arrNames = []
#    for i in range(0, 10):
#        arrNames.append((i, u"Channel %s" % i))
#    jtvDb.addChannelArray(arrNames)
    objJtv = jtv.JTV(zipPath, zipFileName)
    objJtv.execute()

    objJtv.printInfo()

    jtvDb.printChannel()
except Exception, e:
    print "Exception: %s" % e
#    sys.exit(1)
finally:
    jtvDb.close()


print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"



