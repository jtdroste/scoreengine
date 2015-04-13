import thread
import mysql.connector
import time

"""
Database connection object

- Shared between each thread
"""
class Database(object):    
    def __init__(self, config):
        self.config = config
        self.lock = thread.allocate_lock()
        
        self.connect()
    
    def connect(self):
        self.conn = mysql.connector.connect(**self.config)
    
    def addScore(self, team, service, status, output):
        query = "INSERT INTO checks(team_id, service_id, time, status, output)" \
                "VALUES (%s, %s, %s, %s, %s)"
        args = (team, service, int(time.time()), status, output)
        
        self.lock.acquire()
        
        cursor = self.conn.cursor()
        cursor.execute(query, args)
        self.conn.commit()
        
        cursor.close()
        
        self.lock.release()
    
    def getTeams(self):
        result = []
        
        self.lock.acquire()
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM teams WHERE active = 1")
        
        row = cursor.fetchone()
        
        while row is not None:
            team_id = row[0]
            team_name = row[1]
            
            result.append({
                'id': team_id,
                'name': team_name,
            })
            
            row = cursor.fetchone()
        
        cursor.close()
        
        self.lock.release()
        
        return result
    
    def getTeamServices(self, team_id):
        result = []
        
        self.lock.acquire()
        
        conn = self.conn
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        
        cursor1.execute("SELECT * FROM services WHERE enabled = 1")
        row = cursor1.fetchone()
        
        while row is not None:
            service_id = row[0]
            service_name = row[1]
            module = row[2]
            
            cursor2.execute("SELECT `value` FROM services_data WHERE team_id = %s AND service_id = %s ORDER BY `order` ASC", (team_id, service_id))
            
            args = []
            data = cursor2.fetchone()
            
            while data is not None:
                args.append(data[0])
                
                data = cursor2.fetchone()
            
            result.append({
                'id': service_id,
                'name': service_name,
                'module': module,
                'args': args
            })
            
            row = cursor1.fetchone()
        
        cursor1.close()
        cursor2.close()
        
        self.lock.release()
        
        return result