#!/usr/bin/python
# -*- coding: UTF-8 -*-
import locale

import sqlite3 as lite
from datetime import datetime
import sys

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
        except lite.Error, e:
            self.close()
            print "Error: %s" % e.message
            sys.exit(1)


    def close(self):
        if self.__con:
            self.__con.close()


    def printChannel(self):
        sql = self.__con.cursor()
        sql.execute('SELECT * FROM %s ;' % self.__sTvView)
        for row in sql:
            print  "%25s %60s %16s" % (row[0], row[1], datetime.fromtimestamp(row[2]))
        sql.close()

    def updateChannels(self, arrays):
        sql = self.__con.cursor()
        for channel in arrays.keys():
            sql.execute('INSERT OR IGNORE INTO {0}(name) VALUES(?);'.format(self.__sTvChannelTable), (channel,))

            for offset in arrays[channel].keys():
                sqlSelect = "SELECT * FROM {0} WHERE name=?;".format(self.__sTvChannelTable)
                sql.execute(sqlSelect, (channel,))
                row = sql.fetchone()
                keyChannel = row[0]
                nm = arrays[channel][offset]
                if nm[0] is not None and nm[1] is not None:
                    sql.execute('INSERT OR IGNORE INTO {0}(keyChannel, offset, name, time) VALUES(?, ?, ?, ?);'.format(self.__sTvProgrTable), (keyChannel, offset, nm[0], nm[1]))

        self.__con.commit()
        sql.close()


    def removeAll(self):
        sql = self.__con.cursor()
        arrSql = (
            "DROP TABLE IF EXISTS {0};".format(self.__sTvChannelTable),
            "DROP TABLE IF EXISTS {0};".format(self.__sTvProgrTable),
            "DROP VIEW IF EXISTS {0};".format(self.__sTvView),
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
            "PRAGMA foreign_keys=ON;",
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
            "CREATE UNIQUE INDEX IF NOT EXISTS ixChannelName ON {0} (name);".format(self.__sTvChannelTable),
            """
                CREATE VIEW {0} AS SELECT t1.name channel, t2.name prog, t2.time dt FROM {1} t1 LEFT JOIN {2} t2 ON t1.key = t2.keyChannel ORDER BY t1.name, t2.time;
            """.format(self.__sTvView, self.__sTvChannelTable, self.__sTvProgrTable)
            )
        for s002 in arrSql:
            sql.execute(s002)
        self.__con.commit()
        sql.close()





