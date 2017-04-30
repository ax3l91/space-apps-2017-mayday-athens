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
        output = 'var None = null; flightdata = ' + str(json_data)
        return output


class getData:
    def GET(self):
        #callMixalisApp();
        #open csv file
        #transform csv -> json
        with open('Data/respond_data.json') as respond_file:
            respond_data = json.load(respond_file)
        output = 'respond = ' + str(respond_data)
        print("returned respond data")
        return output

class getInfoData:
    def GET(self):
        #open csv file
        #transform csv -> json
        os.system("csvjson.py")
        with open('Data/test.json') as test_json:
            test_data = json.load(test_json)
        output = 'respond = ' + str(test_data)
        print("returned respond data")
        return output


if __name__ == "__main__":
    app.run()
