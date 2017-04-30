#!/usr/bin/env python
import web
import json
import csv
import os


urls = (
    '/api/flightdata','getFlightData',
    '/api/getdata','getData',
    '/api/getinfodata','getInfoData'
)

app = web.application(urls, globals())

class getFlightData:
    def GET(self):
        #Run csvjson to convert from csv to json
        os.system("csvjson.py data planedata")
        with open('Data/planedata.json') as pldata_json:
            plane_data = json.load(pldata_json)
        output = 'respond = ' + str(plane_data)
        print("returned respond data")
        return output


class getData:
    def GET(self):
        #callMixalisApp();
        #open csv file
        #transform csv -> json
        with open('Data/flight_data.json') as respond_file:
            respond_data = json.load(respond_file)
        output = 'respond = ' + str(respond_data)
        print("returned respond data")
        return output

class getInfoData:
    def GET(self):
        #Run csvjson to convert from csv to json
        os.system("csvjson.py -i Data/data.csv -o Data/planedata.json -f pretty")
        with open('Data/planedata.json') as pldata_json:
            plane_data = json.load(pldata_json)
            pl2 = json.dumps(plane_data)
        output = 'planedata = ' + str(pl2)
        print("returned respond data")
        return output


if __name__ == "__main__":
    app.run()
