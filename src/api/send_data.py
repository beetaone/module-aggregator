"""
This file implements output aspect of the module.
It sends data with REST API POST request to the next module.
"""

from os import getenv
from requests import exceptions, post
from logging import getLogger

log = getLogger("send_data")


def send_data(processed_data: any) -> str:
    """
    Send processed data to the next module.

    Args:
        processed_data (any): Processed data that are send to the next module in the edge application as a single dictionary or a list of dictionaries.

    Returns:
        str: Error message if posting data to the next module failed or None if successful.

    """

    try:
        # parse egress urls for fanout
        urls = [url.strip() for url in getenv("EGRESS_URLS").strip(",").split(",")]

        # for collecting REST API POST responses
        failed_responses = []

        # fan-out
        for url in urls:
            # send data to the next module
            response = post(url=url, json=processed_data)

            log.debug(
                f"Sent data to url {url} | Response: {response.status_code} {response.reason}"
            )

            if response.status_code != 200:
                failed_responses.append(
                    {
                        "url": url,
                        "status_code": response.status_code,
                        "message": response.text,
                    }
                )

        if failed_responses:
            return (
                f"Failed sending data to the following egress urls: {failed_responses}"
            )

        return None

    except (
        exceptions.RequestException,
        exceptions.ConnectionError,
        exceptions.ConnectTimeout,
    ) as e:
        return f"Exception when sending data to the next module: {e}"
