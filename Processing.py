import json
from pprint import pprint
import numpy
import math
import pickle
from operator import itemgetter

def in_day_time(str_time):
    str_val = str_time.split(':')
    hours = int(str_val[0])
    min = int(str_val[1])
    return hours*60+min

def is_train(ts_matrix,track,time):
    for entity in ts_matrix:
        if(entity[1] == track[0] and entity[2] == track[1] and (entity[3])[0] >= time):
            return entity[0][0]
    return -r
def hx(source_station,destination_station,adjacency_matrix,ts_matrix):
    #TODO: define the funtion
    h_val = adjacency_matrix[(source_station,destination_station)]
    return h_val

def rand_breakdown():
    # TODO: define, using randomizer
    return

def reroute( ts_matrix,track,time ):
    #track is defined as (source,dest)
    reroute_needed = []
    for entity in ts_matrix:
        if (entity[1][0] == track[0] and entity[2][0] == track[1] and entity[3][0] >= time):
            reroute_needed.append(entity)
    reroute_needed.sort()
    print(reroute_needed)
    sorted(reroute_needed, key=itemgetter(3))
    print(reroute_needed)
    return




def update():
    adjacency_file = open("adjacency_matrix.save",'rb')
    adjacency_matrix = pickle.load(adjacency_file)

    ts_file = open("ts_matrix.save",'rb')
    ts_matrix = pickle.load(ts_file)

    station_dict_file = open("station_dict.save",'rb')
    station_dict = pickle.load(station_dict_file)

    #CORE

    station_dict_file.close()
    adjacency_file.close()
    ts_file.close()
    return


#FOR TESTING ONLY REMOVE AFTER DONE

adjacency_file = open("adjacency_matrix.save",'rb')
adjacency_matrix = pickle.load(adjacency_file)

ts_file = open("ts_matrix.save",'rb')
ts_matrix = pickle.load(ts_file)

station_dict_file = open("station_dict.save",'rb')
station_dict = pickle.load(station_dict_file)

reroute(ts_matrix,('103','104'),200)

station_dict_file.close()
adjacency_file.close()
ts_file.close()
