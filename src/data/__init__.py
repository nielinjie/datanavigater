import sqlalchemy

class Data(object):
    connections=['test moke connection']
    def __init__(self):
        self.tables={}
        self.links={}
        pass
    def ls(self):
        pass
    def select(self,tables):
        pass
    def listLinks(self,tableName):
        return self.links.setdefault(tableName,[])
class DataDescripter(object):
    _descripters={}
    def getEngine(self):
        raise NotImplementedError
    @staticmethod
    def getDescripter(dailect):
        return DataDescripter._descripters[dailect]
class OracleDataDescripter(DataDescripter):
    def __init__(self,**kwd):
        self.host=kwd['host']
        self.port=kwd['port']
        self.sid=kwd['sid']
        self.userName=kwd['userName']
        self.passwd=kwd['passwd']
        pass
    def getEngine(self):
        pass
DataDescripter._descripters.update({'oracle':OracleDataDescripter})
class PostgresDataDescripter(DataDescripter):
    def __init__(self,**kwd):
        self.host=kwd['host']
        self.port=kwd['port']
        self.userName=kwd['userName']
        self.passwd=kwd['passwd']
        self.dbname=kwd['dbname']
    def getEngine(self):
        return sqlalchemy.create_engine('postgres://%s:%s@%s:%s/%s' % (self.userName,self.passwd,self.host,self.port,self.dbname))
DataDescripter._descripters.update({'postgres':PostgresDataDescripter})
class SqliteDataDescripter(DataDescripter):
    def __init__(self,**kwd):
        self.path=kwd['path']
    def getEngine(self):
        return sqlalchemy.create_engine('sqlite:///%s' % (self.path))
DataDescripter._descripters.update({'sqlite':SqliteDataDescripter})
