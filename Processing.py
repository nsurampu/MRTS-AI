import json
import pprint
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

track_conditions = {"100": {"101": 100, "102": 100, "103": 100, "104": 100, "105": 100},
"101": {"102": 100, "103": 100, "104": 100, "105": 100},
"102": {"103": 100, "104": 100, "105": 100},
"103": {"104": 100, "105": 100},
"104": {"105": 100}}

condition_dict = {0: "broken", 10: "extremely bad", 20: "very bad", 30: "bad", 40: "maintainence required soon",
                  50: "average", 60: "average", 70: "above average", 80: "good", 90: "very good", 100: "excellent"}

class processing_class:

    # TODO: Push messages to log

    def in_day_time(self, str_time):
        str_val = str_time.split(':')
        hours = int(str_val[0])
        min = int(str_val[1])
        return hours * 60 + min

    def from_day_time(self, time):
        hour = int(time/60)
        min = int(time%60)
        str_val = str(hour) + ":" + str(min).zfill(2)
        return str_val

    def convert_tsm(self, ts_matrix):
        for entity in ts_matrix:
            str_time_list = entity[3]
            entity[3] = [self.in_day_time(str_time_list[0])]
        return ts_matrix

    def unconvert_tsm(self, ts_matrix):
        for entity in ts_matrix:
            str_time_list = entity[3]
            entity[3] = [self.from_day_time(str_time_list[0])]
        return ts_matrix


    def is_train(self, ts_matrix, track, time):
        for entity in ts_matrix:
            if(entity[1] == track[0] and entity[2] == track[1] and (entity[3])[0] >= time):
                return entity[0][0]
        return -1


    def hx(self, source_station, destination_station, adjacency_matrix, ts_matrix):
        distance = adjacency_matrix[source_station][destination_station]
        return h_val

    def rand_breakdown(self):
        # TODO: define, using randomizer
        h_break = random.choice(
            [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        h_break_val = numpy.random.choice(
            [0, 1], p=[1 - h_break, h_break])   # 1 for breakdown of track
        return h_break_val


    def track_condition(self):
        for station_1 in track_conditions:
            track_key = list(station_1.keys())[0]
            track_list = track_conditions[track_key]
            for track in track_list:
                t_key = list(track.keys())[0]
                t_condition = track[t_key]
                h_condition = random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
                t_condition = t_condition - (1 * h_condition)
                track[t_key] = t_condition
                # t_condition = t_condition - (condition % 10)
                # t_condition = condition_dict[condition]


    def add_node(self, graph, node):
        if node in graph:
            return False

        graph[node] = {}
        return True


    def add_edge(self, graph, node_from, node_to, dist):
        self.add_node(graph, node_from)
        self.add_node(graph, node_to)

        graph[node_from][node_to] = dist
        return

    # Returns dist of edge, else if edge is inf or failure returns -1


    def remove_edge(self, graph, node_from, node_to, dist=UNDEFINED):
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


    def path_sort(self, A):
        # TODO: SORT THE PATH ACCORDING TO WHICH PATH HAS HIGHEST VALUE OF H(X) **Naren
        heuristic_dict = {}
        for route in A:
            heuristic = 0
            distance = route['dist']
            path = route['path']
            for i in range(0, len(path) - 1):
                if int(path[i]) > int(path[i+1]):
                    t_cond = track_conditions[path[i+1]][path[i]]
                else:
                    t_cond = track_conditions[path[i]][path[i+1]]
                heuristic = heuristic + 0.4 * (1 - (t_cond / 100))
            heuristic = heuristic + 0.6 * distance
            heuristic = round(heuristic, 4)
            heuristic_dict[heuristic] = path
        #heuristic_dict = [(p, heuristic_dict[p]) for p in sorted(heuristic_dict, key=heuristic_dict.get)]
        sorted_heuristic_dict = {p: heuristic_dict[p] for p in sorted(heuristic_dict, key=heuristic_dict.get)}
        return sorted_heuristic_dict

    def path(self, previous, node_start, node_end):
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


    def shortest_path(self, graph, node_start, node_end=UNDEFINED):
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
                    'path': self.path(previous, node_start, node_end)}
        else:
            return (distances, previous)


    def k_shortest_path(self, graph, node_start, node_end, max_k=2):
        distances, previous = self.shortest_path(graph, node_start)
        # print(distances)
        # print(previous)
        # A: Confirmed path_sort (Queue)
        #B: Posiible paths (Queue)
        A = [{'dist': distances[node_end],
              'path': self.path(previous, node_start, node_end)}]
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
                        dist = self.remove_edge(graph, curr_path[i], curr_path[i + 1])
                        if dist == -1:
                            continue
                        edges_removed.append(
                            [curr_path[i], curr_path[i + 1], dist])
                path_spur = self.shortest_path(graph, node_spur, node_end)

                if path_spur['path']:
                    path_total = path_root[:-1] + path_spur['path']
                    dist_total = distances[node_spur] + path_spur['dist']
                    potential_k = {'dist': dist_total, 'path': path_total}

                    if not (potential_k in B):
                        B.append(potential_k)

                for edge in edges_removed:
                    self.add_edge(graph, edge[0], edge[1], edge[2])

            if len(B):
                B = sorted(B, key=itemgetter('dist'))
                A.append(B[0])
                B.pop(0)
            else:
                break

        return A


    def reroute(self, ts_matrix, adjacency_matrix, track, time,speed_matrix):
        # track is defined as (source,dest)
        # print(len(ts_matrix))
        reroute_needed = []
        original = ts_matrix.copy()
        for entity in ts_matrix:
            if (entity[1][0] == track[0] and entity[2][0] == track[1] and (entity[3])[0] >= time):
                reroute_needed.append(entity)
        # reroute_needed.sort()
        # print(reroute_needed)
        reroute_needed.sort(key=lambda x: x[3][0])
        print("Reroutes needed:",reroute_needed,"\n")
        # REDEFINE K IF NECESSARY
        k = 3
        num_of_routes = k * len(reroute_needed)
        fresh_matrix = adjacency_matrix.copy()
        fresh_matrix[track] = INFINITY
        A = self.k_shortest_path(adjacency_matrix, track[0], track[1],num_of_routes)
        reroute = A[1:]
        print("Values of reroute:  \n",reroute,"\n")
        self.path_sort(reroute)
        final_route_list = []
        for train in reroute_needed:
            train_no = train[0][0]
            speed = speed_matrix[train_no]
            train_spec = []
            for entity in ts_matrix:
                if(train_no == entity[0][0]):
                    train_spec.append(entity)
            train_spec.sort(key=lambda x: x[3][0])
            print("Train spec   ",train_spec)
            train_spec_previous = []
            train_spec_next = []
            train_spec_reqd = []
            st = False
            for edge in train_spec:
                if(edge[1][0] == track[0] and edge[2][0] == track[1]):
                    st = True
                    train_spec_reqd.append(edge)
                    continue
                if st == True:
                    train_spec_next.append(edge)
                else:
                    train_spec_previous.append(edge)
            print("Prev ",train_spec_previous)
            print("Next", train_spec_next,)
            final_route = []
            for possible_reroute in reroute:
                print()
                print(possible_reroute)
                stations = possible_reroute['path']
                print("stations",stations)
                curr_time = train_spec_reqd[0][3][0]
                print(curr_time)
                intermediate_route = []
                for i in range(0,len(stations)-1):
                    # print(stations[i])
                    intermediate_route.append([[train_no],[stations[i]],[stations[i+1]],[curr_time]])
                    curr_time = curr_time + int(60*(adjacency_matrix[stations[i]][stations[i+1]]/speed))
                for edge in train_spec_next:
                    intermediate_route.append([[train_no],edge[1],edge[2],[curr_time]])
                    curr_time = curr_time + int(60*(adjacency_matrix[edge[1][0]][edge[2][0]]/speed))
                print("intermediate_route   ",intermediate_route)
                keep = True
                for edge in intermediate_route:
                    for entity in ts_matrix:
                        if(entity[1] == edge[1] and entity[2] == edge[2] and entity[3] == edge[3]):
                            keep = False
                            print(entity,"  ",edge)
                            break
                    if(keep == False):
                        break
                if(keep == True):
                    final_route = intermediate_route
                    # break
            for edge in train_spec_previous:
                final_route.append(edge)
            final_route.sort(key=lambda x: x[3][0])
            final_route_list.append(final_route)
            print("Final Route", final_route,"\n")
            new_ts_matrix =[]


        print(reroute_needed)
        #Delete the existing train
        for entity in original:
            print(entity)
            add = True
            for train in reroute_needed:
                train_no = train[0][0]
                print(entity[0][0])
                print(train_no)
                if(train_no == entity[0][0]):
                    add = False
            if(add == True):
                new_ts_matrix.append(entity)
        # print(new_ts_matrix)
        for final_route in final_route_list:
            for entity in final_route:
                new_ts_matrix.append(entity)
        new_ts_matrix.sort(key=lambda x: x[0][0])
        print("\nUpdated TS Matrix:   ",new_ts_matrix,'\n')
        #print(len(new_ts_matrix))
        return new_ts_matrix

    def update(self):
        adjacency_file = open("adjacency_matrix.save", 'rb')
        adjacency_matrix = pickle.load(adjacency_file)

        ts_file = open("ts_matrix.save", 'rb')
        ts_matrix = pickle.load(ts_file)
        # print(len(ts_matrix))

        station_dict_file = open("station_dict.save", 'rb')
        station_dict = pickle.load(station_dict_file)

        speed_file = open("speed_matrix.save", 'rb')
        speed_matrix = pickle.load(speed_file)

        client_json = open('client_stations.json', 'r')
        client_data = json.load(client_json)
        client_json.close()
        # changes teh time format
        ts_matrix = self.convert_tsm(ts_matrix)
        # TODO: CHANGE
        track_1 = input("Enter first station for breakdown: ")
        track_2 = input("Enter second station for breakdown: ")
        new_ts_matrix = self.reroute(ts_matrix, adjacency_matrix, (track_1, track_2), 200,speed_matrix)
        ts_matrix = self.unconvert_tsm(ts_matrix)
        pprint(new_ts_matrix)
        station_keys = list(client_data.keys())
        # TODO: Saving?? **Naren

        for station in station_keys:
            client_data[station]['trains'] = []

        for station in station_keys:
            station = str(station)
            for route in new_ts_matrix:
                if station == route[1][0]:
                    if isinstance(route[3][0], int):
                        time = route[3][0] / 60
                        time = round(time, 2)
                        h_time = math.floor(time)
                        m_time = int((time - h_time) * 60)
                        h_time = h_time
                        route[3][0] = str(h_time) + ":" + str(m_time)
                    client_data[station]['trains'].append({route[0][0]: route[3][0]})

        client_json = open('test_client_stations.json', 'w')
        json.dump(client_data, client_json)
        client_json.close()

        #with open('client_stations.json', 'w') as jf:
            #json.dump(ts_matrix, jf)

        station_dict_file.close()
        adjacency_file.close()
        speed_file.close()
        ts_file.close()
        return

process = processing_class()
process.update()
