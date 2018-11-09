import numpy as np

def hx(source_station,destination_station):
    #TODO: define the funtion


def rand_breakdown():
    # TODO: define, using randomizer

#track is defined as (source,dest)
def update(train_arr,track):
    source = track[0]
    dest = track[1]
    trains_affected = train_arr[:,source,dest]
    

# TODO: Unpickle the array as train_arr
# train_arr [time,source,dest] -> train
