"""
Business logic for health
"""
import time
from flask import jsonify
from app.config import WEEVE
startTime = time.time()


def health_check():
    """
    Returns server status and uptime
    """
    return jsonify({
        "serverStatus": "Running",
        "uptime": time.time() - startTime,
        "module": WEEVE["MODULE_NAME"]
    })
