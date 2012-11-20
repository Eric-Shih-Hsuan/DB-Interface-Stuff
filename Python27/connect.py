"""
Actual connection handles for Mongo and MySQL; used by dbconn
to create the connections.  
"""
import sys, os
import datetime, time

import pymongo, bson
import MySQLdb as ms


def makeMySQLConn(mens):
    '''
    Create MySQLConn object with connection to SQL database of type 'mens';
    return object
    '''
    if mens=='NBA':
        conn = NBASQLConn(db   = 'NBA_temp',
                          h    = 'localhost',
                          u    = 'sinn',
                          p    = 't')
    elif mens=='RSS':
        conn = RSSSQLConn()
    else:
        # error shit
    return conn

def makeMongoConn(mens, **dargs):
    '''
    Create MongoConn object with connection to Mongo database of type 'mens';
    return object
    '''
    if mens=='NBA':
        conn = NBAMonConn(db_name, coll_name)
    elif mens=='RSS':
        db_name = 'WebPages'
        coll_name = 'Wired'
        if 'coll' in dargs.keys():
            coll_name = dargs_coll
            
        conn = RSSMonConn(db_name, coll_name)
    return conn


class MySQLConn:
    """
    General handle for making a connection to a local MySQL database
    from within python; utilizes MySQLdb package;
    """
    def __init__(self, args=None, **dargs):
        args = args if args else dargs
        try:
            conn = ms.connect(db        = db,
                              host      = h,
                              user      = u,
                              passwd    = p)
            print "Connected"
        except ms.Error, e:
            print 'Connection failed'
            print 'Error code: ', e.args[0]
            print 'Error message: ', e.args[1]
            sys.exit(1)
        else:
            self.conn = conn
            self.cursor = self.conn.cursor()

    def respawn(self):
        self.cursor.close()
        self.cursor = self.conn.cursor()

class NBASQLConn(MySQLConn):
    """
    MySQL connection specific to NBA data
    """
    def __init__(self, **dargs):
        MySQLConn.__init__(self, args=dargs)

    def addInfo(self, pageType ,data):
        '''
        Handles the general call to the fucntions for updating the
        MySQL database with new information;
        '''
        if pageType=='pbp':

        elif pageType=='box':
            updateBox(cursor, data)

        elif pageType=='ext':

        else:
            print "Warning! non valid page type; not updating"


    def updateGameInfo(self, data):
        '''
        Update general game info, e.g., MDB id's for game data;
        Data should be from box['playerlinks']; dictionary-ize it;
        Layout for players_site table:
        +---------------+------------------+------+-----+---------+----------------+
        | Field         | Type             | Null | Key | Default | Extra          |
        +---------------+------------------+------+-----+---------+----------------+
        | game_id       | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
        | espn_gid      | int(10) unsigned | NO   |     | NULL    |                |
        | game_date     | date             | NO   |     | NULL    |
        | pbp_mdb_id    | varchar(24)      | NO   |     | NULL    |                |
        | box_mdb_id    | varchar(24)      | NO   |     | NULL    |                |
        | ext_mdb_id    | varchar(24)      | NO   |     | NULL    |                |
        | season        | varchar(7)       | NO   |     | NULL    |                |
        +---------------+------------------+------+-----+---------+----------------+

        '''
        data_list = [(int(ga['id']),
                      ga['date'],
                      ga['pbp_id'],
                      ga['box_id'],
                      ga['ext_id'],
                      ga['season']) for ga in data]
        self.cursor.executemany(
            """INSERT INTO game_mdb_ref (espn_gid,
                                         game_date,
                                         pbp_mdb_id,
                                         box_mdb_id,
                                         ext_mdb_id,
                                         season)
                VALUES(%s, %s, %s, %s, $s, $s)""", data_list) 


    def addPlayers2PS(self, data):
        '''
        Handles connection to db with general player info (ESPN ID,
        Web Page, etc.;
        Data should be from box['playerlinks']; dictionary-ize it;
        Layout for players_site table:
        +---------------+------------------+------+-----+---------+----------------+
        | Field         | Type             | Null | Key | Default | Extra          |
        +---------------+------------------+------+-----+---------+----------------+
        | player_id     | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
        | espn_id       | int(10) unsigned | NO   |     | NULL    |                |
        | last_name     | varchar(30)      | NO   |     | NULL    |                |
        | first_name    | varchar(30)      | NO   |     | NULL    |                |
        | pbp_name      | varchar(50)      | NO   |     | NULL    |                |
        | espn_web_page | varchar(150)     | NO   |     | NULL    |                |
        +---------------+------------------+------+-----+---------+----------------+

        Don't need to input player_id, automatically done
        '''
        data_list = [(int(pl['id']),
                     pl['last'],
                     pl['first'],
                     pl['pbp_name'],
                     pl['web_page']) for pl in data]

        self.cursor.executemany(
                """INSERT INTO players_site (espn_id,
                                             last_name,
                                             first_name,
                                             pbp_name,
                                             espn_web_page)
                   VALUES(%s, %s, %s, %s, %s)""", data_list)

    def addPlayer2PS(self, pl):
        pl = (int(pl['id']),
                   pl['last'],
                   pl['first'],
                   pl['pbp_name'],
                   pl['web_page'])
        self.cursor.execute(
                """INSERT INTO players_site (espn_id,
                                             last_name,
                                             first_name,
                                             pbp_name,
                                             espn_web_page)
                   VALUES(%s, %s, %s, %s, %s)""", pl)

