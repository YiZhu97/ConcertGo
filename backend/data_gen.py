# class DatasetGenerator:
#     def __init__(self,url,apikey):
#         self.url = url
#         self.apikey =apikey
#         self.data = None
#     def get_data(self, ):
#
# class JsonParser:
#     def __init__(self):
#         pass
#     def parse(self):
#         pass
import math
import requests
from tqdm import tqdm
import concurrent.futures
from backend import config
from backend.db import EventDataBase
import datetime
with open("artist.txt", "r") as f:
    lines = f.readlines()
    lines = [int(line[:-1].split(' ', 1)[0]) for line in lines]
    #print(lines)
url_template = "https://api.songkick.com/api/3.0/artists/substitution/gigography.json?apikey=io09K9l3ebJxmxe2"
url_list = []
# for art_id in tqdm(lines):
#
#
#     url = url_template.replace('substitution', str(art_id))
#     res = requests.get(url)
#     data = res.json()
#
#     tot = data['resultsPage']['totalEntries']
#     perPage = data['resultsPage']["perPage"]
#     if tot == 0:
#         continue
#     total_page = math.ceil(tot / perPage)
#     url_list.append(url)
#
#     for j in range(2, total_page + 1):
#         new_url = url + "&page=%d" % (j)
#         url_list.append(new_url)
def parse(data):

    return values
def process(art_id):
    ret = []
    url = url_template.replace('substitution', str(art_id))
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



# print("writing file")
# outF = open("events.txt", "w")
# for v in res:
#   line = "%s\n" %v
#   outF.write(line)
# outF.close()
if __name__ == "__main__":

    res = []
    errors = []
    DB = EventDataBase(config.db_connect)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(process, art_id):art_id for art_id in lines[:]}

        for future in tqdm(concurrent.futures.as_completed(future_to_url)):
            try:
                for value in future.result():

                    date = value['date']
                    time = date.split('T')[0].split('-')
                    DB.insert(value)
            except Exception:
                errors.append(future_to_url[future])
    #a = [process(art_id) for art_id in lines[:5]]
