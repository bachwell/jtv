#!/usr/bin/python
# -*- coding: UTF-8 -*-
import locale

import sqlite3 as lite
import sys
import logging as log

class JtvDB :

    __preferredEncoding = locale.getpreferredencoding()

    __dbName = u"jtv.db"
    __con = None

    __sTvChannelTable = u'tbChannel'
    __sTvProgrTable = u'tbProgr'
    __sTvView = u'vProg'

    def __init__(self):
        try:
            self.__con = lite.connect(self.__dbName)
            sql = self.__con.cursor()

            arrSql = (
                "PRAGMA foreign_keys=ON;",
                """
                    CREATE TEMPORARY VIEW {0} AS SELECT * FROM {1} t1 LEFT JOIN {2} t2 ON t1.key = t2.keyChannel;
                """.format(self.__sTvView, self.__sTvChannelTable, self.__sTvProgrTable)
                )

            for s002 in arrSql:
                sql.execute(s002)

            self.__con.commit()

            sql.close()

        except lite.Error, e:
            self.close()
            print "Error: %s" % e.message
            sys.exit(1)


    def close(self):
        if self.__con:
            self.__con.close()


    def printChannel(self):
        sql = self.__con.cursor()

        sql.execute('SELECT * FROM %s v1 ;' % self.__sTvView)

        for row in sql:
#            pass
#            print  unicode(row, self.__preferredEncoding)
#            sPrint = "\t\t\t\t".join(str(v) for v in row)
            print  row

        sql.close()

    def addChannelArray(self, names):
        sql = self.__con.cursor()
        for nm in names:
            sql.execute('INSERT INTO {0}(name) VALUES(?)'.format(self.__sTvChannelTable), nm)
        self.__con.commit()
        sql.close()

    def removeAll(self):
        sql = self.__con.cursor()

        arrSql = (
            "DROP TABLE IF EXISTS {0};".format(self.__sTvChannelTable),
            "DROP TABLE IF EXISTS {0};".format(self.__sTvProgrTable),
#            "DROP VIEW IF EXISTS {0};".format(self.__sTvView),
            "DROP INDEX IF EXISTS ixKeyChannel;",
            "DROP INDEX IF EXISTS ixOffsetPr;"
            )

        for s002 in arrSql:
            sql.execute(s002)

        self.__con.commit()

        sql.close()

    def create(self):
        sql = self.__con.cursor()

        arrSql = (
#            "PRAGMA foreign_keys=ON;",
            """
                CREATE TABLE {0}
                (
                    key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT
                );
            """.format(self.__sTvChannelTable),
            """
                CREATE TABLE {1}
                (
                    key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    keyChannel INTEGER,
                    offset INTEGER,
                    name TEXT,
                    time TIMESTAMP DEFAULT NULL,
                    FOREIGN KEY(keyChannel) REFERENCES {0}(key) ON DELETE SET NULL
                );
            """.format(self.__sTvChannelTable, self.__sTvProgrTable),
            "CREATE INDEX IF NOT EXISTS ixKeyChannel ON {0} (keyChannel);".format(self.__sTvProgrTable),
            "CREATE UNIQUE INDEX IF NOT EXISTS ixOffsetPr ON {0} (offset);".format(self.__sTvProgrTable)
            )

        for s002 in arrSql:
            sql.execute(s002)

        self.__con.commit()

        sql.close()





