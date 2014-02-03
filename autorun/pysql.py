# -*- encoding:utf8 -*-
import MySQLdb
 
class pysql:
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db     
        self.conn = self.getConnection()
 
    def getConnection(self):
        return MySQLdb.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')
 
    def query(self, sql):
        cursor=self.conn.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        return result
     
    def update(self, sql):
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.close()

#if __name__=="__main__":
#    db=pysql('10.136.18.76',3306,'result','hello','cmdresult')
#    allrow=db.query("select * from cmdresult")
#    for row in allrow:    
#        for r in row:    
#            print r  
