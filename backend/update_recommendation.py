import mysql.connector
import datetime
from backend import config
import urllib.request, json
import tqdm
import geopy.distance

from backend.db import EventDataBase

url_template = 'https://data.smgov.net/resource/ng8m-khuz.json?date_time='


# to get all nearby parking lots information for the two hours before concert

def UrlList(event):
    url_template = 'https://data.smgov.net/resource/ng8m-khuz.json?date_time='
    a = event[2]
    venue_coord = (event[4], event[3])  # latitude, longitude
    preferred_distance = 2  # setting a desired distance (2kms)

    year = str(a.year)
    if a.month >= 10:
        month = str(a.month)
    else:
        month = '0' + str(a.month)

    if a.day >= 10:
        day = str(a.day)
    else:
        day = '0' + str(a.day)

    if a.time().hour >= 10:
        hour = str(a.time().hour)
    else:
        hour = '0' + str(a.time().hour)
    if a.time().minute >= 10:
        minute = str(a.time().minute)
    else:
        minute = '0' + str(a.time().minute)
    if a.time().hour - 2 >= 10:
        hour_start = str(a.time().hour - 2)
    else:
        hour_start = '0' + str(a.time().hour - 2)

    url_end = url_template + year + '-' + month + '-' + day + 'T' + hour + ':' + minute + ':00.000'
    url_start = url_template + year + '-' + month + '-' + day + 'T' + hour_start + ':' + minute + ':00.000'
    url_list = []

    for i in range(24):
        if int(minute) + 5 * i < 60:
            if int(minute) + 5 * i >= 10:
                new_minute = str(int(minute) + 5 * i)
            else:
                new_minute = '0' + str(int(minute) + 5 * i)
            new_hour = hour_start
        else:
            hour_increase = (int(minute) + 5 * i) // 60
            if int(hour_start) + hour_increase >= 10:
                new_hour = str(int(hour_start) + hour_increase)
            else:
                new_hour = '0' + str(int(hour_start) + hour_increase)
            if (int(minute) + 5 * i) % 60 >= 10:
                new_minute = str((int(minute) + 5 * i) % 60)
            else:
                new_minute = '0' + str((int(minute) + 5 * i) % 60)
        url = url_template + year + '-' + month + '-' + day + 'T' + new_hour + ':' + new_minute + ':00.000'
        url_list.append(url)
        # a list of 24 time slots
    return url_list


def two_hours(url_list):
    preferred_distance = 2
    parking_info = []
    for i in url_list:
        data = urllib.request.urlopen(i)
        data_json = json.load(data)
        slot = []
        for j in data_json:
            parking_coord = (j['latitude'], j['longitude'])
            dist = geopy.distance.geodesic(parking_coord, venue_coord).km
            if dist < preferred_distance:
                slot.append(j)
        parking_info.append(slot)
    return parking_info

    # returns a list of 24 elements, each representing a five-minute time slot
    # the 24 elements are lists of same the length, containing the parking lot data that satisfy the distance constraint


def parkSpaces(info_list):
    spaces = []
    lot_names = []
    for i in range(len(info_list[0])):
        lot_names.append(info_list[0][i]['lot_name'])

    for name in lot_names:
        x = []
        for i in range(24):
            for j in range(len(info_list[0])):
                if info_list[i][j]['lot_name'] == name:
                    x.append(int(info_list[i][j]['available_spaces']))
        spaces.append({name: x})
    return spaces
    # return a list of n elements, where n = # of parking lots that are contained in the inputted list
    # each element is a dictionary, with key being the parking lot name,
    # value being a list of # of available spaces of that lot across 2 hours time period


max_space = {'Beach House Lot': 270, 'Civic Center': 705, 'Structure 1': 379, 'Structure 2': 649, 'Structure 3': 344,
             'Structure 4': 659, 'Structure 5': 675,
             'Structure 6': 747, 'Structure 7': 811, 'Structure 8': 1002, 'Structure 9': 294, 'Lot 1 North': 1266,
             'Lot 3 North': 466,
             'Lot 4 South': 1050, 'Lot 5 South': 787, 'Lot 8 North': 214, 'Pier Deck': 266, 'Library': 532}


