import urllib
testfile = urllib.URLopener()
testfile.retrieve("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt", "Data/aurora-nowcast-map.txt")