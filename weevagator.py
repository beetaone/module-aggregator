from flask import Flask, request, jsonify
import threading
import logging
import requests
import numpy as np
from decouple import config

log = logging.getLogger(__name__)

app = Flask(__name__)
__EGRESS_API_HOST__ = config('EGRESS_API_HOST')
__EGRESS_API_METHOD__ = config('EGRESS_API_METHOD')
__HANDLER_HOST__ = config('HANDLER_HOST')
__HANDLER_PORT__ = config('HANDLER_PORT')

#  Set module settings
__INTERVAL_UNIT__ = config('INTERVAL_UNIT')
__INTERVAL_PERIOD__ = float(config('INTERVAL_PERIOD'))
__FUNCTION__ = config('FUNCTION')
__INPUT_LABEL__ = config('INPUT_LABEL')
__DATA_TYPE__ = config('DATA_TYPE')
__OUTPUT_LABEL__ = config('OUTPUT_LABEL')
__OUTPUT_UNIT__ = config('OUTPUT_UNIT')

# Interval data collector
data = []


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


@app.route('/handle', methods=['POST'])
def handle():
    '''
    Receive ReST API POST request with data.
    '''
    global data

    try:
        # receive data
        received_data = request.get_json(force=True)
        #print("RECEIVED DATA: ", received_data)

        # parse target data from the structure
        parsed_data = [sample[__INPUT_LABEL__] for sample in received_data]
        data = data + parsed_data
    except:
        log.exception(f"Wrong data structure.")

    return '', 204


def processing():
    '''
    Sets an interval for receiving data and processes them.
    Returns HTTP ReST request at the end.
    '''
    # convert interval unit to seconds (must do for threading Timer)
    convert_interval_unit = {
        'ms': __INTERVAL_PERIOD__/1000,
        's': __INTERVAL_PERIOD__,
        'm': __INTERVAL_PERIOD__ * 60,
        'h': __INTERVAL_PERIOD__ * 3600,
        'd': __INTERVAL_PERIOD__ * 3600 * 24,
    }
    interval = convert_interval_unit[__INTERVAL_UNIT__]

    # start thread with given interval
    threading.Timer(interval, processing).start()

    # save number of data to process, because new data might arrive when processing
    count = len(data)

    if count != 0:
        # processes data
        processed_data = weevagator_functions[__FUNCTION__](data[:count])
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
            str(__OUTPUT_LABEL__): typed_processed_data,
            "data_type": data_type,
            "input_unit": __OUTPUT_UNIT__
        }

        # post request
        if __EGRESS_API_METHOD__ == "POST":
            resp = requests.post(
                url=f"{__EGRESS_API_HOST__}", data=return_body)
            #print(return_body)
            #print(f"THE RESPONSE:{resp} {resp.text}")
        else:
            log.exception(f"The HTTP Method not supportive.")


if __name__ == "__main__":
    # start processing intervals
    processing()
    app.run(host=__HANDLER_HOST__, port=__HANDLER_PORT__)