import threading
import math
from flask import Flask
import time
from app.config import APPLICATION
from app.weeve.egress import send_data

#  Set module settings
__INTERVAL_UNIT__ = APPLICATION['INTERVAL_UNIT']
__INTERVAL_PERIOD__ = APPLICATION['INTERVAL_PERIOD']
__FUNCTION__ = APPLICATION['FUNCTION']
__INPUT_LABEL__ = APPLICATION['INPUT_LABEL']
__DATA_TYPE__ = APPLICATION['DATA_TYPE']
__OUTPUT_LABEL__ = APPLICATION['OUTPUT_LABEL']
__OUTPUT_UNIT__ = APPLICATION['OUTPUT_UNIT']

# Interval data collector
data = []

# reference Flask app for logging
app = None

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

def set_module_app(appi: Flask):
    global app
    app = appi


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
        #print("PROCESSED DATA", processed_data)

        # send data
        sent = send_data(processed_data)
        if not sent:
            app.logger.error("Error while transfering")

        # remove old data
        del data[:count]


def module_main(received_data):
    """implement module logic here

    Args:
        received_data ([JSON Object]): [The output of data_validation function]

    Returns:
        [string, string]: [data, error]
    """
    global data
    try:
        if type(received_data) == dict:
            data.append(received_data[__INPUT_LABEL__])
        else:
            # parse target data from the structure
            parsed_data = [sample[__INPUT_LABEL__] for sample in received_data]
            data = data + parsed_data

        return None, None
    except Exception:
        return None, "Unable to perform the module logic"
