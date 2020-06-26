import pandas as pd
import pymysql
from config import db_connect




class EventDataBase:
    def __init__(self, conf):
        self.conf = conf
        host = self.conf['host']
        port = self.conf['port']
        dbname = self.conf['dbname']
        user = self.conf['user']
        password = self.conf['password']
        self.conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname, connect_timeout=3)

    def insert(self, data):
        id = data['id']
        city = data['city']
        long = data['long']
        lat = data['lat']
        name = data['name']
        date = data['date']

        query = "insert ignore into `all_events_new` (`id`,`name`,`date`,`long`,`lat`,`city`) values (%d, '%s', '%s', %.3f, %.3f, '%s')" % (id, name, date, long, lat, city)
        with self.conn.cursor() as cursor:

            cursor.execute(query)
            self.conn.commit()

    def update_db(self,data_list):
        for i in data_list:
            self.insert(i)

    def insert_to_future(self,data):
        id = data['id']
        city = data['city']
        long = data['long']
        lat = data['lat']
        name = data['name']
        date = data['date']
        if "'" not in name and [id,city,long,lat,name,date].count(None)==0:
            query = "insert ignore into `future_events` (`id`,`name`,`date`,`long`,`lat`,`city`) values (%d, '%s', '%s', %.3f, %.3f, '%s')" % (id, name, date, long, lat, city)

            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()

    def insert_recommendation(self,data):
        name = data['name']
        r_time = data['recommendation']
        query = "insert ignore into `recommendation` (`name`,`r_time`) values ('%s', %.3f)" % (name, r_time)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()

    def update_recommendation(self,data):
        name = data['name']
        r_time = data['recommendation']
        query = "update `recommendation` set r_time=%.3f where name=%s"%(r_time,name)
        with self.conn.cursor() as cursor:

            cursor.execute(query)
            self.conn.commit()

    def get_all_recommend(self):
        df = pd.read_sql("select * from `recommendation`",con = self.conn)
        return df


    def delete_from_future(self,event_id):
        query = "delete from future_events where id=%d"%(event_id)
        with self.conn.cursor() as cursor:

            cursor.execute(query)
            self.conn.commit()



    def get(self):
        df = pd.read_sql("select * from event", con=self.conn)
        print(df)

    def get_copy(self,i):
        query ="select * from events_copy_%s"%(str(i))
        df = pd.read_sql(query, con=self.conn)
        return df

    def simulate(self,i):
        query = "select * from events_copy_%s" % (str(i))

    def get_all_venues(self):
        df = pd.read_sql("select * from `venue_sm`",con = self.conn)
        return df

    def deleteAll(self):
        query = "delete from `event`"
        with self.conn.cursor() as cursor:

            cursor.execute(query)
            self.conn.commit()
    def get_all_events_sm_14(self):
        df = pd.read_sql("select * from `santa_monica_14`", con = self.conn)
        return df

    def get_all_events_future(self):
        df = pd.read_sql("select * from `future_events`", con = self.conn)
        return df

    def get_venue_by_name(self,venue):
        query = "select `lat`,`long` from venue_sm where name = %s"
        with self.conn.cursor() as cursor:

            cursor.execute(query,[venue])
            row = cursor.fetchone()
        print(row)
        return row
if __name__ == "__main__":
    event_db = EventDataBase(db_connect)
    data = dict()
    # data['id'] = 2
    # data['city'] = 'bos'
    # data['long'] = -118.3275
    # data['lat'] = 41.5234
    # data['name'] = "ych"
    # data['date'] = '2020-05-31'
    # #print(type(data['id']))
    # event_db.insert(data)

    #event_db.deleteAll()
    #event_db.get()
    print(list(event_db.get_all_venues().iterrows())[0])
