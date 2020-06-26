
from backend import config
import requests

import math


from backend.db import EventDataBase

if __name__ == "__main__": 
    DB = EventDataBase(config.db_connect)
    df = DB.get_copy(1)
    for i in range(len(df)):
        a = df.id[i]
        df.id[i] = a+39615404
    print (df)
