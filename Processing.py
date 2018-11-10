import json
from pprint import pprint
import numpy
import math
import pickle
from operator import itemgetter
import random
from prioritydictionary import priorityDictionary

INFINITY = 999
UNDEFINED = None
condition = 100
condition_dict = {0: "broken", 10: "extremely bad", 20: "very bad", 30: "bad", 40: "maintainence required soon",
                  50: "average", 60: "average", 70: "above average", 80: "good", 90: "very good", 100: "excellent"}


def in_day_time(str_time):
    str_val = str_time.split(':')
    hours = int(str_val[0])
    min = int(str_val[1])
    return hours * 60 + min


def convert_tsm(ts_matrix):
    for entity in ts_matrix:
        str_time_list = entity[3]
        entity[3] = [in_day_time(str_time_list[0])]
    return ts_matrix


def is_train(ts_matrix, track, time):
    for entity in ts_matrix:
        if(entity[1] == track[0] and entity[2] == track[1] and (entity[3])[0] >= time):
            return entity[0][0]
    return -1


def hx(source_station, destination_station, adjacency_matrix, ts_matrix):
    # TODO: define the funtion **Naren
    h_val = adjacency_matrix[(source_station, destination_station)]
    return h_val

# No callin yet
def rand_breakdown():
    # TODO: define, using randomizer
    h_break = random.choice(
        [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    h_break_val = numpy.random.choice(
        [0, 1], p=[1 - h_break, h_break])   # 1 for breakdown of track
    return h_break_val


def track_condition():
    h_condition = random.choice(
        [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    condition = condition - (1 * h_condition)
    condition = condition - (condition % 10)
    t_condition = condition_dict[condition]
    return t_condition


def add_node(graph, node):
    if node in graph:
        return False

    graph[node] = {}
    return True


def add_edge(graph, node_from, node_to, dist):
    add_node(graph, node_from)
    add_node(graph, node_to)

    graph[node_from][node_to] = dist
    return

# Returns dist of edge, else if edge is inf or failure returns -1


def remove_edge(graph, node_from, node_to, dist=UNDEFINED):
    if node_from not in graph:
        return -1

    if node_to in graph[node_from]:
        if not dist:
            dist = graph[node_from][node_to]

            if dist == INFINITY:
                return -1
            else:
                graph[node_from][node_to] = INFINITY
                return dist
        elif graph[node_from][node_to] == dist:
            graph[node_from][node_to] = INFINITY

            return dist
        else:
            return -1
    else:
        return -1


def path_sort(A):
    # TODO: SORT THE PATH ACCORDING TO WHICH PATH HAS HIGHEST VALUE OF H(X) **Naren
    return

def path(previous, node_start, node_end):
    route = []

    node_curr = node_end
    while True:
        route.append(node_curr)
        if previous[node_curr] == node_start:
            route.append(node_start)
            break
        elif previous[node_curr] == UNDEFINED:
            return []

        node_curr = previous[node_curr]

    route.reverse()
    return route

# def shortest_path():
#     station_codes = station_dict.keys()
#     station_codes.sort()
#     for k in station_codes:
#         for i in station_codes:
#             for j in station_codes:
#                 # print(i,j,k)
#                 if ( adjacency_matrix[(i,k)] + adjacency_matrix[(k,j)] < adjacency_matrix[(i,j)]):
#                     adjacency_matrix[(i,j)] = adjacency_matrix[(i,k)] + adjacency_matrix[(k,j)]


def shortest_path(graph, node_start, node_end=UNDEFINED):
    INFINITY = 999
    UNDEFINED = None
    distances = {}
    previous = {}
    Q = priorityDictionary()
    # Q = {}
    # print(type(INFINITY))
    for v in graph:
        distances[v] = INFINITY
        previous[v] = UNDEFINED
        Q[v] = INFINITY

    distances[node_start] = 0
    Q[node_start] = 0

    for v in Q:
        if v == node_end:
            break

        for u in graph[v]:
            dist_vu = distances[v] + graph[v][u]

            if dist_vu < distances[u]:
                distances[u] = dist_vu
                Q[u] = dist_vu
                previous[u] = v

    if node_end:
        return {'dist': distances[node_end],
                'path': path(previous, node_start, node_end)}
    else:
        return (distances, previous)


def k_shortest_path(graph, node_start, node_end, max_k=2):
    distances, previous = shortest_path(graph, node_start)
    # print(distances)
    # print(previous)

    A = [{'dist': distances[node_end],
          'path': path(previous, node_start, node_end)}]
    B = []

    if not A[0]['path']:
        return A

    for k in range(1, max_k):
        for i in range(0, len(A[-1]['path']) - 1):
            node_spur = A[-1]['path'][i]
            path_root = A[-1]['path'][:i + 1]
            edges_removed = []
            for path_k in A:
                curr_path = path_k['path']
                if len(curr_path) > i and path_root == curr_path[:i + 1]:
                    dist = remove_edge(graph, curr_path[i], curr_path[i + 1])
                    if dist == -1:
                        continue
                    edges_removed.append(
                        [curr_path[i], curr_path[i + 1], dist])
            path_spur = shortest_path(graph, node_spur, node_end)

            if path_spur['path']:
                path_total = path_root[:-1] + path_spur['path']
                dist_total = distances[node_spur] + path_spur['dist']
                potential_k = {'dist': dist_total, 'path': path_total}

                if not (potential_k in B):
                    B.append(potential_k)

            for edge in edges_removed:
                add_edge(graph, edge[0], edge[1], edge[2])

        if len(B):
            B = sorted(B, key=itemgetter('dist'))
            A.append(B[0])
            B.pop(0)
        else:
            break

    return A


def reroute(ts_matrix, adjacency_matrix, track, time):
    # track is defined as (source,dest)
    reroute_needed = []
    for entity in ts_matrix:
        if (entity[1][0] == track[0] and entity[2][0] == track[1] and (entity[3])[0] >= time):
            reroute_needed.append(entity)
    reroute_needed.sort()
    # print(reroute_needed)
    reroute_needed.sort(key=lambda x: x[3][0])
    print("Reroutes needed:",reroute_needed,"\n")
    # REDEFINE K IF NECESSARY
    k = 3
    num_of_routes = k * len(reroute_needed)
    fresh_matrix = adjacency_matrix.copy()
    fresh_matrix[track] = INFINITY
    A = k_shortest_path(adjacency_matrix, track[0], track[1],num_of_routes)
    A = A[1:]
    print("Values of A:  \n",A,"\n")
    path_sort(A)



def update():
    adjacency_file = open("adjacency_matrix.save", 'rb')
    adjacency_matrix = pickle.load(adjacency_file)

    ts_file = open("ts_matrix.save", 'rb')
    ts_matrix = pickle.load(ts_file)

    station_dict_file = open("station_dict.save", 'rb')
    station_dict = pickle.load(station_dict_file)

    # changes teh time format
    ts_matrix = convert_tsm(ts_matrix)
    # TODO: CHANGE
    reroute(ts_matrix, adjacency_matrix, ('103', '104'), 200)

    station_dict_file.close()
    adjacency_file.close()
    ts_file.close()
    return


# FOR TESTING ONLY REMOVE AFTER DONE

update()
