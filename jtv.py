#!/usr/bin/python
import StringIO
from _io import BytesIO
import locale
import zipfile
import datetime


__author__ = 'bocha'


# n Python 'cp855', 'cp866', 'cp1251', 'iso8859_5', 'koi8_r' are differing Russian code pages.
preferredEncoding = locale.getpreferredencoding()

class JTV :

    __jtvPath = ""
    __jtvFileName = ""
    __jtvEncode = ""
    __zipFile = zipfile.ZipFile

    def __init__(self, path, fileName, encode):
        self.__jtvPath = path
        self.__jtvFileName = fileName
        self.__jtvEncode = encode

    def printInfo(self):
        print "\n"+self.__jtvPath+self.__jtvFileName,"[",self.__jtvEncode,"]"

    def execute (self):

        self.__zipFile = zipfile.ZipFile(self.__jtvPath+'/'+self.__jtvFileName, 'r')
        print "[",self.__jtvFileName,"].len: ", len(self.__zipFile.filelist)

        for jtvFile in self.__zipFile.filelist:
            fileName = jtvFile.filename
            sizeFileName = len(fileName)
            extFile = fileName[sizeFileName-3:]
            fileNameEncoding = fileName.decode(self.__jtvEncode)
            if not isinstance(fileNameEncoding, unicode):
                print "Wrong encode [" + self.__jtvEncode + "]: ",fileName
            else :
                print "\nFile: " + fileNameEncoding,"[",jtvFile.file_size,"]"
#                if extFile.lower() == 'pdt':
#                    self.__readPdtFile(jtvFile)
#                    break
                if extFile.lower() == 'ndx':
                    self.__readNdxFile(jtvFile)
                    break

        self.__zipFile.close()


    def __readPdtFile(self, file):
        fileName = file.filename
        sizeFile = file.file_size
        fileData = self.__zipFile.read(fileName, 'rU')
        bt = BytesIO(fileData)
        bt.seek(int('0x01A', 0))
        while bt.tell() < sizeFile:
            lenBytes = bt.read(2)
            lenSum = ord(lenBytes[0]) + ord(lenBytes[1])
            bytesProName = bt.read(lenSum)
            pos = bt.tell()
            print "[%2s >> %4s] %s" % (lenSum, pos, bytesProName.decode("cp1251"))

        bt.close()

    def __readNdxFile(self, file):
        fileName = file.filename
        sizeFile = file.file_size
        print "--->>> ", fileName
        fileData = self.__zipFile.read(fileName, 'rU')
        bt = BytesIO(fileData)

        bt.seek(0)
        lenBytes = bt.read(2)
        lenSum = ord(lenBytes[0]) + ord(lenBytes[1])

        print "lenSum = ", lenSum
        while bt.tell() < sizeFile:
            lenBytes2 = bt.read(2)
            lenBytes2sum = ord(lenBytes2[0]) + ord(lenBytes2[1])

            startTime = bt.read(8)
            startTimeSum = 0
            for st in startTime:
                startTimeSum += ord(st)

            startTimeSum *= 116444736000000000/10000000

#            print "# " + datetime.datetime.


            offsetPdt = bt.read(2)
            offsetPdtSum = ord(offsetPdt[0]) + ord(offsetPdt[1])

            pos = bt.tell()
            print "--->>> ",pos," -=< ", lenBytes2sum, startTimeSum, offsetPdtSum



