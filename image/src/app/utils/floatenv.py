"""Utility functions for getting the float env variable"""
import os


def floatenv(name: str, default=0.0) -> float:
    """ return value from float environment variable otherwise False

    Args:
        name (str): [ENVIRONMENT_VARIABLE]
        default (float, optional): [Fallback value]. Defaults to 0.0.

    Returns:
        float: [value of the ENVIRONMENT_VARIABLE]
    """
    return float(os.getenv(name)) if os.getenv(name) else default
