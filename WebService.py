#!/usr/bin/env python
import web
import json

with open('Data/flight_data.json') as json_file:
            json_data = json.load(json_file)

urls = (
    '/flightdata','data'
)

app = web.application(urls, globals())

class data:
    def GET(self):
        return json_data


if __name__ == "__main__":
    app.run()
