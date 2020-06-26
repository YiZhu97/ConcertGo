


import datetime
from config import db_connect
import urllib.request, json
import tqdm
import geopy.distance

from db import EventDataBase

url_template = 'https://data.smgov.net/resource/ng8m-khuz.json?date_time='

'''
# to get all nearby parking lots information for the two hours before concert
def twoHours(event):
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
    # return url_list

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
'''

class ZYSB:
    def main(self, event):

        db = EventDataBase(db_connect)
        print(event)
        df = db.get_all_recommend()
        recommended_time = df.set_index('name').T.to_dict('r_time')[0]
        '''
        recommended_time = {'Lot 4 South': 30.93548387096774, 'Library': 30.0, 'Structure 5': 31.134969325153374,
                            'Structure 2': 34.455128205128204, 'Civic Center': 30.0, 'Pier Deck': 56.333333333333336,
                            'Structure 9': 31.161290322580644, 'Structure 3': 78.60759493670886,
                            'Structure 7': 59.31137724550898, 'Beach House Lot': 30.0, 'Structure 4': 39.61538461538461,
                            'Structure 8': 52.125748502994014, 'Lot 1 North': 59.666666666666664, 'Lot 8 North': 34.375,
                            'Structure 1': 57.17948717948718, 'Structure 6': 34.75155279503105,
                            'Lot 3 North': 50.50925925925926, 'Lot 5 South': 33.38383838383838}
        recommended_time = {k: "%0.2f" % v for k, v in recommended_time.items()}
        '''
        # event_id = event['eventid']
        # event_name = event['eventname']
        event_venue = event['venue']
        # event_city = event['city']
        # event_time = event ['time']

        print('DDDDDDDDDDDDDDDDD')
        venue_coord = db.get_venue_by_name(event_venue)

        # venue_coord = list(venue_coord.iterrows())[0][1]
        print(venue_coord)
        venue_coord = (float(venue_coord[0]), float(venue_coord[1]))

        print('EEEEEEEEEEEEEEEEEE')
        random_url = "https://data.smgov.net/resource/ng8m-khuz.json?date_time=2015-11-15T11:25:00.000"
        parking_lot_data = urllib.request.urlopen(random_url)
        data_json = json.load(parking_lot_data)
        alist = []
        preferred_distance = 1
        for j in data_json:
            parking_coord = (j['latitude'], j['longitude'])
            dist = geopy.distance.geodesic(parking_coord, venue_coord).km
            if dist < preferred_distance:
                alist.append((j['lot_name'],j['latitude'],j['longitude']))

        emp_list = []
        print('FFFFFFFFFFFFFF')
        for name,lat,long in alist:  # the list of all parking lots that satisfy the distance
            temp = dict()
            temp["name"] = name
            temp["long"] = long
            temp["lat"] = lat
            temp["recommend"] = recommended_time[name]
            emp_list.append(temp)

        return emp_list

    # returns a dictionary that stores the recommended time for each parking lot


if __name__ == "__main__":
    event = {"venue": "TRiP"}
    db = ZYSB()
    print(db.main(event))
