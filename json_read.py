import json
from pprint import pprint
import numpy
import math

trains_json = open('trains.json')
stations_json = open('stations.json')
trains_data = json.load(trains_json)
stations_data = json.load(stations_json)

trains = list(trains_data.keys())
stations = list(stations_data.keys())
n = len(trains)
# ts_matrix = numpy.zeros((n, n, n))
ts_matrix = []
adjacency_matrix = {}
# train_count = 0
# station_count = 0
'''
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
'''

for train in trains:
    if train != 'sample_train':
        t_code = trains_data[train]['id']
        t_path = trains_data[train]['path']
        speed = int(trains_data[train]['speed'])
        s_time = trains_data[train]['start_time']
        s_time_h = int(s_time.split(':')[0])
        s_time_m = int(s_time.split(':')[1])
        s_station = trains_data[train]['starting_station']
        # d_station = trains_data[train]['destination_station']
        for station in  t_path:
            station_key = list(station.keys())[0]
            s = station[station_key]
            if  s != s_station:
                s_pos = list(station.keys())
                next_station = station[s_pos[0]]
                n_code = stations_data[next_station]['station_code']
                distances = stations_data[s_station]['distances']
                for d in distances:
                    if list(d.keys())[0] == n_code:
                        time = s_time
                        ts_matrix.append([[t_code], [s_station], [next_station], [time]])   # change distance to time
                        s_station = next_station
                        distance = d[n_code]
                        time = distance / speed
                        h_time = math.floor(time)
                        m_time = int(((time - h_time) * 60) + s_time_m)
                        h_time = h_time + s_time_h
                        s_time = str(h_time) + ":" + str(m_time)
                        s_time_h = h_time
                        s_time_m = m_time

for station in stations:
    if station != 'sample_station':
        code = stations_data[station]['station_code']
        distances = stations_data[station]['distances']
        for distance in distances:
            distance_key = list(distance.keys())[0]
            distance = int(distance[distance_key])
            if distance == 0:
                adjacency_matrix[(code, distance_key)] = 0
            else:
                adjacency_matrix[(code, distance_key)] = 1

print(ts_matrix)
print("")
print(adjacency_matrix)
