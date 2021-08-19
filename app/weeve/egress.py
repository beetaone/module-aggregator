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
        post(url=f"{WEEVE['EGRESS_API_HOST']}", json=return_body)
        return True
    except Exception:
        return False
