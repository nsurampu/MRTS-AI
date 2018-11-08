import json
from pprint import pprint
import numpy

trains_json = open('trains.json')
stations_json = open('stations.json')
trains_data = json.load(trains_json)
stations_data = json.load(stations_json)

trains = list(trains_data.keys())
stations = list(stations_data.keys())
n = len(trains)
# ts_matrix = numpy.zeros((n, n, n))
ts_matrix = []
# train_count = 0
# station_count = 0

for train in trains:
    if train != "sample_train":
        t_code = trains_data[train]['id']
        speed = int(trains_data[train]['speed'])
        s_time = trains_data[train]['start_time']
        s_station = trains_data[train]['starting_station']
        s_code = stations_data[s_station]['station_code']
        for station_count in range(0, len(stations) - 1):
            distance_dict = stations_data[s_station]['distances'][station_count]
            distance_key = list(distance_dict.keys())[0]
            distance = int(distance_dict[distance_key])
            time = distance / speed
            ts_matrix.append([[t_code], [distance_key], [time]])

print(ts_matrix)
