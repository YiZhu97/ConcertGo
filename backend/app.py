from flask import Flask, request, jsonify
from config import db_connect
from db import EventDataBase
from flask_cors import CORS
from process_parking import  ZYSB
app = Flask(__name__)
CORS(app)

@app.route('/venues',methods = ['GET'])
def get_unique_venues():
    db = EventDataBase(db_connect)

    venues = db.get_all_venues()
    venue_list = []
    for idx,venue in venues.iterrows():
        temp = {}
        temp['long']=venue[3]
        temp['lat'] = venue[2]
        temp['name'] = venue[1]
        venue_list.append(temp)
    return jsonify(venue_list)

@app.route('/suggestion/parking' ,methods = ['GET'])
def get_parking_suggestion():
    db = ZYSB()
    event = {}
    event["time"] = request.args.get("time")
    event['lat'] = request.args.get("lat")
    event['event_name'] = request.args.get("name")
    event['long'] = request.args.get("long")
    event['venue'] = request.args.get("venue")
    event['city'] = request.args.get("city")
    return jsonify(db.main(event))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
