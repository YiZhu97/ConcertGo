


from backend import config
import requests, json
import datetime
import schedule
import time
import setproctitle
import math

from backend.db import EventDataBase

def main():
    DB = EventDataBase(config.db_connect)
    df = DB.get_all_events_future()
    min_date = df['date'].min()
    while min_date < datetime.date.today():
        min_id = df['id'][df['date'] == min_date].values[0]
        values = dict()
        values['id'] = min_id
        values['name'] = df['name'][df['id'] == min_id].values[0]
        values['long'] = df['long'][df['id'] == min_id].values[0]
        values['lat'] = df['lat'][df['id'] == min_id].values[0]
        values['city'] = df['city'][df['id'] == min_id].values[0]
        values['date'] = min_date.to_pydatetime()
        DB.insert(values)
        DB.delete_from_future(min_id)
        df = DB.get_all_events_future()
        min_date = df['date'].min()
    print ('Update has completed')

schedule.every().day.at("17:00").do(main)
setproctitle.setproctitle('Scheduler')

while 1:
    schedule.run_pending()
    time.sleep(1)

    
        


