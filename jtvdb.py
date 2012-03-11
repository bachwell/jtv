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

            self.removeAll()
            self.create()

            sql = self.__con.cursor()

#            arrSql = (
#                "PRAGMA foreign_keys=ON;",
#                """
#                    CREATE TEMPORARY VIEW {0} AS SELECT t1.name channel, t2.name prog, t2.time dt FROM {1} t1 LEFT JOIN {2} t2 ON t1.key = t2.keyChannel;
#                """.format(self.__sTvView, self.__sTvChannelTable, self.__sTvProgrTable)
#                )
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
#            sys.exit(1)


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

    def addChannelArray(self, values):
        sql = self.__con.cursor()
        for nm in values:
            sql.execute('INSERT OR IGNORE INTO {0}(name) VALUES(?);'.format(self.__sTvChannelTable), nm)
        self.__con.commit()
        sql.close()

    def addTimeArray(self, channel, values):
        self.addChannelArray([(channel,)])
        sql = self.__con.cursor()
        sqlSelect = "SELECT * FROM {0} WHERE name=?;".format(self.__sTvChannelTable)
        sql.execute(sqlSelect, (channel,))
        row = sql.fetchone()
        keyChannel = row[0]

        for nm in values:
            if nm[0] is not None and nm[2] is not None:
                sql.execute('INSERT OR IGNORE INTO {0}(keyChannel, offset, time) VALUES(?, ?, ?);'.format(self.__sTvProgrTable), (keyChannel,nm[0], nm[2]))
                sql.execute('UPDATE {0} SET time=? WHERE offset=? AND keyChannel=?;'.format(self.__sTvProgrTable), (nm[2], nm[0], keyChannel))

            if nm[0] is not None and nm[1] is not None:
                sql.execute('INSERT OR IGNORE INTO {0}(keyChannel, offset, name) VALUES(?, ?, ?);'.format(self.__sTvProgrTable), (keyChannel,nm[0], nm[1]))
                sql.execute('UPDATE {0} SET name=? WHERE offset=? AND keyChannel=?;'.format(self.__sTvProgrTable), (nm[1], nm[0], keyChannel))

        self.__con.commit()
        sql.close()

    def removeAll(self):
        sql = self.__con.cursor()

        arrSql = (
            "DROP TABLE IF EXISTS {0};".format(self.__sTvChannelTable),
            "DROP TABLE IF EXISTS {0};".format(self.__sTvProgrTable),
#            "DROP VIEW IF EXISTS {0};".format(self.__sTvView),
            "DROP INDEX IF EXISTS ixKeyChannel;",
            "DROP INDEX IF EXISTS ixOffsetPr;",
            "DROP INDEX IF EXISTS ixTime;",
            "DROP INDEX IF EXISTS ixChannelName;"
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
                    name TEXT NOT NULL
                );
            """.format(self.__sTvChannelTable),
            """
                CREATE TABLE {1}
                (
                    key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    keyChannel INTEGER DEFAULT NULL,
                    offset INTEGER,
                    name TEXT DEFAULT NULL,
                    time TIMESTAMP DEFAULT NULL,
                    FOREIGN KEY(keyChannel) REFERENCES {0}(key) ON DELETE SET NULL
                );
            """.format(self.__sTvChannelTable, self.__sTvProgrTable),
            "CREATE INDEX IF NOT EXISTS ixKeyChannel ON {0} (keyChannel);".format(self.__sTvProgrTable),
            "CREATE UNIQUE INDEX IF NOT EXISTS ixOffsetPr ON {0} (keyChannel, offset);".format(self.__sTvProgrTable),
            "CREATE  INDEX IF NOT EXISTS ixTime ON {0} (time);".format(self.__sTvProgrTable),
            "CREATE UNIQUE INDEX IF NOT EXISTS ixChannelName ON {0} (name);".format(self.__sTvChannelTable)
            )

        for s002 in arrSql:
            sql.execute(s002)

        self.__con.commit()

        sql.close()