class RSSSQLConn(MySQLConn):
    def __init__(self, **dargs):
        MySQLConn.__init__(self, args=dargs)

class MongoConn:
    """
    General handle for making a connection to a local Mongo database
    from within python; utilizes pymongo package;
    """
    def __init__(self, args=None, **dargs):
        conn = pymongo.Connection()
        if db_name in conn.database_names:
            conn = conn[db_name]
            if coll_name in conn.collection_names():
                self.conn = conn
            elif not coll_nam
                self.conn = conn
    ##        else:
    ##    else:


    def MongoInsert(self, data):
        self.__store['lastIDs'], self.__store['lastErr']\
                                 = self.RecursInsert(self, data)

    def RecursInsert(self, data):
        ids = list()
        ers = list()
        N = len(health_list)
        db_index = math.floor(N/2.0)
        try:
            ids1 = self.conn.insert(data[:db_index])
            ids2 = self.conn.insert(data[db_index:])
            err = []
        except:
            err = sys.exc_info()
            if type(err[1]) in [pymongo.errors.AutoReconnect,
                                bson.errors.InvalidDocument]:
                ids1, err_lst1 = self.recInsert(self, data[:db_index])
                ids2, err_lst2 = self.recInsert(self, data[db_index:])
                err = [err, [err_lst1+err_list2]]
            else:
                ids1 = ids2 = []
                err = [err, 'Fatal']
        ids.append(ids1 + ids2)
        ers.append(err)
        return ids, ers
    
##for p in posts:
##    p['date'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", p['date'])
##    db.Wired.insert(p)

class NBAMonConn(MongoConn):
    def __init__(self, **dargs):
        MongoConn.__init__(self, args=dargs)

    def addInfo(self, pageType ,data):
        '''
        Handles the general call to the fucntions for updating the
        MySQL database with new information;
        '''
        if pageType=='pbp':

        elif pageType=='box':
            self.updateBox(self, data)

        elif pageType=='ext':

        else:
            print "Warning! non valid page type; not updating"

class RSSMonConn(MongoConn):
    def __init__(self, **dargs):
        MongoConn.__init__(self, args=dargs)
        

if __name__=='__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "d:h:p:u",
                                   ["db=", "host=", "password=", "user="])
    except getopt.error as e:
        # for errors, print out info
        print "%s: %s" % (sys.argv[0], e)
        sys.exit(1)
    # defualt conn parameter vals
    database    = 'cookbook'
    host_name   = 'localhost'
    password    = ''
    user_name   = ''
    # iterate over options
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            host_name = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-u", "--user"):
            user_name = arg
        elif opt in ("-d", "--database"):
            database = arg
    # attempt to connect with handcon:
    conn = handcon(database, host_name, password, user_name)
