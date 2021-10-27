"""
All logic related to the module's incoming data validation
Mostly this file requires changes
"""

from app.config import APPLICATION

allowed_data = [dict, list]

def data_validation(data):
    """Validates the incoming JSON data

    Args:
        data ([JSON Object]): [This is the request body in json format]

    Returns:
        [str, str]: [data, error]
    """
    try:
        # check data format
        if(not type(data) in allowed_data):
            return None, 'Invalid input data'
        # check if data contains required label
        elif type(data) == dict and not APPLICATION['INPUT_LABEL'] in data:
            return None, 'Data does not contain required label'
        elif type(data) == list:
            for item in data:
                if not APPLICATION['INPUT_LABEL'] in item:
                    return None, 'Some data does not contain required label'
        return data, None
    except Exception:
        return None, 'Invalid INPUT_LABEL'
