from backend import config
import requests, json
import math
from backend.db import EventDataBase

recommended_time = {'Lot 4 South': 30.93548387096774, 'Library': 30.0, 'Structure 5': 31.134969325153374,
                            'Structure 2': 34.455128205128204, 'Civic Center': 30.0, 'Pier Deck': 56.333333333333336,
                            'Structure 9': 31.161290322580644, 'Structure 3': 78.60759493670886,
                            'Structure 7': 59.31137724550898, 'Beach House Lot': 30.0, 'Structure 4': 39.61538461538461,
                            'Structure 8': 52.125748502994014, 'Lot 1 North': 59.666666666666664, 'Lot 8 North': 34.375,
                            'Structure 1': 57.17948717948718, 'Structure 6': 34.75155279503105,
                            'Lot 3 North': 50.50925925925926, 'Lot 5 South': 33.38383838383838}


if __name__ == "__main__":
    newdict=[]
    for k,v in recommended_time.items():
        temp = {}
        temp['name']=k
        temp['recommendation']=v
        newdict.append(temp)
    DB = EventDataBase(config.db_connect)
    for i in newdict:
        DB.insert_recommendation(i)

