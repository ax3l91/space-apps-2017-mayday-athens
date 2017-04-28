#!/usr/bin/env python
import web
import json

with open('Data/flight_data.json') as json_file:
            json_data = json.load(json_file)

urls = (
    '/flightdata','data',
    '/input','pop'
)

app = web.application(urls, globals())

class data:
    def GET(self):
        output = 'var None = null; flightdata = '+str(json_data)
        return output

class pop:
    def GET(self):
        return null


if __name__ == "__main__":
    app.run()
