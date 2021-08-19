"""
All constants specific to the application
"""
from app.utils.env import env
from app.utils.floatenv import floatenv


APPLICATION = {
    "INTERVAL_UNIT": env("INTERVAL_UNIT", "s"),
    "INTERVAL_PERIOD": floatenv("INTERVAL_PERIOD", "10"),
    "FUNCTION": env("FUNCTION", "sum"),
    "INPUT_LABEL": env("INPUT_LABEL", "temperature"),
    "DATA_TYPE": env("DATA_TYPE", "float"),
    "OUTPUT_LABEL": env("OUTPUT_LABEL", "temperature"),
    "OUTPUT_UNIT": env("OUTPUT_UNIT", "Celsius")
}
