import sqlite3

class DBManager:

    def __init__(self, name='database.db'):
        self.connect(name)
        self.createTables('createFirmwareDBTables.sql')

#--------------------------------------------------------------------------------------------------

    def connect(self, db):
        self.conn = sqlite3.connect(db)
        print "Opened database successfully";

#--------------------------------------------------------------------------------------------------

    def createTables(self, init):
        with open(init, 'r') as f:
            sql = f.read()
            self.conn.executescript(sql)
        print "Created tables successfully";

    def commit(self):
        self.conn.commit()
#--------------------------------------------------------------------------------------------------

    def close(self):
        print "Database closed successfully";
        self.conn.close()

#--------------------------------------------------------------------------------------------------

    def addVendor(self, n):
        """
        Adds vendor to vendor table in database.

        Arguments:
        n: name (text name of vendor)
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO vendor VALUES (NULL, ?);", ((n,)))
        #self.conn.commit()
        #print "Data inserted successfully";

#--------------------------------------------------------------------------------------------------

    def addDevice(self, m, v):
        """
        Adds device to device table in database.

        Arguments:
        m: model (text name of model)
        v: vendor (integer id reference to vendor table)
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO device VALUES (NULL, ?, ?);", (m, v))
        #self.conn.commit()
        #print "Data inserted successfully";

#--------------------------------------------------------------------------------------------------

    def addFirmware(self, d, v, r, e, p, h):
        """
        Adds firmware to firmware table in database.

        Arguments:
        d: device (integer id reference to device table)
        v: vendor (integer id reference to vendor table)
        r: revision (text name of revision)
        e: entropy_plot (text path of stored entropy_plot)
        p: path (text path to stored firmware)
        h: hash (text md5 hash)
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO firmware VALUES (NULL, ?, ?, ?, ?, ?, ?);", (d, v, r, e, p, h,))
        #self.conn.commit()
        #print " - Data inserted successfully";

#--------------------------------------------------------------------------------------------------

    def addDir(self, f, c, d, o, h):
        """
        Adds directory to directory table in database.

        Arguments:
        f: firmware (integer id reference to firmware table)
        d: directory_name (text name of directory)
        o: full path (text path from root of fs)
        h: hash (text md5 hash)
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO directory VALUES (NULL, ?, ?, ?, ?, ?);", (f, c, d, o, h,))
        lastid = cur.execute('SELECT last_insert_rowid()')
        x = lastid.fetchone()
        return x[0]
        #self.conn.commit()
        #print "Data inserted successfully";

#--------------------------------------------------------------------------------------------------

    def addFile(self, d, f, n, p, s, h):
        """
        Adds file to file table in database.

        Arguments:
        d: directory (integer id reference to directory table)
        f: firmware (integer id reference to firmware table)
        n: file_name (text name of file)
        p: full path (text path from root of fs)
        s: size (integer filesize in bytes)
        h: hash (text md5 hash)
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO file VALUES (NULL, ?, ?, ?, ?, ?, ?);", (d, f, n, p, s, h,))
        #self.conn.commit()
        #print "Data inserted successfully";

#--------------------------------------------------------------------------------------------------

    def addLink(self, d, f, n, p, rp):
        """
        Adds file to file table in database.

        Arguments:
        d: directory (integer id reference to directory table)
        f: firmware (integer id reference to firmware table)
        n: file_name (text name of file)
        p: full path (text path from root of fs)
        rp: real path (text path to real file)
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO link VALUES (NULL, ?, ?, ?, ?, ?);", (d, f, n, p, rp,))
        #self.conn.commit()
        #print "Data inserted successfully";

#--------------------------------------------------------------------------------------------------
