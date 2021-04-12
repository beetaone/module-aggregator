from flask import Flask, request, jsonify
import threading
import logging
import requests
import numpy as np
from decouple import config

'''
TODO: What are functions: round, floor, spread?
'''

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
        log.warning(f"Settings Request {settings}")
        settingsSet = True

        # start processing intervals
        processing()
        
        return "Settings received."
    else:
        # receive data
        received_data = request.get_json(force=True)
        #print("RECEIVED DATA: ", received_data)

        # parse target data from the structure
        parsed_data = [sample[settings['input_label']] for sample in received_data]
        data = data + parsed_data
        
        return "Data received."

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
        # select interval data
        interval_data = data[:count]

        # set WeevAgator functions
        weevagator_functions = {
            'mean': np.mean(interval_data),
            'sum': np.sum(interval_data),
            'min': min(interval_data),
            'max': max(interval_data),
            'stddv': np.std(interval_data),
            'last': interval_data[-1],
            'first': interval_data [0],
            'spread': max(interval_data) - min(interval_data ),
            'count': len(interval_data ),
            'round': -1,
            'median': np.median(interval_data ),
            'floor': -1
        }

        # chooses a aggregation function from settings
        function = settings['function']

        # processes data
        processed_data = weevagator_functions[function]
        #print("PROCESSED DATA", processed_data)

        # removes processed data
        data[:] = data[count:]
        
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
            "unit": "Celsius"
        }

        # post request
        if __EGRESS_API_METHOD__ == "POST":
            resp = requests.post(url=f"http://{__EGRESS_API_HOST__}:{__EGRESS_API_PORT__}{__EGRESS_API_URI__}", json=return_body)
            #print(f"The response :{resp} {resp.text}")
        else:
            log.exception(f"The HTTP Method not supportive.")

if __name__ == "__main__":
    app.run(host=__HANDLER_HOST__, port=__HANDLER_PORT__)
