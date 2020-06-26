


from backend import config
import requests, json

import math


from backend.db import EventDataBase
url_template = 'https://api.songkick.com/api/3.0/events.json?apikey=io09K9l3ebJxmxe2&location=substitution'
def find_new(geo):
    #geo = geo:34,-118
    ret = []
    url = url_template.replace('substitution', geo)
    res = requests.get(url)
    data = res.json()

    tot = data['resultsPage']['totalEntries']
    perPage = data['resultsPage']["perPage"]
    if tot == 0:
        return []
    total_page = math.ceil(tot / perPage)
    
    for event in data['resultsPage']['results']['event']:
        idx = event['id']
        name = event['displayName']
        date = event['start']['date'] if not event['start']['datetime'] else event['start']['datetime']

        city = event['location']['city']
        long = event['location']['lng']
        lat = event['location']['lat']
        values = dict()
        values['id'] = idx
        values['name'] = name
        values['long'] = long
        values['lat'] = lat
        values['city'] = city
        values['date'] = date
        ret.append(values)
        #DB.insert(values)
        
    for j in range(2, total_page + 1):

        new_url = url + "&page=%d" % (j)
        #print(new_url)
        res = requests.get(new_url)
        data = res.json()
        for event in data['resultsPage']['results']['event']:
            idx = event['id']
            name = event['displayName']

            date = event['start']['date'] if not event['start']['datetime'] else event['start']['datetime']
            city = event['location']['city']
            long = event['location']['lng']
            lat = event['location']['lat']

            values = dict()
            values['id'] = idx
            values['name'] = name
            values['long'] = long
            values['lat'] = lat
            values['city'] = city
            values['date'] = date
            ret.append(values)

    return ret

if __name__ == "__main__": 
    DB = EventDataBase(config.db_connect)
    data = find_new('geo:34,-118')
    for i in data:
        DB.insert_to_future(i)

