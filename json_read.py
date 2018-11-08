import json
from pprint import pprint
import numpy

trains_json = open('trains.json')
stations_json = open('stations.json')
trains_data = json.load(trains_json)
stations_data = json.load(stations_json)

trains = list(train_data.keys())
stations = list(stations_data.keys())
n = len(trains)
# ts_matrix = numpy.zeros((n, n, n))
ts_matrix = []
# train_count = 0
# station_count = 0

for train in trains:
    t_code = trains_dict[train]['id']
    speed = int(trains_data[train]['speed'])
    s_time = int(trains_data[train]['start_time'])
    s_station = trains_data[train]['starting_station']
    s_code = int(stations_data[s_station]['station_code'])
    for station in stations:
        code = int(stations_data[station]['station_code'])
        distance = stations_dict[s_station][code]
        time = distance / speed
        arrival_time = s_time + time
        ts_matrix.append([t_code, code, arrival_time])
