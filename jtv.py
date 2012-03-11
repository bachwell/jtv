#!/usr/bin/python
import StringIO
from _io import BytesIO
import locale
import zipfile
import datetime

# n Python 'cp855', 'cp866', 'cp1251', 'iso8859_5', 'koi8_r' are differing Russian code pages.
from jtvdb import JtvDB
from datetime import datetime

preferredEncoding = locale.getpreferredencoding()

class JTV :

    __jtvPath = ""
    __jtvFileName = ""
    __jtvEncodeFileName = ""
    __jtvEncodeProgrammName = ""
    __zipFile = zipfile.ZipFile
    __jtvDb = JtvDB()

    def __init__(self, path, fileName):
        self.__jtvPath = path
        self.__jtvFileName = fileName

#        self.__jtvDb.removeAll()
#        self.__jtvDb.create()
        self.__jtvEncodeFileName = u'cp866'
        self.__jtvEncodeProgrammName = u'cp1251'


    def printInfo(self):
        print "\n"+self.__jtvPath+self.__jtvFileName,"[",self.__jtvEncodeFileName,"]"

    def execute (self):

        self.__zipFile = zipfile.ZipFile(self.__jtvPath+'/'+self.__jtvFileName, 'r')
        print "[",self.__jtvFileName,"].len: ", len(self.__zipFile.filelist)

        arrChannel = []

        for jtvFile in self.__zipFile.filelist:
            fileName = jtvFile.filename
            sizeFileName = len(fileName)
            extFile = fileName[sizeFileName-3:]
            fileNameEncoding = unicode(fileName, self.__jtvEncodeFileName)
            if not isinstance(fileNameEncoding, unicode):
                print "Wrong encode [" + self.__jtvEncodeFileName + "]: ",fileName
            else :
                arrNDX = []
#                print "\nFile: " + fileNameEncoding,"[",jtvFile.file_size,"]"
                chName = fileNameEncoding[0:sizeFileName-4]
                if (chName,) not in arrChannel:
                    arrChannel.append((chName,))

                if extFile.lower() == 'pdt':
                    arrNDX = self.__readPdtFile(jtvFile)
                if extFile.lower() == 'ndx':
                    arrNDX = self.__readNdxFile(jtvFile)

                self.__jtvDb.addTimeArray(chName, arrNDX)
                del arrNDX
#                break
#        self.__jtvDb.addChannelArray(arrChannel)
        self.__zipFile.close()
        del arrChannel


    def __readPdtFile(self, file):
        returnData = []
        fileName = file.filename
        sizeFile = file.file_size
        fileData = self.__zipFile.read(fileName, 'rU')
        bt = BytesIO(fileData)
        bt.seek(int('0x01A', 0))
        while bt.tell() < sizeFile:
            pos = bt.tell()
            lenBytes = bt.read(2)
            lenBytesHex = "0x" + ''.join( [ "%02X" % ord( x ) for x in reversed(lenBytes) ] )
            lenSum = int(lenBytesHex, 0)
            bytesProName = unicode(bt.read(lenSum), self.__jtvEncodeProgrammName)
            returnData.append((pos, bytesProName, None))

        bt.close()
        return returnData

    def __readNdxFile(self, file):
        returnData = []
        fileName = file.filename
        sizeFile = file.file_size
#        print "--->>> ", fileName
        fileData = self.__zipFile.read(fileName, 'rU')
        bt = BytesIO(fileData)

        bt.seek(0)
        lenBytes = bt.read(2)
        lenSum = self.BytesToInt(lenBytes)
#        print "lenSum = ", lenSum

        while bt.tell() < sizeFile:
            lenBytes12 = bt.read(12)

            # NULL bytes
            bytesNull = lenBytes12[0:2]
            bytesNullInt = self.BytesToInt(bytesNull)
            # FILETIME bytes
            bytesFileTime = lenBytes12[2:10]
            bytesFileTimeInt = self.BytesToInt(bytesFileTime)
            # offset in PDT bytes
            bytesOffsetPdt = lenBytes12[10:12]
            bytesOffsetPdtInt = self.BytesToInt(bytesOffsetPdt)

            startTimeInt = self.FiletimeToUnixtimestamp(bytesFileTimeInt)
#            print "--->>> ", startTimeInt, " = ", datetime.fromtimestamp(startTimeInt), " =>> ", bytesOffsetPdtInt
            returnData.append((bytesOffsetPdtInt, None, startTimeInt))

        bt.close()
        return returnData


    def FiletimeToUnixtimestamp(self, uts):
        returnValue = -1
        since1601 = 116444736000000000
        IntervalsInSecond = 10000000
        returnValue = (uts - since1601)/IntervalsInSecond

        return returnValue

    def BytesToInt(self, bytes):
        bytesHex = "0x" + ''.join( [ "%02X" % ord( x ) for x in reversed(bytes) ] )
        bytesInt = int(bytesHex, 0)

        return bytesInt








