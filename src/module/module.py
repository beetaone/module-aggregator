"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from .params import PARAMS
from api.send_data import send_data

import threading
import math

log = getLogger("module")

#  Set module settings
__INTERVAL_UNIT__ = PARAMS['INTERVAL_UNIT']
__INTERVAL_PERIOD__ = PARAMS['INTERVAL_PERIOD']
__FUNCTION__ = PARAMS['FUNCTION']
__INPUT_LABEL__ = PARAMS['INPUT_LABEL']
__OUTPUT_LABEL__ = PARAMS['OUTPUT_LABEL']

# Interval data collector
data = []

def mean(data_array):
    '''
    Returns the mean of data in the array.
    '''
    return sum(data_array)/len(data_array)

def std(data_array):
    '''
    Returns the standard deviation of data in the array.
    '''
    mu = mean(data_array)
    sqr_distance = [pow(x - mu, 2) for x in data_array]
    return math.sqrt(sum(sqr_distance)/len(data_array))

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

def median(data_array):
    '''
    Returns the median of data in the array.
    '''
    if len(data_array) == 0:
        return None

    data_array.sort()

    if len(data_array)%2 == 0:
        return (data_array[int(len(data_array)/2) - 1] + data_array[int(len(data_array)/2)])/2
    else:
        return data_array[int(len(data_array)/2)]

weevagator_functions = {
    'mean': mean,
    'sum': sum,
    'min': min,
    'max': max,
    'stddv': std,
    'last': last,
    'first': first,
    'spread': spread,
    'count': len,
    'median': median,
}

def frequency_processing():
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
    threading.Timer(interval, frequency_processing).start()

    # save number of data to process, because new data might arrive when processing
    count = len(data)

    if count != 0:
        # processes data
        processed_data = weevagator_functions[__FUNCTION__](data[:count])

        log.debug("Processed data : %s", processed_data)

        # send data to the next module
        return_body = {
            PARAMS['OUTPUT_LABEL']: processed_data,
        }

        send_error = send_data(return_body)

        if send_error:
            log.error(send_error)
        else:
            log.debug("Data sent.")

        # remove old data
        del data[:count]



def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    try:
        # YOUR CODE HERE
        global data

        if type(received_data) == dict:
            data.append(received_data[__INPUT_LABEL__])
        else:
            # parse target data from the structure
            parsed_data = [sample[__INPUT_LABEL__] for sample in received_data]
            data = data + parsed_data

        return None

    except Exception as e:
        return f"Exception in the module business logic: {e}"