# finding the preferable parking time

def BestTime(available_parkings):
    # input a dictionary
    a = list(available_parkings.keys())[0]
    b = available_parkings[a]
    index = 0
    if b[18] >= 0.3 * max_space[a]:
        index = 18
        # Parking suggestion: no need to arrive early
    else:
        i = 1
        while b[-(i + 6)] < 0.3 * max_space[a] and i < 18:
            index = -i + 18
            i += 1
        index = index - 1
    return index


def RecommendTime(index):
    rt = 0
    if index == 0:
        rt = 120
        print('The parking lot was busy two hours before the event, recommend going as early as possible')
    else:
        rt = (24 - index) * 5
        print('recommend arriving at %d minutes before the event to find a parking spot' % (rt))
    return rt




results are all events from sm_14
import datetime
for i in range(len(results)):
    if results[i][2].time()!=datetime.time(0,0):
        results_filtered.append(results[i])




'''        
all_recommends = {}
for i in tqdm(range(len(results_filtered))):
    a = results_filtered[i]
    b_1 = UrlList(a) # returns a list of urls for requesting parking data given a single event
    b = two_hours(b_1) # returns a list of 24 elements, supposedly of same length 
    
    if all(len(elem)==len(b[0]) for elem in b):
        c = parkSpaces(b) # transforms the list of 24 x n into a list of n dicitonaries  ( n different parking lots)
        
        for j in tqdm(range(len(c))):
            d = RecommendTime(BestTime(c[j]))
            if list(c[j].keys())[0] in all_recommends:
                all_recommends[list(c[j].keys())[0]].append(d)
            else:
                all_recommends[list(c[j].keys())[0]] = [d]
    else:
        continue

    
recommend_time={}
for name in list(all_recommends.keys()):
    value = all_recommends[name]
    length = len(value)
    init = 0
    for i in range(length):
        init+=value[i]
    average_time = init /length
    #print(name, average_time)
    recommend_time[name] = average_time
print(recommend_time,len(recommend_time))

'''

# input a whole list of santa monica events (sm14):
# 

if __name__ == "__main__":
    db = EventDataBase(config.db_connect)
    df = db.get_all_events_sm_14()
    
    results=[]
    results_filtered = []
    for i in range(len(df)):
        id_number = df['id'][i]
        name = df['name'][i]
        time = df['date'][i]
        long = df['long'][i]
        lat = df['lat'][i]
        city = df['city'][i]
        value = (id_number,name,time,long,lat,city)
        results.append(value)

    for i in range(len(results)):
    if results[i][2].time()!=datetime.time(0,0):
        results_filtered.append(results[i])

    all_recommends = {}
    for i in tqdm(range(len(results_filtered))):
        a = results_filtered[i]
        b_1 = UrlList(a) # returns a list of urls for requesting parking data given a single event
        b = two_hours(b_1) # returns a list of 24 elements, supposedly of same length 
        if all(len(elem)==len(b[0]) for elem in b):
            c = parkSpaces(b) # transforms the list of 24 x n into a list of n dicitonaries  ( n different parking lots)
            for j in tqdm(range(len(c))):
                d = RecommendTime(BestTime(c[j]))
                if list(c[j].keys())[0] in all_recommends:
                    all_recommends[list(c[j].keys())[0]].append(d)
                else:
                    all_recommends[list(c[j].keys())[0]] = [d]
        else:
            continue
    
    recommend_time={}
    for name in list(all_recommends.keys()):
        value = all_recommends[name]
        length = len(value)
        init = 0
        for i in range(length):
            init+=value[i]
        average_time = init /length
        #print(name, average_time)
        recommend_time[name] = average_time
    print(recommend_time,len(recommend_time))

