from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import os 

global_path = str(os.getcwd())
global_path = global_path.split('mrts_server')[0]
# Create your views here.
# returns a json array with the list of stations
@csrf_exempt
def client_query(request):
    request_body = request.body 
    parameters = json.loads(request_body)
    start_station_name = parameters['source']
    stop_station_name = parameters['destination']
    stations_path = global_path + 'client_stations.json'
    stations_codes_file = global_path + 'admin_stations.json'
    with open(stations_codes_file,'rb') as f:
        stations_data = json.load(f)
        start_station_code = stations_data[start_station_name]['station_code']
        stop_station_code = stations_data[stop_station_name]['station_code']
    with open(stations_path,'rb') as f:
        station_data = json.load(f)
        start_station = station_data[start_station_code]
        stop_station = station_data[stop_station_code]
    trains_start_station = list(start_station['trains'])
    trains_stop_station = list(stop_station['trains'])
    counter_1 = 0
    counter_2 = 0
    common_trains = []
    while True:
        if counter_1 == len(trains_start_station) or counter_2 == len(trains_stop_station):
            break
        train_1 = list(trains_start_station[counter_1].keys())[0]
        train_2 = list(trains_stop_station[counter_2].keys())[0]
        arrival_time_1 = trains_start_station[counter_1][train_1]
        arrival_time_2 = trains_stop_station[counter_2][train_2]
        converted_time_1 = arrival_time_1[:-3] + arrival_time_1[-2:]
        converted_time_2 = arrival_time_2[:-3] + arrival_time_2[-2:]
        converted_time_1 = int(converted_time_1)
        converted_time_2 = int(converted_time_2)
        if train_1 == train_2 and converted_time_1 < converted_time_2:
            common_trains.append((train_1,arrival_time_1))
            counter_1 += 1
            counter_2 += 1
        elif train_1 > train_2:
            counter_2 += 1
        elif train_2 > train_1:
            counter_1 += 1
    common_trains_dict = {}
    common_trains_dict[0] = common_trains
    to_return_json = json.dumps(common_trains_dict)
    print('to return \n',to_return_json,'\n\n')
    return HttpResponse(to_return_json)

def list_stations(request):
    print(request)
    station_path = global_path + 'client_stations.json'
    with open(station_path,'rb') as f:
        # station_codes = list(json.load(f).keys())
        station_codes = json.load(f)
        print(type(station_codes))
        station_names = []
        for station_code in station_codes:
            print(station_code)
            # print(type(station_code))
            station_names.append(station_codes[station_code]['station_name'])
        station_names_json = json.dumps(station_names)
    return HttpResponse(str(station_names_json))