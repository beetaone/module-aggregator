"""Utility functions for getting the env variable"""
import os


def env(name: str, default="") -> str:
    """Return value from environment variable otherwise default value

    Args:
        name ([string]): [ENVIRONMENT_VARIABLE]
        default (str, optional): [Fallback value]. Defaults to "".

    Returns:
        str: [value of the ENVIRONMENT_VARIABLE]
    """

    return os.getenv(name) if os.getenv(name) else default
