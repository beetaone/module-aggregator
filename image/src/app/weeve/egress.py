""" Egress to the next module
"""
import json
import time
from requests import post
from app.config import APPLICATION, WEEVE


def send_data(data: json, timestamp=time.time()) -> bool:
    """Sends data to the next module

    Args:
        data (json): [description]
        timestamp ([float], optional): [description]. Defaults to time.time().

    Returns:
        bool: If the data was sent properly
    """

    return_body = {
        APPLICATION['OUTPUT_LABEL']: data,
        "outputUnit": APPLICATION['OUTPUT_UNIT'],
        f"{WEEVE['MODULE_NAME']}Time": timestamp
    }

    try:
        # URL Convetion 1
        if not WEEVE['EGRESS_URL']:
            resp = post(url=f"{WEEVE['EGRESS_SCHEME']}://{WEEVE['EGRESS_HOST']}:{WEEVE['EGRESS_PORT']}/{WEEVE['EGRESS_PATH']}", json=return_body)
        # URL Convetion 2
        else:
            resp = post(url=f"{WEEVE['EGRESS_URL']}", json=return_body)
        
        # success = 200
        if resp.status_code == 200:
            return True
        # failure = 500
        else: 
            return False

    except Exception:
        return False
