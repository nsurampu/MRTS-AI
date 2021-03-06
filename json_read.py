import json
from pprint import pprint
import numpy
import math
import pickle

INFINITY = 999
UNDEFINED = None

def in_day_time(str_time):
    str_val = str_time.split(':')
    hours = int(str_val[0])
    min = int(str_val[1])
    return hours*60+min

trains_json = open('admin_trains.json', 'r')
stations_json = open('admin_stations.json', 'r')
trains_data = json.load(trains_json)
stations_data = json.load(stations_json)



trains = list(trains_data.keys())
stations = list(stations_data.keys())
n = len(trains)
# ts_matrix = numpy.zeros((n, n, n))
ts_matrix = []
adjacency_matrix = {}
# train_count = 0
speed_matrix = {}
# station_count = 0

for train in trains:
    if train != 'sample_train':
        t_code = trains_data[train]['id']
        t_path = trains_data[train]['path']
        speed = int(trains_data[train]['speed'])
        speed_matrix[t_code] = speed
        s_time = trains_data[train]['start_time']
        s_time_h = int(s_time.split(':')[0])
        s_time_m = int(s_time.split(':')[1])
        s_station = trains_data[train]['starting_station']
        s_code  = stations_data[s_station]['station_code']
        # d_station = trains_data[train]['destination_station']
        for station in  t_path:
            station_key = list(station.keys())[0]
            s = station[station_key]
            if  s != s_station:
                s_pos = list(station.keys())
                next_station = station[s_pos[0]]
                n_code = stations_data[next_station]['station_code']
                distances = stations_data[s_station]['distances']
                # TODO: if there is no path then set time to 0 **Naren
                for d in distances:
                    if list(d.keys())[0] == n_code:
                        time = s_time
                        ts_matrix.append([[t_code], [s_code], [n_code], [time]])
                        s_code = n_code
                        distance = d[n_code]
                        time = distance / speed
                        time = round(time, 2)
                        h_time = math.floor(time % 60)
                        m_time = int(((time - h_time) * 60) + s_time_m)
                        h_time = h_time + s_time_h
                        s_time = str(h_time) + ":" + str(m_time)
                        s_time_h = h_time
                        s_time_m = m_time

#station_code:station_name
station_dict  = {}
station_codes = []

for station in stations:
    if station != 'sample_station':
        code = stations_data[station]['station_code']
        station_dict[code] = station
        station_codes.append(code)
        distances = stations_data[station]['distances']
        adjacency_matrix[code] = {}
        for distance in distances:
            distance_key = list(distance.keys())[0]
            distance = int(distance[distance_key])
            adjacency_matrix[code][distance_key] = distance
            '''if distance == 0:
                adjacency_matrix[(code, distance_key] = distance
            else:
                adjacency_matrix[(code, distance_key)] = distance'''
station_codes.sort()
# print(adjacency_matrix)

# shortest_matrix_dist = adjacency_matrix.copy()
#
# for k in station_codes:
#     for i in station_codes:
#         for j in station_codes:
#             # print(i,j,k)
#             if ( adjacency_matrix[(i,k)] + adjacency_matrix[(k,j)] < adjacency_matrix[(i,j)]):
#                 adjacency_matrix[(i,j)] = adjacency_matrix[(i,k)] + adjacency_matrix[(k,j)]

'''for entity in ts_matrix:
    str_time_list = entity[3]
    entity[3] = [in_day_time(str_time_list[0])]'''


pprint(ts_matrix)
'''print("")
print(adjacency_matrix)
print("")
print(station_dict)
print(speed_matrix)

for some in ts_matrix:
    print(some)

print(adjacency_matrix)

print(len(ts_matrix))'''

# print(adjacency_matrix[('101','105')])

adjacency_file = open("adjacency_matrix.save",'wb')
pickle.dump(adjacency_matrix,adjacency_file)
adjacency_file.close()

speed_file = open("speed_matrix.save",'wb')
pickle.dump(speed_matrix,speed_file)
speed_file.close()

ts_file = open("ts_matrix.save",'wb')
pickle.dump(ts_matrix,ts_file)
ts_file.close()

station_dict_file = open("station_dict.save",'wb')
pickle.dump(station_dict,station_dict_file)
station_dict_file.close()

trains_json.close()
stations_json.close()
