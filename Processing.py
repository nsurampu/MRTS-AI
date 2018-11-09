import json
from pprint import pprint
import numpy
import math
import pickle
from operator import itemgetter

inf = 999

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

# def DFS_parent(adjacency_matrix,k,depth,start,end):
#     top_k_list = []
#     DFS(adjacency_matrix,k,depth,top_k_list,track)
#     return top_k_list
#
# def DFS(adjacency_matrix,k,depth,top_k_list,start,end):
#     if(start == end and depth >= 0):

def shortest_path():
    station_codes = station_dict.keys()
    station_codes.sort()
    for k in station_codes:
        for i in station_codes:
            for j in station_codes:
                # print(i,j,k)
                if ( adjacency_matrix[(i,k)] + adjacency_matrix[(k,j)] < adjacency_matrix[(i,j)]):
                    adjacency_matrix[(i,j)] = adjacency_matrix[(i,k)] + adjacency_matrix[(k,j)]

def reroute( ts_matrix,adjacency_matrix,track,time ):
    #track is defined as (source,dest)
    reroute_needed = []
    for entity in ts_matrix:
        if (entity[1][0] == track[0] and entity[2][0] == track[1] and (entity[3])[0] >= time):
            reroute_needed.append(entity)
    reroute_needed.sort()
    # print(reroute_needed)
    reroute_needed.sort(key=lambda x: x[3][0])
    # print(reroute_needed)
    #REDEFINE K IF NECESSARY
    k = 1
    num_of_routes = k * len(reroute_needed)
    fresh_matrix = adjacency_matrix.copy()
    fresh_matrix[track] = inf;





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

reroute(ts_matrix,adjacency_matrix,('103','104'),200)

station_dict_file.close()
adjacency_file.close()
ts_file.close()
