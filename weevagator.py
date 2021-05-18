from flask import Flask, request, jsonify
import threading
import logging
import requests
import numpy as np
from decouple import config

log = logging.getLogger(__name__)

app = Flask(__name__)
__EGRESS_API_HOST__ = config('EGRESS_API_HOST')
__EGRESS_API_PORT__ = config('EGRESS_API_PORT')
__EGRESS_API_URI__ = config('EGRESS_API_URI')
__EGRESS_API_METHOD__ = config('EGRESS_API_METHOD')
__HANDLER_HOST__ = config('HANDLER_HOST')
__HANDLER_PORT__ = config('HANDLER_PORT')

# Interval data collector
data = [ ]

def last(data_array):
    '''
    Returns the last element in the array.
    '''
    return data_array[-1]

def first(data_array):
    '''
    Returns the first element in the array.
    '''
    return data_array[0]

def spread(data_array):
    '''
    Returns the spread of data in the array.
    '''
    return max(data_array) - min(data_array)

weevagator_functions = {
    'mean': np.mean,
    'sum': np.sum,
    'min': min,
    'max': max,
    'stddv': np.std,
    'last': last,
    'first': first,
    'spread': spread,
    'count': len,
    'median': np.median,
}

# Set default settings
settings = {
    "interval_unit": 'ms',
    "interval": 20,
    "function": 'mean',
    "input_label": 'temperature',
    "data_type": float,
    "output_label": 'differentialTemp',
    "output_unit": 'Celsius'
}

# Flag if settings are set
settingsSet = False

@app.route('/handle', methods=['POST'])
def handle():
    '''
    Receive ReST API POST request. First request are WeevAgator settings.
    The next requests are data.
    '''
    global settings
    global settingsSet
    global data
    if not settingsSet:
        # set WeevAgator settings
        settings = request.get_json(force=True)
        #log.warning(f"Settings Request {settings}")
        settingsSet = True

        # start processing intervals
        processing()
    else:
        # receive data
        received_data = request.get_json(force=True)
        #print("RECEIVED DATA: ", received_data)

        # parse target data from the structure
        parsed_data = [sample[settings['input_label']] for sample in received_data]
        data = data + parsed_data
        
    return '', 204

def processing():
    '''
    Sets an interval for receiving data and processes them.
    Returns HTTP ReST request at the end.
    '''
    # convert interval unit to seconds (must do for threading Timer)
    convert_interval_unit = {
        'ms': settings['interval']/1000,
        's': settings['interval'],
        'm': settings['interval'] * 60,
        'h': settings['interval'] * 3600,
        'd': settings['interval'] * 3600 * 24,
    }
    interval = convert_interval_unit[settings['interval_unit']]

    # start thread with given interval
    threading.Timer(interval, processing).start()

    # save number of data to process, because new data might arrive when processing
    count = len(data)

    if count != 0:
        # processes data
        processed_data = weevagator_functions[settings['function']](data[:count])
        #print("PROCESSED DATA", processed_data)

        # removes processed data
        del data[:count]
        
        # prepare output HTTP ReST API request
        # 1. change types from numpy type to python type (must do for JSON)
        if isinstance(processed_data, np.int_):
            typed_processed_data = int(processed_data)
            data_type = "int"
        else:
            typed_processed_data = float(processed_data)
            data_type = "float"

        # 2. build JSON body
        return_body = {
            str(settings["output_label"]): typed_processed_data,
            "data_type": data_type,
            "input_unit": settings["output_unit"]
        }

        # post request
        if __EGRESS_API_METHOD__ == "POST":
            resp = requests.post(url=f"http://{__EGRESS_API_HOST__}:{__EGRESS_API_PORT__}{__EGRESS_API_URI__}", json=return_body)
            #print(f"THE RESPONSE:{resp} {resp.text}")
        else:
            log.exception(f"The HTTP Method not supportive.")

if __name__ == "__main__":
    app.run(host=__HANDLER_HOST__, port=__HANDLER_PORT__)
